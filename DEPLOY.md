# Deploying the Fungal Contamination Checker

The app is a **static page** — `index.html` + `data.js`. To *run* it, only those
two files are needed; everything else (`data/`, `build_data.py`, `README.md`) is
for regenerating and documenting the data. There is no server process, so any
static host works and there is no websocket/localhost class of failure.

## Option A — Caltech Apache user directory (astro.caltech.edu/~aam)

The web root for `astro.caltech.edu/~aam` is typically `~/public_html`
(some hosts use `~/www` — check with `ls ~/public_html ~/www`).

```bash
# on the server: make a folder
ssh aam@astro.caltech.edu 'mkdir -p ~/public_html/fungi'

# from a local checkout: copy the two files it needs
scp index.html data.js aam@astro.caltech.edu:~/public_html/fungi/

# permissions (the usual ~user-dir gotcha)
ssh aam@astro.caltech.edu 'chmod o+x ~ ; chmod 755 ~/public_html ~/public_html/fungi ; chmod 644 ~/public_html/fungi/*'
```

Live at: `https://astro.caltech.edu/~aam/fungi/`
Update later by re-`scp`-ing the two files.

## Option B — GitHub Pages

Push this repo, then Settings → **Pages** → Source *Deploy from a branch* →
**main / (root)** → Save. Live in ~1 min at
`https://<org>.github.io/<repo>/`.

## Option C — local

Double-click `index.html` (keep `data.js` beside it). Runs from `file://`.

## Updating the data

Edit the CSVs under `data/`, then:

```bash
python3 build_data.py     # regenerates data.js
```

Commit the regenerated `data.js` (it is committed on purpose so the page runs
without a build step), and re-deploy per whichever option above.
