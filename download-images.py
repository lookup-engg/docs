#!/usr/bin/env python3
"""
download-images.py
Scans all .mdx files in this docs repo, downloads S3 images locally,
and replaces S3 URLs with local paths.

Run from the docs folder:
    python3 download-images.py
"""

import os
import re
import urllib.request
import urllib.error
from pathlib import Path

DOCS_ROOT = Path(__file__).parent
S3_PATTERN = re.compile(
    r'https://(?:dev-)?velo-screen-recordings\.s3\.amazonaws\.com/annotated/(\d+)/scene_(\d+)/([a-f0-9]+)\.png[^\s"\'<>]*'
)

def local_path_for(mdx_path: Path, scene_num: str) -> Path:
    """Returns the local image path for a given MDX file and scene number."""
    rel = mdx_path.relative_to(DOCS_ROOT).with_suffix('')  # e.g. creating-a-velo/upload-recording
    return DOCS_ROOT / "images" / rel / f"scene-{scene_num}.png"

def download_image(url: str, dest: Path) -> bool:
    if dest.exists():
        print(f"  ✓ Already exists: {dest.relative_to(DOCS_ROOT)}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"  ↓ Downloaded: {dest.relative_to(DOCS_ROOT)}")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP {e.code} — URL may have expired: {url[:80]}...")
        return False
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def process_mdx(mdx_path: Path):
    content = mdx_path.read_text(encoding='utf-8')
    matches = S3_PATTERN.findall(content)
    if not matches:
        return

    print(f"\n📄 {mdx_path.relative_to(DOCS_ROOT)} ({len(matches)} image(s))")
    new_content = content

    for (record_id, scene_num, file_hash) in matches:
        # Reconstruct the full URL (with query string) from the original content
        full_url_pattern = re.compile(
            rf'https://(?:dev-)?velo-screen-recordings\.s3\.amazonaws\.com/annotated/{record_id}/scene_{scene_num}/{file_hash}\.png[^\s"\'<>]*'
        )
        full_url_match = full_url_pattern.search(content)
        if not full_url_match:
            continue
        full_url = full_url_match.group(0)

        dest = local_path_for(mdx_path, scene_num)
        local_ref = '/' + str(dest.relative_to(DOCS_ROOT)).replace('\\', '/')

        if download_image(full_url, dest):
            new_content = new_content.replace(full_url, local_ref)

    if new_content != content:
        mdx_path.write_text(new_content, encoding='utf-8')
        print(f"  ✏️  Updated URLs in file")

def main():
    print("🔍 Scanning MDX files for S3 image URLs...\n")
    mdx_files = sorted(DOCS_ROOT.rglob("*.mdx"))
    processed = 0
    for mdx_path in mdx_files:
        content = mdx_path.read_text(encoding='utf-8')
        if 'velo-screen-recordings.s3.amazonaws.com' in content:
            process_mdx(mdx_path)
            processed += 1

    if processed == 0:
        print("No S3 URLs found in any MDX files.")
    else:
        print(f"\n✅ Done! Processed {processed} file(s).")
        print("Run 'mintlify dev' to preview with local images.")

if __name__ == '__main__':
    main()
