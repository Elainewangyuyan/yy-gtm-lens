# Visual QA and release gate

## Required surfaces

Validate separately:

1. Desktop web at 1440 and 1280 px.
2. Tablet at 768 px.
3. Mobile at 390 px.
4. Actual browser-exported PDF.
5. Programmatic public PDF.
6. Private PDF.

The browser-exported and programmatic PDFs are different products. Never substitute one for the other.

## Severity

### P0 — block release

- Private section 09 appears in a public artifact.
- Page or PDF cannot open/export.
- Major content is missing or public text diverges from the reviewed source.

### P1 — must fix

- Title overlaps tags, signals or body.
- Content is clipped, outside the page or hidden by overflow.
- A visual drifts to a corner or is not aligned with the content column.
- A card, bullet or single point is cut across pages.
- Chinese axis text is rotated or unreadable.
- Visual data conflicts with the text.
- Browser print differs materially from the web content.

### P2 — polish before release

- Uneven whitespace.
- Inconsistent card sizes or alignment.
- Unnatural title wrapping.
- Imbalanced visual weight across a two-page section.
- Inconsistent color, icons, footer or source styling.

Release only when P0 = 0, P1 = 0 and every P2 is fixed or explicitly accepted.

## Per-page checklist

### Header

- Correct section number and title.
- Title complete and preferably no more than two lines.
- Three tags aligned in a separate row.
- Three signal cards aligned in a separate row.
- Title/tags/signals have no overlap.
- PART 1/2 and PART 2/2 labels are consistent.

### Body

- Judgment appears first.
- Paragraph and heading spacing is comfortable.
- Lists and tables are not clipped.
- Long links wrap.
- Data, date and scope match the JSON.

### Visual

- One primary visual anchor.
- Visual answers a clear question.
- Left and right edges align with the content column.
- Labels and legends are readable.
- No footer collision.

### Whole page

- No vertical overflow.
- Footer and page number are correct.
- Sufficient bottom safe area.
- Density is balanced against adjacent pages.

## Automated geometry

Measure:

```text
title.bottom < tags.top
tags.bottom < signals.top
signals.bottom < body.top
body/visual.bottom < footer-safe-zone.top
visual.left == content-column.left
visual.right == content-column.right
```

Thresholds:

- Title → tags ≥ 3.2 mm.
- Tags → signals ≥ 4 mm.
- Signals → body ≥ 5 mm.
- Overlap = 0 px.
- Page overflow = 0 px.

Automated success does not replace visual inspection.

## QA evidence

Generate:

- One PNG per page.
- A contact sheet of all pages.
- Enlarged screenshots for the longest title, densest body, most complex visual and longest source-link page.
- A short P0/P1/P2 memo.

Verify that every artifact was generated after the latest style or renderer modification.

