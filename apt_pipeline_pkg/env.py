"""APT environment management utilities.

This module provides light-weight environment handling aligned with APT Methods.

Design:
- Environments are centrally defined under `APT_ENV/venvs/<env_name>/`.
- Each environment folder may contain `requirements.txt` and/or `environment.yaml`.
- `prepare_env(name)` validates presence and returns the absolute path.
- Future: hook actual venv/conda activation and package install here.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


ENV_ROOT = Path("APT_ENV") / "venvs"


def env_root() -> Path:
    return Path(os.getenv("APT_ENV_ROOT", str(ENV_ROOT)))


def env_path(name: str) -> Path:
    return env_root() / name


def venv_path(name: str) -> Path:
    return env_path(name) / ".venv"


def venv_python(name: str) -> Path:
    vp = venv_path(name)
    # Windows vs POSIX
    if os.name == "nt":
        return vp / "Scripts" / "python.exe"
    return vp / "bin" / "python"


def ensure_venv(name: str) -> Path:
    """Create a Python venv for this environment if it does not yet exist."""
    ep = env_path(name)
    ep.mkdir(parents=True, exist_ok=True)
    vp = venv_path(name)
    if not (vp.exists() and (vp / ("Scripts" if os.name == "nt" else "bin")).exists()):
        # Create venv
        subprocess.check_call([sys.executable, "-m", "venv", str(vp)])
    return vp


def install_requirements(name: str) -> None:
    """Install requirements into the env venv if manifest files are present."""
    ep = env_path(name)
    req = ep / "requirements.txt"
    py = venv_python(name)
    # pip install -r requirements.txt if present
    if req.exists():
        subprocess.check_call([str(py), "-m", "pip", "install", "-r", str(req)])
    # Optionally handle conda/mamba here in the future
    _mark_prepared(ep)


def _mark_prepared(env_dir: Path) -> None:
    marker = env_dir / ".apt_env_prepared"
    try:
        marker.write_text("prepared", encoding="utf-8")
    except Exception:
        pass


def prepare_env(name: Optional[str]) -> Path | None:
    """Ensure the environment folder exists, create venv, and install requirements.

    Respects APT_AUTO_INSTALL (default: 1) to auto-install on run.
    If name is None, returns None (use default env).
    """
    if not name:
        return None
    ep = env_path(name)
    ep.mkdir(parents=True, exist_ok=True)
    # Always ensure venv exists
    ensure_venv(name)
    # Optionally auto-install
    if os.getenv("APT_AUTO_INSTALL", "1") not in ("0", "false", "False", "off", "no"):
        try:
            install_requirements(name)
        except subprocess.CalledProcessError as e:
            print(f"[APT][env] install failed for {name}: {e}")
    return ep.resolve()
