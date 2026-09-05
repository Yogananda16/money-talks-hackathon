import os
import json
import time
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import requests
from load_documents import load_all_documents

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

def log_to_prism(question_summary, response_text):
    try:
        requests.post(
            f"{os.environ['PRISMTRACE_HOST']}/api/traces",
            headers={"X-PRISMtrace-Key": os.environ["PRISMTRACE_API_KEY"]},
            json={
                "project_id": os.environ["PRISMTRACE_PROJECT_ID"],
                "model": "gemini-3.6-flash",
                "input_messages": [{"role": "user", "content": question_summary}],
                "output_message": response_text[:2000],
                "latency_ms": 0,
                "session_id": "security-analyst-run"
            },
            timeout=5
        )
    except Exception as e:
        print(f"PRISM log failed (non-blocking): {e}")

docs = load_all_documents()
docs.pop("Regodit_Comprehensive_Vendor_Security_Questionnaire_Clean.xlsx", None)
all_text = "\n\n---\n\n".join(f"DOCUMENT: {name}\n{text}" for name, text in docs.items())

def search_all(questions):
    q_block = "\n".join(f"{q['id']}. {q['question']}" for q in questions)
    prompt = f"""Answer each question using ONLY these documents. Never guess.
Documents:
{all_text}

Questions:
{q_block}

Respond with a JSON array: [{{"id": 1, "found": true, "answer": "...", "evidence": "exact quote", "source": "filename"}}]
Only output JSON. Include all {len(questions)} question IDs."""

    response = model.generate_content(prompt)
    log_to_prism(f"Batch search: {len(questions)} questions", response.text)
    return response.text

if __name__ == "__main__":
    with open("../questions.json") as f:
        questions = json.load(f)

    print(f"Searching all {len(questions)} questions...")
    result = search_all(questions)

    with open("../profile.json", "w") as f:
        f.write(result)

    print("Done. Saved to profile.json")