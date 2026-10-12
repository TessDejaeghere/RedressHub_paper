# Human Out of the Loop — analysis notebooks

Code and data to reproduce the analyses in *Human Out of the Loop: How Contested Colonial Redress Events
Slip Past Generative LLMs' Confidence Thresholds* (Dejaeghere, Evrard, Pallí-Asperó, Singh & Lefever).

| Notebook | Reproduces |
|---|---|
| [`rq_notebooks/RQ1_contestation_is_systematic.ipynb`](rq_notebooks/RQ1_contestation_is_systematic.ipynb) | Table 1, §2.1 (retrospective hesitancy, duplicate check), §3.1 (RQ1: stratification, recurring boundaries, naming test, regression), Figure *Contestation by stratum* |
| [`rq_notebooks/RQ2_uncertainty_vs_contestation.ipynb`](rq_notebooks/RQ2_uncertainty_vs_contestation.ipynb) | §2.5 (letter-token coverage), Tables 5–6, §3.2 (RQ2), Appendix C robustness tables, model outputs for the §3.3 close-read examples |
| [`rq_notebooks/RQ3_thresholds_and_routing.ipynb`](rq_notebooks/RQ3_thresholds_and_routing.ipynb) | §3.4 (RQ3: .90 threshold, direction of the models' readings), §3.5 (routing, alternative signals), Appendix routing and signal tables, Figures *Outcomes* and *Triage trade-off* |

Every notebook ends with a recap table that maps its outputs to the places in the paper where they are reported.
All analysis code is in the notebooks themselves; they do not import any project modules.

## Running the notebooks

```bash
pip install -r requirements.txt
jupyter lab            # or: jupyter notebook / VS Code
```

Open a notebook and choose *Run All*. The notebooks locate the `ls_real/` folder themselves, so they can be run
from the repository root or from `rq_notebooks/`. Running times on a laptop: RQ1 about 1 minute, RQ2 about
5 minutes (bootstraps), RQ3 about 1 minute. Figures are written to `rq_notebooks/figures/`.

No API calls are made: the LLM outputs were computed once and are stored in `ls_real/`.

## Data

`ls_real/` contains:

* **Label Studio exports** (`export_*.json`): the double-annotated dataset, **without the article texts**.
  Each pair of exports covers the same texts, annotated independently by two annotators. Every span is
  identified by its character offsets in the annotated text, with its label, hesitancy rating, alternative
  label and source of doubt. See *Step 0* in any notebook for how the pools are combined.
* **`texts.csv`**: one row per annotated text, with its source URL, source, language, length in characters
  and a SHA-256 checksum of the exact text that was annotated (so that offsets can be checked against a
  restored text).
* **`duplicate_check.csv`** and **`close_read_examples.csv`**: the cross-pool duplicate check (RQ1 notebook)
  and the positions of the close-read examples (§3.3, RQ2 notebook), precomputed from the full texts.
* **Model scores** (`machine_scores*.csv`): one row per annotated span and model, for three uncertainty measures
  (log-probabilities, ten sampled answers, stated confidence), plus the per-template log-probability scores
  (`machine_scores_templates*.csv`). These files contain no article text.

None of the analyses needs the article texts, so every number in the paper can be reproduced from this
repository as it is. Without the texts, the notebooks show span positions instead of span texts, and the
duplicate check shows its stored result.

Notes on how the data are used (all documented in the notebooks):

* Three spans that an annotator accidentally labelled twice (same span, same label) are counted once.
* One Dutch article was annotated twice, in two different pools (`iaa_nl:285645` and `elke_solo_nl:335223`,
  same URL in `texts.csv`); the notebooks keep the first copy only (`EXCLUDE_TEXTS`), giving 67 distinct texts.
* The stored log-probability `consistency` column was computed per prompt template and then averaged. The
  notebooks recompute this confidence on the template-averaged label distribution, as described in §2.5 of the
  paper; the stored value is kept as `consistency_stored`.

## Article texts and copyright

The articles were scraped from the websites listed in `texts.csv` and remain under the copyright of their
publishers. In line with the paper's data statement, this repository therefore releases them only as URLs
with character offsets, not as full text. The texts are not part of this repository's history either.

Project members who hold the full texts can restore them locally:

```bash
python restore_texts.py path/to/texts_full.json      # or: path/to/folder/with/the/original/exports
```

The script checks every text against its checksum in `texts.csv` and writes `ls_real/texts_full.json`, which
`.gitignore` keeps out of the repository. Never commit that file. Others can retrieve the articles from their
URLs; the checksums show whether a retrieved text is identical to the version that was annotated.
