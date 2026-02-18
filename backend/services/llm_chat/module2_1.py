'''
Docstring for module2_1
Contains te chromaDB logic


Stores and Retrive users history using simple JSON file

What Problem Does It Solve?

Without this file:

Every conversation starts fresh.

The AI doesn’t know patient history.

No personalization.

With this file:

The system remembers past conditions.

It remembers previous insights.

It can give context-aware advice.
'''
# module2_1.py - Simple KB without embeddings
from typing import List, Dict, Any, Optional
import json
import os

class KbManager:
    """Simple knowledge base manager using JSON (no embeddings needed)"""
    
    def __init__(self, storage_path: str = "./kb_storage"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def _get_user_file(self, user_id: str) -> str:
        return os.path.join(self.storage_path, f"{user_id}.json")
    
    def _load_user_data(self, user_id: str) -> Dict:
        file_path = self._get_user_file(user_id)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {"profile": [], "insights": []}
    
    def _save_user_data(self, user_id: str, data: Dict):
        file_path = self._get_user_file(user_id)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user_profile(self, user_id: str, entries: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        """Add past medical history entries for a user"""
        if not entries:
            return
        data = self._load_user_data(user_id)
        for entry in entries:
            data["profile"].append({
                "document": entry,
                "metadata": {"type": "past_history"}
            })
        self._save_user_data(user_id, data)
    
    def add_insight_from_prompt(self, user_id: str, prompt_text: str, extracted_insights: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add insights from a user prompt"""
        data = self._load_user_data(user_id)
        insights = extracted_insights if extracted_insights else [prompt_text]
        for insight in insights:
            data["insights"].append({
                "document": insight,
                "metadata": metadata or {"type": "insight", "source": "user_prompt"}
            })
        self._save_user_data(user_id, data)
    
    def semantic_search(self, user_id: str, query: str, top_k: int = 5):
        """Simple keyword-based search (no embeddings)"""
        data = self._load_user_data(user_id)
        all_entries = data.get("profile", []) + data.get("insights", [])
        
        # Simple keyword matching
        query_lower = query.lower()
        results = []
        for entry in all_entries:
            doc_lower = entry["document"].lower()
            # Count matching words
            matches = sum(1 for word in query_lower.split() if word in doc_lower)
            if matches > 0:
                results.append({
                    "document": entry["document"],
                    "metadata": entry["metadata"],
                    "distance": 1.0 / (matches + 1)  # Lower is better
                })
        
        # Sort by distance and return top_k
        results.sort(key=lambda x: x["distance"])
        return results[:top_k]
    
    def list_all_entries(self, user_id: str) -> List[Dict[str, Any]]:
        """Return all documents and metadata for the user"""
        data = self._load_user_data(user_id)
        all_entries = data.get("profile", []) + data.get("insights", [])
        return [{"id": i, **entry} for i, entry in enumerate(all_entries)]
