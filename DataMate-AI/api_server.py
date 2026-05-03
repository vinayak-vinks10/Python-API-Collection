"""
api_server.py — Run this alongside Streamlit for real AI responses in the chatbot UI.

Usage:
  Terminal 1: python api_server.py
  Terminal 2: streamlit run app.py

The chatbot JS will POST to http://localhost:8000/chat and get real AI replies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_logic import get_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = get_response(req.message)
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
