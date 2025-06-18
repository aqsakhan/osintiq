import requests
import os
import json

NVD_API_KEY = os.getenv("NVD_API_KEY");
import requests

def decode_cve(cve_id: str) -> dict:
    """
    Enrich CVE using NVD API v2.0 and extract useful threat context.
    """
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "cveId": cve_id
    }
    headers = {
        "User-Agent": "MCP-CVE-Decoder/1.0",
        "apiKey": NVD_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("vulnerabilities"):
            return {"cve_id": cve_id, "error": "CVE not found in NVD."}

        cve_item = data["vulnerabilities"][0]["cve"]

        # Description
        description = next(
            (desc["value"] for desc in cve_item.get("descriptions", []) if desc["lang"] == "en"),
            "No description available."
        )

        # CVSS Score
        metrics = cve_item.get("metrics", {})
        cvss_data = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})

        # CWE & References
        problem_types = cve_item.get("weaknesses", [])
        cwe_list = []
        for pt in problem_types:
            for desc in pt.get("description", []):
                if desc.get("lang") == "en":
                    cwe_list.append(desc["value"])

        references = [
            ref["url"] for ref in cve_item.get("references", [])
            if "url" in ref
        ]

        # print("=== CVE Decoder Output ===")
        # print("----->>>>> ", cve_id)
        # print("----->>>>> ", description)
        # print("----->>>>> ", cvss_data.get("baseScore"))


        return {
            "cve_id": cve_id,
            "description": description,
            "cvss_score": cvss_data.get("baseScore"),
            "cvss_severity": cvss_data.get("baseSeverity"),
            "attack_vector": cvss_data.get("attackVector"),
            "privileges_required": cvss_data.get("privilegesRequired"),
            "user_interaction": cvss_data.get("userInteraction"),
            "vector": cvss_data.get("vectorString"),
            "cwe_ids": cwe_list,
            "published_date": cve_item.get("published"),
            "last_modified_date": cve_item.get("lastModified"),
            "references": references[:5],  # Only top 5
        }

    except Exception as e:
        return {
            "cve_id": cve_id,
            "error": f"Failed to retrieve CVE details: {str(e)}"
        }

# import requests

# def decode_cve(cve_id: str) -> dict:
#     """
#     Fetch CVE details using CIRCL.lu CVE API.
#     More stable and simpler than NVD.
#     """
#     url = f"https://cve.circl.lu/api/cve/{cve_id}"

#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()

#         # Log basic info
#         print("=== CIRCL CVE Decoder Output ===")
#         print("ID:", data.get("id"))
#         print("Description:", data.get("summary"))
#         print("CVSS:", data.get("cvss"))

#         return {
#             "cve_id": data.get("id"),
#             "description": data.get("summary", "No description available."),
#             "cvss_score": data.get("cvss"),
#             "cvss_vector": data.get("cvss-vector"),
#             "published_date": data.get("Published"),
#             "last_modified_date": data.get("Modified"),
#             "references": data.get("references", [])
#         }

#     except Exception as e:
#         return {
#             "cve_id": cve_id,
#             "error": f"Failed to retrieve CVE from CIRCL: {str(e)}"
#         }


# if __name__ == "__main__":
#     test_id = "CVE-2023-34362"
#     result = decode_cve(test_id)
#     print("=== Test Output ===")
#     print(json.dumps(result, indent=2))
