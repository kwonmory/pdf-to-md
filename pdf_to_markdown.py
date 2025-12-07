#!/usr/bin/env python3
"""
PDF to Markdown Converter
Reads PDF files and converts them to Markdown format
"""

import fitz  # PyMuPDF
import sys
import os
from pathlib import Path
from PIL import Image
import io

# Try to import pytesseract, but make it optional
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not installed. OCR functionality will be disabled.")
    print("Install with: pip install pytesseract")
    print("Also install Tesseract OCR: brew install tesseract (macOS) or apt-get install tesseract-ocr (Linux)")


def extract_text_with_ocr(page, page_num):
    """
    Extract text from a PDF page using OCR
    
    Args:
        page: PyMuPDF page object
        page_num: Page number (for progress indication)
    
    Returns:
        Extracted text string
    """
    if not OCR_AVAILABLE:
        return ""
    
    try:
        # Convert PDF page to image
        # Use higher DPI for better OCR accuracy (300 DPI recommended)
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom = ~144 DPI, increase for better quality
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Perform OCR with Korean and English language support
        # You can add more languages: 'kor+eng+jpn' for Korean, English, Japanese
        try:
            text = pytesseract.image_to_string(img, lang='kor+eng')
        except:
            # Fallback to English only if Korean language pack not installed
            text = pytesseract.image_to_string(img, lang='eng')
        
        return text.strip()
    except Exception as e:
        print(f"  Warning: OCR failed for page {page_num}: {e}")
        return ""


def extract_text_from_pdf(pdf_path, use_ocr=False):
    """
    Extract text from PDF file page by page with improved extraction methods

    Args:
        pdf_path: Path to the PDF file
        use_ocr: Whether to use OCR for image-based PDFs (default: auto-detect)

    Returns:
        List of tuples (page_number, text_content)
    """
    doc = fitz.open(pdf_path)
    pages_content = []
    ocr_used = False

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Method 1: Try standard text extraction
        text = page.get_text("text")
        
        # Filter out image metadata (common pattern: <image: ...>)
        if text.strip():
            lines = text.split("\n")
            filtered_lines = []
            for line in lines:
                line_stripped = line.strip()
                # Skip image metadata lines
                if line_stripped.startswith("<image:") or line_stripped.startswith("image:"):
                    continue
                # Skip lines that look like image metadata
                if "ICCBased" in line_stripped or "width:" in line_stripped or "height:" in line_stripped:
                    continue
                if line_stripped:
                    filtered_lines.append(line_stripped)
            text = "\n".join(filtered_lines)
        
        # Method 2: If empty, try blocks method (preserves layout better)
        if not text.strip():
            blocks = page.get_text("blocks")
            text_parts = []
            for block in blocks:
                if len(block) >= 5:  # block format: (x0, y0, x1, y1, "text", ...)
                    block_text = block[4].strip()
                    # Filter out image metadata
                    if block_text and not block_text.startswith("<image:") and "ICCBased" not in block_text:
                        text_parts.append(block_text)
            text = "\n".join(text_parts)
        
        # Method 3: If still empty, try dict method (most comprehensive)
        if not text.strip():
            text_dict = page.get_text("dict")
            text_parts = []
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = " ".join(
                            span.get("text", "") 
                            for span in line.get("spans", [])
                        )
                        line_text = line_text.strip()
                        # Filter out image metadata
                        if line_text and not line_text.startswith("<image:") and "ICCBased" not in line_text:
                            text_parts.append(line_text)
            text = "\n".join(text_parts)
        
        # Method 4: Try rawdict for complex layouts
        if not text.strip():
            try:
                raw_dict = page.get_text("rawdict")
                text_parts = []
                for block in raw_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            line_text = " ".join(
                                span.get("text", "") 
                                for span in line.get("spans", [])
                            )
                            line_text = line_text.strip()
                            # Filter out image metadata
                            if line_text and not line_text.startswith("<image:") and "ICCBased" not in line_text:
                                text_parts.append(line_text)
                text = "\n".join(text_parts)
            except:
                pass
        
        # Method 5: If still no text and OCR is available, use OCR
        if not text.strip() and OCR_AVAILABLE:
            if use_ocr or page_num == 0:  # Auto-detect: try OCR on first page if no text
                if page_num % 10 == 0:  # Progress indicator every 10 pages
                    print(f"  Processing page {page_num + 1} with OCR...")
                ocr_text = extract_text_with_ocr(page, page_num + 1)
                if ocr_text:
                    text = ocr_text
                    ocr_used = True
                    # If OCR worked on first page, enable it for all pages
                    if page_num == 0:
                        use_ocr = True
        
        pages_content.append((page_num + 1, text))

    doc.close()
    
    if ocr_used:
        print(f"  OCR was used to extract text from image-based pages")
    
    return pages_content


