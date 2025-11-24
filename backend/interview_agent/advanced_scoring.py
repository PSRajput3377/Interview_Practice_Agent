"""
LLM-powered advanced scoring and final report generator.

Outputs:
- Per-answer evaluation with numeric scores (0-10)
- Aggregated final report (averages, strengths, weaknesses, suggestions)
"""

import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(".env")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

# Use same model that works for your agent
_llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.2,
    max_output_tokens=800,
    google_api_key=GEMINI_KEY
)

def _call_llm(prompt: str) -> str:
    resp = _llm.invoke(prompt)
    if hasattr(resp, "content"):
        return resp.content.strip()
    return str(resp).strip()

# Prompt template: strict JSON output
EVAL_PROMPT_TEMPLATE = """
You are an expert interview evaluator. Evaluate the following Q&A pair and return ONLY valid JSON (no commentary).

Role: {role}
Question: {question}
User Answer: {answer}

Evaluate these categories (0-10):
- technical
- communication
- problem_solving
- structure

Also include:
- strengths: ["..",".."]
- weaknesses: ["..",".."]
- suggestions: ["..",".."]

Return EXACT JSON:
{{
  "technical": <number>,
  "communication": <number>,
  "problem_solving": <number>,
  "structure": <number>,
  "strengths": ["...","..."],
  "weaknesses": ["...","..."],
  "suggestions": ["...","..."]
}}
"""

def evaluate_answer(role: str, question: str, answer: str) -> Dict[str, Any]:
    """Run Gemini evaluation with JSON output."""
    prompt = EVAL_PROMPT_TEMPLATE.format(role=role, question=question, answer=answer)
    raw = _call_llm(prompt)

    # Try parsing JSON
    parsed = None
    try:
        parsed = json.loads(raw)
    except Exception:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(raw[start:end+1])
            except:
                parsed = None

    if not parsed:
        # fallback if Gemini returns invalid JSON
        words = len(answer.split())
        technical = min(9.0, max(1.0, words / 10))
        communication = 7.0 if words > 8 else 4.0
        problem_solving = technical * 0.9
        structure = 7.0 if words > 10 else 5.0
        return {
            "technical": round(technical, 1),
            "communication": round(communication, 1),
            "problem_solving": round(problem_solving, 1),
            "structure": round(structure, 1),
            "strengths": ["Concise", "Relevant"],
            "weaknesses": ["Needs more detail", "No examples"],
            "suggestions": ["Add examples", "Explain step-by-step"]
        }

    return parsed

def aggregate_report(role: str, qa_pairs: List[Dict[str, str]]) -> Dict[str, Any]:
    """Aggregate per-answer scores into a final interview report."""
    scores_sum = {"technical": 0, "communication": 0, "problem_solving": 0, "structure": 0}
    per_question = []
    strengths, weaknesses, suggestions = [], [], []

    for pair in qa_pairs:
        q = pair["question"]
        a = pair["answer"]
        result = evaluate_answer(role, q, a)

        per_question.append({
            "question": q,
            "answer": a,
            "evaluation": result
        })

        for k in scores_sum:
            scores_sum[k] += float(result[k])

        for item in result["strengths"]:
            if item not in strengths:
                strengths.append(item)
        for item in result["weaknesses"]:
            if item not in weaknesses:
                weaknesses.append(item)
        for item in result["suggestions"]:
            if item not in suggestions:
                suggestions.append(item)

    n = len(qa_pairs)
    avg_scores = {k: round(scores_sum[k] / n, 2) for k in scores_sum}
    overall = round(sum(avg_scores.values()) / len(avg_scores), 2)

    return {
        "scores": avg_scores,
        "overall_score": overall,
        "per_question": per_question,
        "final_summary": {
            "overall_score": overall,
            "averages": avg_scores,
            "top_strengths": strengths[:3],
            "top_weaknesses": weaknesses[:3],
            "top_suggestions": suggestions[:3]
        }
    }

