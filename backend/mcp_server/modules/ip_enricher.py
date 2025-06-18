import requests
import os

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY");

def enrich_ip(ip: str) -> dict:
    """
    Enriches an IP address using VirusTotal API.
    Returns threat intelligence like reputation, malicious detections, and network owner info.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", {}).get("attributes", {})

        return {
            "ip": ip,
            "reputation": data.get("reputation"),
            "malicious_votes": data.get("last_analysis_stats", {}).get("malicious"),
            "suspicious_votes": data.get("last_analysis_stats", {}).get("suspicious"),
            "harmless_votes": data.get("last_analysis_stats", {}).get("harmless"),
            "asn": data.get("asn"),
            "network": data.get("network"),
            "continent": data.get("continent"),
            "country": data.get("country"),
            "regional_internet_registry": data.get("regional_internet_registry"),
            "tags": data.get("tags", []),
            "whois": data.get("whois"),
        }

    except Exception as e:
        return {
            "ip": ip,
            "error": f"VirusTotal enrichment failed: {str(e)}"
        }
