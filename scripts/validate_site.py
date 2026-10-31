#!/usr/bin/env python3
"""Static validation for the Seven Stages of Alchemy site.

Runs with the Python standard library only. Exits non-zero on any failure.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

EXPECTED = [
    "Calcination", "Dissolution", "Separation", "Conjunction",
    "Fermentation", "Distillation", "Coagulation",
]
# Wording that would imply a medical, therapeutic or brain-entrainment claim,
# or reference proprietary audio programmes.
FORBIDDEN = [
    r"\bheal(s|ing)?\b", r"\bcure[sd]?\b", r"\btherap(y|eutic)\b(?!,? or a substitute)",
    r"brain\s*wave", r"entrain", r"binaural", r"hemi-?sync", r"metamusic",
    r"solfeggio", r"\bhz\b.*\bfrequenc(y|ies)\b.*\bheal",
]

failures = []


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        failures.append(msg)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.append(a["id"])


def main():
    check(INDEX.is_file(), "index.html exists")
    if not INDEX.is_file():
        return
    html = INDEX.read_text(encoding="utf-8")
    p = Collector()
    p.feed(html)

    check(html.lstrip().lower().startswith("<!doctype html>"), "doctype present")
    check(any(t == "html" and a.get("lang") for t, a in p.tags), "html lang attribute set")
    check(any(t == "meta" and a.get("name") == "viewport" for t, a in p.tags), "responsive viewport meta")
    check(any(t == "meta" and a.get("http-equiv", "").lower() == "content-security-policy" for t, a in p.tags),
          "Content-Security-Policy meta present")
    check(len(p.ids) == len(set(p.ids)), "static element ids are unique")

    # Stage data
    m = re.search(r'<script type="application/json" id="stages">(.*?)</script>', html, re.S)
    check(bool(m), "stage data block present")
    stages = json.loads(m.group(1)) if m else []
    names = [s.get("name") for s in stages]
    check(names == EXPECTED, "exactly seven stages in canonical order")
    for s in stages:
        for field in ("id", "prompt", "reality", "structure", "geometry", "lede"):
            check(bool(s.get(field)), f"{s.get('name')}: has {field}")
    rec = [s["name"] for s in stages if s.get("recursive")]
    check(rec == ["Distillation"], "Distillation (and only Distillation) is recursive")
    check("distillAgain" in html, "recursive 'Distill again' control present")

    # Layers hidden until requested
    check("aria-expanded" in html and "'Reality'" in html and "'Structure'" in html,
          "Reality and Structure layers are toggle-driven")
    check(re.search(r"layers\s*:\s*\{\}", html) is not None, "layers default to closed")

    # Sound: optional, no autoplay, no media files
    check(not re.search(r"\bautoplay\b", html, re.I), "no autoplay attribute")
    check(not any(t in ("audio", "video") for t, _ in p.tags), "no embedded audio/video elements")
    check('aria-pressed="false"' in html and "Sound: off" in html, "sound starts off and is opt-in")

    # Self-contained: no remote assets
    remote = [a.get("src") or a.get("href") for t, a in p.tags
              if re.match(r"^(https?:)?//", (a.get("src") or a.get("href") or ""))]
    check(not remote, f"no remote src/href assets {remote if remote else ''}".strip())
    check(not re.search(r"@import|url\(\s*['\"]?https?:", html), "no remote CSS imports")
    check("fetch(" not in html and "XMLHttpRequest" not in html, "no network calls in script")

    # Accessibility and motion
    check("prefers-reduced-motion" in html, "reduced-motion media query present")
    check("focus-visible" in html, "visible focus styling present")

    # Claims
    lowered = html.lower()
    hits = [pat for pat in FORBIDDEN if re.search(pat, lowered)]
    check(not hits, f"no therapeutic / entrainment / proprietary-audio claims {hits if hits else ''}".strip())

    # Persistence is guarded
    check(html.count("localStorage") >= 2 and "try{ localStorage" in html, "localStorage access is try/catch guarded")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} check(s) failed)")
        sys.exit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
