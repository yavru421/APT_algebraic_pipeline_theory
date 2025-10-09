# APT Runner

Run the algebraic pipeline from `APT_PIPELINE.yaml`:

```pwsh
python .\scripts\apt_runner.py
```

- Outputs are written to `APT_PIPELINE_RUNS/<timestamp>/outputs.json`.
- Snapshots (when enabled) go to `APT_PIPELINE_RUNS/<timestamp>/apt_trace.ndjson`.
- Per-step environments can be set with `env: <name>` and are managed under `APT_ENV/venvs/<name>/`.
- Auto-install from `requirements.txt` occurs when `APT_AUTO_INSTALL` is not disabled.