def convert_to_markdown(pages_content, pdf_filename):
    """
    Convert extracted PDF content to Markdown format

    Args:
        pages_content: List of tuples (page_number, text_content)
        pdf_filename: Name of the source PDF file

    Returns:
        Markdown formatted string
    """
    markdown_lines = []

    # Add title
    markdown_lines.append(f"# {pdf_filename}\n")
    markdown_lines.append("---\n")

    # Add content page by page
    for page_num, text in pages_content:
        markdown_lines.append(f"\n## Page {page_num}\n")

        # Clean up and format text
        if text.strip():
            # Remove excessive whitespace but preserve paragraph structure
            cleaned_text = "\n".join(
                line.strip() for line in text.split("\n") if line.strip()
            )
            markdown_lines.append(cleaned_text)
        else:
            markdown_lines.append("*[No text content on this page - may be image-based PDF]*")

        markdown_lines.append("\n")

    return "\n".join(markdown_lines)


def pdf_to_markdown(pdf_path, output_path=None, use_ocr=False):
    """
    Convert PDF file to Markdown

    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output Markdown file (optional)
        use_ocr: Force OCR usage even if text extraction works (default: auto-detect)
    """
    # Validate input file
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("Input file must be a PDF")

    # Determine output path
    if output_path is None:
        output_path = Path(pdf_path).stem + ".md"

    print(f"Reading PDF: {pdf_path}")

    # Extract text from PDF
    pages_content = extract_text_from_pdf(pdf_path, use_ocr=use_ocr)
    print(f"Extracted {len(pages_content)} pages")
    
    # Count pages with text
    pages_with_text = sum(1 for _, text in pages_content if text.strip())
    print(f"Pages with text: {pages_with_text}/{len(pages_content)}")

    # Convert to Markdown
    markdown_content = convert_to_markdown(pages_content, Path(pdf_path).name)

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Markdown file created: {output_path}")
    
    if pages_with_text == 0 and not OCR_AVAILABLE:
        print("\n⚠️  WARNING: No text was extracted from this PDF.")
        print("   This PDF appears to be image-based (scanned).")
        print("   Install OCR tools to extract text:")
        print("   1. pip install pytesseract Pillow")
        print("   2. brew install tesseract tesseract-lang (macOS)")
        print("   3. Run again to automatically use OCR")
    
    return output_path


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_markdown.py <pdf_file> [output_file] [--ocr]")
        print("\nExample:")
        print("  python pdf_to_markdown.py document.pdf")
        print("  python pdf_to_markdown.py document.pdf output.md")
        print("  python pdf_to_markdown.py document.pdf output.md --ocr")
        print("\nOptions:")
        print("  --ocr    Force OCR usage for all pages (slower but works for scanned PDFs)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = None
    use_ocr = False
    
    # Parse arguments
    for arg in sys.argv[2:]:
        if arg == "--ocr":
            use_ocr = True
        elif not arg.startswith("--"):
            output_path = arg

    try:
        pdf_to_markdown(pdf_path, output_path, use_ocr=use_ocr)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
