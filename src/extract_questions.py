import openpyxl
import json

wb = openpyxl.load_workbook("../documents/Regodit_Comprehensive_Vendor_Security_Questionnaire_Clean.xlsx", data_only=True)
sheet = wb["Vendor Security Responses"]

questions = []
current_topic = None
header_found = False

for row in sheet.iter_rows(values_only=True):
    if not header_found:
        if row[0] == "Security Question ID#":
            header_found = True
        continue

    first_col = row[0]
    second_col = row[1]

    if first_col == "Topic":
        current_topic = second_col
        continue

    if isinstance(first_col, (int, float)) and second_col:
        questions.append({
            "id": int(first_col),
            "question": second_col,
            "topic": current_topic
        })

with open("../questions.json", "w") as f:
    json.dump(questions, f, indent=2)

print(f"Extracted {len(questions)} questions")