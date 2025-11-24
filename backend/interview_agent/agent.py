"""
InterviewAgent implementation with:
- Behavior Classification
- Follow-up Logic
- Confusion handling
- Off-topic handling
- Short/Long answer handling
- Evaluation
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, QUESTION_TEMPLATES, BEHAVIOR_CLASSIFIER_PROMPT
from .memory import SessionMemory
from .scoring import ScoreEngine

from langchain_google_genai import ChatGoogleGenerativeAI

# Load API Key
load_dotenv(".env")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY not found in .env")


# Initialize Gemini LLM
_llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.2,
    max_output_tokens=600,
    google_api_key=GEMINI_KEY
)


def _call_llm(prompt: str) -> str:
    """
    Calls Gemini via LangChain wrapper.
    """
    response = _llm.invoke(prompt)

    # LangChain returns .content for chat models
    if hasattr(response, "content"):
        return response.content.strip()

    return str(response).strip()


class InterviewAgent:
    def __init__(self, memory: Optional[SessionMemory] = None):
        self.memory = memory or SessionMemory()
        self.scorer = ScoreEngine()

    # ----------------------------------------------------------
    # START INTERVIEW
    # ----------------------------------------------------------
    def start_interview(self, session_id: str, role: str) -> Dict[str, Any]:
        """Creates session & returns first interview question."""
        self.memory.create_session(session_id, role)

        templates = QUESTION_TEMPLATES.get(
            role, QUESTION_TEMPLATES["software_engineer"]
        )
        first_question = templates[0]

        metadata = {"difficulty": "easy", "topic": role}

        self.memory.append_question(session_id, first_question, metadata)

        return {
            "type": "interviewer_question",
            "message": first_question,
            "metadata": metadata
        }

    # ----------------------------------------------------------
    # ASK NEXT QUESTION
    # ----------------------------------------------------------
    def ask_next_question(self, session_id: str) -> Dict[str, Any]:
        session = self.memory.get(session_id)

        role = session["role"]
        asked_qs = {q["q"] for q in session["questions_asked"]}

        templates = QUESTION_TEMPLATES.get(
            role, QUESTION_TEMPLATES["software_engineer"]
        )

        next_q = None
        for q in templates:
            if q not in asked_qs:
                next_q = q
                break

        if not next_q:
            return {
                "type": "final_summary",
                "message": "We completed the planned questions. Would you like detailed feedback?",
                "metadata": {"topic": "wrap-up", "difficulty": "easy"}
            }

        metadata = {"difficulty": "medium", "topic": role}
        self.memory.append_question(session_id, next_q, metadata)

        return {
            "type": "interviewer_question",
            "message": next_q,
            "metadata": metadata
        }

    # ----------------------------------------------------------
    # HANDLE ANSWER (behavior + follow-up + evaluation)
    # ----------------------------------------------------------
    def handle_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        session = self.memory.get(session_id)
        self.memory.append_answer(session_id, answer)
        self.memory.increment_turn(session_id)

        last_q = session["last_question"]

        # 1️⃣ Classify user behavior
        classify_prompt = f"""
{SYSTEM_PROMPT}

Classify the user's behavior.

User message:
{answer}

{BEHAVIOR_CLASSIFIER_PROMPT}
"""

        behavior = _call_llm(classify_prompt).strip().upper()

        # DEBUG print (optional)
        # print("BEHAVIOR:", behavior)

        # 2️⃣ Routing logic
        if behavior == "CONFUSED":
            self.memory.increment_confusion(session_id)
            return {
                "type": "interviewer_question",
                "message": f"Sure, let me simplify that:\n\n{last_q}",
                "metadata": {"topic": "clarification", "difficulty": "easy"}
            }

        if behavior == "OFF_TOPIC":
            self.memory.increment_off_topic(session_id)
            return {
                "type": "interviewer_question",
                "message": f"Let's stay focused. Please answer the question again:\n\n{last_q}",
                "metadata": {"topic": "redirect", "difficulty": "easy"}
            }

        if behavior == "CHATTY":
            return {
                "type": "interviewer_question",
                "message": f"😄 Haha! But let's continue. Here's the question again:\n\n{last_q}",
                "metadata": {"topic": "redirect", "difficulty": "easy"}
            }

        if behavior == "SHORT_ANSWER":
            return {
                "type": "followup_question",
                "message": "Can you explain that more? Give me more detail.",
                "metadata": {"topic": "depth", "difficulty": "medium"}
            }

        if behavior == "OVERLONG_ANSWER":
            return {
                "type": "followup_question",
                "message": "That's detailed! Can you summarize your answer in 2–3 sentences?",
                "metadata": {"topic": "summary", "difficulty": "medium"}
            }

        # 3️⃣ Normal answer → simple scoring
        scores = self.scorer.simple_scoring(answer)

        evaluation_msg = (
            f"Evaluation:\n"
            f"- Depth: {scores['depth']}/10\n"
            f"- Communication: {scores['communication']}/10\n"
            f"- Technical: {scores['technical']}/10"
        )

        return {
            "type": "evaluation",
            "message": evaluation_msg,
            "metadata": {"scores": scores}
        }

    # ----------------------------------------------------------
    # END INTERVIEW
    # ----------------------------------------------------------
    def end_interview(self, session_id: str) -> Dict[str, Any]:
        session = self.memory.end_session(session_id)

        if not session:
            return {
                "type": "final_summary",
                "message": "Session not found.",
                "metadata": {}
            }

        return {
            "type": "final_summary",
            "message": "Interview completed.",
            "metadata": {
                "role": session["role"],
                "questions_asked": len(session["questions_asked"]),
                "answers_given": len(session["answers"]),
                "confusion_count": session["confusion_count"],
                "off_topic_count": session["off_topic_count"]
            }
        }

