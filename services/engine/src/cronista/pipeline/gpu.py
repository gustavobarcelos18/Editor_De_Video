"""Política de GPU como porta. A implementação real (OBS gravando / jogo em tela cheia) vem na 1B/1C."""

from __future__ import annotations

from typing import Protocol


class GpuGate(Protocol):
    def is_free(self) -> bool:
        """True quando o processamento com GPU pode rodar (OBS parado, sem jogo em tela cheia)."""
        ...


class AlwaysFreeGate:
    """Padrão em `dev` e nos testes: a GPU nunca está ocupada."""

    def is_free(self) -> bool:
        return True
