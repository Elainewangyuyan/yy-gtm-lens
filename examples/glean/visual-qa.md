# Visual QA

- Status: pass
- Company: Glean
- Research date: 2026-06-26
- QA date: 2026-06-26

## Web geometry

- 1440 × 1200: pass; 14 public web pages; 0 overlap; 0 footer collision; 0 horizontal overflow.
- 1280 × 1000: pass; 14 public web pages; 0 overlap; 0 horizontal overflow.
- 768 × 1000: pass; 14 public web pages; 0 overlap; 0 horizontal overflow.
- 390 × 900: pass; 14 public web pages; 0 overlap; 0 horizontal overflow.

## Renderer fixes applied during QA

- Moved judgment tags out of the title row into a dedicated row.
- Raised stylesheet cache version to `styles.css?v=3`.
- Fixed mobile owner-view form overflow.
- Split section 08 owner-view interaction area into an independent public web page to preserve breathing room.

## PDF and privacy

- Programmatic public PDF: pass; 13 pages; readable; no private career judgment phrase detected.
- Programmatic private PDF: pass; 2 pages; contains section 09 only.
- Public/private separation scan: pass.

## Notes

- The public web has one extra interactive owner-view page compared with the programmatic public PDF. This is intentional: the form is a web-only interaction surface and is not part of the fixed research text.
- Full browser-native print/export PDF still needs a manual user-path check if it will be used as the official downloadable artifact.
