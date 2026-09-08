import json
from search_documents import hybrid_search, rerank, extract_sources, build_search_query, is_valid_question
from llm_client import ask_ollama

PROFILE_PATH = "security_profile.json"


def load_profile():
    try:
        with open(PROFILE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def already_known(profile, question_id):
    entry = profile.get(str(question_id))
    return entry is not None and entry["status"] in ("verified", "confirmed_by_user")


def correct_answer(profile, question_id, new_answer):
    key = str(question_id)
    existing = profile.get(key)
    if existing is None:
        print(f"  No existing entry for question {question_id} — nothing to correct.")
        return

    history = existing.get("history", [])
    history.append({
        "previous_status": existing["status"],
        "previous_answer": existing["answer"],
        "previous_sources": existing.get("sources", [])
    })

    profile[key] = {
        **existing,
        "status": "confirmed_by_user",
        "answer": new_answer,
        "sources": ["employee (correction)"],
        "confidence": 1.0,
        "history": history
    }
    save_profile(profile)
    print(f"  Updated. Previous answer preserved in history ({len(history)} correction(s) total).")


def search_and_answer(topic, question_text):
    """Search company data -> Complete, evidence-backed answer?
    The LLM decides ANSWERED vs UNKNOWN itself — the code trusts that
    signal instead of assuming 'evidence exists' means 'question answered'."""
    search_query = build_search_query(topic, question_text)
    candidates = hybrid_search(search_query)
    evidence = rerank(search_query, candidates)

    if not evidence:
        return None  # no confident evidence at all — ask employee

    context = "\n\n---\n\n".join(text for text, score in evidence)
    topic_line = f"This question is under the '{topic}' section of a vendor security questionnaire.\n" if topic else ""

    prompt = f"""You are a security analyst answering a vendor security questionnaire.
{topic_line}Answer using ONLY the evidence below.

Your reply's FIRST LINE must be exactly one of:
STATUS: ANSWERED
STATUS: UNKNOWN

Use STATUS: UNKNOWN if the evidence does not clearly and directly answer the question.
Do not guess, do not partially answer, do not speculate — say UNKNOWN instead.

If ANSWERED, follow with a direct answer grounded only in the evidence.
If UNKNOWN, follow with one short sentence on what's missing.

Evidence:
{context}

Question: {question_text}"""

    raw = ask_ollama(prompt)
    lines = raw.strip().split("\n", 1)
    status_line = lines[0].strip().upper()
    body = lines[1].strip() if len(lines) > 1 else raw.strip()

    if "UNKNOWN" in status_line:
        return None  # LLM itself says it can't answer -> treat exactly like no-evidence, ask employee

    avg_score = sum(s for _, s in evidence) / len(evidence)
    return {
        "answer": body,
        "sources": extract_sources(evidence),
        "evidence": [t for t, s in evidence],
        "confidence": round(float(avg_score), 2)
    }


def ask_employee(question_text):
    print(f"\n🧑\u200d💼 Couldn't find a confirmed answer in the documents — can you answer?")
    print(f"   {question_text}")
    return input("   Your answer: ").strip()


def needs_followup(question_text, answer):
    prompt = f"""A security questionnaire question was asked, and an employee gave a short answer.
Question: {question_text}
Employee's answer: {answer}

Is this answer complete enough to record, or too vague and needing a follow-up (e.g. frequency,
method, scope)? Reply with ONLY "COMPLETE" or a single follow-up question, nothing else."""

    response = ask_ollama(prompt).strip()
    if response.upper().startswith("COMPLETE"):
        return None
    return response


def process_question(profile, question_id, topic, question_text):
    if already_known(profile, question_id):
        print(f"[{question_id}] Already known — skipping.")
        return

    print(f"\n[{question_id}] ({topic}) {question_text}")
    result = search_and_answer(topic, question_text)

    if result:
        print(f"  Found evidence -> {result['sources']}")
        print(f"  Answer: {result['answer'][:200]}...")
        profile[str(question_id)] = {
            "id": question_id, "topic": topic, "question": question_text,
            "status": "verified", "answer": result["answer"],
            "sources": result["sources"], "confidence": result["confidence"],
            "evidence": result["evidence"], "history": []
        }
    else:
        answer = ask_employee(question_text)
        followup = needs_followup(question_text, answer)
        while followup:
            print(f"   Follow-up: {followup}")
            more = input("   Your answer: ").strip()
            answer = f"{answer}. {more}"
            followup = needs_followup(question_text, answer)

        profile[str(question_id)] = {
            "id": question_id, "topic": topic, "question": question_text,
            "status": "confirmed_by_user", "answer": answer,
            "sources": ["employee"], "confidence": 1.0, "evidence": [], "history": []
        }

    save_profile(profile)


def correction_menu(profile):
    print("\n--- Correction menu ---")
    print("Enter a question ID to view/correct it, or 'done' to finish.")
    while True:
        choice = input("\nQuestion ID (or 'done'): ").strip()
        if choice.lower() == "done":
            break
        entry = profile.get(choice)
        if entry is None:
            print(f"  No stored answer for question {choice} yet.")
            continue
        print(f"  Current status: {entry['status']}")
        print(f"  Current answer: {entry['answer']}")
        print(f"  Source: {entry.get('sources')}")
        new_answer = input("  New answer (or press Enter to leave unchanged): ").strip()
        if new_answer:
            correct_answer(profile, choice, new_answer)


def run(limit=None):
    with open("questions.json") as f:
        questions = json.load(f)

    if limit:
        questions = questions[:limit]
        print(f"Running on first {limit} question(s) only.\n")

    profile = load_profile()

    for q in questions:
        valid, reason = is_valid_question(q["question"])
        if not valid:
            print(f"[{q['id']}] Skipped — {reason}")
            continue
        process_question(profile, q["id"], q.get("topic"), q["question"])

    verified = sum(1 for p in profile.values() if p["status"] == "verified")
    confirmed = sum(1 for p in profile.values() if p["status"] == "confirmed_by_user")
    print(f"\nDone. {verified} verified from documents, {confirmed} confirmed by employee.")

    correction_menu(profile)


if __name__ == "__main__":
    run(limit=5)