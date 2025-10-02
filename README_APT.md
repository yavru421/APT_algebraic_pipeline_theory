# APT (Algebraic Pipeline Theory) — Core README

This repository contains experiments and reference code for APT (Algebraic Pipeline Theory).
If this felt like a messy application, that's because historical experiments, demos, and utility code accumulated.
This document states a clear, minimal purpose and a pragmatic plan to turn this repo into a clean, methodology-first project.

Purpose (one sentence)
- APT is a methodology for specifying, composing, executing, and auditing computational pipelines using algebraic notation and explicit module contracts.

Minimal deliverables for a clear APT artifact
- A small, well-documented core (theory + DSL) that fits in `apt_core/`:
  - `specs/` — declarative pipeline examples (YAML/JSON) derived from your OpenAPI (like `llama-chat-completions.yaml`).
  - `executor/` — minimal, auditable executor that turns specs into runs and emits snapshots (no production features)
  - `docs/` — concise methodology documentation, proofs, and examples
  - `tests/` — reproducible unit tests focused on the methodology

Keep everything else experimental
- Move production helpers, telemetry, and heavy demos into `experimental/` so the core remains small and undeniable.

Security & privacy
- Keep API keys and secrets out of the repo. Use `.env` locally or CI secrets. Consider making the repo private if you want to publish later.

Next steps you can ask me to do now (pick one)
1) Create `apt_core/` and move minimal files there (I will not delete anything; I'll copy/organize and leave `experimental/` with existing code). This creates a tidy core and keeps experiments.
2) Produce a small, formal DSL schema and a README example showing how `llama-chat-completions.yaml` maps to it.
3) Make the repo clearly methodology-first: add `docs/APT_CORE.md` (I will create it) and move all non-core files into `experimental/`.
4) Make a private branch and create a minimal public README that hides experimental bits — useful before making the repo public.

If you'd like me to act, say which option (1-4). I recommend (3): create the `docs/APT_CORE.md` and move non-core files into `experimental/` so your public face is focused and clean.
