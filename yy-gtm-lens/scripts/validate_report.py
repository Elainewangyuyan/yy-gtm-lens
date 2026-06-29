#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_PUBLIC = ["01", "02", "03", "04", "05", "06", "07", "08", "10"]
ALLOWED_BLOCKS = {"paragraph", "heading", "list", "table", "quote"}
ALLOWED_VISUALS = {
    "timeline", "matrix", "layers", "funnel", "bars", "capital",
    "orbit", "balance", "org", "roadmap", "gates"
}
ALLOWED_THEMES = {"blue", "mint", "violet", "peach", "gold"}
HIGH_RISK_TERMS = re.compile(
    r"(收入|ARR|MAU|DAU|留存|毛利|付费用户|估值|融资|股权|持股|客户|"
    r"参数|训练|Token|benchmark|评测|人数|汇报线|负责人|薪酬)",
    re.I,
)


def chinese_count(text):
    return len(re.findall(r"[\u3400-\u9fff]", text))


def flatten_blocks(blocks):
    text = []
    for block in blocks:
        text.append(str(block.get("text", "")))
        text.extend(map(str, block.get("items", [])))
        text.extend(map(str, block.get("headers", [])))
        for row in block.get("rows", []):
            text.extend(map(str, row))
    return "\n".join(text)


def citation_ids(text):
    ids = set()
    for match in re.finditer(
        r"(?:来源|媒体披露|公司披露|独立评测)\s*([0-9、,，\-\–—~～至\s]+)", text
    ):
        token = match.group(1)
        numbers = [int(x) for x in re.findall(r"\d+", token)]
        if len(numbers) == 2 and re.search(r"[-–—~～至]", token):
            start, end = numbers
            if 0 < end - start <= 50:
                ids.update(map(str, range(start, end + 1)))
                continue
        ids.update(map(str, numbers))
    return ids


def valid_date(value):
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--allow-short", action="store_true")
    parser.add_argument("--allow-pending-qa", action="store_true")
    args = parser.parse_args()
    path = Path(args.input)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors, warnings = [], []

    required_top = [
        "meta", "sections", "private_section", "sources",
        "owner_views", "comments", "quality_review"
    ]
    for key in required_top:
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    meta = data.get("meta", {})
    for key in [
        "company", "legal_or_business_name", "subtitle", "research_date",
        "language", "audience", "output_slug"
    ]:
        if not meta.get(key):
            errors.append(f"Missing meta.{key}")
    if meta.get("research_date") and not valid_date(meta["research_date"]):
        errors.append("meta.research_date must use YYYY-MM-DD")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta.get("output_slug", "")):
        errors.append("meta.output_slug must be lowercase hyphen-case")

    ordered_numbers = [s.get("number") for s in data.get("sections", [])]
    if ordered_numbers != REQUIRED_PUBLIC:
        errors.append(f"Public section order must be: {', '.join(REQUIRED_PUBLIC)}")
    sections = {s.get("number"): s for s in data.get("sections", [])}
    source_ids = {str(s.get("id")) for s in data.get("sources", [])}
    public_text = []

    for number in REQUIRED_PUBLIC:
        section = sections.get(number, {})
        for key in ["title", "judgment", "tags", "signals", "visual", "blocks"]:
            if not section.get(key):
                errors.append(f"Section {number} missing {key}")
        if len(section.get("tags", [])) != 3:
            errors.append(f"Section {number} must have exactly three judgment tags")
        if len(section.get("signals", [])) != 3:
            errors.append(f"Section {number} must have exactly three signal cards")
        visual_type = section.get("visual", {}).get("type")
        if visual_type not in ALLOWED_VISUALS:
            errors.append(f"Section {number} has unsupported visual type: {visual_type}")
        if section.get("theme") and section["theme"] not in ALLOWED_THEMES:
            errors.append(f"Section {number} has unsupported theme: {section['theme']}")
        blocks = section.get("blocks", [])
        for block in blocks:
            block_type = block.get("type")
            if block_type not in ALLOWED_BLOCKS:
                errors.append(f"Section {number} unsupported block: {block_type}")
            if block_type == "table":
                width = len(block.get("headers", []))
                if not width or any(len(row) != width for row in block.get("rows", [])):
                    errors.append(f"Section {number} table rows must match header width")
        section_text = section.get("judgment", "") + "\n" + flatten_blocks(blocks)
        public_text.append(section_text)
        if HIGH_RISK_TERMS.search(section_text) and not citation_ids(section_text):
            warnings.append(
                f"Section {number} discusses high-risk facts but no source ID was detected"
            )

    joined_public = "\n".join(public_text)
    count = chinese_count(joined_public)
    if not args.allow_short and not 5000 <= count <= 8000:
        errors.append(
            f"Public report Chinese character count is {count}; expected 5000–8000"
        )

    citations = citation_ids(joined_public)
    missing = sorted(citations - source_ids, key=lambda x: int(x))
    if missing:
        errors.append(f"Citations missing from sources: {', '.join(missing)}")

    private = data.get("private_section", {})
    if private.get("number") != "09":
        errors.append("private_section.number must be 09")
    if len(private.get("tags", [])) != 3:
        errors.append("Private section 09 must have exactly three judgment tags")
    if len(private.get("signals", [])) != 3:
        errors.append("Private section 09 must have exactly three signal cards")

    seen_source_ids = set()
    for source in data.get("sources", []):
        sid = str(source.get("id"))
        if sid in seen_source_ids:
            errors.append(f"Duplicate source ID: {sid}")
        seen_source_ids.add(sid)
        url = source.get("url", "")
        if not url or urlparse(url).scheme not in {"http", "https"}:
            errors.append(f"Source {sid} has an invalid URL")
        if not source.get("title"):
            errors.append(f"Source {sid} missing title")
        if source.get("published_date") and not valid_date(source["published_date"]):
            warnings.append(f"Source {sid} published_date is not YYYY-MM-DD")
        if source.get("accessed_date") and not valid_date(source["accessed_date"]):
            errors.append(f"Source {sid} accessed_date must use YYYY-MM-DD")
        if source.get("source_type") in {"primary", "dynamic"} and not source.get("accessed_date"):
            warnings.append(f"Source {sid} should include accessed_date")

    quality = data.get("quality_review", {})
    status = quality.get("status", "pending")
    if status not in {"pending", "pass", "revise"}:
        errors.append("quality_review.status must be pending, pass, or revise")
    if not args.allow_pending_qa and status != "pass":
        errors.append("quality_review.status must be pass before final rendering")
    if quality.get("p0"):
        errors.append("quality_review still contains P0 findings")
    if quality.get("p1"):
        errors.append("quality_review still contains P1 findings")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)
    print(
        f"OK: {meta.get('company')} validated; {count} Chinese characters; "
        f"{len(source_ids)} sources; QA={status}"
    )


if __name__ == "__main__":
    main()
