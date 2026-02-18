'''
Docstring for backend.services.llm_chat.conversation_manager
keeps track of the previous question and answer as well and count the question and decides when to stop asking questions
'''
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
    
    def add_exchange(self, question: str, answer: str):
        """Add a Q&A pair to conversation history"""
        self.conversation_history.append({
            "question": question,
            "answer": answer
        })
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
            context += f"Q{i}: {exchange['question']}\n"
            context += f"A{i}: {exchange['answer']}\n\n"
        
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
