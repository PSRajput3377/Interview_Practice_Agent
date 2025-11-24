from typing import Dict

class ScoreEngine:
    """
    Simple deterministic scoring engine.
    Later we will replace with full LLM-based scoring.
    """

    def __init__(self):
        pass

    def simple_scoring(self, answer: str) -> Dict[str, float]:
        """
        Basic scoring rules:
        - depth score: based on length of response
        - communication clarity: penalizes very long rambling answers
        - technical score: same as depth for now
        """

        text = answer or ""
        words = len(text.split())

        # depth score (based on detail/length)
        if words < 10:
            depth = 3.0
        elif words < 30:
            depth = 6.0
        else:
            depth = 8.0

        # communication clarity
        # long answers slightly penalized
        communication = 7.0 if words <= 120 else 6.0

        return {
            "depth": round(depth, 1),
            "communication": round(communication, 1),
            "technical": round(depth, 1),
        }

