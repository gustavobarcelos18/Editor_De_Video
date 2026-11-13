"""Contrato de uma etapa do pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from cronista.config import Settings
from cronista.domain.models import StageResult


class StageError(Exception):
    """Falha esperada de uma etapa (arquivo inválido, por exemplo); a mensagem vai para o job."""


@dataclass(frozen=True)
class StageContext:
    media_path: Path
    out_dir: Path
    settings: Settings
    inputs: dict[str, StageResult]  # resultados das etapas listadas em `needs`


class Stage(Protocol):
    name: str
    version: str  # sobe quando a lógica muda: invalida o cache da etapa e das seguintes
    needs: tuple[str, ...]
    uses_gpu: bool

    def params(self, settings: Settings) -> dict[str, Any]:
        """Parâmetros que entram na chave de cache."""
        ...

    def run(self, ctx: StageContext) -> StageResult: ...
