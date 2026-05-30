"""Fine-tune entrypoint (scGPT-style expression head).

This is a SCRIPT on purpose. The fine-tune must never live in a notebook:
we want checkpointing, a detachable long-running job, and logged runs. A
fine-tune tied to a Jupyter/marimo kernel is a hung session waiting to happen.

Dossier reminders baked in here:
  * Prefer scGPT as the backbone for a *value-based* regression head
    (Geneformer is rank-based -- it does not natively emit expression values).
  * The output dim must equal the model's REAL gene vocab, not a round 20,480.
    Verify the actual hidden dim and vocab size before wiring the head.

Filled in on the real-stack-hands-on milestone.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune the expression head.")
    parser.add_argument("--data", type=str, required=False, help="path to training .h5ad")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints/")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()

    # TODO (real-stack-hands-on milestone):
    #   1. Load AnnData; VERIFY real shapes (hidden dim, gene vocab) -- print them.
    #   2. Build scGPT backbone + LayerNorm -> Linear -> ReLU -> Linear head
    #      with out_features == real gene vocab.
    #   3. Training loop with checkpointing to args.checkpoint_dir.
    #   4. Log metrics via dct.eval.summarize each eval step.
    raise SystemExit("Fine-tune not implemented yet (real-stack-hands-on milestone).")


if __name__ == "__main__":
    main()
