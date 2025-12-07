# PDF to Markdown Converter

A powerful Python tool to convert PDF files into Markdown format with automatic OCR support for scanned documents.

## Features

- **Multiple text extraction methods**: Tries various extraction techniques for best results
- **Automatic OCR support**: Detects image-based PDFs and uses OCR automatically
- **Manual OCR option**: Force OCR processing with `--ocr` flag
- **Multi-language OCR**: Supports Korean, English, and other languages
- **Clean Markdown output**: Preserves page structure with proper formatting
- **Simple command-line interface**: Easy to use with flexible options

## Installation

### 1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (required for OCR functionality):

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng
```

**Windows:**
Download and install from [GitHub - UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

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

### Force OCR for all pages (for scanned PDFs):

```bash
python pdf_to_markdown.py scanned_document.pdf output.md --ocr
```

### Use as a module:

```python
from pdf_to_markdown import pdf_to_markdown

# Basic usage
pdf_to_markdown('input.pdf', 'output.md')

# With OCR
pdf_to_markdown('input.pdf', 'output.md', use_ocr=True)
```

## How It Works

The tool uses multiple extraction methods in sequence:

1. **Standard text extraction**: Extracts text directly from PDF text layers
2. **Block-based extraction**: Preserves layout better for complex documents
3. **Dictionary-based extraction**: Most comprehensive method for structured content
4. **Raw dictionary extraction**: Handles complex layouts
5. **OCR (automatic)**: If no text is found, automatically uses OCR for image-based PDFs

## Output Format

The generated Markdown file includes:
- Document title (based on PDF filename)
- Page-by-page content with headers (`## Page N`)
- Clean text formatting with preserved paragraph structure
- Placeholder messages for pages without extractable text

## Requirements

- Python 3.6+
- **Required packages:**
  - PyMuPDF (pymupdf) - PDF processing
  - Pillow - Image processing for OCR
  - pytesseract - Python wrapper for Tesseract OCR
- **System requirements:**
  - Tesseract OCR (see Installation section)
  - Tesseract language packs (for non-English text)

## Examples

### Convert a text-based PDF:

```bash
python pdf_to_markdown.py research_paper.pdf
# Output: research_paper.md created
```

### Convert a scanned PDF with OCR:

```bash
python pdf_to_markdown.py scanned_book.pdf book.md --ocr
# Automatically processes all pages with OCR
```

### Convert with auto-detection (recommended):

```bash
python pdf_to_markdown.py document.pdf
# Automatically detects if OCR is needed and uses it
```

## Notes

- **Text-based PDFs**: Best results with PDFs that have text layers
- **Scanned PDFs**: Automatically detected and processed with OCR
- **OCR accuracy**: Depends on image quality. Higher DPI images produce better results
- **Processing time**: OCR processing is slower but necessary for scanned documents
- **Language support**: Install appropriate Tesseract language packs for best results
- **Large files**: Processing time increases with page count, especially with OCR

## Troubleshooting

### OCR not working?

1. Verify Tesseract is installed:
   ```bash
   tesseract --version
   ```

2. Check language packs are installed:
   ```bash
   tesseract --list-langs
   ```

3. If Korean text recognition fails, ensure Korean language pack is installed:
   ```bash
   brew install tesseract-lang  # macOS
   ```

### No text extracted?

- Try using `--ocr` flag to force OCR processing
- Check if PDF is password-protected
- Verify PDF file is not corrupted

## License

See LICENSE file for details.

## Dependencies

- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - AGPL v3.0 or Commercial License
- [pytesseract](https://github.com/madmaze/pytesseract) - Apache 2.0
- [Pillow](https://github.com/python-pillow/Pillow) - PIL License (BSD-like)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Apache 2.0

---

# PDF to Markdown 변환기

스캔된 문서를 위한 자동 OCR 지원 기능이 포함된 강력한 Python PDF to Markdown 변환 도구입니다.

## 주요 기능

- **다양한 텍스트 추출 방법**: 최상의 결과를 위해 여러 추출 기법을 시도합니다
- **자동 OCR 지원**: 이미지 기반 PDF를 자동으로 감지하고 OCR을 사용합니다
- **수동 OCR 옵션**: `--ocr` 플래그로 OCR 처리를 강제할 수 있습니다
- **다국어 OCR 지원**: 한국어, 영어 및 기타 언어를 지원합니다
- **깔끔한 Markdown 출력**: 적절한 포맷팅으로 페이지 구조를 보존합니다
- **간단한 명령줄 인터페이스**: 유연한 옵션으로 사용하기 쉽습니다

## 설치

### 1. Python 의존성 패키지 설치:

```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR 설치 (OCR 기능에 필요):

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng
```

**Windows:**
[GitHub - UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)에서 다운로드 및 설치

## 사용법

### 기본 사용법 (출력 파일명 자동 생성):

```bash
python pdf_to_markdown.py document.pdf
```

현재 디렉토리에 `document.md` 파일이 생성됩니다.

### 출력 파일명 지정:

```bash
python pdf_to_markdown.py document.pdf output.md
```

### 모든 페이지에 OCR 강제 적용 (스캔된 PDF용):

```bash
python pdf_to_markdown.py scanned_document.pdf output.md --ocr
```

### 모듈로 사용:

```python
from pdf_to_markdown import pdf_to_markdown

# 기본 사용
pdf_to_markdown('input.pdf', 'output.md')

# OCR 사용
pdf_to_markdown('input.pdf', 'output.md', use_ocr=True)
```

## 동작 원리

이 도구는 여러 추출 방법을 순차적으로 사용합니다:

1. **표준 텍스트 추출**: PDF 텍스트 레이어에서 직접 텍스트를 추출합니다
2. **블록 기반 추출**: 복잡한 문서의 레이아웃을 더 잘 보존합니다
3. **딕셔너리 기반 추출**: 구조화된 콘텐츠에 가장 포괄적인 방법입니다
4. **원시 딕셔너리 추출**: 복잡한 레이아웃을 처리합니다
5. **OCR (자동)**: 텍스트를 찾을 수 없으면 이미지 기반 PDF에 대해 자동으로 OCR을 사용합니다

## 출력 형식

생성된 Markdown 파일에는 다음이 포함됩니다:
- 문서 제목 (PDF 파일명 기반)
- 페이지별 콘텐츠와 헤더 (`## Page N`)
- 단락 구조가 보존된 깔끔한 텍스트 포맷팅
- 추출 가능한 텍스트가 없는 페이지에 대한 플레이스홀더 메시지

## 요구사항

- Python 3.6+
- **필수 패키지:**
  - PyMuPDF (pymupdf) - PDF 처리
  - Pillow - OCR용 이미지 처리
  - pytesseract - Tesseract OCR의 Python 래퍼
- **시스템 요구사항:**
  - Tesseract OCR (설치 섹션 참조)
  - Tesseract 언어 팩 (비영어 텍스트용)

## 예제

### 텍스트 기반 PDF 변환:

```bash
python pdf_to_markdown.py research_paper.pdf
# 출력: research_paper.md 생성됨
```

### OCR로 스캔된 PDF 변환:

```bash
python pdf_to_markdown.py scanned_book.pdf book.md --ocr
# 모든 페이지를 OCR로 자동 처리
```

### 자동 감지로 변환 (권장):

```bash
python pdf_to_markdown.py document.pdf
# OCR이 필요한지 자동으로 감지하여 사용
```

## 참고사항

- **텍스트 기반 PDF**: 텍스트 레이어가 있는 PDF에서 최상의 결과를 얻습니다
- **스캔된 PDF**: 자동으로 감지되어 OCR로 처리됩니다
- **OCR 정확도**: 이미지 품질에 따라 달라집니다. 더 높은 DPI 이미지가 더 나은 결과를 생성합니다
- **처리 시간**: OCR 처리는 느리지만 스캔된 문서에는 필수입니다
- **언어 지원**: 최상의 결과를 위해 적절한 Tesseract 언어 팩을 설치하세요
- **대용량 파일**: 페이지 수가 증가할수록 처리 시간이 늘어나며, 특히 OCR 사용 시 더욱 그렇습니다

## 문제 해결

### OCR이 작동하지 않나요?

1. Tesseract가 설치되어 있는지 확인:
   ```bash
   tesseract --version
   ```

2. 언어 팩이 설치되어 있는지 확인:
   ```bash
   tesseract --list-langs
   ```

3. 한국어 텍스트 인식이 실패하는 경우, 한국어 언어 팩이 설치되어 있는지 확인:
   ```bash
   brew install tesseract-lang  # macOS
   ```

### 텍스트가 추출되지 않나요?

- `--ocr` 플래그를 사용하여 OCR 처리를 강제해보세요
- PDF가 비밀번호로 보호되어 있는지 확인하세요
- PDF 파일이 손상되지 않았는지 확인하세요
