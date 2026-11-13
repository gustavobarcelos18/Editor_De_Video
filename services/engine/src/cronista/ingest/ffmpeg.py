"""Chamadas ao FFmpeg/FFprobe."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from cronista.config import Settings
from cronista.domain.models import MediaProbe
from cronista.pipeline.stage import StageError


def run_ffmpeg(settings: Settings, args: list[str]) -> None:
    cmd = [settings.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise StageError(f"ffmpeg falhou ({proc.returncode}): {proc.stderr.strip()[-500:]}")


def _bit_depth(pix_fmt: str | None) -> int:
    match = re.search(r"p(\d+)(?:le|be)?$", pix_fmt or "")
    return int(match.group(1)) if match else 8


def is_unfinalized_mp4(path: Path) -> bool:
    """True se o MP4 ficou fragmentado/cortado (gravação interrompida), olhando só as caixas de topo.

    Um Hybrid MP4 finalizado vira um MP4 comum (ftyp, moov, mdat), sem `moof`. Fragmentos `moof`, caixa
    maior que o arquivo ou ausência de `moov` indicam que a gravação não foi finalizada. Só lê cabeçalhos.
    Só vale para contêineres MP4/MOV; outros (MKV) devolvem False.
    """
    if path.suffix.lower() not in {".mp4", ".mov", ".m4v"}:
        return False
    size = path.stat().st_size
    seen_moov = False
    with path.open("rb") as handle:
        pos = 0
        while pos + 8 <= size:
            handle.seek(pos)
            header = handle.read(16)
            box_size = int.from_bytes(header[:4], "big")
            box_type = header[4:8]
            if box_type == b"moof":
                return True
            if box_type == b"moov":
                seen_moov = True
            if box_size == 1:
                box_size = int.from_bytes(header[8:16], "big")
            elif box_size == 0:
                box_size = size - pos
            if box_size < 8 or pos + box_size > size:
                return True  # caixa cortada ou corrompida
            pos += box_size
    return not seen_moov


def probe_media(settings: Settings, path: Path) -> MediaProbe:
    """`ffprobe` do arquivo. Ilegível, sem duração ou MP4 não finalizado → `interrupted`."""
    cmd = [
        settings.ffprobe, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path),
    ]  # fmt: skip
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return MediaProbe(path=str(path), interrupted=True)
    info: dict[str, Any] = json.loads(proc.stdout)
    streams: list[dict[str, Any]] = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_count = sum(1 for s in streams if s.get("codec_type") == "audio")
    raw_duration = info.get("format", {}).get("duration")
    duration = float(raw_duration) if raw_duration not in (None, "N/A") else None
    if video is None:
        return MediaProbe(path=str(path), audio_streams=audio_count, interrupted=True)
    return MediaProbe(
        path=str(path),
        duration_s=duration,
        video_codec=video.get("codec_name"),
        pix_fmt=video.get("pix_fmt"),
        bit_depth=_bit_depth(video.get("pix_fmt")),
        width=video.get("width"),
        height=video.get("height"),
        fps=video.get("r_frame_rate"),
        audio_streams=audio_count,
        interrupted=duration is None or is_unfinalized_mp4(path),
    )
