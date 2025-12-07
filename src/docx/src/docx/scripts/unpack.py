#!/usr/bin/env python3
"""Unpack and format XML contents of Office files (.docx, .pptx, .xlsx)"""

import random
import zipfile
from pathlib import Path

import defusedxml.minidom


def unpack_document(input_file, output_dir):
    """Unpack an Office file and format XML contents.

    Args:
        input_file: Path to Office file (.docx/.pptx/.xlsx)
        output_dir: Path to output directory

    Returns:
        str: Suggested RSID for .docx files, empty string otherwise
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    zipfile.ZipFile(input_file).extractall(output_path)

    xml_files = list(output_path.rglob("*.xml")) + list(output_path.rglob("*.rels"))
    for xml_file in xml_files:
        content = xml_file.read_text(encoding="utf-8")
        dom = defusedxml.minidom.parseString(content)
        xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="ascii"))

    if str(input_file).endswith(".docx"):
        suggested_rsid = "".join(random.choices("0123456789ABCDEF", k=8))
        return suggested_rsid
    return ""
