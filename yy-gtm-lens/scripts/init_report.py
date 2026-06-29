#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(value):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "ai-company"


def empty_section(number, title, visual_type):
    return {
        "number": number,
        "title": title,
        "judgment": "",
        "tags": [
            {"label": "判断", "value": "待研究"},
            {"label": "证据", "value": "待核验"},
            {"label": "透明度", "value": "待判断"}
        ],
        "signals": [
            {"label": "KEY SIGNAL", "value": "待补充", "note": "注明日期与口径"},
            {"label": "KNOWN", "value": "待补充", "note": "优先一手来源"},
            {"label": "UNKNOWN", "value": "待补充", "note": "不要猜测"}
        ],
        "visual": {"type": visual_type, "items": []},
        "blocks": []
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("company")
    parser.add_argument("--output", required=True)
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    data = {
        "meta": {
            "company": args.company,
            "legal_or_business_name": args.company,
            "subtitle": "从核心产品到可持续增长",
            "research_date": args.date,
            "language": "zh-CN",
            "audience": "AI startup founders and GTM professionals",
            "output_slug": slugify(args.company)
        },
        "sections": [
            empty_section("01", "总览与前世今生", "timeline"),
            empty_section("02", "赛道与竞争", "matrix"),
            empty_section("03", "产品与商业模式", "layers"),
            empty_section("04", "用户、收入与增长信号", "bars"),
            empty_section("05", "资本与估值", "capital"),
            empty_section("06", "模型、数据、评测与开源", "orbit"),
            empty_section("07", "团队、组织与招聘", "org"),
            empty_section("08", "GTM 难题与低成本增长建议", "roadmap"),
            empty_section("10", "催化剂、风险与持续观察", "balance")
        ],
        "private_section": empty_section("09", "是否值得 Reach Out", "gates"),
        "sources": [],
        "owner_views": [],
        "comments": {
            "provider": "giscus",
            "enabled": False,
            "repo": "",
            "repo_id": "",
            "category": "General",
            "category_id": ""
        },
        "quality_review": {
            "status": "pending",
            "reviewed_date": "",
            "reviewer": "",
            "summary": "",
            "p0": [],
            "p1": [],
            "p2": [],
            "unresolved_unknowns": []
        }
    }
    path = output / "company-research.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "research-log.md").write_text(
        f"# {args.company} research log\n\n"
        f"- Research cutoff: {args.date}\n"
        "- Record search queries, source decisions and unresolved unknowns here.\n",
        encoding="utf-8"
    )
    (output / "quality-review.md").write_text(
        f"# {args.company} quality review\n\n"
        "- Status: pending\n"
        "- P0:\n"
        "- P1:\n"
        "- P2:\n"
        "- Unresolved unknowns:\n",
        encoding="utf-8"
    )
    print(path)


if __name__ == "__main__":
    main()
