# Seven Stages of Alchemy

An interactive, single-page experience that carries one real thing you're working on through the seven classical stages of alchemical transformation:

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
python scripts/validate_site.py   # structure, stages, recursion, layers, sound, privacy, claims
sha256sum -c SHA256SUMS.txt       # file integrity
```

The same checks run in GitHub Actions on every push. The workflow pins both Actions to immutable commit SHAs.

To regenerate checksums after editing:

```bash
find . -type f ! -path './.git/*' ! -name SHA256SUMS.txt | sort | xargs sha256sum > SHA256SUMS.txt
```

## Note

The stages are a symbolic map drawn from the alchemical tradition and are offered for reflection. They are not a diagnosis, therapy, or a substitute for professional care.
