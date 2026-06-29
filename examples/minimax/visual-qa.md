# Visual QA

- Status: pass
- Company: MiniMax
- Research date: 2026-06-25
- QA date: 2026-06-26

## Checked surfaces

- Desktop web: 1440 × 1200, pass.
- Desktop web: 1280 × 1000, pass.
- Tablet web: 768 × 1000, pass.
- Mobile web: 390 × 900, pass.
- Programmatic public PDF: 14 pages rendered to PNG and reviewed, pass.
- Programmatic private PDF: 4 pages rendered to PNG and reviewed, pass.
- Public/private separation: `publish/` passed leakage scan with source JSON.

## Evidence

- `web-geometry-summary.json`
- `contact-sheet-web.png`
- `contact-sheet-public-pdf.png`
- `contact-sheet-private-pdf.png`
- `web-pages/page-*.png`
- `pdf-public-pages/page-*.png`
- `pdf-private-pages/page-*.png`

## Notes

- Native browser print dialog export was not automated in this sandbox. The public site still contains the “导出 PDF” button for manual browser print/export; the delivered downloadable PDF is the programmatic public PDF.
- Earlier responsive overflow at 1280/768 px was fixed by switching medium-width web cards to adaptive height while keeping the PDF renderer A4-paged.
