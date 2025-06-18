def build_prompt(results: dict) -> str:
    prompt_parts = []

    # Add MITRE mapping context
    mitre_data = results.get("mitre_mapping", [])
    if mitre_data:
        mitre_section = "### Mapped MITRE Techniques:\n"
        for item in mitre_data:
            mitre_section += f"- {item['name']} ({item['mitre_id']})\n"
            mitre_section += f"  Description: {item['description']}\n"
            mitre_section += f"  Tactics: {', '.join(item.get('tactics', []))}\n"
            mitre_section += f"  Kill Chain Phases: {', '.join(item.get('kill_chain_phases', []))}\n"
            mitre_section += f"  Link: {item['url']}\n\n"
        prompt_parts.append(mitre_section)
    else:
        prompt_parts.append("### Mapped MITRE Techniques:\nNone found.\n")

    # Add threat actor linking
    actors = results.get("actor_linking", [])
    if actors:
        actor_section = "### Potential Threat Actors:\n"
        for actor in actors:
            if isinstance(actor, dict):  # <-- prevent crash on string
                actor_section += f"- {actor.get('name', 'Unknown')}: {actor.get('description', 'No description')} (ID: {actor.get('id', 'N/A')})\n"
            else:
                actor_section += f"- {actor} (no details available)\n"
        prompt_parts.append(actor_section)
    else:
        prompt_parts.append("### Potential Threat Actors:\nNone linked.\n")


    # Add IP enrichment
    ips = results.get("ip_enrichment", [])
    if ips:
        ip_section = "### IP Enrichment:\n"
        for ip in ips:
            ip_section += f"- {ip['ip']}: {ip.get('location', 'Unknown')} | {ip.get('threat_level', 'Unknown')}\n"
        prompt_parts.append(ip_section)

    # Add CVE analysis
    cve_data = results.get("cve_analysis", [])
    if cve_data:
        cve_section = "### CVE Analysis:\n"
        for cve in cve_data:
            cve_section += f"- {cve['id']}: {cve['summary']} (Severity: {cve['cvss']})\n"
        prompt_parts.append(cve_section)

    # Add malware analysis (hashes)
    malware_data = results.get("malware_analysis", [])
    if malware_data:
        malware_section = "### Malware/Hash Analysis:\n"
        for sample in malware_data:
            malware_section += f"- {sample['hash']}: {sample.get('malware_name', 'Unknown')} | {sample.get('threat_type', 'Unknown')}\n"
        prompt_parts.append(malware_section)

    # Add email analysis
    emails = results.get("email_analysis", [])
    if emails:
        email_section = "### Email Analysis:\n"
        for entry in emails:
            email_section += f"- From: {entry['sender']}, Subject: {entry['subject']}, Suspicious: {entry['suspicious']}\n"
        prompt_parts.append(email_section)

    # Final request to the LLM
    prompt_parts.append(
        "### Instruction:\n"
        "Based on the data above, generate a concise SOC analyst recommendation outlining the next response steps. "
        "Prioritize mitigation, containment, and investigation actions. Keep it actionable."
    )

    return "\n".join(prompt_parts)