# mcp_server/server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from mcp_server.modules.hash_analyzer import analyze_hash
from mcp_server.modules.ip_enricher import enrich_ip
from mcp_server.modules.email_analyzer import analyze_email
from mcp_server.modules.cve_decoder import decode_cve
from mcp_server.modules.mitre_map_actor_linker import map_to_mitre, link_actors
from mcp_server.modules.response_suggester import generate_response_recommendations
from mcp_server.groq_llama3 import call_llm

app = Flask(__name__)
CORS(app)

@app.route("/generate-insight", methods=["POST"])
def generate_insight():
    try:
        data = request.get_json()
        input_text = data.get("input_text", "").strip()

        if not input_text:
            return jsonify({"error": "Missing input_text"}), 400

        # === Step 1: LLM Alert Parsing ===
#         parse_prompt = f"""
# You're a cybersecurity alert parser.

# Your job is to convert ANY messy alert or analyst input into structured JSON with fields like 'hash', 'ip', 'email', 'domain', 'URL', 'CVE', 'EventID', etc.

# If the input is: "I found this IP 1.2.3.4 and hash abc123", return:
# {{ "ip": "1.2.3.4", "hash": "abc123", "cve" : "cve-2025"}}

# the input can be anything related to cyber security or incident response you need to find any info on that later,
# so make sure you are generating all the info precisely.
# you can also extract the info and put it under "description" : "..."

# If nothing is relevant, return an empty object: {{}}

# Input:
# {input_text}

# Output (JSON only):
# """
        
        parse_prompt = f"""
You are a cybersecurity parsing assistant trained for Security Operations Centers (SOC).

Your task is to extract all relevant threat indicators and contextual details from ANY unstructured security alert or analyst message. Your output must be a single flat JSON object.

Output Format (FLAT JSON ONLY):
Extract relevant fields such as:
- ip
- hash
- cve (e.g. CVE-2023-34362)
- domain
- url
- email
- event_id
- timestamp
- filename
- description

Rules:
- Only include keys that are present in the input.
- DO NOT nest values inside sub-objects like "entities" or "threat_intel". Just output a single flat JSON object.
- Include a "description" key to summarize the alert in 1–2 sentences using the provided info.
- If the alert contains multiple values (e.g., multiple IPs or CVEs), return only the most critical or first one.
- If no relevant data is found, return empty object.
- Ensure CVE IDs are always formatted as 'CVE-YYYY-NNNNN'.

Input:
{input_text}

Output (JSON only):
"""

        # print("✔️ Check this out -->", parse_prompt);
        parsed_json_str = call_llm(parse_prompt)
        print("=== Raw LLM Parse Response ===")
        print(parsed_json_str)

        try:
            parsed = json.loads(parsed_json_str)
        except json.JSONDecodeError as e:
            return jsonify({
                "error": f"Failed to parse LLM JSON: {e}",
                "raw_response": parsed_json_str
            }), 500

        # Normalize keys to lowercase
        parsed = {k.lower(): v for k, v in parsed.items()}
        print("=== Parsed Alert ===")
        print(parsed)

        # === Step 2: Dispatcher-style Enrichment ===
        enrichment_results = {}

        if "hash" in parsed:
            enrichment_results["hash_analysis"] = analyze_hash(parsed["hash"])

        if "ip" in parsed:
            enrichment_results["ip_info"] = enrich_ip(parsed["ip"])

        if "email" in parsed:
            enrichment_results["email_info"] = analyze_email(parsed["email"])

        # Try multiple casing variants for CVE key
        cve_id = parsed.get("CVE") or parsed.get("cve") or parsed.get("Cve")
        print("⚠️ cve_id", cve_id);
        if cve_id:
            enrichment_results["cve_info"] = decode_cve(cve_id)
        else:
            print("⚠️ No CVE found in parsed input")
        
        print("=== Parsed Alert ===")
        print(json.dumps(parsed, indent=2))

        enrichment_results["mitre"] = map_to_mitre(parsed.get("hash") or parsed.get("cve") or "")
        enrichment_results["actor_links"] = link_actors(input_text)

        print("=== Enriched Alert for LLM ===")
        print(enrichment_results.get("cve_info", "⚠️ No CVE info enriched"))

        # === Step 3: SOC Summary via LLM ===
        summary_prompt = f"""
You are a senior SOC analyst tasked with interpreting cybersecurity alerts and enriching threat data for rapid triage.

You are given two inputs:
1. Parsed alert data (directly extracted from the alert)
2. Enrichment data from external sources like CVE databases, threat intel, or malware analysis feeds

Your job is to:
- Provide a clear, concise executive summary of what the alert is about
- Highlight relevant indicators (IPs, hashes, filenames, CVEs) and their significance
- Contextualize the CVE (what it is, how it’s exploited, and its severity)
- Deduce possible MITRE ATT&CK techniques based on the information
- Infer likely threat actors if available or linked to known campaigns
- Provide a prioritized list of SOC actions under: Containment, Investigation, Remediation, and Communication
- Output everything in a clean, readable format using Markdown-style formatting (e.g. headers, bullet points, emojis)

Inputs:

🧾 Parsed Alert:
```json
{json.dumps(parsed, indent=2)}

Enrichment Results:
{json.dumps(enrichment_results, indent=2)}

Summarize what happened, identify MITRE techniques, linked actors, and give SOC action steps (containment, investigation, etc.). Use bullet points if needed. Be concise but useful.
"""
        final_summary = call_llm(summary_prompt)

        return jsonify({
            "topic": input_text[:50] + "...",
            "insight": final_summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_server():
    app.run(debug=True)
