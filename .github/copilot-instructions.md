# Copilot Instructions for APT Algebraic Pipeline Theory Workspace

## Purpose
This document guides AI coding assistants in the APT (Algebraic Pipeline Theory) workspace. Enforce APT principles: pipelines as algebraic equations with indexed modules, explicit I/O, traceability, and reproducibility.

## Core Principles
- **Modular Pipelines**: Represent pipelines as compositions m_k(...m_2(m_1(X))), where each m_i has defined inputs X_i, outputs Y_i, and transformation f_i: Y_i = f_i(X_i).
- **Explicit Variables**: Define all symbols (x_i, y_j) before use. Use indexed notation and snapshot outputs.
- **Fatal Enforcement**: Exceptions are unrecoverable (⊥). No graceful failures; halt execution immediately with traceback.
- **Traceability**: Record every execution (m_i, inputs, output, timestamp, env) using snapshot utilities.

## Developer Workflows
- **Execution**: Run pipelines via APT_PIPELINE.yaml and apt_pipeline_pkg/executor.py. For testing, use test_pipeline.py or pytest.
- **Testing**: Add unit tests for modules (happy path + edge case) in APT_MODULES/tests/. Run with pytest.
- **Archival**: Store outputs in APT_PIPELINE_RUNS/ or archive/. Use snapshot.py for traces.
- **Documentation**: Update docs/ with algebraic equations and module contracts.

## Required Conventions
- **Module Naming**: m{index}_{descriptive}.py (e.g., m1_base64_encode.py). Include contract in docstring.
- **Contracts**: 2-4 bullets: Inputs (name:type), Outputs (name:type), Errors, Success criteria.
- **Pipeline Headers**: Include equation like # y_final = m4(m3(m2(m1(x_image, x_prompt))))
- **YAML DSL**: Use in APT_PIPELINE.yaml for module bindings, e.g., args: {image_b64: $m1}
- **Logging**: Use apt_pipeline_pkg/snapshot.py and telemetry_mysql.py for traces.

## APT Constraints
- Present logic algebraically: y2 = m2(m1(x1)).
- Provide execution contract: inputs, equation, success criteria.
- No implicit assumptions; infer defaults or ask.
- Trace changes: list affected (m_i, inputs, outputs).
- Reproducibility: Specify env (Python version, packages from requirements.txt).

## Examples
- **Module Contract** (from m1_base64_encode.py):
  ```
  Contract:
    Inputs: image_path: str
    Outputs: image_b64: str
    Errors: FileNotFoundError
  Algebraic: y1 = m1(x1)
  ```
- **Pipeline YAML** (from APT_PIPELINE.yaml):
  ```
  - name: m1
    module: APT_MODULES.m1_base64_encode
    fn: run
    args: {image_path: demo_image.png}
  - name: m2
    module: APT_MODULES.m2_build_payload
    fn: run
    args: {image_b64: $m1, apt_prompt: "Describe"}
  ```

## Key Files & Directories
- `APT_MODULES/`: Pipeline modules (m1_*.py) and apt_pipeline_pkg/ (executor, snapshot).
- `APT_PIPELINE.yaml`: Pipeline definition with equations.
- `APT_PIPELINE_RUNS/`: Timestamped outputs.
- `APT_INPUTS/`: Raw inputs.
- `APT_ENV/venvs/`: Per-module environments.
- `docs/`: Theory and proofs.
- `archive/`: Heavyweight outputs.
- `requirements.txt`: Dependencies (pyyaml, requests, sklearn, xgboost).

## Notes
- Changes must be small, tested, documented. Use strict_mode.py for fatal errors.
- For network/secrets: comment credentials, no hardcoding.
- Follow APT_METHODS.md for advanced patterns (P vs NP pipelines, barriers).

For new work: Use algebraic notation, add contracts/tests, snapshot outputs.
