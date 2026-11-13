"""Chave de cache = hash(entrada + parâmetros + versão da etapa)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

_EDGE = 1024 * 1024


def fingerprint_file(path: Path) -> str:
    """Impressão digital barata de uma mídia grande: tamanho + 1 MiB do início + 1 MiB do fim.

    Não lê o arquivo inteiro (masters têm dezenas de GB). Não depende do mtime, para o cache
    sobreviver a cópias entre discos.
    """
    size = path.stat().st_size
    digest = hashlib.sha256()
    digest.update(str(size).encode())
    with path.open("rb") as handle:
        digest.update(handle.read(_EDGE))
        if size > 2 * _EDGE:
            handle.seek(size - _EDGE)
            digest.update(handle.read(_EDGE))
    return digest.hexdigest()


def compute_key(
    stage_name: str,
    stage_version: str,
    params: dict[str, Any],
    root_fingerprint: str,
    needs_keys: Sequence[str],
) -> str:
    payload = json.dumps(
        {
            "stage": stage_name,
            "version": stage_version,
            "params": params,
            "root": root_fingerprint,
            "needs": list(needs_keys),
        },
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode()).hexdigest()
