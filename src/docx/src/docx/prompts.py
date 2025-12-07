from . import mcp


@mcp.prompt()
def docx_workflow() -> str:
    """Provides guidance on working with Word documents."""
    return """# Working with Word Documents (.docx)

## Quick Reference

### Reading Documents
- `convert_to_markdown` - Extract text as markdown (preserves tracked changes)

### Creating/Editing Documents
- `unpack` - Extract .docx to XML for editing
- `pack` - Repack edited XML back to .docx

### Converting Documents
- `convert_to_pdf` - Convert .docx to PDF
- `convert_to_markdown` - Convert to markdown

## Workflow Decision Tree

### Reading/Analyzing Content
- Text extraction: `pandoc --track-changes=all path-to-file.docx -o output.md`
- Raw XML access: Unpack for comments, formatting, structure, media

### Creating New Document
→ Use **docx-js** workflow (see `docx_creation()` prompt)

### Editing Existing Document
- **Your own document + simple changes**: Basic OOXML editing
- **Someone else's document**: Use **Redlining workflow** (recommended)
- **Legal, academic, business, government docs**: Use **Redlining workflow** (required)

See `docx_redlining()` and `docx_ooxml_reference()` prompts for details.

## Typical Workflows

### 1. Read Document Content
```
convert_to_markdown(docx_file="document.docx", output_file="output.md", track_changes="all")
```

### 2. Edit Document (Advanced)
```
# Step 1: Unpack
unpack(input_file="document.docx", output_dir="unpacked")

# Step 2: Edit XML files in unpacked/word/document.xml
# Use grep/sed or custom scripts to modify XML

# Step 3: Repack
pack(input_dir="unpacked", output_file="edited.docx", validate=True)
```

### 3. Convert to PDF
```
convert_to_pdf(docx_file="document.docx")
```

## Notes
- Requires pandoc for markdown conversion
- Requires LibreOffice (soffice) for PDF conversion and validation
- XML editing requires understanding of OOXML format
"""


@mcp.prompt()
def docx_creation() -> str:
    """Creating new Word documents with docx-js."""
    return """# Creating New Word Documents with docx-js

## Workflow

1. **MANDATORY**: Read `docx-js.md` completely (~500 lines, no range limits)
   - Detailed syntax, formatting rules, best practices
2. Create JavaScript/TypeScript file using Document, Paragraph, TextRun components
3. Export as .docx using Packer.toBuffer()

## Basic Example

```javascript
const { Document, Packer, Paragraph, TextRun } = require("docx");
const fs = require("fs");

const doc = new Document({
    sections: [{
        properties: {},
        children: [
            new Paragraph({
                children: [
                    new TextRun({
                        text: "Hello World",
                        bold: true,
                        size: 28,
                    }),
                ],
            }),
            new Paragraph({
                text: "This is a simple document created with docx-js",
            }),
        ],
    }],
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("document.docx", buffer);
});
```

## Key Components

**Document** - Root container for sections
**Section** - Page layout and orientation
**Paragraph** - Text block with formatting
**TextRun** - Inline text with styling (bold, italic, size, color)
**Table** - Tabular data
**Header/Footer** - Page headers and footers
**Numbering** - Bulleted and numbered lists

## Common Formatting

**Text styling**: bold, italic, underline, size, color, font
**Paragraph**: alignment, spacing, indentation, borders
**Lists**: bullets, numbering, multi-level
**Tables**: rows, columns, cell merging, borders
**Page**: margins, orientation, size, headers/footers

## Dependencies

All dependencies should be installed. If not:
- `npm install -g docx`
"""


