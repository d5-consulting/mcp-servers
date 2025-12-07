from . import mcp


@mcp.prompt()
def pptx_workflow_overview() -> str:
    """Decision tree for PPTX workflows - choosing the right approach."""
    return """# PPTX Workflow Overview

## Choosing Your Workflow

### Reading and Analyzing Content
- **Text extraction**: `markitdown path-to-file.pptx` - Convert to markdown
- **Raw XML access**: Unpack with `python ooxml/scripts/unpack.py` for comments, speaker notes, layouts, animations

### Creating New Presentation WITHOUT Template
→ Use **html2pptx** workflow
- Create HTML slides with proper dimensions (720pt × 405pt for 16:9)
- Convert to PowerPoint with accurate positioning
- Add charts/tables via PptxGenJS API
- See `pptx_html2pptx()` prompt for details

### Creating New Presentation WITH Template
→ Use **template workflow**
- Extract template text and create visual thumbnails
- Analyze template inventory
- Duplicate, reorder, delete slides
- Replace placeholder text
- See `pptx_template_workflow()` prompt for details

### Editing Existing Presentation
→ Use **OOXML editing** workflow
- Unpack presentation to XML
- Edit XML files (primarily slide{N}.xml)
- Validate immediately after each edit
- Pack final presentation
- See `pptx_ooxml_editing()` prompt for details

## Key File Structures (Unpacked PPTX)
- `ppt/presentation.xml` - Main presentation metadata
- `ppt/slides/slide{N}.xml` - Individual slide contents
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes
- `ppt/comments/modernComment_*.xml` - Comments
- `ppt/slideLayouts/` - Layout templates
- `ppt/slideMasters/` - Master slide templates
- `ppt/theme/` - Theme and styling
- `ppt/media/` - Images and media
"""


@mcp.prompt()
def pptx_html2pptx() -> str:
    """HTML to PowerPoint creation workflow and design principles."""
    return """# Creating PowerPoint with html2pptx

## Design Principles (CRITICAL)

**Before creating any presentation**, analyze the content and choose design elements:

1. **Consider the subject matter**: What tone, industry, or mood does it suggest?
2. **Check for branding**: Consider company/organization brand colors
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, visual language

## Color Palette Selection

**Think beyond defaults**:
- Topic, industry, mood, energy level, target audience
- Be adventurous - healthcare doesn't have to be green, finance doesn't have to be navy
- Pick 3-5 colors that work together
- Ensure contrast for readability

**Example palettes** (for inspiration):
1. Classic Blue: #1C2833, #2E4053, #AAB7B8, #F4F6F6
2. Teal & Coral: #5EA8A7, #277884, #FE4447, #FFFFFF
3. Bold Red: #C0392B, #E74C3C, #F39C12, #F1C40F, #2ECC71
4. Burgundy Luxury: #5D1D2E, #951233, #C15937, #997929
5. Deep Purple & Emerald: #B165FB, #181B24, #40695B, #FFFFFF
6. Sage & Terracotta: #87A96B, #E07A5F, #F4F1DE, #2C2C2C

## Layout Tips

**For slides with charts or tables**:
- **Two-column layout (PREFERRED)**: Header spanning full width, then columns (40%/60% split)
- **Full-slide layout**: Let content take up entire slide for maximum impact
- **NEVER vertically stack**: Don't place charts/tables below text in single column

## Workflow

1. **MANDATORY**: Read `html2pptx.md` completely (no range limits) for syntax and formatting rules
2. Create HTML file for each slide (720pt × 405pt for 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for text
   - Use `class="placeholder"` for chart/table areas
   - **CRITICAL**: Rasterize gradients/icons as PNG using Sharp first
3. Create JavaScript file using `html2pptx.js` library
   - Use `html2pptx()` function
   - Add charts/tables to placeholders via PptxGenJS API
   - Save with `pptx.writeFile()`
4. **Visual validation**: Generate thumbnails and inspect
   - `python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - Check for: text cutoff, overlap, positioning, contrast issues
   - Adjust HTML and regenerate until correct

## Visual Details Options

**Typography**: Extreme size contrast, all-caps headers, monospace for data
**Geometric**: Diagonal dividers, asymmetric columns, rotated text
**Borders**: Thick single-color, L-shaped, corner brackets
**Backgrounds**: Solid color blocks, split backgrounds, edge-to-edge bands
**Charts**: Monochrome with accent color, horizontal bars, minimal gridlines
"""


