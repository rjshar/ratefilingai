import os
import fitz  # PyMuPDF
import json
import re
from datetime import datetime
from collections import defaultdict

FILINGS_DIR = "filings"
OUTPUT_PATH = "data/parsed_filings.json"

def extract_text(filepath):
    doc = fitz.open(filepath)
    return "\n".join([page.get_text() for page in doc])

def clean_number(val):
    return float(val.replace(",", "").replace("$", "").strip())

def parse_entity_block(text_block):
    entities = []
    entity_pattern = re.compile(
        r"(?P<name>[A-Z][A-Za-z\s&]+?)\s+"
        r"(?P<indicated>[-+]?\d+\.\d+)%\s+"
        r"(?P<impact>[-+]?\d+\.\d+)%\s+\$?(?P<change>[-\d,]+)\s+"
        r"(?P<policyholders>\d+)\s+\$?(?P<written>[\d,]+)\s+"
        r"(?P<max>[-+]?\d+\.\d+)%\s+(?P<min>[-+]?\d+\.\d+)%",
        re.IGNORECASE
    )
    for match in entity_pattern.finditer(text_block):
        try:
            entities.append({
                "Entity": match.group("name").strip(),
                "Indicated Change (%)": float(match.group("indicated")),
                "Rate Impact (%)": float(match.group("impact")),
                "Written Premium Change": clean_number(match.group("change")),
                "Policyholders Affected": int(match.group("policyholders")),
                "Total Written Premium": clean_number(match.group("written")),
                "Max Change (%)": float(match.group("max")),
                "Min Change (%)": float(match.group("min")),
            })
        except Exception:
            continue
    return entities

def parse_effective_date(text):
    match = re.search(r"Effective Date\s*\(New\):\s*(\d{2}/\d{2}/\d{4})", text)
    if match:
        return datetime.strptime(match.group(1), "%m/%d/%Y").date().isoformat()
    return None

def process_filing(filepath):
    text = extract_text(filepath)
    base = os.path.basename(filepath)
    serff = base.replace(".pdf", "")
    group_match = re.search(r"Group Name:\s*(.*?)\n", text)
    method_match = re.search(r"Filing Method:\s*(.*?)\n", text, re.IGNORECASE)
    type_match = re.search(r"Filing Type:\s*(.*?)\n", text, re.IGNORECASE)
    rating_basis = "LCM" if re.search(r"loss cost multiplier|LCM", text, re.IGNORECASE) else "Rates"
    eff_date = parse_effective_date(text)
    entity_block_match = re.search(r"Company\s+Name:(.*?)SERFF Tracking #", text, re.DOTALL)
    entity_block = entity_block_match.group(1) if entity_block_match else ""

    return {
        "SERFF Tracking Number": serff,
        "File": base,
        "Group": group_match.group(1).strip() if group_match else "Unknown",
        "Filing Method": method_match.group(1).strip() if method_match else "Unknown",
        "Filing Type": type_match.group(1).strip() if type_match else "Unknown",
        "Rates or LCMs": rating_basis,
        "Effective Date": eff_date,
        "Entities": parse_entity_block(entity_block)
    }

def main():
    filings_by_group = defaultdict(list)

    for filename in os.listdir(FILINGS_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(FILINGS_DIR, filename)
            try:
                filing = process_filing(filepath)
                filings_by_group[filing["Group"]].append(filing)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    # Sort filings by date within each group
    final = {}
    for group, filings in filings_by_group.items():
        sorted_filings = sorted(
            filings, key=lambda f: f.get("Effective Date") or "0000-00-00", reverse=True
        )
        final[group] = {
            "latest_filing": sorted_filings[0],
            "filing_history": sorted_filings[1:]
        }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(final, f, indent=2)

    print(f"✅ Parsed filings into {OUTPUT_PATH} (grouped by latest + history)")

if __name__ == "__main__":
    main()
