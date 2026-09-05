import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

def check_conflict(question, sources):
    source_block = "\n\n".join(f"[{s['source']}]: {s['text']}" for s in sources)
    prompt = f"""Question being answered: {question}

Here are excerpts from different company documents that relate to this question:
{source_block}

Do these sources agree, or do they conflict with each other (different facts, numbers, or claims)?

Respond in JSON only:
{{"conflict": true/false, "explanation": "...", "recommended_action": "..."}}"""
    response = model.generate_content(prompt)
    text = response.text.strip().strip("```json").strip("```")
    return text

if __name__ == "__main__":
    sources = [
        {"source": "Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx",
         "text": "RTO/RPO targets less than 24 hours. No restore or recovery test has yet been performed. Does not maintain backups in a second geographic region."},
        {"source": "Regodit AI_SOC2_Type_II_Report_Test.docx",
         "text": "Automated database backup processes with cross-region replication. RTO/RPO targeting less than 24 hours, leveraging AWS multi-AZ architecture."}
    ]
    result = check_conflict("What is the process for disaster recovery and backups?", sources)
    print(result)