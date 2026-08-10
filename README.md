# Fungal Contamination Checker

A browser-based tool for predicting fungal contaminants relevant to spacecraft
and space-health. It matches a species list against **1,553 curated fungi**,
each scored on six contamination-relevant properties, and flags likely
contaminants with interactive charts.

**It is a single static page** — `index.html` + `data.js`. There is no server,
no build step to view it, and no data leaves the browser. Open it by
double-clicking `index.html`, or host it anywhere static (e.g. GitHub Pages).

## Live

**Try it:** https://sites.astro.caltech.edu/checkfungalcontam/

## Use it

- **Locally:** open `index.html` in any browser (keep `data.js` beside it).
- **Hosted:** serve the folder as a static site; the entry point is `index.html`.

Pick a bundled sample dataset or choose **Paste / upload CSV…** to supply your
own. Input format:

```
#Datasets,loc1,loc2,loc3
Candida albicans,200,1240,0
Aspergillus sp.,300,4240,0
Candidozyma auris,150,0,80
```

- First column: species name (the header cell is just a label).
- Remaining columns: read counts per location (any column names).

## How scoring works

Each organism is annotated for six properties — antimicrobial resistance,
biofilm formation, human pathogenicity, thermophily, radiation resistance,
spore formation. Evidence per property is `0` (none), `1` (≥35% protein
identity) or `2` (≥75%).

- **A-score** (depth) = Σ weight × evidence
- **S-score** (breadth) = number of contributing properties
- A species is **flagged** when A-score ≥ the A-score threshold **and** at least
  one location has reads ≥ the reads threshold.

Name handling: genus-level inputs (`Candida sp.`) expand to all curated species
in that genus (aggregated by max/mean/sum); different names for one organism
(synonyms) have their reads **summed**; the same name repeated keeps the
**larger** read count per location.

## Data & regenerating `data.js`

`data.js` is generated from the CSVs in `data/`:

```
data/curated_fungi_both.csv   Phyla, Species, + six 0/1/2 property scores
data/synonyms.csv             alias / canonical_name / current_accepted_name
data/samples/*.csv            example input datasets
```

After editing any of those, regenerate the embedded database:

```bash
python3 build_data.py
```

## Credits

- **Concept:** Ashish Mahabal (Caltech), Nitin K. Singh
- **Domain expertise:** Swati Bijlani (COH), Nitin K. Singh
- **Coding:** Vannsh Jani (Caltech VURP ’25), Ashish Mahabal

Supported in part by the Translational Research Institute for Space Health
(TRISH), a NASA-funded consortium, through the Caltech Space-Health Innovation
Fund (CSIF). Loosely based on a similar tool built for bacteria
([checkcontam.streamlit.app](https://checkcontam.streamlit.app)).
