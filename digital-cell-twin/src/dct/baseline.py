"""Linear (ridge) baseline: control expression -> perturbation log-fold-change.

Why this exists, prominently: the field's main critique (Ahlmann-Eltze 2025) is
that transformer "digital twins" often fail to beat a simple linear baseline.
So we build the baseline FIRST and report it *next to* the transformer on the
*same* Replogle split -- not buried in an appendix.

Shape convention:
    X : (n_samples, n_features)  -- control / context features (e.g. mean control
                                    expression, perturbation one-hot, or both)
    y : (n_samples, n_genes)     -- target log-fold-change per gene
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import Ridge


class RidgeBaseline:
    """Thin multi-output ridge wrapper. sklearn's Ridge is natively multi-output,
    so one estimator predicts the full LFC vector."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.model = Ridge(alpha=alpha)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RidgeBaseline":
        """Fit on the training split. X: (n, d), y: (n, n_genes)."""
        self.model.fit(np.asarray(X), np.asarray(y))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict LFC. Returns (n, n_genes)."""
        return self.model.predict(np.asarray(X))
