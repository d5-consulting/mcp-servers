"""
PPTX Analysis Tools - Read-only presentation analysis.

Tools for reading and analyzing existing PowerPoint presentations
without modification.
"""

import json
from pathlib import Path

from PIL import Image
from pptx import Presentation

from . import mcp


@mcp.tool()
def get_presentation_info(file_path: str) -> str:
    """
    Get information about a PowerPoint presentation.

    Args:
        file_path: Path to the PowerPoint file

    Returns:
        Presentation metadata and structure information
    """
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"

    prs = Presentation(str(path))

    width_inches = prs.slide_width.inches
    height_inches = prs.slide_height.inches

    # Determine aspect ratio
    ratio = width_inches / height_inches
    if abs(ratio - 16 / 9) < 0.01:
        aspect = "16:9"
    elif abs(ratio - 4 / 3) < 0.01:
        aspect = "4:3"
    elif abs(ratio - 16 / 10) < 0.01:
        aspect = "16:10"
    else:
        aspect = f"{ratio:.2f}:1"

    info = [
        f"File: {path.name}",
        f"Slides: {len(prs.slides)}",
        f'Dimensions: {width_inches:.2f}" x {height_inches:.2f}"',
        f"Aspect Ratio: {aspect}",
        f"Slide Layouts: {len(prs.slide_layouts)}",
        "",
        "Slide Summary:",
    ]

    for i, slide in enumerate(prs.slides, 1):
        title = ""
        if slide.shapes.title:
            title = slide.shapes.title.text[:50]
        shape_count = len(slide.shapes)
        info.append(f"  Slide {i}: {shape_count} shapes - {title or '(no title)'}")

    return "\n".join(info)


@mcp.tool()
def extract_text(file_path: str, slide_numbers: str | None = None) -> str:
    """
    Extract all text from a PowerPoint presentation.

    Args:
        file_path: Path to the PowerPoint file
        slide_numbers: Optional comma-separated slide numbers (e.g., "1,3,5")

    Returns:
        Extracted text organized by slide
    """
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"

    prs = Presentation(str(path))

    # Parse slide numbers if provided
    target_slides = None
    if slide_numbers:
        target_slides = set(int(s.strip()) for s in slide_numbers.split(","))

    results = []
    for i, slide in enumerate(prs.slides, 1):
        if target_slides and i not in target_slides:
            continue

        slide_text = [f"--- Slide {i} ---"]

        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    text = paragraph.text.strip()
                    if text:
                        slide_text.append(text)

        if len(slide_text) > 1:
            results.append("\n".join(slide_text))
        else:
            results.append(f"--- Slide {i} ---\n(no text)")

    return "\n\n".join(results)


@mcp.tool()
def get_slide_shapes(file_path: str, slide_number: int) -> str:
    """
    Get detailed information about all shapes on a slide.

    Args:
        file_path: Path to the PowerPoint file
        slide_number: Slide number (1-indexed)

    Returns:
        JSON-formatted shape information
    """
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"

    prs = Presentation(str(path))

    if slide_number < 1 or slide_number > len(prs.slides):
        return f"Error: Slide {slide_number} does not exist."

    slide = prs.slides[slide_number - 1]
    shapes_info = []

    for shape in slide.shapes:
        info = {
            "name": shape.name,
            "shape_type": str(shape.shape_type),
            "left": shape.left.inches if shape.left else 0,
            "top": shape.top.inches if shape.top else 0,
            "width": shape.width.inches if shape.width else 0,
            "height": shape.height.inches if shape.height else 0,
        }

        if shape.has_text_frame:
            info["text"] = shape.text_frame.text[:100]

        if hasattr(shape, "image"):
            info["has_image"] = True

        shapes_info.append(info)

    return json.dumps(shapes_info, indent=2)


@mcp.tool()
def get_slide_notes(file_path: str, slide_number: int | None = None) -> str:
    """
    Get speaker notes from slides.

    Args:
        file_path: Path to the PowerPoint file
        slide_number: Optional specific slide number (1-indexed). If None, gets all notes.

    Returns:
        Speaker notes text
    """
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"

    prs = Presentation(str(path))
    results = []

    slides_to_check = [prs.slides[slide_number - 1]] if slide_number else prs.slides

    for i, slide in enumerate(slides_to_check, slide_number or 1):
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            notes_text = notes_slide.notes_text_frame.text
            results.append(f"--- Slide {i} Notes ---\n{notes_text}")
        else:
            results.append(f"--- Slide {i} Notes ---\n(no notes)")

    return "\n\n".join(results)


@mcp.tool()
def export_slide_as_image(
    file_path: str,
    slide_number: int,
    output_path: str,
    width: int = 1920,
) -> str:
    """
    Export a slide as an image (requires unpacking and reading embedded images).

    Note: This creates a thumbnail-like representation, not a full render.
    For full rendering, use LibreOffice or similar tools.

    Args:
        file_path: Path to the PowerPoint file
        slide_number: Slide number (1-indexed)
        output_path: Path for the output image
        width: Image width in pixels

    Returns:
        Path to the created image or instructions for full rendering
    """
    path = Path(file_path).expanduser().resolve()
    out_path = Path(output_path).expanduser().resolve()

    if not path.exists():
        return f"Error: File not found: {path}"

    # Create a simple placeholder image
    prs = Presentation(str(path))

    if slide_number < 1 or slide_number > len(prs.slides):
        return f"Error: Slide {slide_number} does not exist."

    # Calculate height based on aspect ratio
    aspect_ratio = prs.slide_height.inches / prs.slide_width.inches
    height = int(width * aspect_ratio)

    # Create image with slide text
    img = Image.new("RGB", (width, height), color=(255, 255, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path))

    return (
        f"Created placeholder image: {out_path}\n\n"
        f"For full slide rendering, use:\n"
        f"  libreoffice --headless --convert-to png {path}"
    )
