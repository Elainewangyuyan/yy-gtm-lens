# Privacy and publishing

## Physical separation

Public artifacts may contain sections 01–08, 10 and sources.

Private artifacts contain section 09. Do not place private text in:

- Public HTML comments.
- Hidden DOM nodes.
- Public JavaScript configuration.
- Public source maps.

Add private paths to `.gitignore`. Public release checks must scan file contents and filenames. Hiding private content with CSS, client-side routing, authentication UI or an unlinked URL is not physical separation.
- Public PDF metadata.
- The `publish/` directory.

CSS hiding, client-side passwords and obscured URLs are not access control.

## Safe output

The renderer creates:

- `public-site/`: local working website.
- `private-notes/`: private local page.
- `exports/*-public.pdf`: public.
- `exports/*-private-09.pdf`: private.
- `publish/`: public website files only.

Deploy only `publish/`.

## Leakage checks

Scan `publish/` for:

- Section number `09`.
- Private title and distinctive private phrases.
- Reach-out, compensation, equity, manager or diligence text copied from section 09.
- Paths or filenames pointing to private files.

The public site may explain that a private section exists, but must not contain its analysis.

## Comments and owner views

- Owner views may be seeded from the public JSON and extended in local storage.
- Visitor comments are web-only.
- Configure Giscus only after a public GitHub repository exists.
- Never put private career notes into local-storage defaults on the public site.
