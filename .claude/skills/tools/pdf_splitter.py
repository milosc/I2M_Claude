#!/usr/bin/env python3
"""
PDF Splitter Utility for Discovery Analysis
Splits large PDFs into smaller chunks and converts to Markdown for Claude processing.

AUTOMATIC CHUNKING + MARKDOWN CONVERSION:
- PDFs with >10 pages are automatically split into 20-page chunks
- Chunks are converted to Markdown using MarkItDown for better LLM processing
- Markdown is more token-efficient and avoids "PDF too large" errors

Usage:
    # Get page count
    python pdf_splitter.py count <input.pdf>

    # Split PDF into 20-page chunks (default)
    python pdf_splitter.py split <input.pdf> <output_dir> [--pages 20]

    # Convert single PDF to Markdown
    python pdf_splitter.py tomarkdown <input.pdf> [output.md]

    # Auto-process: split if >10 pages, convert all to Markdown (RECOMMENDED)
    python pdf_splitter.py automd <input.pdf> <output_dir>

    # Extract text from PDF (legacy, use tomarkdown instead)
    python pdf_splitter.py extract <input.pdf> [output.txt]

Dependencies:
    pip install PyPDF2 markitdown
"""

import sys
import os
from pathlib import Path

# Configuration
DEFAULT_PAGES_PER_CHUNK = 20  # Maximum pages per chunk for Claude processing
MAX_PAGES_DIRECT_READ = 10   # PDFs with this many pages or fewer can be read directly

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyPDF2
        return True
    except ImportError:
        print("""
⚠️ ERROR: PyPDF2 is not installed.

To install PyPDF2, run one of these commands:

Option 1 - User install (recommended for macOS):
    python3 -m pip install --user PyPDF2

Option 2 - Virtual environment:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install PyPDF2

Option 3 - System-wide (if you have permissions):
    pip install PyPDF2

After installing, run this script again.
""")
        sys.exit(1)


def check_markitdown_dependency():
    """Check if MarkItDown is installed."""
    try:
        from markitdown import MarkItDown
        return True
    except ImportError:
        print("""
⚠️ ERROR: MarkItDown is not installed.

To install MarkItDown, run:
    pip install 'markitdown[all]'

Or with the project virtual environment:
    .venv/bin/pip install 'markitdown[all]'

After installing, run this script again.
""")
        return False


def get_pdf_page_count(input_path: str) -> int:
    """
    Get the total number of pages in a PDF.

    Args:
        input_path: Path to the PDF file

    Returns:
        Number of pages in the PDF
    """
    from PyPDF2 import PdfReader

    reader = PdfReader(str(input_path))
    return len(reader.pages)


def needs_splitting(input_path: str, max_pages: int = MAX_PAGES_DIRECT_READ) -> tuple:
    """
    Check if a PDF needs to be split into chunks.

    Args:
        input_path: Path to the PDF file
        max_pages: Maximum pages before splitting is needed (default: 30)

    Returns:
        Tuple of (needs_split: bool, page_count: int)
    """
    page_count = get_pdf_page_count(input_path)
    return (page_count > max_pages, page_count)


def split_pdf(input_path: str, output_dir: str, pages_per_chunk: int = DEFAULT_PAGES_PER_CHUNK) -> list:
    """
    Split a PDF into smaller chunks.
    
    Args:
        input_path: Path to the input PDF
        output_dir: Directory to save chunks
        pages_per_chunk: Maximum pages per output file (default: 50)
    
    Returns:
        List of created chunk file paths
    """
    from PyPDF2 import PdfReader, PdfWriter
    
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the input PDF
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    print(f"📄 Input PDF: {input_path.name}")
    print(f"📊 Total pages: {total_pages}")
    print(f"📦 Pages per chunk: {pages_per_chunk}")
    
    # Calculate number of chunks
    num_chunks = (total_pages + pages_per_chunk - 1) // pages_per_chunk
    print(f"📁 Will create {num_chunks} chunks")
    
    created_files = []
    base_name = input_path.stem

    for chunk_num in range(num_chunks):
        start_page = chunk_num * pages_per_chunk
        end_page = min(start_page + pages_per_chunk, total_pages)

        # Create a new PDF writer for this chunk
        writer = PdfWriter()

        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Save the chunk with clean naming: {base}_{start}_{end}.pdf
        # e.g., UserManual_1_30.pdf, UserManual_31_60.pdf, UserManual_61_72.pdf
        chunk_filename = f"{base_name}_{start_page + 1}_{end_page}.pdf"
        chunk_path = output_dir / chunk_filename

        with open(chunk_path, 'wb') as output_file:
            writer.write(output_file)

        created_files.append(str(chunk_path))
        print(f"  ✅ Created: {chunk_filename} (pages {start_page + 1}-{end_page})")

    print(f"\n✅ Split complete! Created {len(created_files)} chunks in {output_dir}")
    return created_files


