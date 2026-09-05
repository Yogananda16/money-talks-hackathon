# IRIS — Investigative Risk & Information System

**An AI Security Analyst that answers enterprise security questionnaires from a company's own documents — and asks a human when the documents don't know.**

Built for the **Regodit track: AI Security Analyst**.

---

## Problem

A startup selling into an enterprise gets hit with a security questionnaire:

> Is MFA enabled? Where is customer data stored? Do you encrypt data at rest? How often are backups performed? Do you conduct vulnerability scans? Who has access to production? Do you have an employee offboarding process?

The answers exist — but they're scattered across policy documents, a SOC 2 report, access review spreadsheets, contracts, asset inventories and, for everything else, someone's head. Filling one of these in by hand takes days, and the documents themselves are **incomplete, ambiguous, and sometimes contradict each other**.

The dangerous failure mode isn't a slow answer. It's a **confident wrong answer** — writing "Yes, MFA is enforced" into a customer-facing document when an internal record says otherwise.

## Solution

IRIS reads every company document once, answers as much of the questionnaire as the evidence actually supports, and then behaves like a real analyst about the rest:

- If the documents answer it → **answer, with the source quote attached.**
- If they don't → **ask the employee, and record what they say.**
- If the answer is vague → **ask a follow-up until it's specific.**
- If two documents disagree → **flag the conflict and ask which is true.** Never pick one silently.
- If it still isn't known → **mark it Unknown.**

**The golden rule is enforced structurally, not by prompt politeness:** every answer in the profile carries a `status` of `verified` / `confirmed` / `unknown` plus the exact `evidence` quote and `source` filename it came from. An answer with no evidence and no human confirmation cannot be marked as known.

On the current document set: **66 questions → 61 verified from documents, 5 confirmed by the employee, 1 conflict flagged.**

## Key features

| Requirement | How IRIS does it |
|---|---|
| **Search before asking** | All documents are parsed and searched first; the employee is only asked about questions the documents genuinely don't cover. |
| **Ask when information is missing** | Unknowns go into an interview loop instead of being guessed at. Responses are written back to the profile. |
| **Smart follow-ups** | A vague answer triggers a follow-up chain — *Do you perform backups?* → *Yes* → *How frequently?* → *Daily* → *Are they automated?* → *Yes* → recorded as "backups are automated and performed daily." |
| **Conflict detection** | Contradicting sources are surfaced side by side and escalated to the human rather than resolved automatically. |
| **Persistent memory** | The security profile is a durable JSON store: IRIS remembers what it learned, won't ask the same question twice (it reads the stored answer back and asks "still accurate?"), and any answer can be corrected or updated later. |
| **Completed questionnaire** | Generates a full report grouped by topic, with every item labelled ✅ Verified / 💬 Confirmed / ❓ Unknown, plus a conflicts section. |

### The conflict IRIS caught

The BC/DR policy says the company **does not** keep backups in a second geographic region and **has never run a restore test**. The SOC 2 report says backups are **automated with cross-region replication**. Both are internal, both are "official". IRIS refuses to answer this question and asks which one reflects reality — exactly the answer you don't want a bot inventing for a customer.

It caught a second one in access control: policy requires contractors to hold least-privilege access, while the access review records show a contractor with Admin access the reviewer themselves marked *"not justified"*.

## Tech stack

- **Python 3.10+** — document pipeline
- **Google Gemini** (`gemini-3.6-flash`) — document search, follow-up judgement, conflict detection
- **python-docx / openpyxl** — parsing `.docx` policies and `.xlsx` questionnaires, access reviews and asset inventories
- **JSON** — the security profile (`security_profile.json`) as the persistent memory layer
- **HTML / CSS / vanilla JS** — the chat interface, single self-contained file, no build step
- **PRISMtrace** — LLM call tracing/observability (non-blocking)

## How it works

```
documents/  ──▶ extract_questions.py ──▶ questions.json        (66 questionnaire items + topics)
   │
   └──────────▶ load_documents.py ─────▶ full text of every .docx / .xlsx
                        │
                        ▼
                search_documents.py ───▶ profile.json          (answer + exact evidence quote + source file)
                        │                 "never guess" — unanswerable questions come back found:false
                        ▼
                 build_profile.py ─────▶ security_profile.json (verified / unknown, evidence, source)
                        │
                        ▼
                    ask_loop.py          interviews the employee on every unknown
                        │                follow_up.py decides if an answer is too vague and asks for detail
                        ▼                → status becomes "confirmed"
                 conflict_check.py       compares sources that disagree, recommends an action
                        │
                        ▼
                generate_report.py ───▶ FINAL_REPORT.md        (completed questionnaire, by topic, with statuses)
```

