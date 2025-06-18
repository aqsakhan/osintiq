import requests
from stix2 import MemoryStore
import os, json

CACHE_FILE = "enterprise_attack_cache.json"

def get_data_from_branch(domain="enterprise-attack", branch="master"):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return MemoryStore(stix_data=json.load(f)["objects"])

    url = f"https://raw.githubusercontent.com/mitre/cti/{branch}/{domain}/{domain}.json"
    response = requests.get(url)
    response.raise_for_status()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(response.json(), f)

    return MemoryStore(stix_data=response.json()["objects"])

# def get_data_from_branch(domain="enterprise-attack", branch="master"):
#     """
#     Fetch ATT&CK STIX data from MITRE/CTI GitHub.
#     Domain: 'enterprise-attack', 'mobile-attack', or 'ics-attack'.
#     Branch: typically 'master'.
#     """
#     print(f"Fetching MITRE ATT&CK data from GitHub ({domain}, branch: {branch})...")
#     url = f"https://raw.githubusercontent.com/mitre/cti/{branch}/{domain}/{domain}.json"
#     response = requests.get(url)
#     response.raise_for_status()
#     return MemoryStore(stix_data=response.json()["objects"])
