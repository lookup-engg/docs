"""
Velo Docs Screenshot Tool
=========================
Run this on your Mac to capture all documentation images.

Requirements (run once):
  pip3 install playwright
  python3 -m playwright install chromium

Usage:
  python3 docs/take-screenshots.py

How it works:
  1. Opens a browser — you log in to app.usevelo.ai once
  2. For simple pages it navigates and captures automatically
  3. For editor screenshots it pauses with a prompt telling you exactly
     what state to set up, then you press Enter and it captures
  4. All images land directly in docs/images/ at the correct paths
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

DOCS_IMAGES  = Path(__file__).parent / "images"
BASE_URL     = "https://app.usevelo.ai"
VELOTWIN_URL = f"{BASE_URL}/velo-twin"

# Args:
#   argv[1] = extension path (optional)
#   argv[2] = project ID for the editor, e.g. "42"  (optional, will prompt if missing)
#   argv[3] = section to start from: getting-started | velotwin | editing | sharing | chrome | capture-screen
EXTENSION_PATH = sys.argv[1] if len(sys.argv) > 1 else None
PROJECT_ID     = sys.argv[2] if len(sys.argv) > 2 else None
START_FROM     = sys.argv[3] if len(sys.argv) > 3 else "getting-started"

SECTIONS = ["getting-started", "velotwin", "editing", "sharing", "chrome", "capture-screen"]


def prompt(msg: str):
    input(f"\n  ⏸  {msg}\n     Press Enter when ready…")


def snap(page: Page, rel_path: str):
    out = DOCS_IMAGES / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out), full_page=False)
    print(f"  ✓  {rel_path}")


def go(page: Page, url: str, wait_for: str = None, timeout: int = 30000):
    # Use domcontentloaded for heavy app pages to avoid networkidle timeouts
    wait_until = "domcontentloaded" if "usevelo.ai" in url else "networkidle"
    page.goto(url, wait_until=wait_until, timeout=timeout)
    if wait_for:
        page.wait_for_selector(wait_for, timeout=15000)
    time.sleep(2)  # extra settle time for heavy pages


def run():
    with sync_playwright() as p:
        print("\n🚀  Launching browser…")

        if EXTENSION_PATH:
            print(f"🧩  Loading extension from: {EXTENSION_PATH}\n")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir="/tmp/velo-playwright-profile",
                headless=False,
                slow_mo=150,
                args=[
                    "--window-size=1440,900",
                    f"--disable-extensions-except={EXTENSION_PATH}",
                    f"--load-extension={EXTENSION_PATH}",
                ],
                viewport={"width": 1440, "height": 900},
            )
        else:
            browser = p.chromium.launch(
                headless=False, slow_mo=150,
                args=["--window-size=1440,900"],
            )
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})

        page = ctx.new_page()

        # ── PROJECT ID ─────────────────────────────────────────────────────
        project_id = PROJECT_ID or input("\n🔢  Enter a project ID to use for editor screenshots (check URL of any project): ").strip()
        editor_url = f"{BASE_URL}/project/{project_id}/editor"
        print(f"   Editor URL: {editor_url}\n")

        # ── SKIP TO SECTION ────────────────────────────────────────────────
        start_idx = SECTIONS.index(START_FROM) if START_FROM in SECTIONS else 0
        def should_run(section: str) -> bool:
            return SECTIONS.index(section) >= start_idx

        # ── LOGIN ──────────────────────────────────────────────────────────
        page.goto(f"{BASE_URL}/")
        input("\n🔐  Log in to app.usevelo.ai in the browser window.\n    Press Enter here once you're logged in and see the dashboard…")
        print("✅  Logged in!\n")


        def active_page():
            """Return the most recently active non-blank page."""
            pages = [p for p in ctx.pages if p.url not in ("about:blank", "chrome://newtab/")]
            return pages[-1] if pages else ctx.pages[-1]

        # ══════════════════════════════════════════════════════════════════
        # GETTING STARTED
        # ══════════════════════════════════════════════════════════════════
        if should_run("getting-started"):
            print("── Getting Started ──────────────────────────────────────")

            go(page, f"{BASE_URL}/")
            snap(page, "getting-started/quickstart/1.png")

            go(page, f"{BASE_URL}/make-a-velo")
            snap(page, "getting-started/quickstart/2.png")

            if EXTENSION_PATH:
                # upload-pdfs-pngs
                print("\n  → upload-pdfs-pngs")
                go(page, f"{BASE_URL}/make-a-velo")
                prompt("[upload-pdfs-pngs] Step 1/5 — Click 'Upload PDFs & PNGs' — file upload interface visible")
                snap(page, "getting-started/upload-pdfs-pngs/1.png")
                prompt("[upload-pdfs-pngs] Step 2/5 — Narration canvas open, slides visible")
                snap(page, "getting-started/upload-pdfs-pngs/2.png")
                prompt("[upload-pdfs-pngs] Step 3/5 — VeloTwin setup page")
                snap(page, "getting-started/upload-pdfs-pngs/3.png")
                prompt("[upload-pdfs-pngs] Step 4/5 — Script review screen (before agent recording)")
                snap(page, "getting-started/upload-pdfs-pngs/4.png")
                prompt("[upload-pdfs-pngs] Step 5/5 — Agent recording in progress")
                snap(page, "getting-started/upload-pdfs-pngs/5.png")

                # paste-a-link
                print("\n  → paste-a-link")
                go(page, f"{BASE_URL}/make-a-velo")
                prompt("[paste-a-link] Step 1/5 — Click 'Paste a Link' — name + URL modal open")
                snap(page, "getting-started/paste-a-link/1.png")
                prompt("[paste-a-link] Step 2/5 — Assisted recording modal (URL badge + hints visible)")
                snap(page, "getting-started/paste-a-link/2.png")
                prompt("[paste-a-link] Step 3/5 — Stop recording. Switch to VeloTwin setup tab, then press Enter")
                page = active_page()
                snap(page, "getting-started/paste-a-link/3.png")
                prompt("[paste-a-link] Step 4/5 — Script review screen (before agent recording)")
                page = active_page()
                snap(page, "getting-started/paste-a-link/4.png")
                prompt("[paste-a-link] Step 5/5 — Agent recording / live browser in progress")
                page = active_page()
                snap(page, "getting-started/paste-a-link/5.png")
            else:
                print("  ⚠  Skipping upload-pdfs-pngs, paste-a-link (run with extension path)\n")

            # Upload a Recording — no extension needed
            print("  → upload-recording")
            go(page, f"{BASE_URL}/make-a-velo")
            prompt("[upload-recording] Step 1/4 — Click 'Upload a Recording' — file upload interface visible")
            snap(page, "getting-started/upload-recording/1.png")
            prompt("[upload-recording] Step 2/4 — File selected / uploading / processing preview")
            snap(page, "getting-started/upload-recording/2.png")
            prompt("[upload-recording] Step 3/4 — VeloTwin setup page")
            snap(page, "getting-started/upload-recording/3.png")
            prompt("[upload-recording] Step 4/4 — Editor open with Scripts panel visible")
            snap(page, "getting-started/upload-recording/4.png")


        # ══════════════════════════════════════════════════════════════════
        # CREATING VELOTWIN
        # ══════════════════════════════════════════════════════════════════
        if should_run("velotwin"):
            print("\n── Creating VeloTwin ────────────────────────────────────")
            go(page, VELOTWIN_URL)
            prompt("Navigate to Create VeloTwin → Step 1: Capture Face (camera + countdown)")
            snap(page, "creating-velotwin/steps-to-create/1.png")
            prompt("Step 2: Clone Voice (training script + mic)")
            snap(page, "creating-velotwin/steps-to-create/2.png")
            prompt("Step 3: Generating Twin (progress / completion screen)")
            snap(page, "creating-velotwin/steps-to-create/3.png")


        # ══════════════════════════════════════════════════════════════════
        # EDITING VELO
        # ══════════════════════════════════════════════════════════════════
        if should_run("editing"):
            print("\n── Editing Velo ─────────────────────────────────────────")
            go(page, editor_url)
            time.sleep(2)

            snap(page, "editing-velo/overview/1.png")
            prompt("Open the Screen (Background) panel on the right sidebar")
            snap(page, "editing-velo/overview/2.png")
            prompt("Close the panel — make sure the timeline is fully visible")
            snap(page, "editing-velo/overview/3.png")
            prompt("Show the toolbar (Cut ✂ and Crop ⊡ buttons clearly visible)")
            snap(page, "editing-velo/overview/4.png")

            print("\n  — Background panel —")
            prompt("Open Screen panel → Wallpaper tab")
            snap(page, "editing-velo/background/1.png")
            prompt("Switch to Gradient tab")
            snap(page, "editing-velo/background/2.png")
            prompt("Switch to Color tab OR scroll to show Background Blur slider")
            snap(page, "editing-velo/background/3.png")
            prompt("Scroll to show Padding slider")
            snap(page, "editing-velo/background/4.png")

            print("\n  — Face / VeloTwin panel —")
            prompt("Open Face panel — Use VeloTwin toggle visible")
            snap(page, "editing-velo/velotwin/1.png")
            prompt("Click 'Add face' to show the VeloTwin picker")
            snap(page, "editing-velo/velotwin/2.png")
            prompt("Close picker. Show Camera Position grid")
            snap(page, "editing-velo/velotwin/3.png")
            prompt("Show Camera Size slider")
            snap(page, "editing-velo/velotwin/4.png")
            prompt("Show Shape section (Square / Round / Original)")
            snap(page, "editing-velo/velotwin/5.png")
            prompt("Enable 'Make Smaller during zoom' and show Size during Zoom slider")
            snap(page, "editing-velo/velotwin/6.png")

            print("\n  — Audio panel —")
            prompt("Open Audio panel — Background Music toggle visible")
            snap(page, "editing-velo/audio/1.png")
            prompt("Show Master Volume slider")
            snap(page, "editing-velo/audio/2.png")
            prompt("Show Narration Volume slider")
            snap(page, "editing-velo/audio/3.png")

            print("\n  — Scripts panel —")
            prompt("Open Scripts panel — scrollable transcript visible")
            snap(page, "editing-velo/scripts/1.png")
            prompt("Click the lock icon to unlock the script for editing")
            snap(page, "editing-velo/scripts/2.png")
            snap(page, "editing-velo/scripts/3.png")

            print("\n  — Cards panel —")
            prompt("Open Cards panel — Enable toggle is OFF")
            snap(page, "editing-velo/cards/1.png")
            prompt("Enable the Intro Card toggle — preview appears")
            snap(page, "editing-velo/cards/2.png")
            prompt("Show Light / Dark mode toggle")
            snap(page, "editing-velo/cards/3.png")
            prompt("Show Name and Role fields filled in")
            snap(page, "editing-velo/cards/4.png")
            prompt("Show Title of video and Description fields")
            snap(page, "editing-velo/cards/5.png")

            print("\n  — Insert panel —")
            prompt("Open Insert panel — all three sections visible")
            snap(page, "editing-velo/insert/1.png")
            prompt("Show Elements section clearly (Text Box, Image, Rectangle, Arrow)")
            snap(page, "editing-velo/insert/2.png")
            prompt("Show Effects section (Callout, Spotlight)")
            snap(page, "editing-velo/insert/3.png")
            prompt("Show Focus section (Mask, Zoom)")
            snap(page, "editing-velo/insert/4.png")

            print("\n  — Spotlight —")
            prompt("Click Spotlight in Insert panel — region appears on canvas and in timeline")
            snap(page, "editing-velo/spotlight/1.png")
            snap(page, "editing-velo/spotlight/2.png")
            prompt("Show Background Opacity slider in settings")
            snap(page, "editing-velo/spotlight/3.png")
            prompt("Open Background Color picker")
            snap(page, "editing-velo/spotlight/4.png")
            prompt("Show Border Radius slider")
            snap(page, "editing-velo/spotlight/5.png")
            prompt("Show Duration field")
            snap(page, "editing-velo/spotlight/6.png")

            print("\n  — Callout —")
            prompt("Click Callout in Insert — region on canvas, block in timeline")
            snap(page, "editing-velo/callout/1.png")
            snap(page, "editing-velo/callout/2.png")
            prompt("Show Scale slider")
            snap(page, "editing-velo/callout/3.png")
            prompt("Show Background Opacity slider")
            snap(page, "editing-velo/callout/4.png")
            prompt("Open Background Color picker")
            snap(page, "editing-velo/callout/5.png")
            prompt("Show Border Radius slider")
            snap(page, "editing-velo/callout/6.png")
            prompt("Show Duration field")
            snap(page, "editing-velo/callout/7.png")

            print("\n  — Timeline —")
            prompt("Close all panels — full timeline visible with all 6 tracks")
            snap(page, "editing-velo/timeline/1.png")
            prompt("Zoom timeline in to show track labels clearly")
            snap(page, "editing-velo/timeline/2.png")
            prompt("Click a zoom block in the Zoom track to select it")
            snap(page, "editing-velo/timeline/3.png")
            prompt("Click a callout or spotlight block to show block selection")
            snap(page, "editing-velo/timeline/4.png")
            prompt("Use the timeline zoom slider to show a wide view of the full video")
            snap(page, "editing-velo/timeline/5.png")

            print("\n  — Cut and Crop —")
            prompt("Show toolbar with Cut ✂ and Crop ⊡ buttons clearly visible")
            snap(page, "editing-velo/cut-and-crop/1.png")
            prompt("Position playhead mid-video — hover over the Cut button")
            snap(page, "editing-velo/cut-and-crop/2.png")
            prompt("After a cut, show the two resulting segments in the timeline")
            snap(page, "editing-velo/cut-and-crop/3.png")
            prompt("Click Crop ⊡ — crop modal open with drag handles")
            snap(page, "editing-velo/cut-and-crop/4.png")
            prompt("Open the Aspect Ratio dropdown inside the crop modal")
            snap(page, "editing-velo/cut-and-crop/5.png")


        # ══════════════════════════════════════════════════════════════════
        # SHARING VELO
        # ══════════════════════════════════════════════════════════════════
        if should_run("sharing"):
            print("\n── Sharing Velo ─────────────────────────────────────────")
            go(page, editor_url)
            prompt("Show the Publish button in the editor top-right corner")
            snap(page, "sharing-velo/share-via-link/1.png")
            prompt("Click Publish — show the rendering / processing state")
            snap(page, "sharing-velo/share-via-link/2.png")
            prompt("Rendering complete — show the shareable link")
            snap(page, "sharing-velo/share-via-link/3.png")
            prompt("Show link settings panel (access controls, visibility options)")
            snap(page, "sharing-velo/share-via-link/4.png")
            prompt("Show the Download button alongside the share link")
            snap(page, "sharing-velo/share-via-link/5.png")
            snap(page, "sharing-velo/download/1.png")
            prompt("Show the download-only fallback state (after a failed upload)")
            snap(page, "sharing-velo/download/2.png")


        if should_run("chrome"):
         print("\n── Chrome Extension ─────────────────────────────────────")
        if should_run("chrome") and EXTENSION_PATH:
            page.goto("https://chromewebstore.google.com/detail/velo-companion/gmjgnlhlmipflnfehmchoeeajoegamif",
                      wait_until="networkidle")
            time.sleep(2)
            snap(page, "chrome-extension/installation/1.png")
            prompt("Show Chrome extensions popup with Velo Companion pinned in toolbar")
            snap(page, "chrome-extension/installation/2.png")
            prompt("Show the Velo extension popup (signed-in state)")
            snap(page, "chrome-extension/installation/3.png")

            go(page, f"{BASE_URL}/make-a-velo")
            prompt("Click 'Capture screen recording' — recording modal open (name field + REC)")
            snap(page, "chrome-extension/recording/1.png")
            prompt("Highlight / focus on the Name the Project field")
            snap(page, "chrome-extension/recording/2.png")
            prompt("Recording in progress")
            snap(page, "chrome-extension/recording/3.png")
            prompt("Click Stop — switch to the VeloTwin setup tab, then press Enter")
            page = active_page()
            snap(page, "chrome-extension/recording/4.png")
            prompt("VeloTwin setup page visible (duration shown, select twin, Go Make my Velo)")
            snap(page, "chrome-extension/recording/5.png")

            page.goto("chrome://extensions", wait_until="load")
            time.sleep(1)
            snap(page, "chrome-extension/update/1.png")
            prompt("Enable Developer Mode — Update button visible at top")
            snap(page, "chrome-extension/update/2.png")
            prompt("Find Velo Companion in the list — show Remove button")
            snap(page, "chrome-extension/reinstall/1.png")
            page.goto("https://chromewebstore.google.com/detail/velo-companion/gmjgnlhlmipflnfehmchoeeajoegamif",
                      wait_until="networkidle")
            time.sleep(1)
            snap(page, "chrome-extension/reinstall/2.png")
            prompt("Show the extension pinned + signed in after reinstall")
            snap(page, "chrome-extension/reinstall/3.png")

            # capture-screen — left last because stopping recording closes the tab
            print("\n── Capture Screen (left last — handles tab closing) ────")
            go(page, f"{BASE_URL}/make-a-velo")
            prompt("[capture-screen] Step 1/4 — Click 'Capture Screen Recording' — recording modal open (name + REC button)")
            snap(page, "getting-started/capture-screen/1.png")
            prompt("[capture-screen] Step 2/4 — Recording in progress")
            snap(page, "getting-started/capture-screen/2.png")
            prompt("[capture-screen] Step 3/4 — Stop recording. Switch to the VeloTwin setup tab, then press Enter")
            page = active_page()
            snap(page, "getting-started/capture-screen/3.png")
            prompt("[capture-screen] Step 4/4 — Editor open with Scripts panel visible")
            page = active_page()
            snap(page, "getting-started/capture-screen/4.png")
        else:
            print("  ⚠  Skipped — run with extension path to capture these\n")

        print("\n✅  All done! Screenshots saved to docs/images/")
        ctx.close()


if __name__ == "__main__":
    run()
