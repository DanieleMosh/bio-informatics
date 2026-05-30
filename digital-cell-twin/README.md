# digital-cell-twin

Bite-sized demos toward a high-fidelity **digital cell twin** — single-cell
perturbation prediction (expression → log-fold-change), as an ML engineer
getting fluent with single-cell biology + Transformer AI.

- **Roadmap:** [`ROADMAP.md`](./ROADMAP.md) — the milestone succession, one
  feature branch + PR each.
- **Conventions (read before coding):** [`CLAUDE.md`](./CLAUDE.md) —
  tooling-by-phase, branch/PR workflow, and the domain correctness guards.

## Layout

```
src/dct/      importable logic (data, eval, baseline) — write each thing once
notebooks/    thin marimo EDA (imports dct, only plots/inspects)
scripts/      run_baseline.py, train.py (fine-tune lives here, never a notebook)
data/         datasets (git-ignored)
docs/         one synthesized note per milestone PR
```

## Tooling by phase

| Phase | Where | Rule |
|---|---|---|
| Logic | `src/dct/*.py` | importable, written once |
| EDA / visuals | `notebooks/*.py` (marimo) | thin; import `dct` and plot |
| Fine-tune / GPU | `scripts/train.py` | never a notebook |
| Eval + baseline | `src/dct/{eval,baseline}.py` | called from both |
| Demo | Streamlit (later) | a script |

## Quickstart

```bash
uv sync                                          # core deps (light)
uv run python scripts/run_baseline.py --smoke    # verify baseline -> eval wiring
uv run marimo edit notebooks/0_data_substrate.py # EDA notebook
```

Heavy deps (`torch`, `scgpt`, `geneformer`, `cell-gears`) are added per-milestone
via `uv add` / `uv pip install`, not up front.
