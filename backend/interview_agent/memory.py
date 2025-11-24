from typing import Dict, Any
import time

class SessionMemory:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str, role: str):
        self.sessions[session_id] = {
            "role": role,
            "questions_asked": [],
            "answers": [],
            "created_at": time.time(),
            "turn_count": 0,
            "confusion_count": 0,
            "off_topic_count": 0,
            "last_question": None,
            "metadata": {}
        }

    def get(self, session_id: str):
        return self.sessions.get(session_id)

    def increment_turn(self, session_id: str):
        self.sessions[session_id]["turn_count"] += 1

    def increment_confusion(self, session_id: str):
        self.sessions[session_id]["confusion_count"] += 1

    def increment_off_topic(self, session_id: str):
        self.sessions[session_id]["off_topic_count"] += 1

    def set_last_question(self, session_id: str, question: str):
        self.sessions[session_id]["last_question"] = question

    def append_question(self, session_id: str, question: str, metadata: dict):
        self.sessions[session_id]["questions_asked"].append(
            {"q": question, "metadata": metadata}
        )
        self.set_last_question(session_id, question)

    def append_answer(self, session_id: str, answer: str):
        self.sessions[session_id]["answers"].append(answer)

    def end_session(self, session_id: str):
        return self.sessions.pop(session_id, None)

