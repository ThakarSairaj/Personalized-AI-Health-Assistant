#chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from services.llm_chat.conversation_manager import ConversationManager
from services.llm_chat.llm_utils import generate_medical_response
from services.llm_chat.rag_service import save_symptom
from services.llm_chat.llm_utils import extract_condition
from datetime import datetime

router = APIRouter()

# In-memory sessions
user_sessions: Dict[str, dict] = {}


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    type: str
    content: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_id = request.user_id
    user_input = request.message.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="Empty message")

    # Initialize session if new
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "conv_mgr": ConversationManager(),
            "recurrence_detected": False
        }

    session = user_sessions[user_id]
    conv_mgr = session["conv_mgr"]

    # Reset if previous conversation ended
    if conv_mgr.stage == "concluded":
        conv_mgr.reset()
        session["recurrence_detected"] = False # Check This *********

    

    # Add user message ONCE
    conv_mgr.add_exchange("User", user_input)

###############

# Generate LLM response
    result = generate_medical_response(
        conv_mgr.get_conversation_context(),
        user_id,
        session["recurrence_detected"]
)

    response_data = result["response"]

# Update recurrence flag in session
    if result["recurrence_detected"]:
        session["recurrence_detected"] = True

    response_type = response_data.get("type", "final")
    response_content = response_data.get("content", "")

    if response_type == "question":
        conv_mgr.add_exchange("Assistant", response_content)
        return ChatResponse(type="question", content=response_content)

# Final response
    conv_mgr.stage = "concluded"
    conv_mgr.add_exchange("Assistant", response_content)

###########






    

    # Save structured memory after conclusion
    condition = extract_condition(response_content)

    conversation_text = conv_mgr.get_conversation_context()

    # Extract only user statements
    user_lines = [
    line.replace("User: ", "")
    for line in conversation_text.split("\n")
    if line.startswith("User:")
]

    symptoms_text = " ".join(user_lines)

    structured_memory = f"""
    Medical Record
    Condition: {condition}
    Symptoms: {symptoms_text}
    Date: {datetime.now().strftime("%Y-%m-%d")}
    """

    embedding_text = f"{condition}. Symptoms: {symptoms_text}"
    save_symptom(user_id, embedding_text)
    return ChatResponse(type="final", content=response_content)
