# APT Examples

This repository includes runnable examples demonstrating APT (Algebraic Pipeline Theory) in practice.

## 1) FletAPT Bowling (Sanitized, Offline)

Path: `examples/fletapt_bowling/`

- Safe to run: no API keys, no tokens, no network calls
- Uses only fabricated sample data
- Minimal dependencies (Flet only)
- Demonstrates a clean APT pipeline with UI (Calendar + Leaderboard)

Quickstart:
```bash
cd examples/fletapt_bowling
pip install -r requirements.txt
python -m src.main
```

Core APT equation:
```
y13 = m13(x4)
y10 = m10(y13)
y11 = m11(y10)
y9  = m9(x2, y13, x5)
UI  = (y9, y11)
```

Notes:
- To integrate real image processing and APIs, add modules m2/m3/m4/m6/m12/m14 and gate them with env vars.
- Keep secrets out of source; prefer environment variables or local config ignored by git.
