import os
import requests
from datetime import datetime

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_URL = "https://www.virustotal.com/api/v3/files/"

def analyze_hash(file_hash: str) -> dict:
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }

    # Determine hash type by length
    hash_type = {
        32: "MD5",
        40: "SHA-1",
        64: "SHA-256"
    }.get(len(file_hash), "Unknown")

    try:
        response = requests.get(VT_URL + file_hash, headers=headers, timeout=10)
        response.raise_for_status()
        attributes = response.json().get("data", {}).get("attributes", {})

        stats = attributes.get("last_analysis_stats", {})
        malicious_count = stats.get("malicious", 0)
        total_engines = sum(stats.values())

        # Convert timestamp to readable date
        first_seen_unix = attributes.get("first_submission_date")
        first_seen = datetime.utcfromtimestamp(first_seen_unix).strftime("%Y-%m-%d %H:%M:%S UTC") if first_seen_unix else "Unknown"

        yara_rules = attributes.get("crowdsourced_yara_results", [])
        yara_names = [rule.get("rule_name", "Unnamed") for rule in yara_rules]

        return {
            "hash": file_hash,
            "type": hash_type,
            "malicious": malicious_count > 0,
            "severity": (
                "High" if malicious_count > 15 else
                "Medium" if malicious_count > 5 else
                "Low" if malicious_count > 0 else
                "Unknown"
            ),
            "detection_count": malicious_count,
            "total_engines": total_engines,
            "malware_family": attributes.get("popular_threat_classification", {}).get("suggested_threat_label", "N/A"),
            "file_type": attributes.get("type_description", "Unknown"),
            "first_seen": first_seen,
            "related_tags": attributes.get("tags", []),
            "hunting_query": f'file_hash:"{file_hash}"',
            "mitigation": "If this hash is found, isolate affected systems, block at endpoint, and initiate IR procedures.",
            "yara_rules": yara_names
        }

    except requests.exceptions.RequestException as e:
        print(f"[!] VirusTotal API error: {e}")
        return {
            "hash": file_hash,
            "type": hash_type,
            "error": "Failed to fetch data from VirusTotal"
        }
