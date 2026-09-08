from search_documents import build_search_query
from llm_client import ask_ollama

topic = "Risk Assessment"
question = "Have the findings from the most recent penetration test been remediated?"

# reuse the same evidence from your last run
context = """[VAPT Report 01.docx]
...paste the VAPT chunk here...

[Regodit_information_security_policy_v1.0.docx]
...paste that chunk here..."""

prompt = f"""You are a security analyst answering a vendor security questionnaire.
Answer using ONLY the evidence below.

Your reply's FIRST LINE must be exactly one of:
STATUS: ANSWERED
STATUS: UNKNOWN

Evidence:
{context}

Question: {question}"""

print(ask_ollama(prompt))