@mcp.prompt()
def pptx_ooxml_editing() -> str:
    """OOXML-based editing workflow for existing presentations."""
    return """# Editing Existing PowerPoint (OOXML)

## Workflow

1. **MANDATORY**: Read `ooxml.md` completely (~500 lines, no range limits)
   - Detailed guidance on OOXML structure and editing
2. **Unpack**: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. **Edit XML**: Primarily `ppt/slides/slide{N}.xml` and related files
4. **CRITICAL - Validate**: After EACH edit, validate before proceeding
   - `python ooxml/scripts/validate.py <dir> --original <file>`
   - Fix any validation errors immediately
5. **Pack**: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Key XML Files

**Slides**: `ppt/slides/slide1.xml`, `slide2.xml`, etc.
**Notes**: `ppt/notesSlides/notesSlide1.xml`, etc.
**Comments**: `ppt/comments/modernComment_*.xml`
**Layouts**: `ppt/slideLayouts/` - Layout templates
**Masters**: `ppt/slideMasters/` - Master slide templates
**Theme**: `ppt/theme/theme1.xml` - Colors and fonts

## Typography and Color Extraction

**When emulating a design**:
1. Read theme: `ppt/theme/theme1.xml` for `<a:clrScheme>` and `<a:fontScheme>`
2. Sample slide: `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`)
3. Search patterns: Use grep for color (`<a:solidFill>`, `<a:srgbClr>`) and fonts

## Converting to Images

**Two-step process**:
1. Convert to PDF: `soffice --headless --convert-to pdf template.pptx`
2. Convert PDF to JPEG: `pdftoppm -jpeg -r 150 template.pdf slide`
   - Creates `slide-1.jpg`, `slide-2.jpg`, etc.
   - Options: `-f N` (first page), `-l N` (last page), `-r 150` (resolution)
"""


@mcp.prompt()
def pptx_template_workflow() -> str:
    """Using existing templates to create new presentations."""
    return """# Creating PowerPoint Using Templates

## Workflow

### 1. Extract Template Text and Create Thumbnails
```bash
# Extract text
python -m markitdown template.pptx > template-content.md

# Create thumbnail grids (for visual analysis)
python scripts/thumbnail.py template.pptx
```

Read `template-content.md` completely (no range limits)

### 2. Analyze Template and Save Inventory

**Visual Analysis**: Review thumbnail grids for layouts, design patterns, structure

Create `template-inventory.md`:
```markdown
# Template Inventory Analysis
**Total Slides: [count]**
**IMPORTANT: Slides are 0-indexed (first slide = 0, last = count-1)**

## [Category Name]
- Slide 0: [Layout code] - Description/purpose
- Slide 1: [Layout code] - Description/purpose
[... EVERY slide listed individually ...]
```

**Using thumbnails**: Identify layout patterns, image placeholders, design consistency

### 3. Create Presentation Outline

**CRITICAL - Match Layout to Content**:
- Single-column: Unified narrative or single topic
- Two-column: ONLY for exactly 2 distinct items
- Three-column: ONLY for exactly 3 distinct items
- Image + text: ONLY when you have actual images
- Quote layouts: ONLY for actual quotes with attribution
- Count content pieces BEFORE selecting layout
- Don't force content into mismatched layouts

Save `outline.md` with template mapping:
```python
# Template slides to use (0-based indexing)
# WARNING: Verify indices within range! 73 slides = indices 0-72
template_mapping = [
    0,   # Title/Cover
    34,  # Title and body
    34,  # Duplicate for second slide
    50,  # Quote
    54,  # Closing + Text
]
```

### 4. Rearrange Slides
```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
```

### 5. Extract ALL Text Inventory
```bash
python scripts/inventory.py working.pptx text-inventory.json
```

Read `text-inventory.json` completely (no range limits)

**Inventory structure**:
- Slides: "slide-0", "slide-1", etc.
- Shapes: Ordered visually as "shape-0", "shape-1"
- Placeholder types: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
- Properties: Only non-default values included

### 6. Generate Replacement Text

**CRITICAL**:
- First verify which shapes exist in inventory
- Validation shows errors for non-existent shapes/slides
- ALL shapes cleared unless you provide "paragraphs"
- Don't include "paragraphs" for shapes you want to clear
- When `bullet: true`, DON'T include bullet symbols in text
- Include paragraph properties from original inventory

**Essential formatting**:
- Headers/titles: `"bold": true`
- List items: `"bullet": true, "level": 0`
- Preserve alignment: `"alignment": "CENTER"`
- Colors: `"color": "FF0000"` or `"theme_color": "DARK_1"`

Example paragraphs:
```json
"paragraphs": [
  {
    "text": "New title",
    "alignment": "CENTER",
    "bold": true
  },
  {
    "text": "Bullet point without symbol",
    "bullet": true,
    "level": 0
  }
]
```

Save to `replacement-text.json`

### 7. Apply Replacements
```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```

Validates shapes exist and applies formatting automatically

## Creating Thumbnail Grids

```bash
# Basic usage
python scripts/thumbnail.py template.pptx

# Custom options
python scripts/thumbnail.py template.pptx workspace/analysis --cols 4
```

**Features**:
- Default: 5 columns, max 30 slides per grid
- Range: 3-6 columns
- Zero-indexed slide labels
"""


