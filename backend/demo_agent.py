print("🔥 Demo starting...")

from interview_agent.agent import InterviewAgent
from interview_agent.memory import SessionMemory
import uuid

print("🔥 Imports successful!")

agent = InterviewAgent(memory=SessionMemory())

session_id = str(uuid.uuid4())[:8]
print("🔥 Session:", session_id)

start = agent.start_interview(session_id, role="software_engineer")
print("🔥 First Question:", start)

