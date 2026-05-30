"""AnnData load + inspection helpers.

Purpose: make it trivial to print the *real* shapes and layout before writing
any modeling code. Half the silent bugs in this space are shape/vocab
mismatches (e.g. assuming a 768 hidden dim or a round 20,480 gene vocab that
isn't the model's actual vocab). Look first, model second.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # keep anndata import lazy so `import dct.data` is cheap
    from anndata import AnnData


def load_anndata(path: str) -> "AnnData":
    """Load an .h5ad file into an AnnData object."""
    import anndata

    return anndata.read_h5ad(path)


def describe_anndata(adata: "AnnData") -> dict:
    """Print and return the layout: obs/var/X/layers/obsm/uns + their shapes.

    Paste this output into the chat before asking for modeling code.
    """
    info = {
        "n_obs": int(adata.n_obs),
        "n_vars": int(adata.n_vars),
        "X_dtype": str(adata.X.dtype),
        "obs_columns": list(adata.obs.columns),
        "var_columns": list(adata.var.columns),
        "layers": list(adata.layers.keys()),
        "obsm": list(adata.obsm.keys()),
        "uns": list(adata.uns.keys()),
    }
    print(f"AnnData: {info['n_obs']} cells x {info['n_vars']} genes  (X dtype {info['X_dtype']})")
    print(f"  obs cols : {info['obs_columns']}")
    print(f"  var cols : {info['var_columns']}")
    print(f"  layers   : {info['layers']}")
    print(f"  obsm     : {info['obsm']}")
    print(f"  uns      : {info['uns']}")
    return info


def control_vs_perturbed(adata: "AnnData", label_col: str, control_value: str = "control") -> dict:
    """Count control vs. perturbed cells using `obs[label_col]`.

    Returns {"control": n, "perturbed": n, "n_perturbations": k}.
    """
    if label_col not in adata.obs.columns:
        raise KeyError(f"{label_col!r} not in obs columns: {list(adata.obs.columns)}")
    labels = adata.obs[label_col]
    n_control = int((labels == control_value).sum())
    summary = {
        "control": n_control,
        "perturbed": int(len(labels) - n_control),
        "n_perturbations": int(labels.nunique()),
    }
    print(summary)
    return summary
