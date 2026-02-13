'''
backend\services\pdf_text_extractor.py
This file is use to extract the text from the document or report provided as input

'''
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import tempfile
import os
import re



# Add this line - point it to the tesseract.exe you just installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file_bytes: bytes) -> str:
    extracted_text = ""

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


def extract_text_from_ocr(file_bytes: bytes) -> str:
    extracted_text = ""
    images = convert_from_bytes(file_bytes)

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        extracted_text += f"\n--- Page {i+1} ---\n{text}"

    return extracted_text.strip()


def is_text_valid(text: str) -> bool:
    if not text:
        return False

    clean_text = text.strip()

    if len(clean_text) < 100:
        return False

    alphabets = re.findall(r'[A-Za-z]', clean_text)
    ratio = len(alphabets) / len(clean_text)

    return ratio > 0.2


def extract_text_hybrid(file_bytes: bytes) -> str:
    text = extract_text_from_pdf(file_bytes)

    if is_text_valid(text):
        return text

    ocr_text = extract_text_from_ocr(file_bytes)

    if is_text_valid(ocr_text):
        return ocr_text

    return ""


