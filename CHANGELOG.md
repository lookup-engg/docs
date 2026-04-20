# Changelog

## v4.0.0 — 2026-04-20

### Documentation Hygiene & Positioning Refresh

#### Positioning
- Replaced all instances of "demo" / "demos" with "Velo" (when referring to the created artifact) or "video message" (when referring to the product category) across all nav-referenced documentation files
- Affected files span all four creation method sections (Capture Screen Recording, Upload a Recording, Upload PDFs & PNGs, Paste a Link), Getting Started guides, Creating VeloTwin, Editing Velo, Chrome Extension, and FAQ

#### Pricing Accuracy
- Fixed avatar minutes billing description: "per video" changed to "per month" in `pricing/pricing.mdx` and `faq/faq.mdx`
- Pro plan: "Up to 3 minutes of avatar video per month"
- Ultra plan: "Up to 30 minutes of avatar video per month"

#### UI Label Accuracy
- Corrected two instances of "Create New Velo" to "Generate a Velo" to match the actual dashboard button label
  - `upload-pdfs-pngs/setup.mdx`
  - `paste-a-link/setup.mdx`

#### Formatting
- Replaced all em dashes (`—`) with hyphens (`-`) across 57 mdx files for consistent punctuation style
- Escaped dollar signs (`\$`) in pricing content to prevent MDX math rendering

#### Introduction
- Updated product description in `getting-started/introduction.mdx` from "AI-native product demo and walkthrough generator" to "AI-native video message tool"

### Manual Content Updates

#### Editor Documentation
- `editing-velo/callout.mdx` - Updated Callout description to reflect zoom effect behaviour
- `editing-velo/cut-and-crop.mdx` - Rewrote Crop section: now describes cropping height/width of the video rather than trimming start/end
- `editing-velo/scripts.mdx` - Updated lock behaviour description and changed regeneration instruction to reference the Generate Voice button
- `editing-velo/velotwin.mdx` - Updated VeloTwin face section to clarify the face cannot be changed after voice selection
- `editing-velo/zooms.mdx` - Updated zoom auto-generation behaviour and manual zoom instructions

#### FAQ
- `faq/faq.mdx` - Minor copy update: "studio-quality video" to "awesome video"

#### Getting Started
- `getting-started/capture-screen.mdx` - Minor rewording of method description

### Typo Fixes
- `getting-started/introduction.mdx` - Fixed "awwesome" to "awesome"
- `editing-velo/callout.mdx` - Fixed "ont he" to "on the"
