> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- This is a documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Run `mint dev` to preview locally
- Run `mint broken-links` to check links

## What Velo is

Velo is the video layer for work — AI video infrastructure that helps people and
companies explain, train, and sell faster.

Never position Velo as "a tool to make videos." Position it as the layer that
lets people, teams, and agents explain work through video.

Explain the mechanism. Velo should sound like it has a model of the world:
context, artifacts, intent, memory, rendering, distribution, feedback.

## Terminology

| Use | Not |
| --- | --- |
| **Velo** — always the platform, never one output | "a Velo", "Velos", "Velo video" |
| **a video** — one output made with Velo | "a Velo" used as a countable noun |
| **VeloTwin** — the umbrella term for a user's AI presenter | "Velo Twin" · "Velotwin" |
| **Voice clone** and **Face clone** — the two halves of a VeloTwin | "avatar" as the primary noun |
| **Public avatars** | "actors" · "AI presenters" |
| **Prompt to Video** | "Prompt-to-Video" · "PtV" |
| **workspace**, **library**, **member** (lowercase in prose) | "project" · "folder" · "user" |
| **Brand Kit** (title case) | "brand kit" |
| **Velo minutes** — the billing unit (Velo stays attached here) | "credits" (credits are Prompt to Video only) |

Note: the app currently labels the Prompt to Video area **Reach** and its
currency **Reach credits**. The docs use "Prompt to Video" and "Prompt to Video
credits", with a bridge note wherever a reader could hit the mismatch.

## Voice

Calm intelligence. Scientific clarity. Infrastructure confidence. Human but not
cute. Quiet superiority.

**Words to use:** video layer · grounded · context · source artifacts ·
workflow memory · output · reasons · traces · explanation · source · renders ·
reliable · show-and-tell · distributes · natively · async workflows ·
infrastructure · explain · signal · clarity · speed · clear · precise ·
native · contextual

**Words to avoid:** polished · stunning · beautiful · effortless · magical ·
magic · game-changing · seamless · awesome · amazing · powerful ·
hyper-realistic · "in minutes" · "10x your videos" · viral · wow ·
"no editing skills required" · "super easy" · "AI-powered video maker" ·
"AI-native video messaging tool" · "no camera anxiety" · "perfect take" ·
"flawless take" · "just Velo it"

No exclamation marks. No hype. Say less, but make each line feel engineered.

Never attack competitors. Make them feel like editing tools. Velo feels like a
system.

## Style preferences

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references
- Every page needs a frontmatter `description` — it is the meta description
- Reproduce UI labels exactly as they appear in the app, even when the label
  itself uses a word from the avoid list (e.g. the voice named "Professional
  and clear")
- Image paths start with a leading slash: `/images/section/page/01.png`
- New screenshots go to `images/<section>/<page>/NN.png`, max 1600px wide
- Screenshots must show Velo's own product or neutral demo content — never a
  customer's data, branding, or recordings. Check the video title, the canvas,
  and the Recent Chats sidebar before capturing
- Do not use annotated screenshots. If a step needs a specific control pointed
  out, name it in the prose: "Select **Public Voices**"

## Content boundaries

- Document what has shipped in the app, not what is on the marketing site
- Directories listed in `.mintignore` are archived — do not edit or link to them
- If a feature is documented but you cannot find it in the app, flag it rather
  than describing it from assumption
