# Velo Documentation

The public documentation for [Velo](https://usevelo.ai) — the video layer for
work. Published with [Mintlify](https://mintlify.com) at
[docs.usevelo.ai](https://docs.usevelo.ai).

## Working on the docs

```bash
npm i -g mint     # once
mint dev          # local preview at localhost:3000
mint broken-links # check internal links before pushing
```

Pages are MDX with YAML frontmatter. Navigation and redirects live in
`docs.json` — that is the only config the site builds from.

## Before you write

Read **`AGENTS.md`**. It carries the positioning statement, the product-noun
glossary, and the words-to-use / words-to-avoid lists from the brand
guidelines. Anything written here is expected to match it.

Two rules that catch people out:

- Every page needs a frontmatter `description`. It is the meta description.
- Reproduce UI labels exactly as they appear in the app, even when the label
  uses a word the brand guidelines otherwise avoid.

## Repository layout

| Path | What it is |
| --- | --- |
| `docs.json` | Navigation, theme, redirects. The live config |
| `AGENTS.md` | Brand voice, terminology, style rules |
| `images/` | Screenshots, as `images/<section>/<page>/NN.png`, max 1600px wide |
| `scripts/` | Authoring tooling, excluded from the build |
| `snippets/` | Reusable MDX fragments |

### Archived pages

Directories listed in `.mintignore` are superseded pages kept in git for
reference. They are not built, not served, and not indexed, and `docs.json`
redirects their old URLs to the current equivalents. Do not edit or link to
them — if you need something from one, move it into the live page instead.

## Screenshots

`scripts/take-screenshots.py` drives a real browser through the app and writes
captures straight to the correct `images/` paths, pausing where a screenshot
needs a specific editor state set up by hand.

```bash
python3 scripts/take-screenshots.py
```

New captures: PNG, max 1600px wide, at `images/<section>/<page>/NN.png`.
