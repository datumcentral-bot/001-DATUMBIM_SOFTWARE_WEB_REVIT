#!/usr/bin/env python3
"""Resource Discovery and Indexing for DATUMBIM — TASK 000.

Scans accessible drives (F:\\, Z:\\) and catalogs resources for reuse.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

DRIVES = ["F:\\", "Z:\\"]
MAX_DEPTH = 3

EXTENSIONS = {
    "sdk": [".sdk", ".exe", ".msi", ".dll", ".addin", ".bundle"],
    "addons": [".addin", ".dll", ".py", ".rb", ".dynamo"],
    "readers": [".py", ".rb", ".cs", ".dll"],
    "writers": [".py", ".rb", ".cs", ".dll"],
    "converters": [".py", ".rb", ".exe", ".dll"],
    "parsers": [".py", ".rb", ".cs", ".dll"],
    "samples": [".rvt", ".rfa", ".ifc", ".nwd", ".nwc", ".dwg", ".dxf", ".pdf", ".xlsx", ".csv", ".obj", ".fbx", ".gltf", ".glb", ".step", ".stl", ".png", ".jpg", ".svg"],
    "images": [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".svg", ".webp"],
    "fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "documentation": [".pdf", ".docx", ".doc", ".txt", ".md", ".rst", ".chm", ".html"],
}

FORMAT_SOFTWARE = {
    ".rvt": "Revit",
    ".rfa": "Revit",
    ".dwg": "AutoCAD",
    ".dxf": "AutoCAD",
    ".ifc": "IFC",
    ".nwd": "Navisworks",
    ".nwc": "Navisworks",
    ".pdf": "Adobe Acrobat",
    ".xlsx": "Microsoft Excel",
    ".csv": "Generic CSV",
    ".obj": "Wavefront",
    ".fbx": "Autodesk FBX",
    ".gltf": "glTF",
    ".glb": "glTF",
    ".step": "STEP",
    ".stl": "STL",
    ".png": "Image",
    ".jpg": "Image",
    ".svg": "SVG",
}

def classify_resource(path: str) -> dict:
    p = Path(path)
    ext = p.suffix.lower()
    category = "other"
    for cat, exts in EXTENSIONS.items():
        if ext in exts:
            category = cat
            break
    software = FORMAT_SOFTWARE.get(ext, "Unknown")
    return {
        "category": category,
        "software": software,
        "extension": ext,
        "filename": p.name,
        "path": str(p),
    }

def scan_drive(drive: str) -> list:
    resources = []
    if not os.path.exists(drive):
        return resources
    for root, dirs, files in os.walk(drive):
        depth = root.replace(drive, "").count(os.sep)
        if depth >= MAX_DEPTH:
            dirs.clear()
            continue
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                stat = os.stat(fpath)
                info = classify_resource(fpath)
                info.update({
                    "size": stat.st_size,
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "drive": drive,
                })
                resources.append(info)
            except Exception:
                continue
    return resources

def build_indexes(resources: list) -> dict:
    drive_index = defaultdict(list)
    sdk_index = defaultdict(list)
    format_index = defaultdict(list)
    image_index = defaultdict(list)
    document_index = defaultdict(list)
    resource_index = []

    for r in resources:
        drive_index[r.get("drive", "unknown")].append(r)
        resource_index.append(r)
        if r["category"] == "sdk" or r["software"] in ("Revit", "AutoCAD", "Navisworks", "Dynamo", "IFC"):
            sdk_index[r["software"]].append(r)
        if r["extension"] in FORMAT_SOFTWARE:
            format_index[r["extension"]].append(r)
        if r["category"] == "images":
            image_index[r["extension"]].append(r)
        if r["category"] == "documentation":
            document_index[r["extension"]].append(r)

    return {
        "resource_index": resource_index,
        "drive_index": dict(drive_index),
        "sdk_index": dict(sdk_index),
        "format_index": dict(format_index),
        "image_index": dict(image_index),
        "document_index": dict(document_index),
    }

def main():
    print("DATUMBIM Resource Discovery — TASK 000")
    all_resources = []
    for drive in DRIVES:
        if os.path.exists(drive):
            print(f"Scanning {drive} (max depth {MAX_DEPTH}) ...")
            resources = scan_drive(drive)
            print(f"  Found {len(resources)} resources")
            all_resources.extend(resources)
        else:
            print(f"Drive {drive} not accessible — BLOCKED")

    indexes = build_indexes(all_resources)
    output_dir = Path(__file__).resolve().parents[1] / "resources" / "external-index"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, data in indexes.items():
        json_path = output_dir / f"{name.upper()}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Wrote {json_path}")

    md_lines = ["# DATUMBIM Resource Index", "", f"Generated: {datetime.now().isoformat()}", ""]
    md_lines.append(f"Total resources discovered: {len(all_resources)}")
    md_lines.append("")
    for drive, items in indexes["drive_index"].items():
        md_lines.append(f"## {drive}")
        md_lines.append(f"Items: {len(items)}")
        md_lines.append("")
    with open(output_dir / "RESOURCE_INDEX.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("Wrote RESOURCE_INDEX.md")
    print("Resource discovery complete.")

if __name__ == "__main__":
    main()
