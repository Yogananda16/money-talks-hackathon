# IRIS - Investigative Risk & Information System

**An AI Security Analyst that answers enterprise security questionnaires from a company's own documents — and asks a human when the documents don't know.**

Built for the **Regodit track: AI Security Analyst**.

**Live:** https://money-talks-hackathon.vercel.app/

<img width="1438" height="852" alt="image" src="https://github.com/user-attachments/assets/a2bcc392-7334-4d8c-bfb3-eb1de4b3ea36" />

## Problem

A startup selling into an enterprise gets a security questionnaire: *Is MFA enabled? Where is customer data stored? How often are backups performed? Who has access to production?*

The answers are scattered across policies, a SOC 2 report, access reviews and contracts — incomplete, ambiguous, and sometimes contradicting each other. The dangerous failure isn't a slow answer. It's a **confident wrong answer** shipped to a customer.

## Solution

IRIS reads every company document, answers what the evidence supports, and behaves like a real analyst about the rest:

- Documents answer it → **answers, with the source quote recorded**
- They don't → **asks, and remembers what you say**
- Answer is vague → **asks follow-ups until it's specific**
- Two documents disagree → **flags the conflict, never picks one silently**
- Still unknown → **marks it Unknown**

Every answer carries a status — `verified` (from a document, with the quote), `confirmed` (a human said it), or `unknown`. An answer with neither evidence nor confirmation can't be marked known. **66 questions → 61 verified, 5 confirmed, 1 conflict flagged.**

### The conflict it caught

The BC/DR policy says there are **no** second-region backups and **no** restore test. The SOC 2 report says backups are **automated with cross-region replication**. Both internal, both official. IRIS refuses to answer and asks which is true.

## Try it

Open the live link, or `index.html` locally — the data is embedded, so it runs with no server and no API key.

- `Is MFA enabled?` — answered from documents
- `Do you perform backups?` → `Yes` → `Daily` → `Yes` — the follow-up chain
- `Do we keep backups in a second region?` — the conflict
- `Do you check people before hiring?` — undocumented, so it asks you
- Ask something twice — it reads back what it knows
- `Give me a summary` — everything recorded so far

## How it works

```
documents/ ──▶ extract_questions.py ──▶ questions.json          66 questionnaire items
           └─▶ load_documents.py ─────▶ text of every .docx / .xlsx
                      ▼
              search_documents.py ────▶ profile.json            answer + evidence quote + source
                      ▼                 unanswerable → found:false, never guessed
               build_profile.py ──────▶ security_profile.json   verified / unknown
                      ▼
                  ask_loop.py           interviews a human on every unknown
                      ▼                 follow_up.py asks again when an answer is vague
              conflict_check.py         compares sources that disagree
                      ▼
             generate_report.py ──────▶ FINAL_REPORT.md         completed questionnaire
```

`index.html` is the chat layer over the same profile — searches first, asks when it can't answer, runs the follow-up chains, surfaces conflicts, and remembers within the session.

## Tech stack

Python 3.10+ · Google Gemini (`gemini-3.6-flash`) · python-docx / openpyxl · JSON profile store · vanilla HTML/CSS/JS (no build step) · PRISMtrace for LLM tracing

## Run the pipeline

```bash
pip install google-generativeai python-docx openpyxl python-dotenv requests
# src/.env  →  GEMINI_API_KEY=your_key
cd src && python main.py
```

Stages run in order: `extract_questions` → `search_documents` → `build_profile` → `ask_loop` (interactive) → `conflict_check` → `generate_report`. Output: **`FINAL_REPORT.md`**.

## Notes

`documents/` and `src/.env` are gitignored — the documents are provided data and the `.env` holds keys. Everything derived from them (`questions.json`, `security_profile.json`, `FINAL_REPORT.md`) is committed, so results are inspectable without re-running anything.
