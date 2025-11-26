# vectorstore/chroma_client.py — ФИНАЛЬНАЯ ЛОКАЛЬНАЯ ВЕРСИЯ
import chromadb
from chromadb.utils import embedding_functions
import os

# Локальная модель — быстро и без API
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="intfloat/multilingual-e5-large"
)

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(
    name="lots",
    embedding_function=embedding_func
)

def add_lot(lot_id: str, text: str, metadata: dict):
    try:
        collection.add(
            ids=[lot_id],
            documents=[text],
            metadatas=[metadata]
        )
    except Exception as e:
        print(f"Ошибка добавления {lot_id}: {e}")

def search_similar(query: str, top_k: int = 100, filter_dict: dict = None):
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=filter_dict
        )
        return [
            {
                "id": id_,
                "text": doc,
                "metadata": meta,
                "distance": dist
            }
            for id_, doc, meta, dist in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []

print("Chroma + multilingual-e5-large готова! (без API, молниеносно)")