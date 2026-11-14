#!/usr/bin/env python3
"""Structural checks and inspectable previews for the published A5 guide.

Automated checks are not a substitute for a human visual and phone review.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
edition=json.loads((ROOT/"pdf/edition.json").read_text(encoding="utf-8"))
source=ROOT/edition["pdf_path"]
web_pdf=ROOT/"_site/downloads"/source.name
homepage=ROOT/"_site/index.html"

def validate_file(p:Path):
    assert p.is_file(), f"Missing release file: {p}"
    blob=p.read_bytes()
    assert blob.startswith(b"%PDF-"), f"Invalid PDF header: {p}"
    assert len(blob)==edition["bytes"], f"PDF size does not match edition manifest: {p}"
    digest=hashlib.sha256(blob).hexdigest()
    assert digest==edition["sha256"], f"PDF hash differs from the reviewed edition: {p}"
    return digest

sha=validate_file(source)
assert sha==validate_file(web_pdf)
html=homepage.read_text(encoding="utf-8")
assert "downloads/"+source.name in html, "Missing download link on the website"
assert "AIPMAndy" in html and "www.a6no1.cn" in html

import fitz
doc=fitz.open(str(source))
assert len(doc)==edition["pages"], f"Expected {edition['pages']} pages, got {len(doc)}"
text="\n".join(page.get_text() for page in doc)
urls="\n".join(item.get("uri","") for page in doc for item in page.get_links() if item.get("uri"))
visible=text+"\n"+urls
for required in ("AIPMAndy","metaver.vip","a6no1.cn"):
    assert required in visible, f"Missing author or contact: {required}"
toc_count=len(doc.get_toc())
link_count=sum(len(page.get_links()) for page in doc)
warnings=[]
if not toc_count:
    warnings.append("No embedded bookmarks; inspect the contents page")
if not link_count:
    warnings.append("No clickable links; inspect the printed URLs")
out=ROOT/"pdf-qa"
out.mkdir(exist_ok=True)
for title,i in (("cover",0),("middle",len(doc)//2),("last",len(doc)-1)):
    doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(out/f"{title}.png"))
report={"pages":len(doc),"sha256":sha,"bytes":edition["bytes"],"bookmarks":toc_count,"links":link_count,"warnings":warnings,"visual_review_status":"awaiting human inspection"}
(out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
