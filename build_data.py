#!/usr/bin/env python3
"""Regenerate data.js (embedded database) from the CSVs in data/.

The app is a single static page: index.html + data.js. All data is baked
into data.js so the page runs from file:// or any static host with no
server. Run this whenever the source CSVs under data/ change:

    python3 build_data.py

Inputs  (data/):
  curated_fungi_both.csv   Phyla, Species, + six 0/1/2 property scores
  synonyms.csv             alias, canonical_name, ...
  samples/*.csv            example input datasets shown in the dropdown
Output:
  data.js                  window.CURATED / window.SYNONYMS / window.SAMPLES
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SAMPLE_LABELS = {
    "lab_culture.csv": "Lab cell culture",
    "iss_environment.csv": "ISS surface microbiome",
    "hospital_icu.csv": "Hospital ICU air sampling",
}


def build():
    curated = []
    with open(os.path.join(DATA, "curated_fungi_both.csv")) as f:
        for r in csv.DictReader(f):
            curated.append([
                r["Phyla"], r["Species"],
                int(r["antimicrobial-resistance"]), int(r["Biofilm-formation"]),
                int(r["Human-pathogenicity"]), int(r["Thermophile"]),
                int(r["Radiation-resistance"]), int(r["Spore-formation"]),
            ])

    synonyms = []
    with open(os.path.join(DATA, "synonyms.csv")) as f:
        for r in csv.DictReader(f):
            synonyms.append([
                r["alias"], r["canonical_name"],
                r.get("current_accepted_name", ""), r.get("relationship", ""),
            ])

    samples = {}
    for fn, label in SAMPLE_LABELS.items():
        with open(os.path.join(DATA, "samples", fn)) as f:
            samples[label] = f.read()

    out = (
        "window.CURATED=%s;\nwindow.SYNONYMS=%s;\nwindow.SAMPLES=%s;\n" % (
            json.dumps(curated, separators=(",", ":")),
            json.dumps(synonyms, separators=(",", ":"), ensure_ascii=False),
            json.dumps(samples, ensure_ascii=False),
        )
    )
    with open(os.path.join(HERE, "data.js"), "w") as f:
        f.write(out)

    print(f"wrote data.js — {len(curated)} organisms, {len(synonyms)} synonyms, "
          f"{len(samples)} samples ({os.path.getsize(os.path.join(HERE, 'data.js'))} bytes)")


if __name__ == "__main__":
    build()
