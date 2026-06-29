# Report schema

## Public sections

Use these numbers and purposes consistently:

1. **01 总览与前世今生** — identity, founding, strategic shifts, current positioning.
2. **02 赛道与竞争** — segments, competitors, relative advantages, distribution constraints.
3. **03 产品与商业模式** — products, scenarios, pricing, confirmed and potential monetization.
4. **04 用户、收入与增长信号** — users, customers, revenue, growth, retention, developer signals; mark unavailable metrics.
5. **05 资本与估值** — rounds, completed versus proposed valuation, investors/shareholders, capital efficiency.
6. **06 模型、数据、评测与开源** — self-developed versus wrapper, architecture, use cases, data flywheel, evaluations, open/closed strategy.
7. **07 团队、组织与招聘** — founders, team size, workflow/stack when known, current hiring, careers link, GTM leadership and reporting line.
8. **08 GTM 难题与低成本增长建议** — prioritized problems, evidence, low/medium/high-cost labels, a 0–90 day owner/resource/metric/stop-condition plan, founder lessons, interactive owner opinions.
9. **09 私密职业判断** — reach-out value, role boundaries, internal diligence, risks, 90-day role hypothesis. Never place in public output.
10. **10 催化剂、风险与持续观察** — upside triggers, downside risks, metrics to monitor, final judgment.

## JSON top level

Required keys:

```json
{
  "meta": {},
  "sections": [],
  "private_section": {},
  "sources": [],
  "owner_views": [],
  "comments": {},
  "quality_review": {}
}
```

### `meta`

Required:

- `company`
- `legal_or_business_name`
- `subtitle`
- `research_date` in `YYYY-MM-DD`
- `language`
- `audience`
- `output_slug`

Optional:

- `sector`
- `location`
- `public_version_note`

### Section

```json
{
  "number": "01",
  "title": "总览与前世今生",
  "judgment": "1–2 line conclusion",
  "tags": [
    {"label": "总体判断", "value": "值得跟踪"}
  ],
  "signals": [
    {"label": "COMPANY STAGE", "value": "2023 → 2026", "note": "战略迁移"}
  ],
  "visual": {
    "type": "timeline",
    "items": [
      {"label": "2023", "value": "成立", "note": "起点", "score": 80}
    ]
  },
  "blocks": [
    {"type": "paragraph", "text": "... [来源 1]"},
    {"type": "heading", "text": "..."},
    {"type": "list", "items": ["...", "..."]},
    {
      "type": "table",
      "headers": ["时间", "事件", "证据"],
      "rows": [["2024", "...", "[来源 2]"]]
    }
  ]
}
```

Supported visual types:

- `timeline`
- `matrix`
- `layers`
- `funnel`
- `bars`
- `capital`
- `orbit`
- `balance`
- `org`
- `roadmap`
- `gates`

Use `page_break_before: true` on a block to split a long theme into a balanced second page.

Optional section fields:

- `theme`: `blue`, `mint`, `violet`, `peach`, or `gold`.
- `nav_label`: shorter navigation label.
- `evidence_status`: short summary such as `verified`, `mixed`, or `low-transparency`.

### Source

```json
{
  "id": 1,
  "category": "公司与产品",
  "title": "Official website",
  "url": "https://example.com",
  "source_type": "primary",
  "published_date": "2026-01-10",
  "accessed_date": "2026-06-25",
  "notes": "Dynamic pricing page"
}
```

### Owner view

```json
{
  "date": "2026-06-25",
  "title": "A personal judgment",
  "body": "...",
  "tags": ["判断", "GTM"]
}
```

### Quality review

```json
{
  "status": "pass",
  "reviewed_date": "2026-06-25",
  "reviewer": "independent QA",
  "summary": "No P0/P1 issues remain.",
  "p0": [],
  "p1": [],
  "p2": [],
  "unresolved_unknowns": [
    "Current ARR is not publicly verifiable."
  ]
}
```

## Writing rules

- Count 5,000–8,000 Chinese characters across public sections, excluding sources.
- Put the judgment before supporting detail.
- Keep language concise and conversational, not promotional.
- Avoid repeated company introductions across sections.
- Write the company’s current state, not only its founding story.
- For every meaningful metric, include its date and scope.
- Use exactly three judgment tags and three signal cards per public section.
- Store private career, compensation, manager and diligence analysis only in `private_section`.
