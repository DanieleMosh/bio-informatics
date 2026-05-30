"""Run the ridge baseline and print a metrics table.

Usage:
    uv run python scripts/run_baseline.py --smoke          # synthetic data, no dataset
    uv run python scripts/run_baseline.py --data path.h5ad # (TODO) real Replogle split

The --smoke path exists so the wiring (baseline -> eval -> table) is verifiable
before any real dataset is downloaded.
"""

from __future__ import annotations

import argparse

import numpy as np

from dct.baseline import RidgeBaseline
from dct.eval import summarize


def smoke() -> dict:
    """Fit ridge on a tiny random X->y and return the metrics dict."""
    rng = np.random.default_rng(0)
    n, d, n_genes = 200, 50, 300
    X = rng.normal(size=(n, d))
    W = rng.normal(size=(d, n_genes))
    y = X @ W + 0.1 * rng.normal(size=(n, n_genes))

    split = n // 2
    model = RidgeBaseline(alpha=1.0).fit(X[:split], y[:split])
    pred = model.predict(X[split:])
    return summarize(pred, y[split:])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ridge baseline.")
    parser.add_argument("--smoke", action="store_true", help="run on synthetic data")
    parser.add_argument("--data", type=str, default=None, help="path to .h5ad (TODO)")
    args = parser.parse_args()

    if args.smoke:
        metrics = smoke()
    else:
        # TODO (critique-and-baseline milestone): load the real Replogle split,
        # build X/y, fit, predict, summarize. Report this NEXT TO the transformer.
        raise SystemExit("Real-data path not implemented yet. Use --smoke for now.")

    print("=== ridge baseline metrics ===")
    for name, value in metrics.items():
        print(f"  {name:18s} {value:.4f}")


if __name__ == "__main__":
    main()
