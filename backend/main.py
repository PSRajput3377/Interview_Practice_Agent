from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid

from interview_agent.agent import InterviewAgent
from interview_agent.memory import SessionMemory
from interview_agent.advanced_scoring import aggregate_report

# -------------------------------------------
# APP INITIALIZATION
# -------------------------------------------
app = FastAPI()

# Global Interview Agent
memory = SessionMemory()
agent = InterviewAgent(memory=memory)

# -------------------------------------------
# CORS (Allow all for now, restrict later)
# -------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------
# TEXT CHAT ENDPOINT
# -------------------------------------------
@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_msg = data.get("message")
    session_id = data.get("session_id")

    # If no session provided → start new interview
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
        start = agent.start_interview(session_id, role="software_engineer")
        return {"session_id": session_id, "response": start}

    # Otherwise, handle answer
    response = agent.handle_answer(session_id, user_msg)
    return {"session_id": session_id, "response": response}

# -------------------------------------------
# VAPI WEBHOOK (VOICE MODE)
# -------------------------------------------
@app.post("/vapi-webhook")
async def vapi_webhook(request: Request):
    body = await request.json()

    session_id = body.get("conversation_id")
    user_msg = body.get("transcript")

    if not session_id:
        # Start new session
        session_id = str(uuid.uuid4())[:8]
        start = agent.start_interview(session_id, role="software_engineer")
        return {
            "response": start["message"],
            "conversation_id": session_id
        }

    # Handle voice message
    result = agent.handle_answer(session_id, user_msg)

    return {
        "response": result["message"],
        "conversation_id": session_id
    }

# -------------------------------------------
# REPORT ENDPOINT (Advanced Scoring)
# -------------------------------------------
@app.post("/report")
async def generate_report(request: Request):
    data = await request.json()
    session_id = data.get("session_id")

    if not session_id:
        return {"error": "session_id is required"}

    session_data = memory.get(session_id)
    if not session_data:
        return {"error": "No session found with this ID"}

    # Build QA pairs in order
    qa_pairs = []
    for i, q in enumerate(session_data["questions_asked"]):
        answer = session_data["answers"][i] if i < len(session_data["answers"]) else ""
        qa_pairs.append({
            "question": q["q"],
            "answer": answer
        })

    # Generate full report
    report = aggregate_report(session_data["role"], qa_pairs)

    return {"session_id": session_id, "report": report}

# -------------------------------------------
# ROOT
# -------------------------------------------
@app.get("/")
async def root():
    return {"message": "Interview Practice Partner Backend Running!"}

# -------------------------------------------
# SERVER START
# -------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

