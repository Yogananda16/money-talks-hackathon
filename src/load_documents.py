import os
from pathlib import Path

import docx
import openpyxl
from pypdf import PdfReader

DOCS_DIR = Path(__file__).parent.parent / "documents"
QUESTIONNAIRE_FILENAME = "Regodit_Comprehensive_Vendor_Security_Questionnaire_Clean.xlsx"


def load_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def load_xlsx(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    lines = []
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for row in ws.iter_rows(values_only=True):
            values = [str(v) for v in row if v is not None]
            if values:
                lines.append(" | ".join(values))
    return "\n".join(lines)


def load_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_all_documents():
    documents = []
    for file in DOCS_DIR.iterdir():
        if file.is_dir():
            continue
        if file.name == QUESTIONNAIRE_FILENAME:
            continue  # this is the form being filled out, not evidence

        ext = file.suffix.lower()
        text = ""
        readable = True

        try:
            if ext == ".docx":
                text = load_docx(file)
            elif ext == ".xlsx":
                text = load_xlsx(file)
            elif ext == ".pdf":
                text = load_pdf(file)
            elif ext in (".png", ".jpg", ".jpeg"):
                text = ""  # images: no text extraction, handled below
            else:
                continue  # unsupported file type, skip entirely
        except Exception as e:
            print(f"Could not read {file.name}: {e}")
            readable = False

        if not readable or not text.strip():
            text = (
                f"[Attachment: {file.name} — exists as supporting evidence, "
                f"but its content was not text-extracted (scanned, image-based, "
                f"a diagram, or unreadable). Reference by filename.]"
            )
            print(f"No extractable text in {file.name} — added as filename-only evidence")

        documents.append({"filename": file.name, "text": text})

    return documents


if __name__ == "__main__":
    docs = load_all_documents()
    print(f"\nLoaded {len(docs)} documents:")
    for d in docs:
        print(f" - {d['filename']}: {len(d['text'])} characters")