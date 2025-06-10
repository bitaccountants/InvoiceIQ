import os
import json
from pathlib import Path
from src.llm_processor import process_invoice_with_llm

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data" / "samples"
PROMPT_PATH = BASE_DIR / "models" / "prompt.txt"
OUTPUT_DIR = BASE_DIR / "output"

OCR_SUFFIXES = ["pymupdf", "pdfplumber", "pdfminer", "ocr"]

def find_best_ocr_file(base_filename):
    scores = {}
    for suffix in OCR_SUFFIXES:
        candidate = SAMPLES_DIR / f"{base_filename}_{suffix}.txt"
        if candidate.exists():
            with open(candidate, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                scores[suffix] = (candidate, len(content))
    if not scores:
        raise FileNotFoundError("❌ No OCR files found.")

    # Select the file with the most content
    best_file = max(scores.items(), key=lambda x: x[1][1])[1][0]
    print(f"📄 Using OCR file: {best_file.name}")
    return best_file

'''
def run_pipeline(base_pdf_name):
    try:
        best_ocr_file = find_best_ocr_file(base_pdf_name)
        with open(best_ocr_file, 'r', encoding='utf-8') as f:
            ocr_text = f.read()

        result = process_invoice_with_llm(ocr_text, PROMPT_PATH)

        # Save output
        output_path = OUTPUT_DIR / f"{base_pdf_name}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)

        print(f"✅ Output saved: {output_path}")
    except Exception as e:
        print(f"⚠️ Pipeline failed: {e}")
'''        
def run_pipeline(filename):
    try:
        print(f"📄 Using OCR file: {filename}_pdfminer.txt")
        input_path = f"data/samples/{filename}_pdfminer.txt"
        prompt_path = "models/prompt.txt"
        output_path = f"output/{filename}.json"

        # Load OCR text
        with open(input_path, 'r', encoding='utf-8') as f:
            ocr_text = f.read()
        print("✅ OCR loaded")

        from src.llm_processor import process_invoice_with_llm
        result = process_invoice_with_llm(ocr_text, prompt_path)
        print("✅ LLM processed invoice")

        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)
        print(f"✅ Output saved: {output_path}")

    except Exception as e:
        import traceback
        print("⚠️ Pipeline failed:")
        traceback.print_exc()

'''
if __name__ == "__main__":
    run_pipeline("Acoufelt1")  # don't include .pdf or .txt
'''
