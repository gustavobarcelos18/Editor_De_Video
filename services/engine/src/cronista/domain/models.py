"""Contratos compartilhados com o Studio. Fonte de verdade: estes modelos Pydantic (decisão D2).

Não há `day_number` em lugar nenhum: o número do dia é decidido na edição (plano mestre, seção 4).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class MarkerKind(StrEnum):
    MOMENTO = "momento"
    MORTE_FALHA = "morte_falha"
    ENGRACADO = "engracado"
    CONQUISTA = "conquista"
    NOVO_DIA = "novo_dia"
    CONSTRUCAO = "construcao"
    FOTO_PROGRESSO = "foto_progresso"
    CINEMATICA = "cinematica"


class MediaProbe(BaseModel):
    """Resultado do `ffprobe` de um arquivo de gravação."""

    path: str
    duration_s: float | None = None
    video_codec: str | None = None
    pix_fmt: str | None = None
    bit_depth: int = 8
    width: int | None = None
    height: int | None = None
    fps: str | None = None  # fração "num/den", ex.: "60/1"
    audio_streams: int = 0
    interrupted: bool = False


class StageResult(BaseModel):
    """Saída de uma etapa do pipeline, persistida como `result.json` no cache."""

    files: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
