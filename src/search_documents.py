import json
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
from llm_client import ask_ollama

CHROMA_DIR = "chroma_db"
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"
RERANK_MODEL = "Qwen/Qwen3-Reranker-0.6B"
MIN_RERANK_SCORE = 0.3
OUTPUT_PATH = "security_profile.json"

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("company_evidence")

print("Loading embedding + reranker models (one-time)...")
embedder = SentenceTransformer(EMBED_MODEL)
reranker = CrossEncoder(RERANK_MODEL)

all_docs = collection.get()
all_ids = all_docs["ids"]
all_texts = all_docs["documents"]
bm25 = BM25Okapi([t.lower().split() for t in all_texts])
id_to_text = dict(zip(all_ids, all_texts))


def is_valid_question(text):
    text = text.strip()
    if len(text) < 10:
        return False, "too short to be a real question"
    if text.replace(".", "", 1).isdigit():
        return False, "question text is just a number"
    if not any(c.isalpha() for c in text):
        return False, "contains no letters"
    return True, None


def build_search_query(topic, question_text):
    return f"{topic}: {question_text}" if topic else question_text


def hybrid_search(query, k=30, final_k=20, bm25_weight=2.0):
    q_emb = embedder.encode([query], normalize_embeddings=True).tolist()
    dense_hits = collection.query(query_embeddings=q_emb, n_results=k)["ids"][0]
    bm25_scores = bm25.get_scores(query.lower().split())
    ranked_idx = sorted(range(len(all_ids)), key=lambda i: -bm25_scores[i])[:k]
    sparse_hits = [all_ids[i] for i in ranked_idx]
    scores = {}
    for rank, doc_id in enumerate(dense_hits):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (60 + rank)
    for rank, doc_id in enumerate(sparse_hits):
        scores[doc_id] = scores.get(doc_id, 0) + bm25_weight * (1 / (60 + rank))
    top_ids = sorted(scores, key=scores.get, reverse=True)[:final_k]
    return [id_to_text[i] for i in top_ids]


def rerank(query, candidates, n_results=3, min_score=MIN_RERANK_SCORE):
    pairs = [(query, c) for c in candidates]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    return [(c, s) for c, s in ranked if s >= min_score][:n_results]


def extract_sources(evidence_chunks):
    """Pulls the [filename] prefix off each chunk and dedupes — 
    turns raw evidence chunks into a clean citation list."""
    sources = []
    for chunk, score in evidence_chunks:
        if chunk.startswith("["):
            filename = chunk.split("]")[0].lstrip("[")
            if filename not in sources:
                sources.append(filename)
    return sources


def answer_question(question_id, topic, question_text):
    valid, reason = is_valid_question(question_text)
    if not valid:
        return {
            "id": question_id, "topic": topic, "question": question_text,
            "status": "malformed_input", "answer": None, "sources": [], "evidence": [],
            "note": f"Skipped pipeline — {reason}."
        }

    search_query = build_search_query(topic, question_text)
    candidates = hybrid_search(search_query)
    evidence = rerank(search_query, candidates)

    if not evidence:
        return {
            "id": question_id, "topic": topic, "question": question_text,
            "status": "unknown", "answer": None, "sources": [], "evidence": []
        }

    context = "\n\n---\n\n".join(text for text, score in evidence)
    topic_line = f"This question is under the '{topic}' section of a vendor security questionnaire.\n" if topic else ""
    prompt = f"""You are a security analyst answering a vendor security questionnaire.
{topic_line}Answer using ONLY the evidence below. If it doesn't clearly answer the question,
say so explicitly instead of guessing.

Evidence:
{context}

Question: {question_text}

Give a direct answer grounded only in the evidence above."""

    answer = ask_ollama(prompt)

    return {
        "id": question_id, "topic": topic, "question": question_text,
        "status": "verified", "answer": answer,
        "sources": extract_sources(evidence),
        "evidence": [t for t, s in evidence]
    }


def process_all_questions(questions_path="questions.json", output_path=OUTPUT_PATH):
    with open(questions_path) as f:
        questions = json.load(f)

    profile = []
    already_done_ids = set()
    try:
        with open(output_path) as f:
            profile = json.load(f)
            already_done_ids = {p["id"] for p in profile}
        print(f"Resuming — {len(already_done_ids)} question(s) already answered, skipping those.\n")
    except FileNotFoundError:
        pass

    for i, q in enumerate(questions):
        if q["id"] in already_done_ids:
            continue

        print(f"\n[{i+1}/{len(questions)}] ({q.get('topic')}) {q['question']}")
        result = answer_question(q["id"], q.get("topic"), q["question"])
        profile.append(result)

        print(f"  -> {result['status']}")
        if result["status"] == "verified":
            print(f"  Sources: {result['sources']}")
            print(f"  Answer: {result['answer'][:150]}...")

        with open(output_path, "w") as f:
            json.dump(profile, f, indent=2)

    verified = sum(1 for p in profile if p["status"] == "verified")
    unknown = sum(1 for p in profile if p["status"] == "unknown")
    malformed = sum(1 for p in profile if p["status"] == "malformed_input")
    print(f"\nDone. {verified} verified, {unknown} unknown, {malformed} malformed input.")

    from collections import Counter
    topic_unknowns = Counter(p["topic"] for p in profile if p["status"] == "unknown")
    if topic_unknowns:
        print("\nUnknowns by topic:")
        for topic, count in topic_unknowns.most_common():
            print(f"  {topic}: {count}")


if __name__ == "__main__":
    process_all_questions()