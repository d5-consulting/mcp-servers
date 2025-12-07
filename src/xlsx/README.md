# xlsx MCP Server

MCP server for Excel spreadsheet (.xlsx) creation, editing, and analysis.

## Features

- **Read/Write**: Read Excel data as markdown, write cells with values or formulas
- **Create**: Create new Excel files from CSV data
- **Formulas**: Recalculate formulas and check for errors using LibreOffice
- **Sheets**: List, add, and manage multiple sheets
- **Convert**: Convert Excel to CSV format

## Tools

### `read_excel`
Read an Excel file and return its contents as markdown table.

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str, optional): Sheet name to read (default: first sheet)

### `create_excel`
Create a new Excel file with data.

**Parameters:**
- `file_path` (str): Path to output Excel file
- `data` (str): CSV formatted data to write
- `sheet_name` (str, optional): Name of the sheet (default: 'Sheet1')

### `write_cell`
Write a value or formula to a specific cell.

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str): Name of the sheet
- `cell` (str): Cell address (e.g., 'A1', 'B5')
- `value` (str): Value or formula to write (formulas start with '=')

### `recalculate`
Recalculate all formulas in Excel file and check for errors.

**Parameters:**
- `file_path` (str): Path to Excel file
- `timeout` (int, optional): Maximum time to wait for recalculation (default: 30 seconds)

### `get_sheet_names`
Get list of sheet names in an Excel file.

**Parameters:**
- `file_path` (str): Path to Excel file

### `add_sheet`
Add a new sheet to an Excel file.

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str): Name for the new sheet

### `convert_to_csv`
Convert an Excel sheet to CSV.

**Parameters:**
- `file_path` (str): Path to Excel file
- `output_file` (str): Path to output CSV file
- `sheet_name` (str, optional): Sheet name to convert (default: first sheet)

## Requirements

- Python 3.12+
- LibreOffice (for formula recalculation)

## Installation

```bash
pip install -e .
```

## Usage

### stdio
```bash
python -m xlsx
```

### HTTP
```bash
TRANSPORT=sse HOST=0.0.0.0 PORT=8000 python -m xlsx
```

## Testing

```bash
pytest
```
