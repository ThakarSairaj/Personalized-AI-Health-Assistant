import pdfplumber
import tempfile
import os

def extract_text_from_pdf(file_bytes: bytes) -> str:
    extracted_text = ""

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        with pdfplumber.open(tmp_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    extracted_text += f"\n--- Page {page_num} ---\n{text}"

    finally:
        os.remove(tmp_path)

    return extracted_text.strip()
