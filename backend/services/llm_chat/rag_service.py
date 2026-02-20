import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection("medical_memory")
model = SentenceTransformer("all-MiniLM-L6-v2")


def save_symptom(user_id: str, symptom_text: str):

    embedding = model.encode(symptom_text).tolist()

    collection.add(
        documents=[symptom_text],
        embeddings=[embedding],
        metadatas=[{
            "user_id": user_id,
            "timestamp": str(datetime.now())
        }],
        ids=[f"{user_id}_{datetime.now().timestamp()}"]
    )


def retrieve_similar(user_id: str, query: str, top_k=3):
    
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"user_id": user_id}
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    docs = results["documents"][0]
    distances = results["distances"][0]

    filtered = [
        doc for doc, dist in zip(docs, distances)
        if dist < 0.85
    ]

    print("Retrieved memories:", filtered)
    print("Distances:", distances)

    return filtered


