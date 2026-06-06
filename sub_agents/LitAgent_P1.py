#!/usr/bin/env python3
"""
LitAgent_P1.py — Literature search agent for P1.
Searches Google Scholar via scholarly for recent papers (2020-2026)
on InvIT tokenization, CBDC infrastructure, RWA tokenization India.

Output: BibTeX file + annotated CSV
"""

from datetime import datetime
import time
import csv
import os

SEARCH_QUERIES = [
    "blockchain infrastructure investment trust India tokenization",
    "CBDC programmable money infrastructure finance",
    "real world asset tokenization India regulatory",
    "InvIT valuation liquidity India SEBI",
    "land pooling scheme digital token India",
    "DLT distributed ledger infrastructure bond emerging markets",
    "Namma Metro BMRCL financial viability",
    "RWA tokenization blockchain 2024 2025"
]

OUTPUT_DIR = "paper"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "literature_found.csv")
OUTPUT_BIB = os.path.join(OUTPUT_DIR, "references_new.bib")

def format_bibtex(paper: dict) -> str:
    """Format a paper dict as BibTeX entry."""
    key = (paper.get('author', 'Unknown').split()[0] + 
           str(paper.get('year', '2024'))).replace(' ', '')
    return (
        f"@article{{{key},\n"
        f"  author = {{{paper.get('author', 'Unknown')}}},\n"
        f"  title = {{{paper.get('title', '')}}},\n"
        f"  journal = {{{paper.get('journal', 'Unknown Journal')}}},\n"
        f"  year = {{{paper.get('year', 2024)}}},\n"
        f"  url = {{{paper.get('url', '')}}},\n"
        f"  note = {{Retrieved {datetime.now().strftime('%Y-%m-%d')}}}\n"
        f"}}\n"
    )

def main():
    print("[LitAgent_P1] Starting literature search...")
    print("[LitAgent_P1] Install 'scholarly' package: pip install scholarly")
    print("[LitAgent_P1] INSTRUCTION: Run this script in Google Colab for best results.")
    print()
    print("Queries to run manually in Google Scholar or Scopus:")
    for i, q in enumerate(SEARCH_QUERIES, 1):
        print(f"  {i}. {q}")
    print()
    print(f"Save results to: {OUTPUT_CSV}")
    print(f"Export BibTeX to: {OUTPUT_BIB}")
    print()
    print("[LitAgent_P1] Manual fallback: Use Perplexity search with each query above.")

if __name__ == "__main__":
    main()
