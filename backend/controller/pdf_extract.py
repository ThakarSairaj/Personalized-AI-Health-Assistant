from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_extractor import extract_text_from_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_bytes = await file.read()

    extracted_text = extract_text_from_pdf(file_bytes)

    # Print to terminal
    print("\n======= EXTRACTED PDF TEXT =======\n")
    print(extracted_text)
    print("\n=================================\n")

    if not extracted_text:
        return {
            "message": "No text found (possibly scanned PDF)",
            "text": ""
        }

    return {
        "message": "Text extracted successfully",
        "text": extracted_text
    }
