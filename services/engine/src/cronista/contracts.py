"""Gera o JSON Schema dos contratos (decisão D2: Pydantic é a fonte; o TypeScript é gerado a partir dele)."""

from __future__ import annotations

import json

from pydantic import TypeAdapter

from cronista.domain.models import MarkerKind, MediaProbe, StageResult


def build_schema() -> dict[str, object]:
    defs: dict[str, object] = {}
    for model in (MediaProbe, StageResult):
        schema = model.model_json_schema(ref_template="#/$defs/{model}")
        defs.update(schema.pop("$defs", {}))
        defs[model.__name__] = schema
    kind = TypeAdapter(MarkerKind).json_schema()
    defs["MarkerKind"] = kind
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "CronistaContracts",
        "$defs": dict(sorted(defs.items())),
    }


def render_schema() -> str:
    return json.dumps(build_schema(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> None:
    """Escreve `packages/contracts/schema.json` (caminho relativo à raiz do repositório)."""
    from cronista.config import find_repo_root

    target = find_repo_root() / "packages" / "contracts" / "schema.json"
    target.write_text(render_schema(), encoding="utf-8")
    print(f"Escrito {target}")


if __name__ == "__main__":
    main()
