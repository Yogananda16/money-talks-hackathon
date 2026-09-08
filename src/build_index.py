import re
import os
import json
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer
from load_documents import load_documents

CHROMA_DIR = "chroma_db"
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"
COLLECTION_NAME = "company_evidence"
CHECKPOINT_EMB = "embeddings_checkpoint.npy"
CHECKPOINT_META = "chunks_checkpoint.json"

client = chromadb.PersistentClient(path=CHROMA_DIR)

print("Loading embedding model (one-time)...")
embedder = SentenceTransformer(EMBED_MODEL)


def chunk_document(text, filename, max_chars=800, overlap=100):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) > max_chars and current:
            chunks.append(current.strip())
            current = current[-overlap:] + "\n\n" + para
        else:
            current += ("\n\n" if current else "") + para
    if current.strip():
        chunks.append(current.strip())
    return [f"[{filename}]\n{c}" for c in chunks]


def get_fresh_collection():
    """
    Deletes and recreates the collection instead of reusing whatever's on disk.
    Chroma locks in the embedding dimension on first use — reusing an old
    collection after switching embedding models causes a dimension-mismatch
    crash on add(), AFTER the expensive embedding step, not before.
    """
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # didn't exist yet — fine
    return client.create_collection(COLLECTION_NAME)


def build_index():
    documents = load_documents()

    ids, texts, metadatas = [], [], []
    for doc in documents:
        for i, chunk in enumerate(chunk_document(doc["text"], doc["filename"])):
            ids.append(f"{doc['filename']}::{i}")
            texts.append(chunk)
            metadatas.append({"filename": doc["filename"], "chunk_index": i})

    print(f"Embedding {len(texts)} chunks (one-time cost, may take a while on CPU)...")
    embeddings = embedder.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    # Checkpoint immediately — if collection.add() fails for any reason,
    # you reload this instead of recomputing 50+ minutes of embeddings.
    np.save(CHECKPOINT_EMB, embeddings)
    with open(CHECKPOINT_META, "w") as f:
        json.dump({"ids": ids, "texts": texts, "metadatas": metadatas}, f)
    print(f"Checkpoint saved ({CHECKPOINT_EMB}, {CHECKPOINT_META}) — safe even if the next step fails.")

    collection = get_fresh_collection()
    collection.add(ids=ids, documents=texts, embeddings=embeddings.tolist(), metadatas=metadatas)
    print(f"Indexed {len(texts)} chunks from {len(documents)} documents.")
    return collection


def test_search(collection, query, n_results=3):
    q_emb = embedder.encode([query], normalize_embeddings=True).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=n_results)
    print(f"\nTest search: '{query}'\n")
    for doc in results["documents"][0]:
        print(doc[:300])
        print("---")


if __name__ == "__main__":
    coll = build_index()
    test_search(coll, "Is MFA required?")