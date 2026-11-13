"""Ingestão sobre fixtures sintéticas do FFmpeg."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from cronista.config import Settings
from cronista.db.models import Artifact, Job, MediaFile, RecordingSession
from cronista.ingest.ffmpeg import probe_media
from cronista.ingest.service import ingest_folder
from cronista.pipeline import AlwaysFreeGate
from tests.conftest import needs_ffmpeg

pytestmark = needs_ffmpeg


def _ingest(db: Session, folder: Path, settings: Settings):  # type: ignore[no-untyped-def]
    return ingest_folder(db, folder, settings, AlwaysFreeGate())


def test_normal_recording_produces_proxy_and_wavs(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    report = _ingest(db, fixture_folders["normal"], settings)
    assert report.ok
    (result,) = report.files.values()
    assert result.executed == ["normalize", "proxy", "audio"]
    assert result.results["normalize"].data["actions"] == []  # arquivo íntegro: sem remux nem conversão

    proxy = probe_media(settings, Path(str(result.results["proxy"].data["proxy"])))
    assert proxy.height == 360 and proxy.audio_streams == 1 and proxy.fps == "60/1"
    for label in ("game", "mic"):
        wav = Path(str(result.results["audio"].data[label]))
        assert wav.suffix == ".wav" and wav.stat().st_size > 10_000


def test_reingest_creates_nothing_new(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    _ingest(db, fixture_folders["normal"], settings)
    counts = [
        db.scalar(select(func.count()).select_from(t)) for t in (RecordingSession, MediaFile, Artifact, Job)
    ]
    report = _ingest(db, fixture_folders["normal"], settings)
    (result,) = report.files.values()
    assert result.executed == [] and result.cached == ["normalize", "proxy", "audio"]
    assert counts == [
        db.scalar(select(func.count()).select_from(t)) for t in (RecordingSession, MediaFile, Artifact, Job)
    ]


def test_interrupted_file_is_remuxed_keeping_three_audio_tracks(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    broken = next(fixture_folders["interrompida"].iterdir())
    assert probe_media(settings, broken).interrupted  # a fixture realmente está interrompida

    report = _ingest(db, fixture_folders["interrompida"], settings)
    assert report.ok, report.failures
    (result,) = report.files.values()
    normalize = result.results["normalize"]
    assert normalize.data["actions"] == ["remux"]
    assert probe_media(settings, Path(str(normalize.data["media"]))).audio_streams == 3


def test_10bit_is_warned_and_converted_to_8bit(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    report = _ingest(db, fixture_folders["tenbit"], settings)
    assert report.ok, report.failures
    (result,) = report.files.values()
    normalize = result.results["normalize"]
    assert normalize.data["actions"] == ["convert_8bit"]
    assert any("10-bit" in w for w in normalize.warnings)
    assert probe_media(settings, Path(str(normalize.data["media"]))).bit_depth == 8


def test_5994_fps_is_rejected_with_clear_message(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    report = _ingest(db, fixture_folders["fps5994"], settings)
    assert not report.ok
    (error,) = report.failures.values()
    assert "60000/1001" in error and "60/1" in error
    assert db.scalar(select(Job.status).where(Job.stage == "normalize")) == "failed"


def test_split_recording_is_one_session_with_two_files(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    report = _ingest(db, fixture_folders["split"], settings)
    assert report.ok and len(report.files) == 2
    assert db.scalar(select(func.count()).select_from(RecordingSession)) == 1
    assert [m.ordinal for m in db.scalars(select(MediaFile).order_by(MediaFile.ordinal))] == [0, 1]


def test_changing_proxy_parameter_reruns_only_proxy(
    db: Session, settings: Settings, fixture_folders: dict[str, Path]
) -> None:
    _ingest(db, fixture_folders["normal"], settings)
    report = _ingest(db, fixture_folders["normal"], settings.model_copy(update={"proxy_height": 240}))
    (result,) = report.files.values()
    assert result.executed == ["proxy"] and result.cached == ["normalize", "audio"]
