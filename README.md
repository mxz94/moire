
<div align="center">
  <img src="images/icon.svg" width="120" height="auto" alt="Moire Logo">
  <br/>
  <br/>
  <h1>Moire</h1>
  <p>
    Sync your thoughts from Apple Notes to GitHub Pages by Shortcuts.
  </p>
  <p>
    <a href="https://moire.blog">Moire</a> &nbsp;&nbsp;|&nbsp;&nbsp; <a href="https://docs.moire.blog">Docs</a> &nbsp;&nbsp;|&nbsp;&nbsp; <a href="https://themes.moire.blog">Themes</a>
  </p>
  <br/>
  <img src="images/moire.png" width="100%" alt="Moire Preview">
</div>

<br/>

## Introduction

Moire is a tool designed to seamlessly synchronize your thoughts from Apple Notes using Shortcuts.

## Features

- **Seamless Sync**: Direct integration with Apple Notes via Shortcuts.
- **Markdown Export**: Convert your notes to Markdown format. Easy to migrate.
- **Static Generator**: A Python script (`scripts/generate.py`) reads `src/memos/**/*.md` and renders a single dense, dated HTML log (`build/index.html`) — no Node build step required.

## Development

### Prerequisites

- Python 3.11+
- `markdown` (`pip install markdown`)

### Generate the site

```bash
python scripts/generate.py      # -> build/index.html
```

### Preview locally

```bash
pnpm dev                        # serves build/ at http://localhost:5173
```

### Deploy

`deploy.yml` runs `python scripts/generate.py` on push to `main` and publishes `build/` to GitHub Pages.

## License

This project is licensed under the GPL-3.0 License.
