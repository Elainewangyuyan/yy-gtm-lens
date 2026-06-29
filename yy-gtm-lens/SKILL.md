---
name: yy-gtm-lens
description: YY-branded GTM lens for researching, fact-checking, evaluating, designing, and publishing Chinese deep dives on any AI-native company or AI business unit. Use when Codex needs a 5,000–8,000-character evidence-led report covering company history, market competition, products, business model, users, revenue and growth signals, funding and valuation, models, data, evaluations, open-source strategy, founders, organization, hiring, GTM challenges, low-cost growth advice, risks, and a private career/reach-out assessment; or when it needs synchronized Markdown, a visual website, browser-printable and programmatic PDFs, independent research QA, visual QA, public/private separation, and a GitHub-safe publish bundle for YY GTM Lens.
---

# YY GTM Lens

Build every deliverable from one structured JSON source. Use the current date as the research cutoff unless the user specifies another date.

## Default outcome

Given only a company name, produce:

- Chinese public report, 5,000–8,000 Chinese characters excluding sources.
- Public sections 01–08 and 10.
- Physically separated private section 09.
- Research QA memo and revised final text.
- Responsive public website with owner-view input and optional comments.
- Browser-printable PDF plus programmatic public/private PDFs.
- Visual QA evidence and a GitHub-safe `publish/` directory.

Ask only when a missing choice materially changes the work. Otherwise state assumptions and proceed.

## Workflow

### 1. Initialize

Run:

```bash
python3 scripts/init_report.py "<company>" --output "<workspace>"
```

Treat `<workspace>/company-research.json` as the single source of truth. Do not maintain separate wording in Markdown, HTML, and PDF.

Read:

- [references/report-schema.md](references/report-schema.md) before editing JSON.
- [references/research-method.md](references/research-method.md) before browsing.
- [references/workflow.md](references/workflow.md) for role handoffs and approval-first behavior.

### 2. Research

Browse current sources. Prefer official product, pricing, API, model, repository, careers, regulatory and investor materials. Use reputable media or independent analytics only with explicit labels.

For each section:

- Lead with a 1–2 line judgment.
- Add exactly 3 judgment tags and 3 signal cards.
- Include dates and scope for every meaningful metric.
- Label evidence as fact, company-reported, media disclosure, independent evaluation, inference, or unknown.
- Cite high-risk claims with source IDs.
- State unknowns instead of guessing.

Keep section 09 out of all public artifacts.

### 3. Research QA

Have an independent reviewer audit the draft when subagents are available. Do not reveal the desired conclusion. The reviewer checks freshness, source traceability, numerical scope, missing dimensions, overclaiming, GTM usefulness and privacy.

Apply [references/quality-gate.md](references/quality-gate.md). The QA revision governs the final text.

If the user wants text approval first, stop after delivering the reviewed public/private Markdown and QA memo. Render visuals only after approval.

### 4. Validate and render

Run:

```bash
python3 scripts/validate_report.py "<workspace>/company-research.json"
python3 scripts/render_report.py "<workspace>/company-research.json" --output "<workspace>/output"
python3 scripts/check_output.py "<workspace>/output"
```

Expected output:

```text
output/
├── research/
│   ├── public.md
│   ├── private-09.md
│   └── quality-review.md
├── public-site/
├── private-notes/
├── exports/
│   ├── <slug>-public.pdf
│   └── <slug>-private-09.pdf
├── publish/
└── qa/
```

Only deploy `publish/`.

### 5. Design and visual QA

Read:

- [references/visual-system.md](references/visual-system.md) before rendering or changing layout.
- [references/visual-qa.md](references/visual-qa.md) before release.
- [references/privacy-publishing.md](references/privacy-publishing.md) before building `publish/`.

Validate these surfaces separately:

1. Desktop web.
2. Mobile web.
3. The actual browser “Export PDF” path.
4. Programmatic public PDF.
5. Private PDF.

Never use one PDF path as evidence that another path is correct. Generate page screenshots and a contact sheet. Require zero title/card overlap, zero clipping, zero vertical overflow and zero private-content leakage before release.

## Update an existing report

Update the JSON source, rerun validation, rendering and output checks, then repeat research and visual QA. Do not hand-edit generated Markdown, HTML, PDFs or `publish/` unless repairing the generator itself.