def auto_process_pdf(input_path: str, output_dir: str = None, pages_per_chunk: int = DEFAULT_PAGES_PER_CHUNK) -> dict:
    """
    Automatically process a PDF: check page count and split if needed.

    This is the main function for Discovery Analysis to call.

    Args:
        input_path: Path to the input PDF
        output_dir: Directory to save chunks (optional, defaults to same dir as input)
        pages_per_chunk: Maximum pages per chunk (default: 30)

    Returns:
        Dictionary with:
            - 'status': 'direct' | 'chunked' | 'error'
            - 'page_count': total pages in original PDF
            - 'chunks': list of chunk file paths (if chunked)
            - 'original': original file path
            - 'message': human-readable status
    """
    input_path = Path(input_path)

    if not input_path.exists():
        return {
            'status': 'error',
            'page_count': 0,
            'chunks': [],
            'original': str(input_path),
            'message': f"File not found: {input_path}"
        }

    try:
        page_count = get_pdf_page_count(str(input_path))

        if page_count <= pages_per_chunk:
            # PDF is small enough to read directly
            return {
                'status': 'direct',
                'page_count': page_count,
                'chunks': [str(input_path)],
                'original': str(input_path),
                'message': f"📄 {input_path.name}: {page_count} pages (can read directly)"
            }
        else:
            # PDF needs to be split
            if output_dir is None:
                output_dir = input_path.parent / f"{input_path.stem}_chunks"

            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            num_chunks = (page_count + pages_per_chunk - 1) // pages_per_chunk
            print(f"📚 {input_path.name}: {page_count} pages → splitting into {num_chunks} chunks of {pages_per_chunk} pages")

            chunk_files = split_pdf(str(input_path), str(output_dir), pages_per_chunk)

            return {
                'status': 'chunked',
                'page_count': page_count,
                'chunks': chunk_files,
                'original': str(input_path),
                'message': f"📚 {input_path.name}: {page_count} pages → split into {len(chunk_files)} chunks"
            }

    except Exception as e:
        return {
            'status': 'error',
            'page_count': 0,
            'chunks': [],
            'original': str(input_path),
            'message': f"Error processing {input_path.name}: {str(e)}"
        }


def extract_text_from_pdf(input_path: str, output_path: str = None) -> str:
    """
    Extract all text from a PDF into a single text file.
    This is the PREFERRED method for Discovery Analysis.
    
    Args:
        input_path: Path to the input PDF
        output_path: Path for output text file (optional)
    
    Returns:
        Extracted text content
    """
    from PyPDF2 import PdfReader
    
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)
    
    print(f"📄 Extracting text from: {input_path.name}")
    
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text.append(f"\n--- Page {i + 1} ---\n")
            all_text.append(text)
        
        # Progress indicator every 50 pages
        if (i + 1) % 50 == 0:
            print(f"  📖 Processed {i + 1}/{total_pages} pages...")
    
    full_text = "\n".join(all_text)
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"✅ Extracted {total_pages} pages to: {output_path}")
    print(f"📊 Output size: {len(full_text):,} characters")

    return full_text


