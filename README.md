# PDF to Markdown Converter

A simple Python tool to convert PDF files into Markdown format.

## Features

- Extracts text from PDF files
- Converts to clean Markdown format
- Preserves page structure
- Simple command-line interface

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage (auto-generates output filename):

```bash
python pdf_to_markdown.py document.pdf
```

This will create `document.md` in the current directory.

### Specify output filename:

```bash
python pdf_to_markdown.py document.pdf output.md
```

### Use as a module:

```python
from pdf_to_markdown import pdf_to_markdown

pdf_to_markdown('input.pdf', 'output.md')
```

## Output Format

The generated Markdown file includes:
- Document title (based on PDF filename)
- Page-by-page content with headers
- Clean text formatting

## Requirements

- Python 3.6+
- PyMuPDF (fitz)

## Example

```bash
# Convert a PDF file
python pdf_to_markdown.py research_paper.pdf

# Output: research_paper.md created
```

## Notes

- Text extraction quality depends on the PDF structure
- Best results with text-based PDFs (not scanned images)
- For scanned PDFs, consider using OCR tools first