@mcp.prompt()
def docx_redlining() -> str:
    """Tracked changes workflow for document review."""
    return """# Redlining Workflow for Document Review

## When to Use

- Editing someone else's document
- Legal, academic, business, or government docs
- Any situation requiring change tracking

## Principle: Minimal, Precise Edits

**Only mark text that actually changes**. Don't repeat unchanged text.

**BAD** - Replaces entire sentence:
```python
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'
```

**GOOD** - Only marks what changed:
```python
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

## Workflow

### 1. Get Markdown Representation
```bash
pandoc --track-changes=all path-to-file.docx -o current.md
```

### 2. Identify and Group Changes

**Batching strategy**: Group 3-10 related changes per batch

**Location methods** (for finding in XML):
- Section/heading numbers (e.g., "Section 3.2")
- Paragraph identifiers
- Grep patterns with unique surrounding text
- Document structure (e.g., "first paragraph")
- **DO NOT use markdown line numbers**

**Batch organization**:
- By section: "Batch 1: Section 2 amendments"
- By type: "Batch 1: Date corrections"
- By complexity: Simple text first, then structural
- Sequential: "Batch 1: Pages 1-3"

### 3. Read Documentation and Unpack

**MANDATORY**: Read `ooxml.md` completely (~600 lines, no range limits)
- Focus on "Document Library" and "Tracked Change Patterns" sections

**Unpack**:
```bash
python ooxml/scripts/unpack.py <file.docx> <dir>
```

**Note the suggested RSID** from unpack output for tracked changes

### 4. Implement Changes in Batches

For each batch (3-10 related changes):

**a. Map text to XML**: Grep for text in `word/document.xml` to verify `<w:r>` splitting

**b. Create and run script**: Use `get_node` to find nodes, implement changes, `doc.save()`

**Note**: Always grep `word/document.xml` before writing script (line numbers change after each run)

### 5. Pack the Document

After all batches:
```bash
python ooxml/scripts/pack.py unpacked reviewed-document.docx
```

### 6. Final Verification

```bash
# Convert to markdown
pandoc --track-changes=all reviewed-document.docx -o verification.md

# Verify changes
grep "original phrase" verification.md  # Should NOT find
grep "replacement phrase" verification.md  # Should find
```

## Key File Structures

- `word/document.xml` - Main document
- `word/comments.xml` - Comments
- `word/media/` - Embedded images
- Tracked changes: `<w:ins>` (insertions), `<w:del>` (deletions)
"""


@mcp.prompt()
def docx_ooxml_reference() -> str:
    """OOXML editing patterns and Document library reference."""
    return """# OOXML Editing Reference

## Unpacking and Packing

### Unpack
```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
```

### Pack
```bash
python ooxml/scripts/pack.py <input_directory> <office_file>
```

## Key XML Files

- `word/document.xml` - Main document contents
- `word/comments.xml` - Comments referenced in document.xml
- `word/media/` - Embedded images and media files
- Tracked changes: `<w:ins>` and `<w:del>` tags

## Document Library (Python)

**MANDATORY**: Read `ooxml.md` completely (~600 lines, no range limits) for:
- Complete Document library API
- XML patterns for editing
- Tracked change patterns
- Example scripts

The Document library automatically handles infrastructure setup and provides:
- High-level methods for common operations
- Direct DOM access for complex scenarios
- `get_node` for finding elements
- `doc.save()` for persisting changes

### Basic Pattern

```python
from ooxml import Document

# Load unpacked document
doc = Document("unpacked_dir")

# Find and modify nodes
node = doc.get_node("//w:p[1]")  # First paragraph
# ... make changes ...

# Save
doc.save()
```

## Converting to Images

**Two-step process**:

1. Convert to PDF:
```bash
soffice --headless --convert-to pdf document.docx
```

2. Convert PDF to JPEG:
```bash
pdftoppm -jpeg -r 150 document.pdf page
```

Creates `page-1.jpg`, `page-2.jpg`, etc.

**Options**:
- `-r 150`: Resolution (DPI)
- `-jpeg`: JPEG format (or `-png`)
- `-f N`: First page
- `-l N`: Last page
- `page`: Output prefix

Example for range:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # Pages 2-5
```

## Code Style

**IMPORTANT**:
- Write concise code
- Avoid verbose variable names
- Avoid unnecessary print statements
- Avoid redundant operations

## Dependencies

- **pandoc**: `sudo apt-get install pandoc` (text extraction)
- **docx**: `npm install -g docx` (creating new documents)
- **LibreOffice**: `sudo apt-get install libreoffice` (PDF conversion)
- **Poppler**: `sudo apt-get install poppler-utils` (pdftoppm)
- **defusedxml**: `pip install defusedxml` (secure XML parsing)
"""
