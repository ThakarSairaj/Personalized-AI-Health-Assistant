from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from services.llm_chat.module2_1 import KbManager
from services.llm_chat.conversation_manager import ConversationManager
from services.llm_chat.llm_utils import generate_medical_response

router = APIRouter()

# ======================================================
# In-memory session storage
# ======================================================
user_sessions: Dict[str, dict] = {}

kb_manager = KbManager()

# ======================================================
# Request / Response Schema
# ======================================================
class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    type: str
    content: str


# ======================================================
# Main Chat Endpoint
# ======================================================
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_id = request.user_id
    user_input = request.message.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="Empty message")

    # Initialize session if new user
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "conv_mgr": ConversationManager(),
            "initial_query": ""
        }

    session = user_sessions[user_id]
    conv_mgr = session["conv_mgr"]

    # Reset if conversation concluded
    if conv_mgr.stage == "concluded":
        conv_mgr.reset()
        session["initial_query"] = ""

    # Store initial query only once
    if not session["initial_query"]:
        session["initial_query"] = user_input

    # Store user message
    conv_mgr.conversation_history.append({
        "question": "User",
        "answer": user_input
    })

    # Call unified LLM engine
    response_data = generate_medical_response(
        session["initial_query"],
        conv_mgr.get_conversation_context(),
        user_id,
        kb_manager
    )

    response_type = response_data.get("type", "final")
    response_content = response_data.get("content", "")

    # Handle response types
    if response_type == "question":
        conv_mgr.conversation_history.append({
            "question": "Assistant",
            "answer": response_content
        })
        return ChatResponse(type="question", content=response_content)

    elif response_type == "reset":
        conv_mgr.reset()
        session["initial_query"] = ""
        return ChatResponse(type="reset", content=response_content)

    else:  # final
        conv_mgr.stage = "concluded"
        conv_mgr.conversation_history.append({
            "question": "Assistant",
            "answer": response_content
        })
        return ChatResponse(type="final", content=response_content)
