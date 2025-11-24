"""
Demo to generate a full interview report for the current in-memory session.
Run this after a demo interview (or adapt to export session data).
"""

from interview_agent.memory import SessionMemory
from interview_agent.advanced_scoring import aggregate_report

# Example: build fake session or use real one
mem = SessionMemory()
sid = "demo01"
mem.create_session(sid, "software_engineer")
mem.append_question(sid, "Explain the difference between a process and a thread.", {"difficulty": "easy"})
mem.append_answer(sid, "A thread is a lighter unit that runs in the same memory space. A process has its own memory.")
mem.append_question(sid, "What is a race condition?", {"difficulty": "medium"})
mem.append_answer(sid, "When two threads access same data without sync.")

# Convert memory into qa pairs
s = mem.get(sid)
qa_pairs = []
for i, q in enumerate(s["questions_asked"]):
    ans = s["answers"][i] if i < len(s["answers"]) else ""
    qa_pairs.append({"question": q["q"], "answer": ans})

report = aggregate_report(s["role"], qa_pairs)
import json
print(json.dumps(report, indent=2))

