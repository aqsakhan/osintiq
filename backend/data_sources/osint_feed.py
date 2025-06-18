def get_osint_data(topic):
    # Mock data; later you'll pull from threat intel sources
    examples = {
        'phishing': "Recent campaigns use fake login pages to harvest credentials, especially targeting Office365.",
        'malware': "RedLine Stealer activity spiked this month, spreading through cracked software torrents.",
        'ransomware': "New BlackCat ransomware variants use improved evasion and extortion tactics."
    }

    return examples.get(topic.lower(), f"No recent OSINT found for {topic}.")
