# 🧾 InvoiceIQ — OCR + LLM Invoice Parser

Turn any invoice PDF into clean, structured data using OCR and LLMs — all **offline and free** with [Ollama](https://ollama.com).

[InvoiceIQ Demo]

!http://googleusercontent.com/image_generation_content/0

---

## 🔍 What It Does

**InvoiceIQ** is a mini-project that replicates a real-world pipeline:
- 📄 Extracts raw text from invoice PDFs using 4 OCR engines
- 🧠 Feeds it to an LLM (LLaMA3 via Ollama)
- 📊 Outputs structured JSON + CSV with fields like:
  - Invoice Number
  - Vendor
  - Date
  - Line Items
  - Totals

---

## ⚙️ Tech Stack

| Layer        | Tool                        |
|--------------|-----------------------------|
| OCR          | Tesseract, pdfminer, pdfplumber, PyMuPDF |
| LLM          | LLaMA 3 via [Ollama](https://ollama.com) |
| Language     | Python                      |
| Extras       | dotenv, pandas, open-source only |

---

## 🚀 How to Run Locally

### 🔧 1. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate       # or source venv/bin/activate
pip install -r requirements.txt


📄 2. Setup .env file in root
env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
POPPLER_PATH=C:\Program Files\poppler\bin

🧠 3. Run OCR on your PDF
Drop your invoice in data/samples/ as invoice_sample.pdf and run:

python src/ocr.py

🤖 4. Run the LLM pipeline
python src/pipeline.py

📊 5. Convert JSON to CSV
python src/convert.py

🧠 Prompt Template
Used with LLM:

markdown
Copy
Edit
You are an invoice parser. Your task is to extract structured data from raw invoice text. The required fields are:
- Invoice Number
- Invoice Date
- Vendor Name
- Line Items (Description, Quantity, Unit Price, Total)
- Subtotal
- Tax
- Total Amount
Return the result in JSON format enclosed between:
### START ###
{...}
### END ###


📁 Project Structure
InvoiceIQ/
├── data/           # Raw PDF + extracted OCR text
├── output/         # JSON + CSV output
├── models/         # Prompt templates
├── src/            # Code (OCR, LLM, pipeline, utils)
├── .env            # API keys & paths
├── README.md
└── requirements.txt


✨ Example Output
{
  "Invoice Number": "INV-2023-001",
  "Invoice Date": "2023-10-01",
  "Vendor Name": "Acme Supplies",
  "Line Items": [
    {"Description": "Printer Paper", "Quantity": 5, "Unit Price": 3.50, "Total": 17.50}
  ],
  "Subtotal": 17.50,
  "Tax": 1.75,
  "Total Amount": 19.25
}
👨‍💻 Author
Built with ❤️ by Amit Jadhav
🔗 GitHub: @amitjadhav055
🐦 Twitter: @Amitjadhav_01

📜 License
This project is licensed under the MIT License.
