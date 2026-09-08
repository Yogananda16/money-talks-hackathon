import json
import openpyxl

XLSX_PATH = "questions/Regodit_Comprehensive_Vendor_Security_Questionnaire_Clean.xlsx"
SHEET_NAME = "Vendor Security Responses"
OUTPUT_PATH = "questions.json"


def extract_questions():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    sheet = wb[SHEET_NAME]

    questions = []
    skipped = []
    current_topic = None
    blank_streak = 0

    for row in sheet.iter_rows(min_row=4, values_only=True):
        id_cell, question_text = row[0], row[1]

        if id_cell is None and question_text is None:
            blank_streak += 1
            if blank_streak >= 5:
                break
            continue
        blank_streak = 0

        if isinstance(id_cell, str) and id_cell.strip().lower() == "topic":
            if question_text:
                current_topic = str(question_text).strip()
            continue

        if not isinstance(id_cell, (int, float)):
            continue

        text = str(question_text).strip() if question_text is not None else ""

        # defensive check: catches row 52's exact bug — question text that's just a number
        if not text or text.replace(".", "", 1).isdigit():
            skipped.append({"id": id_cell, "topic": current_topic, "raw_value": question_text})
            continue

        questions.append({"id": int(id_cell), "topic": current_topic, "question": text})

    with open(OUTPUT_PATH, "w") as f:
        json.dump(questions, f, indent=2)

    print(f"Extracted {len(questions)} questions -> {OUTPUT_PATH}")
    if skipped:
        print(f"\n⚠️  Skipped {len(skipped)} row(s) with bad data — these need manual follow-up with the customer:")
        for s in skipped:
            print(f"  ID {s['id']} ({s['topic']}): raw value was {s['raw_value']!r}")

    return questions


if __name__ == "__main__":
    extract_questions()