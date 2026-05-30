# Data substrate

Milestone 1 of [ROADMAP](../ROADMAP.md). Goal: live inside AnnData, map its
layout, and pin down the target variable (expression → log-fold-change) before
touching a model.

## What I built

- `notebooks/0_data_substrate.py` — runs the standard Scanpy PBMC 3K pipeline
  (QC → normalize → log1p → 2000 HVGs → scale → PCA → neighbors → Leiden →
  UMAP), prints the layout at each stage via `dct.data.describe_anndata`, and
  plots the UMAP colored by cluster.
- Graph-clustering deps moved to an opt-in `eda` extra in `pyproject.toml`
  (core stays light): `uv sync --extra eda`.

## AnnData layout map (the point of this milestone)

| Slot | Holds | Example here |
|---|---|---|
| `X` | the expression matrix (cells × genes) | raw counts (CSR, `float32`); after preprocessing, scaled `float64` |
| `obs` | per-**cell** metadata (rows) | `n_genes`, `leiden` — **perturbation labels live here** |
| `var` | per-**gene** metadata (cols) | `gene_ids`, `highly_variable`, `means`, … |
| `layers` | alt matrices, same shape as `X` | (none yet; e.g. `counts`, `lognorm`) |
| `obsm` | per-cell multi-dim arrays | `X_pca`, `X_umap` (embeddings) |
| `uns` | unstructured run metadata | `log1p`, `hvg`, `pca`, `neighbors`, `leiden`, `umap` |

`adata.raw` stashes the log-normalized full-gene matrix before subsetting to
HVGs, so per-gene expression stays recoverable.

## Key shapes / results (real, from the run)

- **Raw:** `2700 cells × 32738 genes`; `X` CSR raw counts, max ≈ 419; `obs` empty;
  `var = [gene_ids]`.
- **Processed:** `2700 × 2000` HVGs; `obs = [n_genes, leiden]`;
  `obsm = [X_pca, X_umap]`; `uns = [log1p, hvg, pca, neighbors, leiden, umap]`.
- **Leiden:** 7 clusters (`0`–`6`). Label-sanity check (leiden as a stand-in
  categorical, cluster `0` as mock control): `{control: 1204, perturbed: 1496,
  n_perturbations: 7}`.

## CRISPR + expression → LFC (target-variable primer)

- A **perturbation** here = a CRISPR knockdown/knockout of one gene (CRISPRi/a or
  KO) applied to a cell; **perturb-seq** then reads out that cell's full
  transcriptome.
- The **target variable** is the **log-fold-change (LFC)** of each gene's
  expression: `LFC_g = log(expr_g | perturbed) − log(expr_g | control)`. Because
  the matrix is already `log1p`, an LFC is a *difference of log-normalized
  values* — most genes sit near zero; only a handful move.
- That's why eval (`dct.eval.compute_spearman_top100`) scores correlation over
  the **top-DE genes**, not the full ~20k vocab — a full-vector metric is
  dominated by the silent majority.

## How to verify

```bash
uv sync --extra eda
MPLBACKEND=Agg uv run python notebooks/0_data_substrate.py   # runs clean, prints both layouts
uv run marimo edit notebooks/0_data_substrate.py             # interactive, shows the UMAP
```

## What's next

`feat/perturb-seq-target`: load Replogle 2022 (validation) / Norman 2019 (GEARS
dataset), find the **real** perturbation column in `obs`, and run the same
`control_vs_perturbed` check against it — this time with a genuine control value.
Then normalization / pseudobulk / dropout basics, since those distort the LFC the
eval depends on.
