import os
import json
from pathlib import Path

import pytest

from apt_pipeline_pkg import snapshot


def test_snapshot_writes_ndjson(tmp_path, monkeypatch):
    # Enable tracing via env
    monkeypatch.setenv("APT_TRACE", "1")
    out = tmp_path / "apt_trace.ndjson"

    # Write a couple of snapshots
    snapshot.snapshot(0, "test", "v", "hello", out_path=out)
    snapshot.snapshot(1, "test", "v2", {"a": 1}, out_path=out)

    assert out.exists()
    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    records = [json.loads(l) for l in lines]
    assert records[0]["step"] == 0
    assert records[1]["step"] == 1
