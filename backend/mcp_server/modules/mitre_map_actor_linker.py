import re
from stix2 import Filter
from modules.mitre_utils import get_data_from_branch

# Load MITRE ATT&CK STIX data into memory store
memory_store = get_data_from_branch()

def map_to_mitre(indicator_name: str):
    """
    Map input indicators (e.g., attack names, behaviors) to MITRE ATT&CK techniques.
    Uses fuzzy matching for better coverage.
    """
    if not indicator_name:
        return []

    indicator_name = indicator_name.lower().strip()
    enriched = []

    # Get all attack-patterns
    attack_patterns = memory_store.query([Filter("type", "=", "attack-pattern")])

    for pattern in attack_patterns:
        name = pattern.get("name", "").lower()

        # Fuzzy match: substring or whole word match
        if indicator_name in name or re.search(rf'\b{re.escape(indicator_name)}\b', name):
            kill_chain_phases = [
                phase.phase_name for phase in pattern.get("kill_chain_phases", [])
            ]

            tactics = list(set(kill_chain_phases))

            mitre_id, mitre_url = "", ""
            for ref in pattern.get("external_references", []):
                if ref.get("source_name") == "mitre-attack":
                    mitre_id = ref.get("external_id", "")
                    mitre_url = ref.get("url", "")

            enriched.append({
                "name": pattern.get("name", "Unknown Pattern"),
                "mitre_id": mitre_id,
                "url": mitre_url,
                "description": pattern.get("description", "No description available."),
                "kill_chain_phases": kill_chain_phases,
                "tactics": tactics
            })

    return enriched


def link_actors(text: str):
    """
    Match known threat actors (intrusion sets) based on names and aliases found in the alert text.
    Returns actor details with match type.
    """
    if not text:
        return []

    text_lower = text.lower()
    matched_actors = []

    # Fetch all known intrusion sets (APT groups)
    groups = memory_store.query([Filter("type", "=", "intrusion-set")])

    for group in groups:
        name = group.get("name", "")
        aliases = group.get("aliases", [])

        match_score = 0
        if name.lower() in text_lower:
            match_score += 2
        if any(alias.lower() in text_lower for alias in aliases):
            match_score += 1

        if match_score > 0:
            matched_actors.append({
                "id": group.get("id"),
                "name": name,
                "aliases": aliases,
                "match_type": "direct" if match_score >= 2 else "alias",
                "description": group.get("description", "No description."),
                "external_references": [
                    {
                        "source_name": ref.get("source_name", ""),
                        "url": ref.get("url", ""),
                        "external_id": ref.get("external_id", "")
                    }
                    for ref in group.get("external_references", [])
                    if isinstance(ref, dict)
                ]
            })

    return matched_actors




# from stix2 import Filter
# from mcp_server.modules.mitre_utils import get_data_from_branch

# # Shared STIX memory store (from GitHub ATT&CK data)
# memory_store = get_data_from_branch()

# def map_to_mitre(indicator_name: str):
#     """
#     Map indicator names to MITRE ATT&CK attack patterns.
#     """
#     filters = [
#         Filter("type", "=", "attack-pattern"),
#         Filter("name", "=", indicator_name)
#     ]
#     results = memory_store.query(filters)

#     enriched = []

#     for pattern in results:
#         kill_chain_phases = []
#         tactics = []

#         # Extract kill chain phases
#         if hasattr(pattern, "kill_chain_phases") and pattern.kill_chain_phases:
#             for phase in pattern.kill_chain_phases:
#                 if hasattr(phase, "phase_name"):
#                     kill_chain_phases.append(phase.phase_name)

#         # Deduplicate as a simple tactic placeholder
#         tactics = list(set(kill_chain_phases))

#         # Extract MITRE ID and URL
#         mitre_id = ""
#         mitre_url = ""
#         if hasattr(pattern, "external_references"):
#             for ref in pattern.external_references:
#                 if hasattr(ref, "source_name") and ref.source_name == "mitre-attack":
#                     mitre_id = getattr(ref, "external_id", "")
#                     mitre_url = getattr(ref, "url", "")

#         enriched.append({
#             "name": pattern.name,
#             "mitre_id": mitre_id,
#             "url": mitre_url,
#             "description": getattr(pattern, "description", "No description available."),
#             "kill_chain_phases": kill_chain_phases,
#             "tactics": tactics
#         })

#     return enriched


# def link_actors(text: str):
#     """
#     Detect threat actors (intrusion sets) that match the text input (e.g., alert title).
#     """
#     text_lower = text.lower()
#     results = []

#     # Query intrusion sets (threat groups)
#     groups = memory_store.query([Filter("type", "=", "intrusion-set")])

#     for group in groups:
#         name = group.get("name", "").lower()
#         aliases = [alias.lower() for alias in group.get("aliases", [])]

#         if name in text_lower or any(alias in text_lower for alias in aliases):
#             results.append({
#                 "id": group.get("id"),
#                 "name": group.get("name"),
#                 "aliases": group.get("aliases", []),
#                 "description": group.get("description", "No description."),
#                 "external_references": [
#                     {
#                         "source_name": ref.get("source_name", ""),
#                         "url": ref.get("url", ""),
#                         "external_id": ref.get("external_id", "")
#                     }
#                     for ref in group.get("external_references", [])
#                     if isinstance(ref, dict) or hasattr(ref, "get")
#                 ]
#             })

#     return results
