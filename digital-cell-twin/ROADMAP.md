# Roadmap — a cohesive succession of milestones

A single arc from data fluency → mechanism → machinery → critique → hands-on →
synthesis. Each milestone is one feature branch → one PR, shipping a demo plus a
synthesized `docs/<milestone>.md`. Read top to bottom; each leans on the last.

---

### 1 · Data substrate → `feat/data-substrate`
You'll live inside AnnData for the rest of this; muscle memory beats theory.
- Scanpy PBMC 3K tutorial (×2).
- Map the AnnData layout (`obs / var / X / layers / obsm / uns`) — your
  perturbation labels and gene vocab live here; you can't debug what you can't
  navigate.
- One CRISPR explainer + one "expression → LFC" model write-up — the minimum to
  not misread your own target variable.
- *Skip Alberts — too slow; that depth is what a recruited biologist is for.*

### 2 · Perturb-seq + validation target → `feat/perturb-seq-target`
- **Replogle 2022** (your validation set) + **Norman 2019** (the GEARS dataset).
  Adamson: just recognize it.
- Load one in code; inspect control vs. perturbed — you can't compute a metric on
  a structure you've never seen.
- Normalization / pseudobulk / dropout basics — these distort fold-change;
  ignorance here silently corrupts your eval.

### 3 · Geneformer mechanism → `feat/geneformer-mechanism`
- Rank-value encoding + native in-silico deletion ("suppression de token").
  This *is* the dossier's deletion mechanism — read it so you implement it right.

### 4 · scGPT + GEARS machinery → `feat/scgpt-gears-machinery`
- scGPT expression decoder — your regression head is copied from it; understand
  the original.
- GEARS (×2) — closest prior art to your exact task; be able to state how you
  differ.
- *Skim CPA, skip scFoundation — good concept, not core to a short build.*

### 5 · Critique + linear baseline → `feat/critique-and-baseline`  *(critical)*
- Ahlmann-Eltze 2025 (×2) — the field's main critique; ignoring it reads as naïve
  to any informed judge.
- Kedzierska + an attention-interpretability paper — they directly contest the
  "latent space is mechanistic" claim.
- **Build the linear baseline yourself** (`src/dct/baseline.py`, already
  stubbed) and run it on the Replogle split — the practitioner litmus test *and*
  your contingency deliverable in one. Report it **next to** the transformer.

### 6 · Real stack hands-on → `feat/real-stack-hands-on`
- GEARS-on-Norman, scGPT fine-tune, Geneformer deletion — the exact patterns
  you'll copy-paste-adapt under time pressure. Run them now, not at hour 12.
- Fine-tune lives in `scripts/train.py`, never a notebook.

### 7 · Synthesis + eval hierarchy → `feat/synthesis-eval`
- CZI Virtual Cells + Open Problems — the eval frameworks judges recognize;
  speaking their language buys credibility.
- Lock the eval hierarchy: **ID < OOD-pert < OOD-cell-type** — decide which one
  your "digital twin" claim honestly tests.

---

## Skipped on purpose
STATE et al. (Stage 8), most of Stage 1, KEGG/STRING internals, Seurat,
Discord/X — zero payoff for this project. Documented so the boundary is a choice,
not an oversight.