def convert_pdf_to_markdown(input_path: str, output_path: str = None) -> dict:
    """
    Convert a single PDF to Markdown using MarkItDown.

    Args:
        input_path: Path to the input PDF
        output_path: Path for output Markdown file (optional)

    Returns:
        Dictionary with:
            - 'status': 'success' | 'error'
            - 'input': input file path
            - 'output': output markdown file path
            - 'message': human-readable status
    """
    if not check_markitdown_dependency():
        return {
            'status': 'error',
            'input': str(input_path),
            'output': None,
            'message': 'MarkItDown not installed'
        }

    from markitdown import MarkItDown

    input_path = Path(input_path)

    if not input_path.exists():
        return {
            'status': 'error',
            'input': str(input_path),
            'output': None,
            'message': f'File not found: {input_path}'
        }

    if output_path is None:
        output_path = input_path.with_suffix('.md')
    else:
        output_path = Path(output_path)

    try:
        print(f"📄 Converting to Markdown: {input_path.name}")

        md = MarkItDown()
        result = md.convert(str(input_path))

        # Write markdown content to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)

        print(f"✅ Created: {output_path.name} ({len(result.text_content):,} chars)")

        return {
            'status': 'success',
            'input': str(input_path),
            'output': str(output_path),
            'message': f'Converted {input_path.name} to {output_path.name}'
        }

    except Exception as e:
        return {
            'status': 'error',
            'input': str(input_path),
            'output': None,
            'message': f'Error converting {input_path.name}: {str(e)}'
        }


def auto_process_to_markdown(input_path: str, output_dir: str = None, pages_per_chunk: int = DEFAULT_PAGES_PER_CHUNK) -> dict:
    """
    Auto-process PDF: split if >30 pages, convert all chunks to Markdown.

    This is the RECOMMENDED function for Discovery Analysis.

    Args:
        input_path: Path to the input PDF
        output_dir: Directory to save Markdown files
        pages_per_chunk: Maximum pages per chunk (default: 30)

    Returns:
        Dictionary with:
            - 'status': 'direct' | 'chunked' | 'error'
            - 'page_count': total pages in original PDF
            - 'markdown_files': list of created .md file paths
            - 'original': original file path
            - 'message': human-readable status
    """
    if not check_markitdown_dependency():
        return {
            'status': 'error',
            'page_count': 0,
            'markdown_files': [],
            'original': str(input_path),
            'message': 'MarkItDown not installed'
        }

    input_path = Path(input_path)

    if not input_path.exists():
        return {
            'status': 'error',
            'page_count': 0,
            'markdown_files': [],
            'original': str(input_path),
            'message': f'File not found: {input_path}'
        }

    try:
        page_count = get_pdf_page_count(str(input_path))

        if output_dir is None:
            output_dir = input_path.parent / f"{input_path.stem}_markdown"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        markdown_files = []

        if page_count <= pages_per_chunk:
            # PDF is small enough - convert directly
            print(f"📄 {input_path.name}: {page_count} pages (converting directly)")

            output_md = output_dir / f"{input_path.stem}.md"
            result = convert_pdf_to_markdown(str(input_path), str(output_md))

            if result['status'] == 'success':
                markdown_files.append(result['output'])

            return {
                'status': 'direct',
                'page_count': page_count,
                'markdown_files': markdown_files,
                'original': str(input_path),
                'message': f"📄 {input_path.name}: {page_count} pages → 1 Markdown file"
            }

        else:
            # PDF needs splitting first
            num_chunks = (page_count + pages_per_chunk - 1) // pages_per_chunk
            print(f"📚 {input_path.name}: {page_count} pages → splitting into {num_chunks} chunks")

            # Create temp directory for PDF chunks
            temp_chunks_dir = output_dir / "_temp_chunks"
            temp_chunks_dir.mkdir(parents=True, exist_ok=True)

            # Split PDF into chunks
            chunk_files = split_pdf(str(input_path), str(temp_chunks_dir), pages_per_chunk)

            # Convert each chunk to Markdown
            print(f"\n📝 Converting {len(chunk_files)} chunks to Markdown...")
            for chunk_path in chunk_files:
                chunk_path = Path(chunk_path)
                output_md = output_dir / f"{chunk_path.stem}.md"
                result = convert_pdf_to_markdown(str(chunk_path), str(output_md))

                if result['status'] == 'success':
                    markdown_files.append(result['output'])

            # Clean up temp PDF chunks (optional - keep for debugging)
            # import shutil
            # shutil.rmtree(temp_chunks_dir)

            print(f"\n✅ Created {len(markdown_files)} Markdown files in {output_dir}")

            return {
                'status': 'chunked',
                'page_count': page_count,
                'markdown_files': markdown_files,
                'original': str(input_path),
                'message': f"📚 {input_path.name}: {page_count} pages → {len(markdown_files)} Markdown files"
            }

    except Exception as e:
        return {
            'status': 'error',
            'page_count': 0,
            'markdown_files': [],
            'original': str(input_path),
            'message': f'Error processing {input_path.name}: {str(e)}'
        }


