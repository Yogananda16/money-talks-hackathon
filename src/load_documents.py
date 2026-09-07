import os
from docx import Document
import openpyxl
from pypdf import PdfReader
from PIL import Image
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

DOCS_DIR = "documents"  # <- confirm this matches your actual folder
VL_MODEL_NAME = "Qwen/Qwen3-VL-8B-Instruct"

_vl_model = None
_vl_processor = None


def get_vl_model():
    """Lazy-load the vision model — only loads into memory if an image actually needs it."""
    global _vl_model, _vl_processor
    if _vl_model is None:
        print("Loading Qwen3-VL for diagram analysis (first image only)...")
        _vl_processor = AutoProcessor.from_pretrained(VL_MODEL_NAME)
        _vl_model = AutoModelForImageTextToText.from_pretrained(
            VL_MODEL_NAME, torch_dtype=torch.bfloat16, device_map="auto"
        )
    return _vl_model, _vl_processor


def describe_diagram(filepath):
    model, processor = get_vl_model()
    image = Image.open(filepath)

    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": (
                "This is a diagram from a company's security documentation. "
                "Describe every security control, access path, data flow, and "
                "component shown, in enough detail to answer a vendor security "
                "questionnaire. Be literal about what's in the image — don't "
                "infer controls that aren't visibly shown."
            )}
        ]
    }]

    inputs = processor.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)

    output = model.generate(inputs, max_new_tokens=500)
    return processor.decode(output[0], skip_special_tokens=True)


def load_docx(filepath):
    doc = Document(filepath)
    parts = []

    for para in doc.paragraphs:
        if para.text.strip():
            parts.append(para.text.strip())

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if any(cells):
                parts.append(" | ".join(cells))

    return "\n\n".join(parts)


def load_xlsx(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    parts = []

    for sheet in wb.worksheets:
        parts.append(f"Sheet: {sheet.title}")
        for row in sheet.iter_rows(values_only=True):
            cells = [str(c).strip() for c in row if c is not None]
            if cells:
                parts.append(" | ".join(cells))

    return "\n\n".join(parts)


def load_pdf(filepath):
    reader = PdfReader(filepath)
    parts = []

    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            parts.append(text.strip())

    return "\n\n".join(parts)


def load_documents():
    documents = []

    for filename in os.listdir(DOCS_DIR):
        filepath = os.path.join(DOCS_DIR, filename)
        ext = filename.lower().split(".")[-1]
        text = ""

        try:
            if ext == "docx":
                text = load_docx(filepath)
            elif ext == "xlsx":
                text = load_xlsx(filepath)
            elif ext == "pdf":
                text = load_pdf(filepath)
            elif ext in ("png", "jpg", "jpeg"):
                text = describe_diagram(filepath)
            else:
                continue  # skip unrecognized file types
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        if not text.strip():
            print(f"No extractable content in {filename} — added as filename-only evidence")
            text = f"[Document: {filename} — content not extractable. File exists as evidence but requires manual review.]"

        documents.append({"filename": filename, "text": text})

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")
    for d in docs[:3]:
        print(f"\n{d['filename']}:")
        print(d["text"][:300])