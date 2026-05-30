# digital-cell-twin — working conventions

## Goal

Get fluent, by building **bite-sized demos**, with single-cell biology +
Transformer AI for a high-fidelity **digital cell twin**. The concrete task is
**perturbation prediction**: given a cell's state, predict the
**log-fold-change (LFC)** in gene expression caused by a (CRISPR) perturbation.

Progress follows a **cohesive succession of milestones** — see `ROADMAP.md`.
Each milestone is one feature branch → one PR.

## Tooling by phase (match the tool to the phase)

| Phase | Where it lives | Rule |
|---|---|---|
| Logic (data ops, models, utils) | `src/dct/*.py` | Importable modules. Write each thing once. |
| EDA / visuals (UMAPs, label sanity, "is it in `obs`?") | `notebooks/*.py` (marimo) | Thin: **import `dct` and plot**. No real logic, no stateful tangles. |
| Fine-tune / GPU work | `scripts/train.py` | **Never a notebook.** Checkpointing, detachable jobs, logged runs. |
| Eval + linear baseline | `src/dct/eval.py`, `src/dct/baseline.py` | Called from both notebook and scripts. |
| Demo | Streamlit script (later) | Already a script; what judges expect. |

Why this pairs well with Claude: `.py` files edit cleanly (precise string
replaces), diff sanely, and merge normally across parallel branches. `.ipynb` is
JSON — awkward edits, horrible diffs, merge hell. marimo notebooks are pure
`.py`, so they get the same benefits *and* avoid Jupyter's stale-state bug.

## Working with Claude

- **Feed real shapes early.** Before asking for modeling code, paste the actual
  `adata.obs` columns, `var` size, and the model's hidden dim / gene vocab.
  Use `dct.data.describe_anndata(adata)` and paste its output. This is what
  kills silent shape bugs *before* runtime.
- Prefer `.py` over `.ipynb`. Keep logic in modules; the notebook just imports.

## Three correctness guards (highest leverage — do not skip)

1. **Backbone choice.** Geneformer is **rank-based** — it does not natively emit
   expression values. Your head is **value-based**
   (`LayerNorm → Linear → ReLU → Linear`), so **scGPT** fits it far better.
   Pick the backbone knowing this.
2. **Verify real dimensions day one.** Geneformer's hidden dim is **not** 768,
   and the output dim must equal the model's **real** gene vocab — **not** a
   round 20,480. Print the actual numbers before wiring any head.
3. **Lead with the baseline, don't bury it.** Show the ridge baseline
   *next to* Geneformer/scGPT on the **same** Replogle split. This pre-empts the
   field's biggest critique (Ahlmann-Eltze 2025) instead of walking into it.

## Feature-branch + PR workflow

One branch + one PR **per milestone** (1:1 with `ROADMAP.md`):

```
feat/data-substrate
feat/perturb-seq-target
feat/geneformer-mechanism
feat/scgpt-gears-machinery
feat/critique-and-baseline
feat/real-stack-hands-on
feat/synthesis-eval
```

Each PR ships:
- the demo code / notebook for that milestone,
- any new helpers in `src/dct/`,
- a concise synthesis note at `docs/<milestone>.md`.

**PR body template:**

```
## Goal
## What I built
## Key shapes / results
## Papers
## How to verify
## What's next
```

## Synthesis / notebook style

`docs/<milestone>.md` is markdown-notebook style: **terse, results-forward**.
State what was done, the real shapes/numbers, the results, the papers (linked),
and what you'd verify next. No filler.

## Environment

Separate `pyproject.toml` here (the course labs keep the lightweight root env).
Core deps stay light; heavy/finicky deps (`torch`, `scgpt`, `geneformer`,
`cell-gears`) are added **per-milestone** via `uv add` / `uv pip install`, not
forced on every branch.

```
uv sync                                   # install core deps
uv run python scripts/run_baseline.py --smoke   # verify wiring
uv run marimo edit notebooks/0_data_substrate.py
```

## Out of scope (don't get pulled in)

STATE et al. (Stage 8), most of Stage 1, KEGG/STRING internals, Seurat,
Discord/X. Zero payoff for this project.
