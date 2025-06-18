# import requests

# def ask_llama(osint_context):
#     prompt = f"""
#     You are a cybersecurity analyst assistant.
#     Analyze the following OSINT data and provide a brief risk summary:

#     {osint_context}

#     Your answer should be concise and useful to a SOC analyst.
#     """

#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "llama3",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )
#         response.raise_for_status()
#         result = response.json()
#         print("💬 Raw LLaMA response:", result) # well here we dont need complete raw log --> will remove later for now i need terminal response

#         return result.get('response', 'No response from LLaMA.')

#     except Exception as e:
#         print("❌ Error querying LLaMA:", e)
#         return "No response from LLaMA."
