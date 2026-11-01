#!/usr/bin/env python3
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
FORBIDDEN = [
    r"\bheal(s|ing)?\b", r"\bcure[sd]?\b", r"\btherap(y|eutic)\b(?!,? or a substitute)",
    r"brain\s*wave", r"entrain", r"binaural",
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

    check("aria-expanded" in html and "'Reality'" in html and "'Structure'" in html,
          "Reality and Structure layers are toggle-driven")
    check(re.search(r"layers\s*:\s*\{\}", html) is not None, "layers default to closed")

    check(not re.search(r"\bautoplay\b", html, re.I), "no autoplay attribute")
    check(not any(t in ("audio", "video") for t, _ in p.tags), "no embedded audio/video elements")
    check('aria-pressed="false"' in html and "Sound: off" in html, "sound starts off and is opt-in")

    remote = [a.get("src") or a.get("href") for t, a in p.tags
              if re.match(r"^(https?:)?//", (a.get("src") or a.get("href") or ""))]
    check(not remote, f"no remote src/href assets {remote if remote else ''}".strip())
    check(not re.search(r"@import|url\(\s*['\"]?https?:", html), "no remote CSS imports")
    check("fetch(" not in html and "XMLHttpRequest" not in html, "no network calls in script")

    check("prefers-reduced-motion" in html, "reduced-motion media query present")
    check("Symbolic and reflective" in html, "scope notice present")
    check("focus-visible" in html, "visible focus styling present")

    lowered = html.lower()
    hits = [pat for pat in FORBIDDEN if re.search(pat, lowered)]
    check(not hits, f"no therapeutic / entrainment claims {hits if hits else ''}".strip())

    check("localStorage.setItem" not in html, "private reflection is not persisted in shared-origin localStorage")
    check("localStorage.getItem(KEY)" in html and "localStorage.removeItem(KEY)" in html,
          "legacy shared-origin data is migrated and removed once")
    check("window.addEventListener('beforeunload'" in html,
          "unsaved work is guarded against accidental reload")
    check("Your work stays in this tab only" in html and "Save as text to keep a copy." in html,
          "user-visible privacy and persistence limitations are clear")

    for f in ("LICENSE", "SECURITY.md", "README.md", "social-preview.png", "tests/uat.cjs", ".nojekyll"):
        check((ROOT / f).is_file(), f"{f} present")
    check(any(t == "link" and a.get("rel") == "icon" and (a.get("href") or "").startswith("data:image/svg+xml")
              for t, a in p.tags), "inline favicon present")
    for prop in ("og:title", "og:description", "og:image", "og:url"):
        check(any(t == "meta" and a.get("property") == prop and a.get("content") for t, a in p.tags), f"{prop} metadata present")

    wf_dir = ROOT / ".github" / "workflows"
    unpinned = []
    for wf in sorted(wf_dir.glob("*.yml")):
        for line in wf.read_text(encoding="utf-8").splitlines():
            m2 = re.match(r"\s*-?\s*uses:\s*(\S+)", line)
            if m2 and not m2.group(1).startswith("./") and not re.search(r"@[0-9a-f]{40}$", m2.group(1)):
                unpinned.append(f"{wf.name}: {m2.group(1)}")
    check(not unpinned, f"all workflow actions pinned to commit SHAs {unpinned if unpinned else ''}".strip())
    check((wf_dir / "pages.yml").is_file(), "Pages deploy + live-verify pipeline present")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} check(s) failed)")
        sys.exit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
