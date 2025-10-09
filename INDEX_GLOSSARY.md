# APT System Index & Glossary

**Generated:** October 9, 2025
**System Version:** APT 1.0 - Algebraic Pipeline Theory
**Repository:** APT_algebraic_pipeline_theory

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Directory Structure](#directory-structure)
3. [Active Files](#active-files)
4. [Module Registry](#module-registry)
5. [Pipeline Formats](#pipeline-formats)
6. [Environment System](#environment-system)
7. [Execution Model](#execution-model)
8. [Quick Start](#quick-start)
9. [Archived Components](#archived-components)

---

## Core Concepts

### Algebraic Pipeline Theory (APT)
A formal methodology for specifying, composing, and reasoning about computational pipelines using algebraic notation. Every pipeline step is an explicit, traceable, reproducible transformation.

**Core Principles:**
- **Modularity:** Each transformation is a discrete module (m₁, m₂, ..., mₙ)
- **Explicitness:** All inputs (x), outputs (Y), and intermediates are explicitly defined
- **Traceability:** Every execution step is logged and auditable
- **Reproducibility:** Pipeline equation + environment + inputs = deterministic output
- **Composability:** Modules compose algebraically: Y = mₙ(...m₂(m₁(x₁)))

### Key Equations

**Pipeline Composition:**
```
Y = m₄(m₀(x₁), path, m₂(m₁(x₂), x₃), dry_run) @ venvA
```

**Module Signature:**
```
mᵢ: (inputs) → output
```

---

## Directory Structure

### Active APT Folders

```
APM/
├── APT_INPUTS/              # All raw inputs (images, config, data)
├── APT_MODULES/             # Modular pipeline scripts (m0, m1, m2, ...)
├── APT_PIPELINE_RUNS/       # Timestamped execution outputs
├── APT_OUTPUTS/             # Final deliverables only
├── APT_MANUAL/              # Manual intervention scripts
├── APT_LOGS/                # Execution logs and audit trails
├── APT_ENV/                 # Environment definitions and venvs
│   └── venvs/               # Central registry: venvA, venvB, py39, r_env, node_env
├── apt_pipeline_pkg/        # Core executor, pipeline, snapshot, env, rapt
├── scripts/                 # Runners and utilities
│   ├── apt_runner.py        # Main pipeline runner
│   └── Invoke-AptStep.ps1   # PowerShell env activator
├── tests/                   # Unit and integration tests
├── docs/                    # APT theory, proofs, and documentation
├── archive/                 # Legacy/deprecated code and docs
├── APT_PIPELINE.yaml        # Declarative pipeline spec (YAML)
├── RAPT_PIPELINE.RAPT       # Algebraic DSL pipeline spec
├── APT_METHODS.md           # Workspace execution standard
└── INDEX_GLOSSARY.md        # This file
```

### Deprecated/Archived Folders (see archive/)
- `apt_core/` → archive/legacy_code/apt_core
- `apt_image_pipeline/` → archive/legacy_code/apt_image_pipeline
- `results/` → APT_PIPELINE_RUNS (outputs moved)
- `images/` → APT_INPUTS (inputs moved)
- Old scripts → archive/legacy_scripts

---

## Active Files

### Core System

| File | Purpose | Type |
|------|---------|------|
| `APT_METHODS.md` | Workspace execution standard & methodology | Documentation |
| `APT_PIPELINE.yaml` | Declarative YAML pipeline definition | Pipeline Spec |
| `RAPT_PIPELINE.RAPT` | Algebraic DSL pipeline definition | Pipeline Spec |
| `README.md` | Project overview and quick start | Documentation |
| `INDEX_GLOSSARY.md` | System index and glossary (this file) | Documentation |
| `requirements.txt` | Root Python dependencies for CI | Config |
| `netlify-llama-proxy-openapi.yaml` | OpenAPI spec for proxy endpoint | API Spec |

### Core Packages

#### `apt_pipeline_pkg/`
- `executor.py` - Pipeline execution engine with env support
- `pipeline.py` - Core pipeline helper functions
- `snapshot.py` - Execution tracing and audit trail
- `env.py` - Environment management (venv creation, installation)
- `rapt.py` - .RAPT DSL parser (algebraic equation → executor spec)
- `telemetry_mysql.py` - Optional MySQL telemetry (legacy)

### Runner Scripts

#### `scripts/`
- `apt_runner.py` - Main pipeline runner (YAML or .RAPT)
- `Invoke-AptStep.ps1` - PowerShell env activator for per-step execution

### Tests

#### `tests/`
- `test_snapshot.py` - Snapshot/tracing tests
- Additional tests for executor, env, rapt (to be added)

---

## Module Registry

### Active Modules (APT_MODULES/)

| Module | Function | Inputs | Output | Description |
|--------|----------|--------|--------|-------------|
| `m0_openapi_resolve.py` | `run(openapi_file, server_index)` | OpenAPI YAML path, server index | Server URL (str) | Extracts server URL from OpenAPI spec |
| `m1_base64_encode.py` | `run(image_path)` | Image file path | Base64 string | Encodes image to base64 |
| `m2_build_payload.py` | `run(image_b64, apt_prompt, model)` | Base64 image, prompt, model | Payload dict | Builds API request payload |
| `m3_parse_response.py` | `run(response)` | Any response | Passthrough | Placeholder parser |
| `m4_call_proxy.py` | `run(base_url, path, payload, bearer_token?, dry_run)` | Proxy URL, path, payload, optional token, dry_run flag | Request or response dict | Calls Netlify proxy (or dry-runs) |
| `m5_parse_chat_completions.py` | `run(response)` | Chat completion response | {text, response} | Extracts chat completion text |

### Registry Mapping (rapt.py)

```python
MODULE_REGISTRY = {
    "m0": ("APT_MODULES.m0_openapi_resolve", "run"),
    "m1": ("APT_MODULES.m1_base64_encode", "run"),
    "m2": ("APT_MODULES.m2_build_payload", "run"),
    "m3": ("APT_MODULES.m3_parse_response", "run"),
    "m4": ("APT_MODULES.m4_call_proxy", "run"),
    "m5": ("APT_MODULES.m5_parse_chat_completions", "run"),
}
```

---

## Pipeline Formats

### YAML Format (APT_PIPELINE.yaml)

```yaml
pipeline:
  - name: m0
    module: APT_MODULES.m0_openapi_resolve
    fn: run
    env: venvA
    args:
      openapi_file: netlify-llama-proxy-openapi.yaml
      server_index: 0
  - name: m1
    module: APT_MODULES.m1_base64_encode
    fn: run
    env: venvA
    args:
      image_path: $m0  # Reference to m0 output
```

### .RAPT DSL Format (RAPT_PIPELINE.RAPT)

```rapt
# Variable bindings
x1 = "netlify-llama-proxy-openapi.yaml"
x2 = "demo_image.png"

# Algebraic equation with per-call env annotations
Y = m4(
  base_url=m0(openapi_file=x1) @ venvA,
  path="/chat/completions",
  payload=m2(image_b64=m1(image_path=x2) @ venvA, apt_prompt="Describe", model="demo") @ venvA,
  dry_run=true
) @ venvA
```

---

## Environment System

### Central Registry: `APT_ENV/venvs/`

Each environment is a named folder containing:
- `requirements.txt` (Python)
- `environment.yaml` (Conda/Mamba)
- `package.json` (Node.js)
- Other language-specific manifests

### Active Environments

| Environment | Type | Dependencies | Purpose |
|-------------|------|--------------|---------|
| `venvA` | Python venv | numpy, pandas, requests | Primary Python pipeline env |
| `venvB` | Python venv | scipy, matplotlib | Scientific computing |
| `py39` | Conda | python=3.9, numpy, pandas | Python 3.9 specific |
| `r_env` | R | (renv) | R environment placeholder |
| `node_env` | Node.js | express | Node.js environment placeholder |

### Environment Activation

**Automatic (default):**
```python
# Executor prepares env, creates venv, installs packages
step.env = "venvA"
```

**PowerShell-based (per-step isolation):**
```pwsh
$env:APT_USE_PS = "1"
python .\scripts\apt_runner.py
```

---

## Execution Model

### Pipeline Execution Flow

1. **Load Spec:** Runner reads `APT_PIPELINE.yaml` or `.RAPT` file
2. **Parse:** YAML loader or .RAPT parser converts to executor spec
3. **Create Run Dir:** `APT_PIPELINE_RUNS/<timestamp>/`
4. **Set Environment:** `APT_RUN_DIR` for snapshots and outputs
5. **Build Expression:** Algebraic equation from step names
6. **Execute Steps:** For each step:
   - Prepare environment (venv, install packages)
   - Resolve arguments (variable substitution: `$m1` → previous output)
   - Snapshot inputs
   - Execute function (in-process or via PowerShell invoker)
   - Snapshot output
7. **Persist Outputs:** Write `outputs.json` and optional `apt_trace.ndjson`

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `APT_RUN_DIR` | `APT_PIPELINE_RUNS` | Run directory for outputs/traces |
| `APT_ENV_ROOT` | `APT_ENV/venvs` | Environment registry root |
| `APT_AUTO_INSTALL` | `1` | Auto-install packages on env prepare |
| `APT_TRACE` | `0` | Enable snapshot tracing to ndjson |
| `APT_USE_PS` | `0` | Use PowerShell invoker for env isolation |

---

## Quick Start

### Run a Pipeline (YAML)

```pwsh
python .\scripts\apt_runner.py
```

### Run a Pipeline (.RAPT DSL)

```pwsh
python .\scripts\apt_runner.py .\RAPT_PIPELINE.RAPT
```

### Inspect Latest Outputs

```pwsh
Get-ChildItem APT_PIPELINE_RUNS | Where-Object { $_.PSIsContainer } | Sort-Object Name -Descending | Select-Object -First 1 | % { Get-Content "$($_.FullName)\outputs.json" }
```

### Enable Snapshots

```pwsh
$env:APT_TRACE = "1"
python .\scripts\apt_runner.py
```

### Use PowerShell Env Isolation

```pwsh
$env:APT_USE_PS = "1"
python .\scripts\apt_runner.py
```

---

## Archived Components

Deprecated code, scripts, and documentation have been moved to:

### `archive/legacy_code/`
- `apt_core/` - Early executor/pipeline/snapshot implementations
- `apt_image_pipeline/` - Legacy image pipeline experiments
- `apt_screenshot/` - Screenshot-related legacy code
- `experimental/` - Experimental/incomplete features
- `gui/` - GUI attempts (incomplete)
- Loose Python files: `apt_curl.py`, `apt_curl_3.py`, `conftest.py`

### `archive/legacy_scripts/`
- Old demo and pipeline scripts from `scripts/` that are superseded by `apt_runner.py`
- Example: `demo_pipeline_demo.py`, `flet_app.py`, `screenshot_session.py`

### `archive/legacy_docs/`
- Older iterations of APT documentation
- Research notes and chat transcripts
- Redundant README files

### Still Active (Not Archived)
- `docs/` - Current APT theory, proofs, and methodology documentation
- `APT-AlgebraicPipelineTheory/` - Separate repo/submodule for web interface (kept)
- `.github/` - CI/CD workflows (active)

---

## Glossary

**APT** - Algebraic Pipeline Theory
**RAPT** - Runner for Algebraic Pipeline Theory (.RAPT file extension)
**Module (mᵢ)** - A discrete, indexable pipeline transformation
**Variable (xᵢ)** - An input to the pipeline
**Output (Y, yᵢ)** - Result of a module or the entire pipeline
**Environment (@env)** - Named, isolated dependency context (venv, conda, etc.)
**Snapshot** - Audit trail record of a step's inputs/outputs
**Run Directory** - Timestamped folder containing outputs for a single execution
**Executor** - Engine that interprets and executes pipeline specs
**Registry** - Mapping of module identifiers to Python module:function pairs
**Dry Run** - Execution mode that constructs requests without network calls

---

## Contributing & Extending

### Adding a New Module

1. Create `APT_MODULES/mX_descriptive_name.py` with a `run(**kwargs)` function
2. Add to `MODULE_REGISTRY` in `apt_pipeline_pkg/rapt.py`
3. Reference in `APT_PIPELINE.yaml` or `.RAPT` file
4. Document in this glossary

### Adding a New Environment

1. Create `APT_ENV/venvs/<env_name>/`
2. Add `requirements.txt`, `environment.yaml`, or other manifest
3. Reference via `env: <env_name>` in pipeline specs

### Running Tests

```pwsh
pytest -q
```

### CI/CD

GitHub Actions runs:
- `pytest` on all Python tests
- `.RAPT` smoke test to validate DSL path

---

**End of Index & Glossary**
