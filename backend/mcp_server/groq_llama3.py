# mcp_server/groq_llama3.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a smart cybersecurity assistant. Always respond with JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        content = response.choices[0].message.content.strip()

        # Remove markdown wrappers like ```json
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]

        return content

    except Exception as e:
        print(f"[Groq LLM Error] {e}")
        return '{"error": "Groq LLM failed"}'
