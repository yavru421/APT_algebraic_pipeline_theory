# Copilot Instructions for APT Algebraic Pipeline Theory Workspace (UPDATED)

## Purpose
This document prescribes how the automated coding assistant (Copilot) should behave when operating inside the APT (Algebraic Pipeline Theory) workspace. It enforces the APT Chat Mode constraints: pipelines must be expressed algebraically, modules indexed, inputs/outputs explicit, and all interactions traceable and reproducible.

## Core Principles
- Modular algebraic pipelines: represent every pipeline as a composition of indexed modules m1, m2, ..., mk, where each module mi has an explicit input tuple Xi and output Yi and a well-defined transformation fi: Yi = fi(Xi).
- Explicit variable definitions: every symbol (xi, yi, parameters) must be defined before use. Use indexed notation (x1, x2, y1, y2) and snapshot outputs when useful.
- Pipeline equation: represent the full pipeline as a single algebraic expression when possible, e.g. Y = mk(...m2(m1(X))). This equation plus the environment deterministically defines outputs.
- Traceability and reproducibility: for every module execution record (mi, inputs, output, timestamp, environment) and store snapshots in `snapshot` utilities where applicable.

## Developer Workflows (enforced)
- Execution: run pipeline entrypoints in `scripts/` or `apt_pipeline_pkg/pipeline.py`. When proposing or editing runnable code, include a minimal runner and usage example.
- Testing: provide at least one unit test for new or modified modules (happy path + 1 edge case). Place tests under `tests/` or `scripts/tests/` and ensure they run with the repository's test runner.
- Archival: store heavyweight outputs in `archive/` or `results/` (ignored by git). Provide helper functions to save and verify snapshots.
- Documentation: update `docs/` and include algebraic equations describing module behavior and dependencies.

## Required Conventions (formatting & content)
- Module naming and indexing: name modules with an index prefix where possible (e.g., `m1_base64_encode.py`) and document the mapping in module docstrings.
- Function contracts: each module must declare its contract in 2–4 bullets: inputs (names/types), outputs (names/types), error modes, and success conditions.
- Algebraic pipeline header: top-level pipeline files must include a short header showing the pipeline equation. Example:

  # Pipeline equation
  # y_final = m4(m3(m2(m1(x_image, x_meta), x_prompt), x_config))

- YAML DSL: When describing pipelines in metadata or configs, prefer a compact YAML DSL that binds inputs to module outputs. Example:

  pipeline:
    - name: m1
      fn: base64_encode_image
      inputs: { image: x1 }
      output: y1
    - name: m2
      fn: build_payload
      inputs: { image_b64: y1, prompt: x2 }
      output: y2

- Logging & telemetry: use `apt_pipeline_pkg/snapshot.py` and `telemetry_mysql.py` where available; otherwise add structured logs for each module step.

## APT Chat Mode Constraints (for Copilot responses)
- Always present pipeline logic using algebraic notation and explicit variable binders. Example: y2 = m2(m1(x1)).
- Provide an execution contract before running or editing code: list required inputs, modules, pipeline equation, and success criteria.
- No implicit assumptions: if a required variable or configuration is missing, either infer a single reasonable default and state it, or ask a clarifying question.
- Trace each step: for any code change that modifies pipeline behavior, list (mi, inputs, outputs) for each affected module.
- Reproducibility: Include required environment details (Python version and key packages) for runnable changes and add or update `requirements.txt` entries if adding dependencies.

## Examples & Templates
- Pipeline header example (place near top of pipeline files):

  # Equation: y_final = m5(m4(m3(m2(m1(x_image, x_prompt), x_config))))
  # Contract:
  # - Inputs: x_image: bytes, x_prompt: str
  # - Outputs: y_final: dict

- Module docstring template:

  """
  m2_build_payload

  Contract:
    Inputs: image_b64: str, prompt: str
    Outputs: payload: dict
    Errors: Raises ValueError for missing prompt, TypeError for invalid image
  Algebraic: y2 = m2(x1 = y1, x2 = x_prompt)
  """

- YAML DSL snippet (as above) — use this for pipeline config files.

## Key Files & Directories
- `scripts/`, `apt_pipeline_pkg/`: pipeline logic and runners
- `apt_pipeline_pkg/snapshot.py`: snapshot & trace utilities (use to record mi runs)
- `docs/`: documentation and algebraic proofs
- `archive/`, `results/`: binary or heavyweight outputs

## Small automation & safety notes
- When editing repository files, ensure changes are small, documented, and include tests. Avoid large refactors without opening an issue first.
- For any change that introduces external network calls or secrets handling, add clear comments about credentials and do not hardcode secrets.

---

For new modules or changes: follow the algebraic documentation and modular structure, include a pipeline header and contract, add a unit test, and snapshot outputs for reproducibility.
