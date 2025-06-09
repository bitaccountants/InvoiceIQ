import json
import csv
from pathlib import Path

def json_to_csv(json_file_path):
    output_path = Path(json_file_path)
    csv_file_path = output_path.with_suffix(".csv")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle line items separately if present
    line_items = data.pop("Line Items", [])

    # Save the top-level invoice info
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.keys())
        writer.writerow(data.values())

        if line_items:
            csvfile.write("\nLine Items:\n")
            keys = line_items[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(line_items)

    print(f"✅ CSV saved to: {csv_file_path}")
