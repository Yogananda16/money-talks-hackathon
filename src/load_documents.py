import os
from pathlib import Path

import docx
import openpyxl
from pypdf import PdfReader

DOCS_DIR = Path(__file__).parent.parent / "documents"

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
        ext = file.suffix.lower()
        try:
            if ext == ".docx":
                text = load_docx(file)
            elif ext == ".xlsx":
                text = load_xlsx(file)
            elif ext == ".pdf":
                text = load_pdf(file)
            elif ext in (".png", ".jpg", ".jpeg"):
                # Not text-extracted — treated as an attachable piece of evidence,
                # referenced by filename rather than by content.
                text = f"[Attachment: {file.name} — an image/diagram file. Its content was not read; it exists as supporting evidence and can be referenced by filename.]"
            else:
                continue  # images etc. — skipped for now
        except Exception as e:
            print(f"Could not read {file.name}: {e}")
            continue

        if text.strip():
            documents.append({"filename": file.name, "text": text})
        else:
            print(f"No extractable text in {file.name} (might be a scanned/image-only file)")

    return documents

if __name__ == "__main__":
    docs = load_all_documents()
    print(f"Loaded {len(docs)} documents:")
    for d in docs:
        print(f" - {d['filename']}: {len(d['text'])} characters")