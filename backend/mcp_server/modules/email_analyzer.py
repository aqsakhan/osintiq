import re

# Minimal list of known disposable email providers
DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "tempmail.com", "trashmail.com", "dispostable.com"
}

def analyze_email(email: str) -> dict:
    result = {
        "email": email,
        "valid_format": False,
        "is_disposable": False,
    }

    # Regex to check email format
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_regex, email):
        result["valid_format"] = True

        # Check disposable domain
        domain = email.split('@')[-1].lower()
        if domain in DISPOSABLE_DOMAINS:
            result["is_disposable"] = True

    return result

# import os
# import requests
# import re

# EMAILREP_API_KEY = os.getenv("EMAILREP_API_KEY")

# def is_valid_email(email: str) -> bool:
#     """Simple email format check"""
#     pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
#     return re.match(pattern, email) is not None

# def analyze_email(email: str) -> dict:
#     """
#     Analyze an email using EmailRep.io to gather reputation, compromise status, and linked intel.
#     """
#     if not is_valid_email(email):
#         return {
#             "email": email,
#             "valid_format": False,
#             "error": "Invalid email format"
#         }

#     url = f"https://emailrep.io/{email}"
#     headers = {
#         "Accept": "application/json"
#     }

#     # Only add API key if provided
#     if EMAILREP_API_KEY:
#         headers["Key"] = EMAILREP_API_KEY

#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code != 200:
#             return {
#                 "email": email,
#                 "error": f"EmailRep API returned status {response.status_code}",
#                 "details": response.text
#             }

#         data = response.json()

#         return {
#             "email": email,
#             "reputation": data.get("reputation", "unknown"),
#             "suspicious": data.get("suspicious", False),
#             "references": data.get("references", 0),
#             "malicious_activity": data.get("details", {}).get("malicious_activity", False),
#             "credentials_leaked": data.get("details", {}).get("credentials_leaked", False),
#             "blacklisted": data.get("details", {}).get("blacklisted", False),
#             "last_seen": data.get("details", {}).get("last_seen", "Unknown"),
#             "tags": data.get("details", {}).get("tags", []),
#             "linked_profiles": data.get("details", {}).get("profiles", [])
#         }

#     except requests.exceptions.RequestException as e:
#         return {
#             "email": email,
#             "error": f"Request failed: {str(e)}"
#         }