`iris-v2.html` is the conversational front end over the same profile. It searches the profile first, falls back to asking, runs the follow-up chains, surfaces the known conflicts, remembers answers within the session, and can read back everything it has learned.

### Status model

Every question in `security_profile.json` looks like this:

```json
{
  "question_id": 1,
  "answer": "Yes, Solsphere / Regodit has established a formal Information Security Program...",
  "status": "verified",
  "evidence": "This Information Security Policy defines how the company protects...",
  "source": "Regodit_information_security_policy_v1.0.docx",
  "confidence": "high"
}
```

- `verified` — found in a company document, with the quote that proves it
- `confirmed` — not in any document; the employee stated it in the interview
- `unknown` — nobody has confirmed it; it ships as Unknown, not as a guess

## How to run

### 1. Chat interface (no setup)

Open **`iris-v2.html`** in any browser — double-click it. The questionnaire and security profile are embedded in the file, so it works offline with no server and no API key.

Try:

- `Is MFA enabled?` — answered from documents
- `Where is customer data stored?` — answered from documents
- `Do you perform backups?` → `Yes` → `Daily` → `Yes` — the follow-up chain
- `Do we keep backups in a second region?` — the conflict
- `Do you conduct employee background checks?` — not documented, so IRIS asks
- Ask something twice — it reads back what it already knows
- `Give me a summary` — everything recorded so far

### 2. Full pipeline

```bash
pip install google-generativeai python-docx openpyxl python-dotenv requests

# src/.env
GEMINI_API_KEY=your_key
PRISMTRACE_API_KEY=your_key          # optional
PRISMTRACE_PROJECT_ID=your_project   # optional
PRISMTRACE_HOST=https://...          # optional

cd src
python main.py
```

`main.py` runs the stages in order: `extract_questions` → `search_documents` → `build_profile` → `ask_loop` → `conflict_check` → `generate_report`.

`ask_loop.py` is interactive — it prints each unanswered question and waits for you to type the answer, asking follow-ups when your answer is too vague. Everything else runs unattended.

Output: **`FINAL_REPORT.md`** — the completed questionnaire, grouped by topic, with a conflicts section at the end.

Individual stages can be run on their own (`python build_profile.py`), and `apply_corrections.py` shows the memory-correction path: overwriting stored answers and resetting over-confident ones back to `unknown`.

## Repo structure

```
├── iris-v2.html            # chat interface (self-contained, open directly)
├── questions.json          # 66 extracted questionnaire items
├── profile.json            # raw document-search output
├── security_profile.json   # the security profile / persistent memory
├── FINAL_REPORT.md         # generated completed questionnaire
├── documents/              # company documents (not committed — see below)
└── src/
    ├── main.py                 # runs the whole pipeline
    ├── extract_questions.py    # questionnaire .xlsx → questions.json
    ├── load_documents.py       # .docx / .xlsx text extraction
    ├── search_documents.py     # document search, evidence + source per answer
    ├── build_profile.py        # verified / unknown status model
    ├── ask_loop.py             # employee interview over the unknowns
    ├── follow_up.py            # is this answer too vague?
    ├── conflict_check.py       # do these sources contradict each other?
    ├── apply_corrections.py    # update / reset stored answers
    └── generate_report.py      # FINAL_REPORT.md
```

## Notes for judges

- **`documents/` and `src/.env` are gitignored.** The company documents are provided data, not ours to publish, and the `.env` holds API keys. Drop the provided documents into `documents/` before running the pipeline. Everything derived from them — `questions.json`, `security_profile.json`, `FINAL_REPORT.md` — is committed, so the results are inspectable without re-running anything.
- **Nothing in the profile is unsourced.** Every `verified` answer carries the quote and filename it came from; spot-check any of them against `FINAL_REPORT.md`.
- **The two conflicts were not hardcoded findings** — they came out of comparing what the documents actually say. They're surfaced in the chat and in the report because a human, not a model, should decide which source is true.
- **Known limits:** the chat interface matches questions with keyword + synonym scoring rather than embeddings, so unusual phrasings can miss; the interview memory lives in the browser session, while the pipeline's memory persists in `security_profile.json`. Wiring the chat directly to the live profile (and to embeddings-based retrieval) is the next step.
