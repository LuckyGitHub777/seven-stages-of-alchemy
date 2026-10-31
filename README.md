# Seven Stages of Alchemy

**v1.0.3** · [Notice](NOTICE.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md) · MIT licensed

An interactive, single-page experience that carries one real thing you're working on through seven stages of alchemical transformation:

**Calcination → Dissolution → Separation → Conjunction → Fermentation → Distillation → Coagulation**

It's an experience you move through, not a page that explains alchemy. You bring raw material (a situation, a question, a pattern), respond to each stage, and finish on **Apply**, where the result becomes one concrete action with a time and a first step.

## What's inside

- **Seven stages**, each with its own sacred-geometry figure drawn in inline SVG: triangle, circle, divided circles, vesica, pentagon, spiral, heptagram.
- **Recursive Distillation.** Refine your insight pass after pass. Each pass is kept, and you leave when it's clear.
- **Reality and Structure layers.** These stay hidden until you open them. *Reality* gives a practical reading of the stage. *Structure* gives its traditional correspondences (element, planet, metal, figure).
- **Optional sound.** A soft synthesized drone that changes with each stage. It's off by default and only starts when you turn it on, and it never autoplays. It's there for atmosphere only, with no claims about effects on the brain or health.
- **Apply.** Copy your whole journey or save it as a text file.
- **Private by design.** Progress is saved only in your browser's local storage. There's no network access, analytics, external fonts or remote assets, and a Content-Security-Policy enforces this.
- **Accessible.** Keyboard navigable, visible focus states, ARIA labelling, respects `prefers-reduced-motion`, and responsive down to 320 px wide.

## Run it

Open `index.html` in any modern browser. There's no build step and no dependencies.

## Validate

```bash
python scripts/validate_site.py   # structure, stages, recursion, layers, sound, privacy, claims, release files
sha256sum -c SHA256SUMS.txt       # file integrity

# Browser UAT (Playwright, pinned in package-lock.json)
npm ci && npx playwright install chromium
python -m http.server 8765 &      # serve the repo root
npm run uat                       # 1440×900, 390×844, 320×568
```

GitHub Actions runs both the static checks and the browser UAT on every push. Every Action is pinned to an immutable commit SHA.

To regenerate checksums after editing:

```bash
find . -type f ! -path './.git/*' ! -path './node_modules/*' ! -name SHA256SUMS.txt | sort | xargs sha256sum > SHA256SUMS.txt
```

## Note

The stages are a symbolic map drawn from alchemical imagery, offered for reflection. They are not a diagnosis, therapy, or a substitute for professional care.
