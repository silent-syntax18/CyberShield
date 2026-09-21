import os
from dotenv import load_dotenv
from groq import Groq

from rag.rag_engine import get_context

load_dotenv()

# ============================================================
# CyberShield AI Configuration
# ============================================================

MODEL = "openai/gpt-oss-120b"

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)


def ask_cybershield(question, language="English"):
    """
    Ask CyberShield AI using RAG knowledge.
    """

    context = get_context(question)

    system_prompt = """
You are CyberShield AI, a defensive cybersecurity assistant.

Your responsibilities:
- Explain cybersecurity concepts clearly.
- Analyze security-related questions.
- Give defensive and educational recommendations.
- Use the supplied CyberShield knowledge base when relevant.
- Do not invent facts when the knowledge base does not contain enough information.
- Clearly mention uncertainty when information is incomplete.
- Never claim that an IP address gives an exact physical location.
- Never claim that a URL alone identifies a person's exact identity or device.
- For suspicious links, focus on safe analysis and defensive guidance.
- Do not provide instructions for malware creation, credential theft,
  unauthorized access, evasion, or other harmful activity.

Language rules:
- If the user asks in English, answer in English.
- If the user asks in Roman Urdu, answer in Roman Urdu.
- If the user mixes English and Roman Urdu, you may use the same mixed style.

Keep answers practical and easy to understand.
"""

    user_prompt = f"""
Cybersecurity knowledge retrieved from CyberShield RAG:

{context}

--------------------------------------------------

User question:

{question}

Answer using the relevant knowledge above.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=1200
    )

    return response.choices[0].message.content