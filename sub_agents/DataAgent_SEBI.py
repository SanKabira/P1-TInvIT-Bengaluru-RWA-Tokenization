#!/usr/bin/env python3
"""
DataAgent_SEBI.py — Sub-agent to download SEBI Master Circular for InvITs
and extract key regulatory provisions for P1 analysis.

Data Integrity: All data from official SEBI sources. No fabrication.
"""

import requests
import pdfplumber
import pandas as pd
from datetime import datetime
import os

SEBI_URLS = {
    "master_circular_2025": "https://www.sebi.gov.in/sebi_data/meetingfiles/sep-202517581979290031.pdf",
    "invit_3rd_amendment_2025": "https://www.sebi.gov.in/legal/regulations/sep-2025/securities-and-exchange-board-of-india-infrastructure-investment-trusts-third-amendment-regulations-2025_87082.html",
    "ifsca_consultation": "https://ifsca.gov.in/Document/ReportandPublication/ifsca-consultation-paper-on-regulatory-approach-towards-tokenization-of-real-world-assets03032025111644.pdf"
}
OUTPUT_DIR = "data/raw/SEBI_regulations"
COLLECTION_DATE = datetime.now().strftime("%Y-%m-%d")

def download_file(url: str, name: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fname = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    print(f"[DataAgent_SEBI] Downloading {name}...")
    try:
        r = requests.get(url, timeout=60, stream=True, headers={'User-Agent': 'ResearchBot/1.0'})
        r.raise_for_status()
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[DataAgent_SEBI] ✅ Saved: {fname}")
        return fname
    except Exception as e:
        print(f"[DataAgent_SEBI] ❌ ERROR downloading {name}: {e}")
        return ""

def code_provisions(pdf_path: str) -> pd.DataFrame:
    """
    Code regulatory provisions as Aligned (1) / Neutral (0.5) / Conflicted (0)
    with blockchain/tokenization requirements.
    """
    ALIGNMENT_KEYWORDS = ["digital", "electronic", "demat", "online", "automated", "smart"]
    CONFLICT_KEYWORDS = ["physical", "manual", "paper", "original certificate", "ink signature"]
    
    provisions = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            sentences = text.split('.')
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 50:  # Skip very short fragments
                    alignment = 0.5  # Default: Neutral
                    if any(k in sent.lower() for k in ALIGNMENT_KEYWORDS):
                        alignment = 1  # Aligned
                    elif any(k in sent.lower() for k in CONFLICT_KEYWORDS):
                        alignment = 0  # Conflicted
                    provisions.append({
                        "page": i + 1,
                        "provision_text": sent[:300],
                        "alignment_code": alignment,
                        "alignment_label": {1: "Aligned", 0.5: "Neutral", 0: "Conflicted"}[alignment],
                        "source": os.path.basename(pdf_path),
                        "collection_date": COLLECTION_DATE
                    })
    return pd.DataFrame(provisions)

def main():
    for name, url in SEBI_URLS.items():
        if url.endswith('.pdf'):
            pdf_path = download_file(url, name)
            if pdf_path:
                df = code_provisions(pdf_path)
                out_path = os.path.join(OUTPUT_DIR, f"{name}_coded.csv")
                df.to_csv(out_path, index=False)
                print(f"[DataAgent_SEBI] Coded {len(df)} provisions → {out_path}")

if __name__ == "__main__":
    main()
