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


def search_and_answer(topic, question_text):
    """Search company data -> Complete, evidence-backed answer?"""
    search_query = build_search_query(topic, question_text)
    candidates = hybrid_search(search_query, k=15)
    evidence = rerank(search_query, candidates)

    if not evidence:
        return None  # no confident evidence — triggers the "ask employee" branch

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
    avg_score = sum(s for _, s in evidence) / len(evidence)

    return {
        "answer": answer,
        "sources": extract_sources(evidence),
        "evidence": [t for t, s in evidence],
        "confidence": round(float(avg_score), 2)  # rough proxy, not a calibrated probability yet
    }


def ask_employee(question_text):
    """Ask employee / follow-up — CLI stand-in for the future chat UI."""
    print(f"\n🧑\u200d💼 Couldn't find this in the documents — can you answer?")
    print(f"   {question_text}")
    return input("   Your answer: ").strip()


def needs_followup(question_text, answer):
    """Smart follow-up: LLM decides if the employee's answer is complete or too vague."""
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
        profile[str(question_id)] = {
            "id": question_id, "topic": topic, "question": question_text,
            "status": "verified", "answer": result["answer"],
            "sources": result["sources"], "confidence": result["confidence"],
            "evidence": result["evidence"]
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
            "sources": ["employee"], "confidence": 1.0, "evidence": []
        }

    save_profile(profile)


def run():
    with open("questions.json") as f:
        questions = json.load(f)

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


if __name__ == "__main__":
    run()