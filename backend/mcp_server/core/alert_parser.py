import re

def extract_alert_entities(alert: dict) -> dict:
    """
    Extracts CVEs, IPs, hashes, emails, and other useful indicators from a SOC alert.
    Scans across all keys and values, supporting flexible alert structures.
    """
    def flatten_dict(d):
        """Flatten dict to a string including keys and values."""
        items = []
        for k, v in d.items():
            items.append(str(k))
            if isinstance(v, dict):
                items.append(flatten_dict(v))
            elif isinstance(v, list):
                items.extend([str(i) for i in v])
            else:
                items.append(str(v))
        return " ".join(items)

    alert_text = flatten_dict(alert) # Flatten to string for regex searching

    # CVE pattern (supports CVE-YYYY-NNNNN etc.)
    cves = re.findall(r"CVE-\d{4}-\d{4,7}", alert_text)

    # Email pattern
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", alert_text)

    # IP address pattern
    ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", alert_text)

    # SHA256 hash pattern
    # MD5, SHA1, SHA256 (32, 40, 64 chars)
    hashes = re.findall(r"\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b", alert_text)


    # Domains (skip emails)
    domains = []
    for match in re.findall(r"(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+)", alert_text):
        if not any(match in e for e in emails):  # skip if it's part of an email
            domains.append(match)

    # Meta fields from alert dict
    alert_type = alert.get("type", "").strip()
    alert_title = alert.get("title", "")
    rule_id = alert.get("event_id", "")
    severity = alert.get("severity", "")
    timestamp = alert.get("event_time", "")

    return {
        "cves": list(set(cves)),
        "emails": list(set(emails)),
        "ips": list(set(ips)),
        "hashes": list(set(hashes)),
        "domains": list(set(domains)),
        "alert_type": alert_type,
        "rule_id": rule_id,
        "title": alert_title,
        "severity": severity,
        "timestamp": timestamp
    }
