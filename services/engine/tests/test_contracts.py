from __future__ import annotations

from pathlib import Path

from cronista.config import find_repo_root
from cronista.contracts import render_schema


def test_versioned_schema_is_up_to_date() -> None:
    """Se falhar: `uv run python -m cronista.contracts` e depois `pnpm gen` em packages/contracts."""
    path = find_repo_root(Path(__file__)) / "packages" / "contracts" / "schema.json"
    assert path.read_text(encoding="utf-8") == render_schema()
