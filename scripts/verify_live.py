#!/usr/bin/env python3
"""Compare the actual GitHub Pages release to the deterministic site build.

Do not treat a successful git commit or deploy event as proof of live content.
Run only after deploy-pages, with PAGES_URL from the deployment output.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
FILES = (
    "index.html",
    "tools.html",
    "plan.html",
    "sources.html",
    "privacy.html",
    "chapters/01.html",
    "assets/app.js",
    "assets/style.css",
    "content.json",
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "downloads/local-business-ai-growth-handbook-guide.pdf",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> None:
    base = os.environ.get("PAGES_URL", "").rstrip("/") + "/"
    if not base.startswith("https://") or "aipmandy.github.io/local-business-ai-growth-handbook/" not in base:
        raise ValueError("PAGES_URL must be the expected HTTPS GitHub Pages project URL")
    expected = {path: sha256((SITE / path).read_bytes()) for path in FILES}
    edition = json.loads((ROOT / "pdf/edition.json").read_text(encoding="utf-8"))
    pdf = FILES[-1]
    if expected[pdf] != edition["sha256"]:
        raise ValueError("Built site PDF does not match the reviewed publication")
    errors = []
    for attempt in range(12):
        errors = []
        verified = []
        for path in FILES:
            url = urljoin(base, path)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "StarAwakening-Live-QA/1.0"})
                with urllib.request.urlopen(req, timeout=22) as response:
                    body = response.read()
                    code = response.status
                if code != 200:
                    raise ValueError(f"HTTP {code}")
                actual = sha256(body)
                if actual != expected[path]:
                    raise ValueError(f"SHA mismatch: actual={actual[:12]} expected={expected[path][:12]}")
                verified.append({"url": url, "sha256": actual, "bytes": len(body)})
            except (OSError, ValueError, urllib.error.URLError) as exc:
                errors.append(f"{path}: {exc}")
        if not errors:
            report = {
                "status": "PASS",
                "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                "site": base,
                "resource_count": len(verified),
                "resources": verified,
                "pdf_sha256": edition["sha256"],
                "notes": "HTTP 200 and exact byte-for-byte comparison against this workflow's build. Not physical-device or human PDF proofing.",
            }
            out = ROOT / "qa" / "live-verification.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"PASS: {len(verified)} actual Pages resources match SHA-256; PDF matches reviewed edition")
            return
        print(f"CDN may still be updating: attempt {attempt + 1}/12: {'; '.join(errors[:3])}", flush=True)
        if attempt < 11:
            time.sleep(6)
    raise RuntimeError("Pages live verification failed: " + "; ".join(errors))


if __name__ == "__main__":
    verify()
