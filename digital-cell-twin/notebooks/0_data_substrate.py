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
    # Data substrate — AnnData sanity checks (PBMC 3K)

    Thin EDA notebook: it **imports `dct`** and runs the standard Scanpy PBMC 3K
    pipeline so we can live inside AnnData and map its layout
    (`obs / var / X / layers / obsm / uns`).

    Run order matters in marimo only through cell *dependencies*, not position —
    each cell declares what it needs as arguments.

    Needs the `eda` extra (graph clustering): `uv sync --extra eda`.
    """
    )
    return


@app.cell
def _():
    import scanpy as sc

    # Logic comes from the package, not from notebook cells.
    from dct.data import control_vs_perturbed, describe_anndata

    sc.settings.verbosity = 1
    return control_vs_perturbed, describe_anndata, sc


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 1 · Raw AnnData

    `sc.datasets.pbmc3k()` downloads the 10x PBMC 3K dataset (cached locally).

    **Real raw shape:** `2700 cells × 32738 genes`, `X` is a CSR sparse matrix of
    **raw counts** (`float32`, max ≈ 419). `obs` is empty; `var` only has
    `gene_ids`. This is the ground truth — print it, don't assume it.
    """
    )
    return


@app.cell
def _(describe_anndata, sc):
    adata = sc.datasets.pbmc3k()
    adata.var_names_make_unique()
    describe_anndata(adata)
    return (adata,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 2 · Standard preprocessing

    QC filter → normalize to 10k counts → `log1p` → 2000 highly-variable genes →
    scale → PCA. We stash the log-normalized full matrix in `adata.raw` before
    subsetting to HVGs (so per-gene expression stays recoverable).

    Note the target variable lens for later: a perturbation's effect is a
    **log-fold-change** of expression — i.e. a difference of `log1p` values.
    """
    )
    return


@app.cell
def _(adata, sc):
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    adata.raw = adata
    proc = adata[:, adata.var.highly_variable].copy()
    sc.pp.scale(proc, max_value=10)
    sc.tl.pca(proc, n_comps=50)
    return (proc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 3 · Neighbors → Leiden → UMAP

    **Real processed layout** after this cell: `2700 × 2000`,
    `obs = [n_genes, leiden]` (7 clusters, 0–6),
    `obsm = [X_pca, X_umap]`,
    `uns = [log1p, hvg, pca, neighbors, leiden, umap]`.

    This is the map: cluster labels land in `obs`, embeddings in `obsm`, run
    params in `uns`. Perturbation labels would live in `obs` too.
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
    # The payoff plot: clusters in the 2D UMAP embedding.
    sc.pl.umap(proc, color="leiden", legend_loc="on data")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 4 · Label sanity (toward perturb-seq)

    PBMC 3K has no perturbation column — `leiden` stands in as the categorical
    label here. On the next milestone (`feat/perturb-seq-target`) the same
    `control_vs_perturbed` check runs against the real perturbation column of
    Replogle / Norman, where one value is the control.
    """
    )
    return


@app.cell
def _(control_vs_perturbed, proc):
    # leiden as a stand-in categorical; no single "control" value here.
    control_vs_perturbed(proc, label_col="leiden", control_value="0")
    return


if __name__ == "__main__":
    app.run()
