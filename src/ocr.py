import os
from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from dotenv import load_dotenv
load_dotenv()


# Tesseract & Poppler paths
POPPER_PATH = os.getenv("POPPLER_PATH", r"C:\Program Files\poppler-24.02.0\Library\bin")
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data" / "samples"

def get_output_path(pdf_path, suffix):
    return pdf_path.parent / f"{pdf_path.stem}_{suffix}.txt"

def extract_with_pymupdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    out_path = get_output_path(pdf_path, "pymupdf")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_with_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    out_path = get_output_path(pdf_path, "pdfplumber")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_with_pdfminer(pdf_path):
    text = extract_text(str(pdf_path))
    out_path = get_output_path(pdf_path, "pdfminer")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_with_tesseract(pdf_path):
    text = ""
    try:
        images = convert_from_path(str(pdf_path), poppler_path=POPPER_PATH)
        for i, img in enumerate(images):
            text += f"\n--- Page {i+1} ---\n"
            text += pytesseract.image_to_string(img)
    except Exception as e:
        text = f"OCR Error: {e}"
    out_path = get_output_path(pdf_path, "ocr")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_all(pdf_filename):
    pdf_path = SAMPLES_DIR / pdf_filename
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    print(f"🔍 Extracting text from: {pdf_filename}")
    extract_with_pymupdf(pdf_path)
    extract_with_pdfplumber(pdf_path)
    extract_with_pdfminer(pdf_path)
    extract_with_tesseract(pdf_path)
    print("✅ All extraction methods complete.")

if __name__ == "__main__":
    # Change to your actual filename
    extract_all("Acoufelt1.pdf")
