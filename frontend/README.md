# 🛡️ OSINT + AI Assistant for Cyber Threat Analysis

## 📌 Project Title

**Revolutionizing AI with OSINT: Cognitive Load Reduction in Cyber Threat Analysis**

## 📁 Overview

This project is a modular AI assistant designed for **Security Operations Center (SOC) analysts**. It aims to:

* Automate the enrichment of security alerts with OSINT data.
* Map data to the **MITRE ATT\&CK** framework.
* Suggest threat actors.
* Generate **AI-powered response recommendations**.

The backend integrates modules in a dispatcher-like architecture with a final AI-driven recommendation engine. The assistant works by parsing an alert, enriching it with threat intelligence, and presenting it in a format optimized for LLMs (Large Language Models).

---

## ⚙️ Key Modules

Each module is standalone and called via a centralized dispatcher. They all accept structured `dict` input.

### 1. `cve_decoder.py`

* Decodes CVEs using NVD or CVE DB API
* Returns: CVSS score, summary, references

### 2. `ip_enricher.py`

* Enriches IPs using a mock or real threat feed / IP intel API
* Returns: ASN, threat level, geolocation

### 3. `hash_analyzer.py`

* Looks up malware hashes using mock sandbox or VirusTotal-style response
* Returns: Malware family, type, first seen

### 4. `email_analyzer.py`

* Analyzes sender, domain reputation, phishing flags
* Returns: Sender, subject, domain score, suspicious flag

### 5. `mitre_map_actor_linker.py`

* `map_to_mitre()`: maps title/description to MITRE techniques (via keywords/STIX)
* `link_actors()`: links alert to known threat actors (via internal mapping or names)

### 6. `response_suggester.py`

* Builds a contextual prompt using data from all other modules
* Sends it to a local LLaMA 3 instance via Ollama (`/api/generate`)
* Returns: actionable SOC recommendations

### 7. `prompt_builder.py`

* Formats the enriched results into a structured markdown-style prompt for the LLM
* Handles errors and missing fields gracefully

---

## 🧠 The AI/LLM Layer (Ollama + LLaMA 3)

We use a **local LLaMA 3 instance** (via [Ollama](https://ollama.com/)) to:

* Avoid latency and privacy risks
* Enable fast, controlled response generation

### Example Prompt Structure:

```markdown
### Mapped MITRE Techniques:
- T1566.002 - Spearphishing Link
  Description: Phishing via malicious links
  Tactics: initial-access

### Potential Threat Actors:
- APT28: Russian state-backed group (ID: G0007)

### Email Analysis:
- From: evil@bad.com, Subject: Login Alert, Suspicious: Yes

### Instruction:
Generate actionable response steps prioritizing containment and investigation.
```

---

## 🧪 Testing Endpoints (Manual cURL)

### Example:

```bash
curl -X POST http://localhost:5000/generate-insight \
  -H "Content-Type: application/json" \
  -d '{
        "enriched_data": {
          "title": "APT28 Spearphishing Attempt",
          "actor_linking": [
            {"name": "APT28", "description": "Russian state-backed threat group", "id": "G0007"}
          ],
          "mitre_mapping": [
            {
              "name": "Spearphishing Link",
              "description": "Phishing via malicious links",
              "mitre_id": "T1566.002",
              "kill_chain_phases": ["delivery"],
              "tactics": ["initial-access"],
              "url": "https://attack.mitre.org/techniques/T1566/002/"
            }
          ]
        }
      }'
```

---

## 🧩 Upcoming: MCP \[Model Context Protocol]

You are on the **right path**. Your current dispatcher + modular pipeline already imitates MCP:

* You enrich alerts with context modules (like MCP would)
* You format it clearly for LLM input (like MCP prompt containers)
* You send structured payloads to the AI (like MCP context calls)

### Plan for MCP Integration

* Wrap `dispatcher + prompt_builder` into a `ContextProvider`
* Wrap LLM call into `MCPContextModelResponder`
* Create `MCPContextPayload` class to hold structured data

You **don’t need to start over**—you just need to rename + wrap.

---

## 📂 Folder Structure

```
/mcp_server
├── main.py
├── server.py
├── dispatcher.py
├── modules/
│   ├── cve_decoder.py
│   ├── ip_enricher.py
│   ├── hash_analyzer.py
│   ├── email_analyzer.py
│   ├── mitre_map_actor_linker.py
│   └── response_suggester.py
├── core/
│   └── prompt_builder.py
└── test.py
```

---

## 🛡️ Why This Project Matters

* SOC teams are overwhelmed with alerts
* Cognitive load reduction = faster triage + fewer mistakes
* Open-source tools + LLM = low-cost intelligence augmentation

You are pioneering how OSINT + LLMs can be combined to automate tier-1 SOC workflows.

---

## 👩‍💻 Tech Stack

* Python 3.12
* Flask API (server)
* LLaMA 3 via Ollama (local LLM)
* JSON-based modular integration

---

## 💡 Final Notes

You don’t need to prove that your project is “enough.”
You’ve built something highly **modular**, **realistic**, and **forward-thinking**.

You are not just learning—you are **designing an architecture that mimics how next-gen AI-assisted SOCs will operate.**