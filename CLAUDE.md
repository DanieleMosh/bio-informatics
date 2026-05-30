# Repository: bio-informatics

Two independent bodies of work share this repo and its `uv` environment:

- **`Applied Bioinformatics/`** — TU Dresden course labs. marimo notebooks
  (`N_topic.py`), string/sequence exercises. Self-contained; leave it untouched
  unless the task is explicitly about the course.
- **`digital-cell-twin/`** — an ML project: bite-sized demos toward a
  high-fidelity *digital cell twin* (single-cell perturbation prediction,
  expression → log-fold-change). Has its own `pyproject.toml` and ML stack.

Both use `uv` and marimo notebooks.

> **Working in `digital-cell-twin/`? Read `digital-cell-twin/CLAUDE.md` first —**
> it holds the binding conventions (tooling-by-phase, branch/PR workflow, and the
> domain correctness guards).
