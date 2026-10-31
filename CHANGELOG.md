# Changelog

## v1.0.4

- Added an automated Pages pipeline: checks → deploy (public files only) → live verification (byte match, 404 for repository-only files, full browser UAT on the live URL) → weekly re-verification.
- Every workflow `uses:` reference is now validated as pinned to a full commit SHA.
- README: "Local by design", plus a deployment section and the live link.

## v1.0.3

- Simplified the About panel and `NOTICE.md`.
- Refined the introductory copy.
- Added `.nojekyll` so GitHub Pages serves the site as-is.

## v1.0.2

- Added an About panel, `NOTICE.md`, `LICENSE` (MIT) and `SECURITY.md`.
- Added an inline favicon, Open Graph and Twitter card metadata, and `social-preview.png`.
- Added browser UAT to CI (Playwright) at 1440×900, 390×844 and 320×568.
- Extended `scripts/validate_site.py` to check release files and metadata.

## v1.0.1

- Single-page seven-stage experience with recursive Distillation, hidden Reality and Structure layers, opt-in synthesized sound, Apply with copy and export, local-only persistence, CSP, reduced-motion support and accessibility basics.
- Static validator, checksum manifest, and a CI workflow with pinned Actions.
