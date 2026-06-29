# Quality gate

Reject or revise the report if any mandatory check fails.

## Accuracy

- Current date and cutoff are explicit.
- Proposed and completed financing are distinguished.
- Historical metrics are not presented as current.
- Every high-risk number has a source ID, date and scope.
- Dynamic facts such as pricing, hiring, repository stars and market value include an accessed date.
- Capital structure and named shareholders come from a prospectus, filing or company register rather than an encyclopedia or unsourced list.
- Legal allegations identify separate cases correctly and use a filing, original statement or at least two reputable reports; allegations are never written as adjudicated facts.
- Open-weight/open-source status is checked against the actual downloadable repository and license, not marketing copy alone.
- Unsupported claims are removed or marked unknown.

## Coverage

- Sections 01–08 and 10 are public.
- Section 09 exists only in the private artifact.
- Private files are excluded by `.gitignore`, build rules and a post-build leakage scan; CSS hiding does not count as separation.
- Pricing, careers link, investors/shareholders and GTM reporting line are covered or explicitly unknown.
- Model use cases accompany architecture details.
- Capital efficiency distinguishes engineering efficiency from financial efficiency.

## Usefulness

- Each section starts with a clear judgment.
- GTM advice is prioritized, measurable and low-cost.
- Advice explains what to test, which metric moves and why.
- Career assessment separates “worth contacting” from “worth joining.”
- Employee equity diligence covers strike price, dilution, liquidation preference, repurchase and lock-up where relevant.

## Sources

- Primary sources dominate factual claims.
- Dynamic pages include access dates.
- Sources are reachable URLs and grouped by category.
- Text points to source IDs rather than ending with an untraceable link pool.

## Visual and privacy

- Public text and web/PDF text come from the same JSON.
- Every theme fits one page or two balanced pages.
- No text, chart or small point is split or clipped.
- Browser-exported PDF and programmatic PDF are checked separately.
- Title/tag/signal overlap and vertical overflow are zero.
- Public website and `publish/` contain no private section phrases.
- Static passwords are never described as real access control.

## QA output

Classify findings:

- P0: privacy leak, unusable artifact or major missing content.
- P1: factual error, unsupported high-risk claim, overlap, clipping or inconsistent output.
- P2: clarity, balance or polish issue.

Release only with P0 = 0 and P1 = 0. Record unresolved unknowns in `quality_review`.
