import gradio as gr
from pathlib import Path
from src.ocr import extract_all
from src.pipeline import run_pipeline
from src.utils import json_to_csv

OUTPUT_DIR = Path("output")
SAMPLES_DIR = Path("data/samples")

def process_invoice(pdf_file):
    try:
        file_path = Path(pdf_file)
        extract_all(file_path.name)
        run_pipeline(file_path.stem)

        json_file = OUTPUT_DIR / f"{file_path.stem}.json"
        if not json_file.exists():
            return f"❌ Failed to generate output: {json_file.name} not found.", None

        csv_file = json_file.with_suffix(".csv")
        json_to_csv(json_file)

        with open(json_file, 'r', encoding='utf-8') as f:
            json_output = f.read()

        return json_output, str(csv_file)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {e}", None

# Create the interface
app = gr.Interface(
    fn=process_invoice,
    inputs=gr.File(label="Upload Invoice PDF"),
    outputs=[
        gr.Textbox(label="Extracted Invoice JSON", lines=20),
        gr.File(label="Download CSV Output")
    ],
    title="InvoiceIQ - AI Invoice Parser",
    description="Upload an invoice PDF. We'll extract it using OCR + LLM and give you structured output."
)

if __name__ == "__main__":
    app.launch()
