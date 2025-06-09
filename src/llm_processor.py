import os
import re
import json
import ollama
from dotenv import load_dotenv

load_dotenv()

def load_prompt_template(prompt_path):
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def stringify_expressions(json_str):
    pattern = r'(?<=:\s)(\d+\.\d+\s*[\+\-\*/]\s*\d+\.\d+)(?=\s*[,\\n\\r\\}])'
    return re.sub(pattern, r'"\1"', json_str)

def evaluate_string_expressions(data):
    if isinstance(data, dict):
        return {k: evaluate_string_expressions(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [evaluate_string_expressions(item) for item in data]
    elif isinstance(data, str) and re.match(r'^\d+\.?\d*\s*[\+\-\*/]\s*\d+\.?\d*$', data):
        try:
            return round(eval(data), 2)
        except:
            return data
    return data

def extract_json_between_markers(text):
    match = re.search(r"### START ###(.*?)### END ###", text, re.DOTALL)
    return match.group(1).strip() if match else None

def call_llm(prompt_text):
    response = ollama.chat(
        model='llama3',
        messages=[
            {"role": "system", "content": "You are an invoice parser."},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response['message']['content']

def process_invoice_with_llm(ocr_text, prompt_path):
    base_prompt = load_prompt_template(prompt_path)
    full_prompt = f"{base_prompt}\n\n{ocr_text}"

    raw_response = call_llm(full_prompt)
    json_chunk = extract_json_between_markers(raw_response)

    if not json_chunk:
        raise ValueError("No JSON found between markers.")

    json_chunk = stringify_expressions(json_chunk)
    json_data = json.loads(json_chunk)
    return evaluate_string_expressions(json_data)
