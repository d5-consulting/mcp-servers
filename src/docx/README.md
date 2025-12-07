# docx MCP Server

MCP server for Word document (.docx) creation, editing, and analysis.

## Features

- **Unpack/Pack**: Extract .docx files to XML for editing and repack them
- **Convert to Markdown**: Extract text content with tracked changes support
- **Convert to PDF**: Convert .docx to PDF using LibreOffice
- **Validation**: Optional LibreOffice validation when packing documents

## Tools

### `unpack`
Unpack a .docx, .pptx, or .xlsx file and format XML contents.

**Parameters:**
- `input_file` (str): Path to Office file
- `output_dir` (str): Path to output directory

### `pack`
Pack a directory into a .docx, .pptx, or .xlsx file.

**Parameters:**
- `input_dir` (str): Path to unpacked directory
- `output_file` (str): Path to output Office file
- `validate` (bool, optional): Validate with LibreOffice (default: False)

### `convert_to_markdown`
Convert .docx to markdown using pandoc.

**Parameters:**
- `docx_file` (str): Path to .docx file
- `output_file` (str): Path to output markdown file
- `track_changes` (str, optional): How to handle tracked changes: 'accept', 'reject', or 'all' (default: 'all')

### `convert_to_pdf`
Convert .docx to PDF using LibreOffice.

**Parameters:**
- `docx_file` (str): Path to .docx file
- `output_file` (str, optional): Path to output PDF (default: same name as input with .pdf extension)

## Requirements

- Python 3.12+
- pandoc (for markdown conversion)
- LibreOffice (for PDF conversion and validation)

## Installation

```bash
pip install -e .
```

## Usage

### stdio
```bash
python -m docx
```

### HTTP
```bash
TRANSPORT=sse HOST=0.0.0.0 PORT=8000 python -m docx
```

## Testing

```bash
pytest
```
