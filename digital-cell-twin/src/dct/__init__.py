"""dct — digital-cell-twin.

Shared, importable logic for the single-cell perturbation-prediction demos.
Notebooks and scripts import from here; logic does NOT live in notebooks.

Modules:
    data     -- AnnData load / inspection helpers (feed Claude real shapes early)
    eval     -- metrics (Spearman over top-DE genes, etc.); written once, reused
    baseline -- ridge expression->LFC baseline (the practitioner litmus test)
"""

__version__ = "0.0.1"
