# Papers — running bibliography

One trail for every paper central to a milestone. Append as you read; each
per-milestone note (`docs/<milestone>.md`) links into the relevant entries here.
Every entry: **author + year**, the one-line claim that matters here, and a
**working link to the paper / source itself**.

Anchor papers not yet reached are listed without notes; fill the one-liner and
confirm the link when the milestone lands (don't cite what you haven't read).

## Data substrate

- **Satija et al. 2015** — spatial reconstruction / guided clustering of
  single-cell RNA-seq; the Seurat PBMC clustering workflow that the Scanpy PBMC
  3K tutorial reproduces.
  <https://doi.org/10.1038/nbt.3192>
- **Scanpy PBMC 3K tutorial** — the canonical preprocess→cluster walkthrough this
  milestone follows (QC → normalize → HVG → PCA → neighbors → Leiden → UMAP).
  <https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html>
- **`sc.datasets.pbmc3k`** — the dataset loader (2700 cells × 32738 genes, 3k
  PBMCs from a healthy donor, 10x Genomics).
  <https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc3k.html>
- **Wolf et al. 2018** — Scanpy itself (the toolkit all of the above runs on).
  <https://doi.org/10.1186/s13059-017-1382-0>

## Perturb-seq + validation target  *(feat/perturb-seq-target — not yet read)*

- **Replogle et al. 2022** — genome-scale Perturb-seq; the validation set.
- **Norman et al. 2019** — combinatorial Perturb-seq; the GEARS dataset.
- **Adamson et al. 2016** — early Perturb-seq (recognize only).

## Geneformer mechanism  *(feat/geneformer-mechanism — not yet read)*

- **Theodoris et al. 2023** — Geneformer; rank-value encoding + native in-silico
  deletion.

## scGPT + GEARS machinery  *(feat/scgpt-gears-machinery — not yet read)*

- **Cui et al. 2024** — scGPT; the expression decoder our head copies.
- **Roohani et al. 2023** — GEARS; closest prior art to the task.

## Critique + linear baseline  *(feat/critique-and-baseline — not yet read)*

- **Ahlmann-Eltze et al. 2025** — the field's main critique (linear baselines
  often match the transformers).
- **Kedzierska et al. 2023** — contests the "latent space is mechanistic" claim.

## Synthesis + eval hierarchy  *(feat/synthesis-eval — not yet read)*

- **CZI Virtual Cells / Open Problems** — the eval frameworks judges recognize.
