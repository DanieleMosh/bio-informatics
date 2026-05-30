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
    # Data substrate — AnnData sanity checks

    Thin EDA notebook: it **imports `dct`** and only plots / inspects.
    No modeling logic lives here (that goes in `src/dct/`). Visuals and fast
    iteration are the whole point of this file.

    Goal for this milestone: live inside AnnData, map its layout
    (`obs / var / X / layers / obsm / uns`), and confirm the perturbation
    labels are really where you think they are.
    """
    )
    return


@app.cell
def _():
    # Logic comes from the package, not from notebook cells.
    from dct.data import control_vs_perturbed, describe_anndata, load_anndata

    return control_vs_perturbed, describe_anndata, load_anndata


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Load a dataset

    Start with the Scanpy PBMC 3K tutorial dataset, then a perturb-seq dataset
    (Replogle / Norman) on the next milestone. Set `PATH` to your `.h5ad`.
    """
    )
    return


@app.cell
def _(describe_anndata, load_anndata):
    # PATH = "data/pbmc3k.h5ad"
    # adata = load_anndata(PATH)
    # layout = describe_anndata(adata)   # paste this output into the chat
    # layout
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Control vs. perturbed

    Once a perturb-seq dataset is loaded, confirm the label column and the
    control/perturbed split before computing any metric.
    """
    )
    return


@app.cell
def _(control_vs_perturbed):
    # control_vs_perturbed(adata, label_col="perturbation", control_value="control")
    return


if __name__ == "__main__":
    app.run()
