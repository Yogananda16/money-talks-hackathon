import re
import os
import chromadb
from load_documents import load_documents  # adjust import path if different

CHROMA_DIR = "chroma_db"  # <- confirm this matches your actual path

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("company_evidence")


def chunk_document(text, filename, max_chars=800, overlap=100):
    """
    Splits on paragraph boundaries (never mid-sentence), keeps a small
    overlap between chunks so context isn't lost at the boundary, and
    prefixes each chunk with its source filename for cheap context injection.
    """
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


def build_index():
    documents = load_documents()  # expects list of dicts: {"filename": ..., "text": ...}

    ids, texts, metadatas = [], [], []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["filename"])
        for i, chunk in enumerate(chunks):
            ids.append(f"{doc['filename']}::{i}")
            texts.append(chunk)
            metadatas.append({"filename": doc["filename"], "chunk_index": i})

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])  # clear old data so re-runs don't duplicate

    collection.add(ids=ids, documents=texts, metadatas=metadatas)
    print(f"Indexed {len(texts)} chunks from {len(documents)} documents.")
    return collection


def search(query, n_results=3):
    return collection.query(query_texts=[query], n_results=n_results)


if __name__ == "__main__":
    build_index()
    results = search("Is MFA required?")
    for doc in results["documents"][0]:
        print(doc[:300])
        print("---")