#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def text_fragments(value):
    text = json.dumps(value, ensure_ascii=False)
    candidates = re.findall(r"[\u3400-\u9fffA-Za-z0-9][^\"\\n]{10,60}", text)
    return [x.strip(" ,，。；;:：") for x in candidates if len(x.strip()) >= 10]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--source-json")
    args = parser.parse_args()
    root = Path(args.output)
    errors, warnings = [], []

    required = [
        "research/public.md",
        "research/private-09.md",
        "research/quality-review.md",
        "public-site/index.html",
        "public-site/styles.css",
        "public-site/print.css",
        "public-site/app.js",
        "private-notes/index.html",
        "publish/index.html",
        "qa/visual-qa.md",
        "qa/visual-tokens.json",
    ]
    for rel in required:
        if not (root / rel).is_file():
            errors.append(f"Missing output: {rel}")

    pdfs = list((root / "exports").glob("*.pdf"))
    if len(pdfs) != 2:
        warnings.append(f"Expected two PDFs; found {len(pdfs)}")
    for pdf in pdfs:
        if pdf.stat().st_size < 1000 or not pdf.read_bytes().startswith(b"%PDF"):
            errors.append(f"Invalid PDF: {pdf.name}")

    publish_files = [p for p in (root / "publish").rglob("*") if p.is_file()]
    public_blob = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in publish_files
        if p.suffix.lower() in {".html", ".js", ".css", ".json", ".md", ".txt"}
    )
    forbidden_paths = [
        "private-notes", "private-09.pdf", "private-09.md", "PRIVATE DECISION MEMO"
    ]
    for phrase in forbidden_paths:
        if phrase in public_blob:
            errors.append(f"Public bundle contains private marker: {phrase}")

    if args.source_json:
        data = json.loads(Path(args.source_json).read_text(encoding="utf-8"))
        public_source_text = json.dumps({
            "meta": data.get("meta", {}),
            "sections": data.get("sections", []),
            "sources": data.get("sources", []),
            "owner_views": data.get("owner_views", []),
        }, ensure_ascii=False)
        for fragment in text_fragments(data.get("private_section", {})):
            if fragment in public_source_text:
                continue
            if fragment in public_blob:
                errors.append(f"Public bundle leaked private text: {fragment[:40]}")
                break

    public_md = (root / "research" / "public.md")
    web = root / "public-site" / "index.html"
    if public_md.exists() and web.exists():
        headings = re.findall(r"^## (\d{2}) (.+)$", public_md.read_text(encoding="utf-8"), re.M)
        web_text = web.read_text(encoding="utf-8")
        for number, title in headings:
            if number == "09":
                errors.append("Public Markdown contains section 09")
            if title not in web_text:
                errors.append(f"Web output missing public heading: {number} {title}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)
    print(f"OK: output structure and public/private separation passed at {root}")


if __name__ == "__main__":
    main()