@mcp.prompt()
def pptx_design_principles() -> str:
    """Design principles and visual details for presentations."""
    return """# PPTX Design Principles

## Core Design Requirements

1. **Content-First Design**
   - Analyze subject matter before choosing design
   - Consider: tone, industry, mood, target audience
   - Match palette to content (don't use autopilot choices)
   - State design approach BEFORE coding

2. **Typography**
   - Web-safe fonts ONLY: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
   - Clear visual hierarchy via size, weight, color
   - Strong contrast for readability
   - Consistent patterns across slides

3. **Color Strategy**
   - Think beyond defaults
   - Be adventurous with combinations
   - Pick 3-5 colors that work together
   - Ensure text/background contrast

## Visual Details Library

### Typography Treatments
- Extreme size contrast (72pt headlines vs 11pt body)
- All-caps headers with wide letter spacing
- Numbered sections in oversized display type
- Monospace (Courier New) for data/stats
- Outlined text for emphasis

### Geometric Patterns
- Diagonal section dividers
- Asymmetric column widths (30/70, 40/60, 25/75)
- Rotated text headers (90° or 270°)
- Circular/hexagonal frames for images
- Triangular accent shapes in corners
- Overlapping shapes for depth

### Border & Frame Treatments
- Thick single-color borders (10-20pt) on one side
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)
- Underline accents beneath headers (3-5pt thick)

### Chart & Data Styling
- Monochrome charts with single accent color for key data
- Horizontal bar charts instead of vertical
- Dot plots instead of bar charts
- Minimal gridlines or none
- Data labels directly on elements (no legends)
- Oversized numbers for key metrics

### Layout Innovations
- Full-bleed images with text overlays
- Sidebar column (20-30% width) for navigation/context
- Modular grid systems (3×3, 4×4 blocks)
- Z-pattern or F-pattern content flow
- Floating text boxes over colored shapes
- Magazine-style multi-column layouts

### Background Treatments
- Solid color blocks occupying 40-60% of slide
- Gradient fills (vertical or diagonal only)
- Split backgrounds (two colors, diagonal or vertical)
- Edge-to-edge color bands
- Negative space as design element

## Layout Best Practices

**Charts/Tables**:
- Two-column preferred: header + content side-by-side
- Full-slide for maximum impact
- Never vertical stack (chart below text)

**Content Matching**:
- Match layout structure to actual content count
- Don't force 2 items into 3-column layout
- Use appropriate placeholders for your content type
"""
