#!/usr/bin/env python3
"""
DataAgent_ADB.py — Sub-agent to download and extract ADB Financial Analysis
for Namma Metro Phase 2A/2B.

Paper: P1 - T-InvIT Bengaluru RWA Tokenization
Author: Sandeep S | PhD Scholar, University of Mysore
Data Integrity: All data extracted from official ADB source. No fabrication.
"""

import requests
import pdfplumber
import pandas as pd
from datetime import datetime
import os

ADB_URL = "https://www.adb.org/sites/default/files/linked-documents/ind-53326-001-fa.pdf"
OUTPUT_DIR = "data/raw/BMRCL"
OUTPUT_FILE = "adb_financial_analysis_extracted.csv"
COLLECTION_DATE = datetime.now().strftime("%Y-%m-%d")

KEY_METRICS = [
    "FIRR", "WACC", "DSCR", "ridership", "subsidy", 
    "NPV", "revenue", "cost", "tariff", "debt"
]

def download_pdf(url: str, save_path: str) -> bool:
    """Download PDF from ADB. Returns True if successful."""
    print(f"[DataAgent_ADB] Downloading: {url}")
    try:
        r = requests.get(url, timeout=60, stream=True)
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[DataAgent_ADB] Downloaded to {save_path}")
        return True
    except Exception as e:
        print(f"[DataAgent_ADB] ERROR: {e}")
        print("DATA GAP: ADB PDF could not be downloaded. Manual download required.")
        return False

def extract_tables(pdf_path: str) -> list:
    """Extract all tables from ADB PDF."""
    records = []
    print(f"[DataAgent_ADB] Extracting tables from {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if any(keyword.lower() in str(row).lower() for keyword in KEY_METRICS):
                        records.append({
                            "page": i + 1,
                            "row_data": " | ".join([str(cell) for cell in row if cell]),
                            "source": "ADB Financial Analysis, ind-53326-001-fa.pdf",
                            "url": ADB_URL,
                            "collection_date": COLLECTION_DATE
                        })
    return records

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "adb_fa_ind53326.pdf")
    
    if not os.path.exists(pdf_path):
        success = download_pdf(ADB_URL, pdf_path)
        if not success:
            return
    
    records = extract_tables(pdf_path)
    
    if records:
        df = pd.DataFrame(records)
        out_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        df.to_csv(out_path, index=False)
        print(f"[DataAgent_ADB] ✅ Extracted {len(records)} rows → {out_path}")
    else:
        print("[DataAgent_ADB] ⚠️ No metric rows found. Review PDF manually.")

if __name__ == "__main__":
    main()
