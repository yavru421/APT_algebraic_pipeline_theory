"""APT Runner (.RAPT/.yaml executor)

Reads `APT_PIPELINE.yaml` and executes steps using apt_pipeline_pkg.executor.
Establishes an APT run directory in APT_PIPELINE_RUNS/<timestamp> and sets
APT_RUN_DIR to route snapshots and outputs.
"""
from __future__ import annotations

import os
import sys
import json
import time
from pathlib import Path
from typing import Any, Dict

import yaml  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apt_pipeline_pkg import executor
from apt_pipeline_pkg import rapt


def _make_run_dir(base: Path | None = None) -> Path:
    ts = time.strftime("%Y%m%d_%H%M%S")
    base = base or Path("APT_PIPELINE_RUNS")
    run = base / ts
    run.mkdir(parents=True, exist_ok=True)
    return run


def main(spec_path: str = "APT_PIPELINE.yaml") -> int:
    spec_file = Path(spec_path)
    if not spec_file.exists():
        # Try .RAPT alias
        alt = Path("RAPT_PIPELINE.RAPT")
        if alt.exists():
            spec_file = alt
        else:
            print(f"[APT] Spec not found: {spec_file}")
        return 1

    # Establish run directory and set env for snapshots
    run_dir = _make_run_dir()
    os.environ["APT_RUN_DIR"] = str(run_dir)

    spec: Dict[str, Any]
    if spec_file.suffix.lower() == ".rapt":
        spec = rapt.parse_rapt(spec_file.read_text(encoding="utf-8"))
    else:
        spec = yaml.safe_load(spec_file.read_text(encoding="utf-8")) or {}

    # Normalize: allow either 'pipeline' or 'steps'
    steps: list[dict[str, Any]] = spec.get("pipeline") or spec.get("steps") or []  # type: ignore[assignment]
    if steps:
        spec = {"steps": steps}

    print(f"[APT] Running pipeline from {spec_file} -> run dir {run_dir}")
    outputs = executor.execute(spec)

    # Persist outputs summary
    (run_dir / "outputs.json").write_text(json.dumps(outputs, default=str, indent=2), encoding="utf-8")
    print(f"[APT] Completed. Outputs written to {run_dir / 'outputs.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
