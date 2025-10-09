# APT Methods: Workspace Execution Standard

## 1. Folder and File Structure
- All data, scripts, and outputs are organized under a strict folder hierarchy:
  - `APT_INPUTS/`: All raw user inputs (video, frames, SRT, config)
  - `APT_MODULES/`: All modular pipeline scripts (named m1, m2, ...)
  - `APT_PIPELINE_RUNS/`: All pipeline run outputs (timestamped)
  - `APT_OUTPUTS/`: Final deliverables
  - `APT_MANUAL/`: Manual intervention scripts and notebooks
  - `APT_LOGS/`: Execution logs and audit trails
  - `APT_ENV/`: Environment setup and reproducibility files
    - `APT_ENV/venvs/`: Central registry of all environments (venvA, venvB, py39, r_env, node_env, ...)
  - `APT_PIPELINE.yaml`: The algebraic pipeline equation and module order
  - `APT_METHODS.md`: This methods document



## 2. Algebraic Pipeline & Environment Definition

- The pipeline is defined in `APT_PIPELINE.yaml` or `.RAPT` as a sequence of modules, each with:
  - `name`: Algebraic index (m1, m2, ...)
  - `fn`: Function/module name (must match a script in `APT_MODULES/`)
  - `inputs`: Explicit variable bindings (inputs or outputs from previous modules)
  - `output`: Output variable name
  - `env`: (Optional) Environment name (must match a folder in `APT_ENV/venvs/`)
- Example equation:
  - $Y = m_6(m_5(m_2(x_3), m_3(x_2), m_1(x_1)), x_1) @ venvA$
- All modules/scripts must use only `APT_INPUTS/` and `APT_PIPELINE_RUNS/` for I/O.
- All environments are centrally defined and referenced algebraically, ensuring modular, reproducible, and auditable execution.


## 3. Execution Flow

- The pipeline runner reads `APT_PIPELINE.yaml` or `.RAPT`, resolves dependencies and environments, and executes modules in order.
- Each module reads its inputs, activates the correct environment, performs its transformation, and writes its outputs as defined.
- All intermediate and final outputs are stored in `APT_PIPELINE_RUNS/` (with timestamp/version).


## 4. Manual Intervention

- If a step fails, logs and intermediate files are in the current `APT_PIPELINE_RUNS/` folder.
- Manual scripts in `APT_MANUAL/` can be used to fix, override, or rerun any step.
- All interventions are logged in `APT_LOGS/`.


## 5. Extensibility

- To add a new module:
  - Place the script in `APT_MODULES/` (e.g., `m7_new_module.py`)
  - Add the module to `APT_PIPELINE.yaml` with explicit inputs/outputs and (optionally) environment
- To add a new environment:
  - Create a folder in `APT_ENV/venvs/` (e.g., `venvC/`)
  - Add `requirements.txt` or `environment.yaml`
- To change the pipeline flow, edit `APT_PIPELINE.yaml` (no code changes needed)


## 6. Reproducibility & Traceability

- All runs are fully determined by the pipeline equation, variable bindings, and environment.
- All logs, errors, and interventions are recorded in `APT_LOGS/`.
- All outputs are versioned in `APT_PIPELINE_RUNS/`.
- All environments are versioned and auditable in `APT_ENV/venvs/`.


## 7. PATH and Environment

- All scripts use relative paths from the project root, referencing only the above folders.
- No hardcoded absolute paths; all modules read from `APT_INPUTS/` and write to `APT_PIPELINE_RUNS/`.
- Environment setup is defined in `APT_ENV/venvs/` and referenced algebraically in the pipeline equation.



## 8. Example: Adding a New Pipeline Variant

- To run a visual-only pipeline:
  - Add a new equation to `APT_PIPELINE.yaml` (e.g., skip audio_analysis)
  - Specify environments as needed for each module
  - Run the pipeline runner with the new equation

---

This APT Methods document ensures all work in this workspace is modular, algebraic, reproducible, and easy to maintain or extend. Environments are now a first-class, algebraic, and auditable part of the pipeline.
