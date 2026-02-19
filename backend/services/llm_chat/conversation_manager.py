# conversation_manager.py
from typing import List, Dict, Optional

class ConversationManager:
    """Manages multi-turn conversation state for symptom gathering"""
    
    def __init__(self, max_questions: int = 6):
        self.max_questions = max_questions
        self.question_count = 0
        self.conversation_history: List[Dict[str, str]] = []
        self.gathered_symptoms: List[str] = []
        self.stage = "initial"  # initial, questioning, diagnosing, concluded
    
    def add_exchange(self, speaker: str, message: str):
        """Add a message to conversation history"""

        self.conversation_history.append({
            "speaker": speaker,
            "message": message
        })

        # Only count assistant medical questions
        if speaker == "Assistant" and self.stage != "concluded":
            self.question_count += 1

    
    def add_symptom(self, symptom: str):
        """Add identified symptom to list"""
        if symptom and symptom not in self.gathered_symptoms:
            self.gathered_symptoms.append(symptom)
    
    def can_ask_more_questions(self) -> bool:
        """Check if we can ask more questions"""
        return self.question_count < self.max_questions
    
    def get_conversation_context(self) -> str:
        """Format conversation history for LLM context"""
        context = f"Questions asked so far: {self.question_count}/{self.max_questions}\n\n"
        context += "Conversation history:\n"
        for i, exchange in enumerate(self.conversation_history, 1):
            context += f"{exchange['speaker']}: {exchange['message']}\n"

        
        if self.gathered_symptoms:
            context += f"Gathered symptoms: {', '.join(self.gathered_symptoms)}\n"
        
        return context
    
    def should_conclude(self) -> bool:
        """Determine if conversation should end"""
        return self.question_count >= self.max_questions or self.stage == "concluded"
    
    def reset(self):
        """Reset conversation state"""
        self.question_count = 0
        self.conversation_history = []
        self.gathered_symptoms = []
        self.stage = "initial"
