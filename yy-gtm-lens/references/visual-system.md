# Web and PDF visual system

## Contents

1. Design goals
2. Page structure
3. Layout and typography
4. Color and components
5. Visual mappings
6. Web/PDF consistency
7. Prohibited patterns

## 1. Design goals

Use a technology-forward, minimal, light and evidence-led style:

- Soft colors and clearly separated page regions.
- Restrained decoration and shadows.
- Strong judgment/data hierarchy.
- Generous breathing room.
- One meaningful visual anchor per page.

## 2. Page structure

Use this order:

1. Section number.
2. Title.
3. Three equal-width judgment tags.
4. Three equal-width signal cards.
5. Judgment summary.
6. Evidence and analysis.
7. One chart, diagram or color-block composition.
8. Footer and page number.

Keep title, tags and signal cards in three independent document-flow rows. Never position tags or cards beside a title whose height can change.

Split long themes at a heading or complete paragraph/list boundary. Never split a card, bullet or small point across pages.

## 3. Layout and typography

### Web

- Maximum report width: 1120 px.
- Page aspect ratio: 210/297.
- Desktop: sticky side navigation plus report.
- Mobile: single column with no horizontal overflow.
- Page radius: 24–32 px.

### PDF

- A4 portrait: 210 × 297 mm.
- Padding: top/right/left 14 mm, bottom 12 mm.
- Number column: 13 mm; column gap: 5 mm.
- Content indent after number column: 18 mm.
- Footer safe zone: at least 12 mm.

### Type

- Font stack: PingFang SC, Noto Sans CJK SC, Microsoft YaHei, system-ui, sans-serif.
- Web title: 31–47 px; PDF title: 18 pt, line-height 1.22.
- PDF body: 8.35–9 pt, line-height about 1.62.
- Keep Chinese axis labels horizontal.
- Keep chart labels short and move full explanations into body text.

### Minimum PDF spacing

- Title → tags: 3.2 mm.
- Tags → signal cards: 4 mm.
- Signal cards → body: 5 mm.
- Any overlap: 0 px.
- Any vertical overflow: 0 px.

## 4. Color and components

Core colors:

- Ink `#182235`
- Secondary ink `#34425A`
- Muted `#748096`
- Blue `#667FF0`
- Blue deep `#4057C9`
- Mint `#5AB79F`
- Violet `#8E72D2`
- Peach `#DC8C68`
- Gold `#C89842`
- Paper `#F4F7FB`

Theme mapping:

- Blue: overview and growth signals.
- Mint: product, model and open ecosystem.
- Violet: competition, team, organization and private decision.
- Peach: capital, GTM and risk.
- Gold: sources, catalysts and final observation.

Cards use light backgrounds, thin borders and rounded corners. Web may use restrained shadows; print should remove or soften them.

Use exactly three judgment tags and three signal cards. If a metric is unavailable, display “未披露” or “无法验证”; do not leave a blank card.

## 5. Visual mappings

- 01: company timeline.
- 02: competition matrix.
- 03: product layers and monetization funnel.
- 04: evidence-confidence bars.
- 05: funding timeline and investor/shareholder cloud.
- 06: model core/orbit and open/closed balance.
- 07: founder map and GTM organization tree.
- 08: 0–90 day roadmap and editable owner-view cards.
- 09: reach-out decision path and diligence gates.
- 10: upside/downside balance.
- Sources: primary → media → analyst-judgment flow.

Use uniform linear SVG icons. Icons aid recognition but never replace text.

## 6. Web/PDF consistency

Title, section order, tags, signals, judgment, body, sources, visual labels and numbers must come from the same JSON.

Allowed differences:

- Web includes navigation, comments and input controls.
- Print hides interactive controls and uses fixed A4 geometry.
- Mobile changes layout but not information order.

## 7. Prohibited patterns

- Title, tags, cards or body overlap.
- Absolute positioning that assumes a fixed title height.
- Applying both positional offsets and margins to the same visual.
- Rotated or inverted Chinese axis labels.
- Shrinking body text to force a crowded page.
- Decorative charts without a clear research question.
- Precision charts based on unsupported estimates.
- Treating an independently generated PDF as proof that browser export works.

