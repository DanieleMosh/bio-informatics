"""Evaluation metrics for perturbation prediction (expression -> LFC).

Write each metric ONCE here; import it from notebooks and scripts alike.
Do not reimplement Spearman/Pearson in three different cells.

Shape convention (state it, then trust it):
    pred, truth : np.ndarray, shape (n_perturbations, n_genes)
        Predicted vs. measured log-fold-change per gene, per perturbation.
        Rows align (same perturbation order); columns align (same gene order).

The canonical perturb-seq metric is correlation over the *top differentially
expressed* genes, not over the full ~20k vocab -- most genes don't move, so a
full-vector correlation is dominated by noise near zero.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import pearsonr, spearmanr


def _check_shapes(pred: np.ndarray, truth: np.ndarray) -> None:
    pred = np.asarray(pred)
    truth = np.asarray(truth)
    if pred.shape != truth.shape:
        raise ValueError(f"pred {pred.shape} != truth {truth.shape}")


def compute_spearman_top100(pred: np.ndarray, truth: np.ndarray, k: int = 100) -> float:
    """Mean Spearman correlation over the top-`k` DE genes, averaged across perturbations.

    Top-k is chosen per row by |truth| (the genes that actually moved in the
    measurement). Returns the mean Spearman across all rows.
    """
    _check_shapes(pred, truth)
    pred = np.asarray(pred)
    truth = np.asarray(truth)
    if pred.ndim == 1:  # single perturbation -> treat as one row
        pred = pred[None, :]
        truth = truth[None, :]

    rhos: list[float] = []
    k = min(k, truth.shape[1])
    for p_row, t_row in zip(pred, truth):
        top = np.argsort(np.abs(t_row))[-k:]
        rho, _ = spearmanr(p_row[top], t_row[top])
        if not np.isnan(rho):
            rhos.append(float(rho))
    return float(np.mean(rhos)) if rhos else float("nan")


def compute_pearson_delta(pred: np.ndarray, truth: np.ndarray) -> float:
    """Mean Pearson correlation of the LFC vectors, averaged across perturbations.

    TODO: decide whether to restrict to DE genes here too; for now full-vector.
    """
    _check_shapes(pred, truth)
    pred = np.asarray(pred)
    truth = np.asarray(truth)
    if pred.ndim == 1:
        pred = pred[None, :]
        truth = truth[None, :]
    rs = []
    for p_row, t_row in zip(pred, truth):
        r, _ = pearsonr(p_row, t_row)
        if not np.isnan(r):
            rs.append(float(r))
    return float(np.mean(rs)) if rs else float("nan")


def mse(pred: np.ndarray, truth: np.ndarray) -> float:
    """Plain mean-squared error over all entries."""
    _check_shapes(pred, truth)
    return float(np.mean((np.asarray(pred) - np.asarray(truth)) ** 2))


def summarize(pred: np.ndarray, truth: np.ndarray) -> dict[str, float]:
    """Aggregate the headline metrics into one dict for logging / result tables."""
    return {
        "spearman_top100": compute_spearman_top100(pred, truth),
        "pearson_delta": compute_pearson_delta(pred, truth),
        "mse": mse(pred, truth),
    }
