"""
Follow-up Question Generator
Uses Gemini to generate deep, structured follow-ups.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(".env")

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

_llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=200,
    google_api_key=GEMINI_KEY
)

def _call_llm(prompt: str) -> str:
    response = _llm.invoke(prompt)
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()


FOLLOWUP_SYSTEM_PROMPT = """
You are an expert technical interviewer.

Your task:
Generate a SINGLE follow-up question that:
- Is based strictly on the user’s previous answer
- Probes deeper understanding or reasoning
- Is NOT a repeated question
- Is NOT too broad
- Is NOT an explanation—must be a question only
- Should be short, precise, and interview-like

Return ONLY the question. No explanations.
"""


def generate_followup(previous_question: str, user_answer: str, role: str) -> str:
    """
    Generate deep follow-up question using Gemini.
    """

    prompt = f"""
{FOLLOWUP_SYSTEM_PROMPT}

Role: {role}

Original question:
{previous_question}

User's answer:
{user_answer}

Generate ONE deep follow-up question:
"""

    output = _call_llm(prompt)
    return output.split("\n")[0]  # return only first line

