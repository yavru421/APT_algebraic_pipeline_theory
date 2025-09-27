# Copilot Instructions for APT Algebraic Pipeline Theory Workspace

## Big Picture Architecture
- **Modular Algebraic Pipelines:** The workspace is organized around the Algebraic Pipeline Theory (APT) methodology. All workflows are decomposed into modules ($m_i$), each with explicit input/output variables and algebraic relationships. Pipelines are documented and executed as sequences of algebraic operations.
- **Key Directories:**
  - `scripts/`: Core Python and PowerShell scripts for pipeline execution, visualization, and automation.
  - `apt_pipeline_pkg/`: Contains reusable pipeline logic and module definitions.
  - `archive/`, `results/`, `images/`: Store outputs, iterations, and assets. These are excluded from git to prevent bloat.
  - `docs/`: Theory, research notes, and markdown documentation.
  - `apm_research/`, `apt_chatmode_useage/`, `apt_image_pipeline/`: Specialized submodules for research, chat experiments, and image processing.

## Developer Workflows
- **Execution:** Run main pipeline scripts from `scripts/` (e.g., `pipeline.py`, `apt_image_methods_pipeline.py`). Use PowerShell scripts (`run.ps1`) for automation.
- **Testing:** Place and run tests in `scripts/tests/` or relevant submodule test folders. Use standard Python test runners.
- **Archival:** Archive results and iterations regularly in `archive/` and `results/` for traceability.
- **Documentation:** Update algebraic documentation in `docs/` and ensure all new modules are described with explicit variable and dependency notation.

## Project-Specific Conventions
- **Algebraic Notation:** All pipeline steps, variables, and dependencies are documented using indexed algebraic equations (e.g., $y_2 = f(x_1, x_3)$).
- **Explicit Variable Management:** Define all variables and outputs before use. Maintain traceability by logging each transformation and result.
- **Module Indexing:** Assign unique indices to each module for dependency resolution and reproducibility.
- **Archival Policy:** Exclude large outputs and assets from git; use dedicated folders for archiving.

## Integration Points & Dependencies
- **Python:** Main language for pipeline logic and automation.
- **PowerShell:** Used for orchestration and automation tasks.
- **External Tools:** Integrate with visualization and image processing libraries as needed (see `requirements.txt`).
- **Cross-Component Communication:** Modules interact via explicit input/output variables; dependencies are resolved algebraically and documented.

## Examples
- **Pipeline Definition:**
  ```python
  # Example: scripts/pipeline.py
  # y2 = f(x1, x3)
  y2 = my_module(x1, x3)
  log_step('y2', y2)
  ```
- **Archival:**
  ```python
  # Save results to archive/output/
  save_results(y2, 'archive/output/y2_results.json')
  ```
- **Documentation:**
  ```markdown
  # docs/APT_Image_Pipeline_Theory_Proofs.md
  # Document algebraic relationships and module dependencies
  ```

## Key Files & Directories
- `scripts/pipeline.py`, `apt_pipeline_pkg/pipeline.py`: Main pipeline logic
- `docs/`: Theory, methodology, and research notes
- `archive/`, `results/`: Output and archival folders
- `apt_pipeline_pkg/`: Pipeline module definitions

---

For new modules or changes, follow the algebraic documentation and modular structure. Archive results regularly and maintain explicit variable definitions for reproducibility.
