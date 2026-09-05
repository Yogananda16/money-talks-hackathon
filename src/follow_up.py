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
{{"needs_followup": true/false, "followup_question": "..." or null, "reason": "..."}}"""
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    question = "Do you monitor the security of your wireless networks?"
    answer = "yes"
    try:
        result = check_needs_followup(question, answer)
        print("RESULT:", result)
    except Exception as e:
        print("ERROR:", e)