def main():
    """Main entry point."""
    check_dependencies()

    if len(sys.argv) < 2:
        print("""
PDF Splitter Utility for Discovery Analysis
============================================

AUTOMATIC CHUNKING + MARKDOWN CONVERSION for large PDFs.

Commands:
    count <input.pdf>
        Get page count of a PDF

    auto <input.pdf> [output_dir]
        Auto-process: check pages, split if >10 pages (PDF output)

    automd <input.pdf> <output_dir>
        Auto-process + convert to Markdown (RECOMMENDED for Discovery)
        Splits if >10 pages, converts all chunks to .md files

    tomarkdown <input.pdf> [output.md]
        Convert single PDF to Markdown

    split <input.pdf> <output_dir> [--pages 20]
        Split PDF into chunks (default: 20 pages per chunk)

    extract <input.pdf> [output.txt]
        Extract all text from PDF to text file (legacy)

Examples:
    python pdf_splitter.py count manual.pdf
    python pdf_splitter.py automd manual.pdf ./markdown_output
    python pdf_splitter.py tomarkdown manual.pdf manual.md
    python pdf_splitter.py auto manual.pdf ./chunks
    python pdf_splitter.py split manual.pdf ./chunks --pages 30

Output Naming (automd):
    UserManual.pdf (72 pages) →
        UserManual_1_20.md
        UserManual_21_40.md
        UserManual_41_60.md
        UserManual_61_72.md
        """)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "count":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py count <input.pdf>")
            sys.exit(1)
        input_pdf = sys.argv[2]
        page_count = get_pdf_page_count(input_pdf)
        needs_split = page_count > MAX_PAGES_DIRECT_READ
        status = "⚠️ NEEDS SPLITTING" if needs_split else "✅ Can read directly"
        print(f"📄 {Path(input_pdf).name}: {page_count} pages")
        print(f"   {status} (threshold: {MAX_PAGES_DIRECT_READ} pages)")

    elif command == "auto":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py auto <input.pdf> [output_dir]")
            sys.exit(1)
        input_pdf = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        result = auto_process_pdf(input_pdf, output_dir)
        print(result['message'])
        if result['status'] == 'chunked':
            print(f"   Chunks saved to: {Path(result['chunks'][0]).parent}")
            for chunk in result['chunks']:
                print(f"   - {Path(chunk).name}")

    elif command == "split":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py split <input.pdf> <output_dir> [--pages 30]")
            sys.exit(1)
        input_pdf = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "./pdf_chunks"
        pages = DEFAULT_PAGES_PER_CHUNK

        # Check for --pages argument
        for i, arg in enumerate(sys.argv):
            if arg == "--pages" and i + 1 < len(sys.argv):
                pages = int(sys.argv[i + 1])

        split_pdf(input_pdf, output_dir, pages)

    elif command == "extract":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py extract <input.pdf> [output.txt]")
            sys.exit(1)
        input_pdf = sys.argv[2]
        output_txt = sys.argv[3] if len(sys.argv) > 3 else None
        extract_text_from_pdf(input_pdf, output_txt)

    elif command == "tomarkdown":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py tomarkdown <input.pdf> [output.md]")
            sys.exit(1)
        input_pdf = sys.argv[2]
        output_md = sys.argv[3] if len(sys.argv) > 3 else None
        result = convert_pdf_to_markdown(input_pdf, output_md)
        print(result['message'])
        if result['status'] == 'error':
            sys.exit(1)

    elif command == "automd":
        if len(sys.argv) < 3:
            print("Usage: python pdf_splitter.py automd <input.pdf> <output_dir>")
            sys.exit(1)
        input_pdf = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        result = auto_process_to_markdown(input_pdf, output_dir)
        print(result['message'])
        if result['status'] in ['direct', 'chunked']:
            print(f"   Markdown files in: {Path(result['markdown_files'][0]).parent if result['markdown_files'] else 'N/A'}")
            for md_file in result['markdown_files']:
                print(f"   - {Path(md_file).name}")
        if result['status'] == 'error':
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Use 'count', 'auto', 'automd', 'tomarkdown', 'split', or 'extract'")
        sys.exit(1)


if __name__ == "__main__":
    main()
