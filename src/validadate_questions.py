import json
import pandas as pd

with open("questions.json") as f:
    questions = json.load(f)

df = pd.DataFrame(questions)
print(f"Total rows: {len(df)}\n")

# duplicate IDs
dupes = df[df.duplicated(subset="id", keep=False)]
if not dupes.empty:
    print("⚠️ Duplicate IDs:")
    print(dupes[["id", "question"]], "\n")

# missing/empty questions
missing = df[df["question"].isna() | (df["question"].str.strip() == "")]
if not missing.empty:
    print("⚠️ Missing questions:")
    print(missing[["id", "topic"]], "\n")

# question text that's just a number — the row 52 bug specifically
numeric_only = df[df["question"].str.replace(".", "", regex=False).str.strip().str.isdigit()]
if not numeric_only.empty:
    print("⚠️ Question text is just a number (likely corrupted row):")
    print(numeric_only[["id", "topic", "question"]], "\n")

# suspiciously short — possible truncation
short = df[df["question"].str.len() < 15]
if not short.empty:
    print("⚠️ Suspiciously short questions — check these manually:")
    print(short[["id", "topic", "question"]], "\n")

if dupes.empty and missing.empty and numeric_only.empty and short.empty:
    print("No issues found.")