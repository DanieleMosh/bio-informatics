import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Data substrate — AnnData by hand (PBMC 3K)

    Run in `uv run marimo edit notebooks/0_data_substrate.py`, one cell at a time.
    Rhythm per step: **predict the shape/values, run, reconcile.** Logic lives in
    `dct`; the notebook is the learning surface.

    Needs the `eda` extra: `uv sync --extra eda`.

    **Papers traced** (full list: `docs/papers.md`):
    [Scanpy PBMC 3K tutorial](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html)
    — the workflow below; reproduces the Seurat guided-clustering analysis of
    [Satija et al. 2015](https://doi.org/10.1038/nbt.3192); toolkit is
    [Scanpy, Wolf et al. 2018](https://doi.org/10.1186/s13059-017-1382-0).
    """
    )
    return


@app.cell
def _():
    import numpy as np
    import scanpy as sc

    from dct.data import control_vs_perturbed, describe_anndata

    sc.settings.verbosity = 1
    return control_vs_perturbed, describe_anndata, np, sc


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 1 · Raw AnnData

    `pbmc3k()` is the 10x PBMC dataset (cached). Predict: counts or floats? sparse
    or dense? `X.max()`?
    """
    )
    return


@app.cell
def _(describe_anndata, sc):
    adata = sc.datasets.pbmc3k()
    adata.var_names_make_unique()  # gene symbols repeat; make the index unique
    describe_anndata(adata)
    return (adata,)


@app.cell
def _(adata):
    # X is a CSR matrix of raw UMI counts; obs is empty on a fresh load.
    adata.X[:3, :8].toarray(), adata.X.max()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 2 · QC filtering

    Drop low-quality cells (< 200 genes) and near-absent genes (< 3 cells).
    Predict: how many of 2700 cells and 32738 genes survive?
    """
    )
    return


@app.cell
def _(adata, sc):
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    adata.shape  # (cells, genes) after filtering
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3 · Normalize + log1p — defines the target variable

    `normalize_total` removes sequencing-depth differences (every cell → 10k
    counts); `log1p` takes log(1 + x). A perturbation effect is a **log-fold-
    change** = a difference of these log1p values. Predict: row sum after
    normalize? `X.max()` after log1p?
    """
    )
    return


@app.cell
def _(adata, np, sc):
    sc.pp.normalize_total(adata, target_sum=1e4)
    row_sum_normalized = np.asarray(adata.X.sum(axis=1)).ravel()[:5]  # ~1e4 each
    sc.pp.log1p(adata)
    row_sum_normalized, adata.X.max()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 4 · Highly variable genes

    Flag the 2000 most informative genes (high dispersion at given mean); the rest
    is mostly noise. Predict: flag stored in `obs` or `var`?
    """
    )
    return


@app.cell
def _(adata, sc):
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    adata.raw = adata  # keep log-normalized full-gene matrix before subsetting
    proc = adata[:, adata.var.highly_variable].copy()
    proc.shape
    return (proc,)


@app.cell
def _(adata, sc):
    # The selection rule: dispersion vs. mean, HVGs highlighted.
    sc.pl.highly_variable_genes(adata)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 5 · Scale + PCA

    Z-score each gene (mean 0, unit variance, clipped at 10), then reduce 2000
    genes → 50 PCs. Predict: why is `X` negative after scaling? shape of `X_pca`?
    """
    )
    return


@app.cell
def _(proc, sc):
    sc.pp.scale(proc, max_value=10)  # z-score per gene -> negatives appear
    sc.tl.pca(proc, n_comps=50)
    proc.X.min(), proc.obsm["X_pca"].shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 6 · Neighbors → Leiden → UMAP

    kNN graph on PCA space → Leiden clustering → 2D UMAP embedding. Predict: how
    many clusters at `resolution=0.5`? where do labels (`obs`) and embedding
    (`obsm`) land?
    """
    )
    return


@app.cell
def _(describe_anndata, proc, sc):
    sc.pp.neighbors(proc, n_neighbors=10, n_pcs=40)
    sc.tl.leiden(proc, resolution=0.5, flavor="igraph", n_iterations=2, directed=False)
    sc.tl.umap(proc)
    describe_anndata(proc)
    return


@app.cell
def _(proc, sc):
    sc.pl.umap(proc, color="leiden", legend_loc="on data")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 7 · Label sanity (toward perturb-seq)

    No perturbation column here — `leiden` is a stand-in categorical. Next
    milestone runs the same `control_vs_perturbed` check against the real
    perturbation column of Replogle / Norman.
    """
    )
    return


@app.cell
def _(control_vs_perturbed, proc):
    control_vs_perturbed(proc, label_col="leiden", control_value="0")
    return


if __name__ == "__main__":
    app.run()
