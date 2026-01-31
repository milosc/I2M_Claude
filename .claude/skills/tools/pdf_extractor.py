#!/usr/bin/env python3
"""
PDF Text Extractor - MANUAL USE ONLY

This tool is for users to manually extract text from large PDFs
that Claude cannot read directly.

Usage:
    python pdf_extractor.py <input.pdf> [output.txt]

Requirements:
    pip install PyPDF2

Example:
    python pdf_extractor.py manual.pdf manual_text.txt
    
Then add manual_text.txt to your materials folder for analysis.
"""

import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("""
PDF Text Extractor
==================

Usage: python pdf_extractor.py <input.pdf> [output.txt]

This extracts all text from a PDF into a text file.
Use this for PDFs that Claude cannot read directly.

Steps:
1. Run: python pdf_extractor.py your_large_file.pdf
2. Add the resulting .txt file to your materials folder
3. Re-run the discovery analysis
""")
        sys.exit(0)
    
    # Check for PyPDF2
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("Installing PyPDF2...")
        os.system(f"{sys.executable} -m pip install PyPDF2")
        from PyPDF2 import PdfReader
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_suffix('.txt')
    
    print(f"Reading: {input_path}")
    
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    print(f"Pages: {total_pages}")
    
    text_parts = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_parts.append(f"\n--- Page {i+1} ---\n{text}")
        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{total_pages} pages...")
    
    full_text = "\n".join(text_parts)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"\n✅ Saved to: {output_path}")
    print(f"   Size: {len(full_text):,} characters")
    print(f"\nAdd this file to your materials folder for analysis.")

if __name__ == "__main__":
    main()
