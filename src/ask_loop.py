import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

def check_needs_followup(question, answer):
    prompt = f"""A security questionnaire question was asked, and an employee gave an answer.
Question: {question}
Answer: {answer}

Judge if this answer is specific enough to record as final, or too vague and needs a follow-up question for more detail (e.g. frequency, method, scope).

Respond in JSON only:
{{"needs_followup": true, "followup_question": "..."}} or {{"needs_followup": false}}"""
    response = model.generate_content(prompt)
    text = response.text.strip().strip("```json").strip("```")
    return json.loads(text)

with open("../security_profile.json") as f:
    profile = {k: v for k, v in json.load(f).items()}

with open("../questions.json") as f:
    questions = {str(q["id"]): q["question"] for q in json.load(f)}

unknowns = [pid for pid, p in profile.items() if p["status"] == "unknown"]

print(f"\n{len(unknowns)} questions need to be asked.\n")

for pid in unknowns:
    question = questions[pid]
    print(f"Q{pid}: {question}")
    answer = input("Your answer: ")

    try:
        check = check_needs_followup(question, answer)
    except Exception as e:
        print(f"(Follow-up check failed, accepting answer as-is: {e})")
        check = {"needs_followup": False}

    if check.get("needs_followup"):
        print(f"  -> Follow-up: {check['followup_question']}")
        more = input("  Your answer: ")
        answer = f"{answer}. Additional detail: {more}"

    profile[pid]["answer"] = answer
    profile[pid]["status"] = "confirmed"
    profile[pid]["evidence"] = "Employee interview response"
    profile[pid]["source"] = "Employee (verbal/typed)"
    print()

with open("../security_profile.json", "w") as f:
    json.dump(profile, f, indent=2)

print("All questions answered. Profile updated.")