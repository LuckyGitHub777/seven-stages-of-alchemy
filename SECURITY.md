# Security

## Design

- It's a static, single-file site (`index.html`) with no server, accounts, analytics, cookies or third-party scripts.
- A Content-Security-Policy (`default-src 'none'`) blocks every network request, remote asset and form submission.
- What you type is stored only in your own browser's `localStorage`. "Begin again" erases it, and so does clearing site data.
- CI pins its GitHub Actions to immutable commit SHAs, runs with read-only permissions, and doesn't persist checkout credentials.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub's **Security → Report a vulnerability** form on this repository. If that form isn't available, open an issue that asks for a private contact without giving any details. Please don't post exploit details publicly before a fix is available.

## Supported versions

Only the latest commit on `main` is supported.
