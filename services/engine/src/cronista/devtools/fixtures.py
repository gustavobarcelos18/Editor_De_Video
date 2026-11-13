"""Fixtures sintéticas geradas pelo FFmpeg (nunca versionadas; saem em `data/fixtures/`).

Cada variante é uma pasta (= uma sessão) com 1080p60 H.264 8-bit e três faixas de áudio
(1 = mix, 2 = jogo, 3 = microfone), cada uma com um tom diferente.
"""

from __future__ import annotations

from pathlib import Path

from cronista.config import Settings
from cronista.ingest.ffmpeg import run_ffmpeg

DURATION_S = 2
_AUDIO_TONES = (440, 660, 880)


def _encode(
    settings: Settings,
    out: Path,
    *,
    rate: str = "60",
    pix_fmt: str = "yuv420p",
    extra: list[str] | None = None,
    start: int = 0,
) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    args = ["-f", "lavfi", "-i", f"testsrc2=size=1920x1080:rate={rate}:duration={DURATION_S}"]
    for tone in _AUDIO_TONES:
        args += ["-f", "lavfi", "-i", f"sine=frequency={tone + start}:duration={DURATION_S}"]
    args += ["-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "3:a"]
    args += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", pix_fmt, "-r", rate, "-c:a", "aac"]
    args += extra or []
    run_ffmpeg(settings, [*args, str(out)])


def make_fixtures(settings: Settings, root: Path) -> dict[str, Path]:
    """Gera as variantes em `root/<nome>/` e devolve nome → pasta."""
    folders: dict[str, Path] = {}

    def folder(name: str) -> Path:
        folders[name] = root / name
        return folders[name]

    _encode(settings, folder("normal") / "gravacao.mp4", extra=["-movflags", "+faststart"])
    _encode(settings, folder("split") / "gravacao_1.mp4", extra=["-movflags", "+faststart"])
    _encode(settings, folder("split") / "gravacao_2.mp4", start=100, extra=["-movflags", "+faststart"])
    _encode(settings, folder("tenbit") / "gravacao.mp4", pix_fmt="yuv420p10le")
    _encode(settings, folder("fps5994") / "gravacao.mp4", rate="60000/1001")

    # Interrompida: MP4 fragmentado (como o Hybrid MP4) com o final cortado, sem finalização.
    broken = folder("interrompida") / "gravacao.mp4"
    # `-g 30`: um fragmento a cada 0,5 s, com vídeo e áudio intercalados como no OBS (sem isso há um
    # fragmento só e o corte do final levaria todo o áudio).
    _encode(settings, broken, extra=["-g", "30", "-movflags", "frag_keyframe+empty_moov"])
    data = broken.read_bytes()
    broken.write_bytes(data[: int(len(data) * 0.85)])
    return folders
