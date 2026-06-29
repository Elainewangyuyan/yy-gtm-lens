#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SECTION_DATA = [
    ("01", "总览与前世今生", "timeline"),
    ("02", "赛道与竞争", "matrix"),
    ("03", "产品与商业模式", "layers"),
    ("04", "用户、收入与增长信号", "bars"),
    ("05", "资本与估值", "capital"),
    ("06", "模型、数据、评测与开源", "orbit"),
    ("07", "团队、组织与招聘", "org"),
    ("08", "GTM 难题与低成本增长建议", "roadmap"),
    ("10", "催化剂、风险与持续观察", "balance"),
]


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True)


def main():
    skill = Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory(prefix="ai-company-skill-") as temp:
        workspace = Path(temp) / "kimi"
        run(skill / "scripts" / "init_report.py", "Kimi / 月之暗面", "--output", workspace)
        source = workspace / "company-research.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["meta"]["output_slug"] = "kimi"
        data["meta"]["subtitle"] = "从长文本助手到 Agent 平台"
        data["quality_review"].update({
            "status": "pass",
            "reviewed_date": data["meta"]["research_date"],
            "reviewer": "smoke test QA",
            "summary": "Synthetic fixture passed.",
        })
        for index, section in enumerate(data["sections"], 1):
            number, title, visual_type = SECTION_DATA[index - 1]
            section["title"] = title
            section["judgment"] = (
                "这是用于验证研究、设计、公开私密隔离与多格式渲染流程的合成样本，"
                "不代表真实商业结论。"
            )
            section["tags"] = [
                {"label": "总体判断", "value": "待持续验证"},
                {"label": "证据质量", "value": "合成测试"},
                {"label": "透明度", "value": "有限"},
            ]
            section["signals"] = [
                {"label": "SECTION", "value": number, "note": "固定研究框架"},
                {"label": "SOURCE", "value": f"{index}", "note": "测试引用"},
                {"label": "STATUS", "value": "QA PASS", "note": "仅用于冒烟测试"},
            ]
            section["visual"] = {
                "type": visual_type,
                "items": [
                    {"label": "阶段 A", "value": "研究", "note": "收集证据", "score": 78},
                    {"label": "阶段 B", "value": "质检", "note": "修订结论", "score": 66},
                    {"label": "阶段 C", "value": "设计", "note": "网页与 PDF", "score": 54},
                ],
            }
            section["blocks"] = [
                {
                    "type": "paragraph",
                    "text": (
                        f"第 {number} 部分使用统一结构验证标题、判断标签、数据卡、正文与图表。"
                        f"所有事实应在真实研究中标注日期、口径和来源，本段引用测试来源。[来源 {index}]"
                    ),
                },
                {
                    "type": "list",
                    "items": [
                        "确认网页和 PDF 文字来自同一份 JSON。",
                        "确认公开发布包不含私密第 09 部分。",
                        "确认图表标签保持横向并与正文列对齐。",
                    ],
                },
            ]
        private = data["private_section"]
        private["judgment"] = "值得联系与值得加入需要分开判断，本内容必须保持私密。"
        private["tags"] = [
            {"label": "联系判断", "value": "待验证"},
            {"label": "加入判断", "value": "待尽调"},
            {"label": "角色匹配", "value": "GTM"},
        ]
        private["signals"] = [
            {"label": "DECISION", "value": "Reach Out", "note": "仅限本人"},
            {"label": "AUTHORITY", "value": "未知", "note": "验证产品与预算权限"},
            {"label": "EQUITY", "value": "未知", "note": "验证股权与流动性"},
        ]
        private["visual"] = {
            "type": "gates",
            "items": [
                {"label": "权限", "value": "待验证", "note": "产品与预算"},
                {"label": "数据", "value": "待验证", "note": "收入与留存"},
                {"label": "上级", "value": "待验证", "note": "汇报线"},
            ],
        }
        private["blocks"] = [
            {"type": "paragraph", "text": "私密职业判断、尽调问题和角色边界只进入私密文件。"}
        ]
        data["sources"] = [
            {
                "id": index,
                "category": "测试来源",
                "title": f"Synthetic source {index}",
                "url": f"https://example.com/source-{index}",
                "source_type": "primary",
                "published_date": data["meta"]["research_date"],
                "accessed_date": data["meta"]["research_date"],
                "notes": "Synthetic fixture",
            }
            for index in range(1, 10)
        ]
        source.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        run(skill / "scripts" / "validate_report.py", source, "--allow-short")
        output = workspace / "output"
        run(skill / "scripts" / "render_report.py", source, "--output", output)
        run(skill / "scripts" / "check_output.py", output, "--source-json", source)
        print(f"SMOKE TEST OK: {output}")


if __name__ == "__main__":
    main()
