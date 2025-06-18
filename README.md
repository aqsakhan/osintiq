# OSINTIQ: AI-Powered SOC Intelligence Hub

**OSINTIQ** is an AI-enhanced cybersecurity assistant designed to automate the analysis and enrichment of security alerts for Security Operations Center (SOC) analysts.  
It leverages OSINT data, MITRE ATT&CK mappings, and AI-generated SOC action steps to reduce cognitive load and accelerate incident response.

---

## 🚀 Features

- 🔍 **Natural Language Alert Parsing** via LLaMA 3 (Groq API)
- 🧠 **Threat Indicator Enrichment**:
  - IP Analysis (via VirusTotal)
  - Hash Intelligence (via VirusTotal)
  - CVE Decoding (via NVD)
  - Email Reputation (via EmailRep.io)
- 🎯 **MITRE ATT&CK Mapping** (via MITRE STIX data)
- 🎭 **Threat Actor Linking** (APT groups via STIX `intrusion-set`)
- 📋 **AI-Generated SOC Recommendations**
- 🖥️ **Interactive Frontend with Typewriter Output**

---

## 🗂️ Folder Structure

```
mcp_server/
├── core/
│   └── prompt_builder.py         # Builds prompts for LLM responses
├── modules/
│   ├── cve_decoder.py            # CVE decoding using NVD
│   ├── email_analyzer.py         # Email reputation via EmailRep.io
│   ├── hash_analyzer.py          # File hash analysis via VirusTotal
│   ├── ip_enricher.py            # IP reputation via VirusTotal
│   ├── mitre_map_actor_linker.py# Maps techniques & actors from STIX
│   ├── mitre_utils.py           # Loads MITRE STIX data from GitHub
│   └── response_suggester.py     # Generates AI response recommendations
├── groq_llama3.py                # LLaMA 3 integration via Groq API
├── server.py                     # Flask backend server
└── test.py                       # Optional testing scripts

frontend/
├── src/
│   ├── App.jsx                   # Main React component
│   ├── main.jsx                  # React app entry point
│   └── styles.css                # Custom CSS (dark theme, console UI)
├── public/
│   └── index.html                # HTML shell for React app
└── vite.config.js                # Vite configuration

.env                              # Contains API keys for Groq, VT, EmailRep
README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/osintiq.git
cd osintiq
```

### 2. Configure API Keys

Create a `.env` file in the root and add:

```env
GROQ_API_KEY=your_groq_key
VIRUSTOTAL_API_KEY=your_virustotal_key
EMAILREP_API_KEY=your_emailrep_key
```

### 3. Install Backend Dependencies

```bash
cd mcp_server
pip install -r requirements.txt
```

### 4. Start Flask Backend

```bash
python server.py
```

### 5. Start Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

---

## 📎 Example Input

> I found this IP 185.100.87.202 and a suspicious hash e99a18c428cb38d5f260853678922e03 linked to CVE-2023-34362

---

## 📄 Future Enhancements

- 🔄 AI-guided feedback loop for SOC analyst suggestions
- 🧠 LLM-based threat actor fingerprinting
- 📦 File upload for hash extraction
- 🧬 Custom YARA rule generation
- 📊 SOC metrics dashboard

---

## 👩‍💻 Built With

- Python (Flask)
- React + Vite
- OpenAI SDK (Groq endpoint)
- STIX 2.1 & MITRE ATT&CK
- VirusTotal API
- EmailRep.io
- Markdown-based AI Prompting

---

## 🛡️ License

MIT License

---

## 🤝 Acknowledgements

- [MITRE ATT&CK](https://attack.mitre.org/)
- [VirusTotal](https://www.virustotal.com/)
- [EmailRep.io](https://emailrep.io/)
- [Groq](https://groq.com/)
