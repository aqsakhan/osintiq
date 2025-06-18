from mcp_server.modules.cve_decoder import decode_cve
from mcp_server.modules.ip_enricher import enrich_ip
from mcp_server.modules.hash_analyzer import analyze_hash
from mcp_server.modules.email_analyzer import analyze_email
from mcp_server.modules.mitre_map_actor_linker import map_to_mitre, link_actors
from mcp_server.modules.response_suggester import generate_response_recommendations

def dispatch_modules(parsed_alert: dict) -> dict:
    results = {}

    # CVE Decoder
    cves = parsed_alert.get("cves", [])
    if cves:
        results["cve_analysis"] = [decode_cve(cve) for cve in cves]
    
    # IP Enrichment
    if ips := parsed_alert.get("ips"):
        results["ip_enrichment"] = [enrich_ip(ip) for ip in ips]

    # Hash Analysis
    if hashes := parsed_alert.get("hashes"):
        results["malware_analysis"] = [analyze_hash(h) for h in hashes]

    # Email Analysis
    if emails := parsed_alert.get("emails"):
        results["email_analysis"] = [analyze_email(email) for email in emails]

    # MITRE Mapping using the alert title/description
    if title := parsed_alert.get("title", ""):
        if len(title.split()) >= 2:
            # raw_stix = map_to_mitre(title)
            # results["mitre_mapping"] = extract_useful_fields(raw_stix)
            results["mitre_mapping"] = map_to_mitre(title)
        else:
            results["mitre_mapping"] = []
    
    # Actor Linker: Link threat actors based on title/description
    if title := parsed_alert.get("title", ""):
        if len(title.split()) >= 2:
            results["actor_linking"] = link_actors(title)
        else:
            results["actor_linking"] = []

    results["response_recommendations"] = generate_response_recommendations(results)

    return results
