import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from mcp_server.core.prompt_builder import build_prompt

# Load environment variables
load_dotenv()

# Groq API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not set in .env")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def call_llama3(prompt: str) -> str:
    """
    Send a prompt to Groq-hosted LLaMA 3 and return the response.
    """
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a cybersecurity assistant that provides SOC-ready response recommendations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200  # allow a bit more space
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"[LLM ERROR] Groq API call failed: {e}")
        return "❌ LLaMA 3 (Groq) could not process this input. Please review manually."

def generate_response_recommendations(results: dict) -> dict:
    """
    Orchestrates prompt construction and LLM call. Returns final response.
    """
    prompt = build_prompt(results)
    print("=== ✅ Prompt Sent to LLM ===\n", prompt[:3000])  # safe print truncation if large

    response_text = call_llama3(prompt)
    print("=== ✅ LLM Output ===\n", response_text)

    return {"recommendation": response_text}
