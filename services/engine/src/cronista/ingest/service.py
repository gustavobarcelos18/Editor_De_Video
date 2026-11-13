"""Caso de uso `cronista ingest <pasta>`: projeto incremental, uma sessão por pasta."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from cronista.config import Settings
from cronista.db.models import MediaFile, Project, RecordingSession
from cronista.ingest.stages import ingest_stages
from cronista.logging_setup import log_event
from cronista.pipeline import GpuGate, StageFailedError, run_pipeline
from cronista.pipeline.runner import PipelineReport


@dataclass
class IngestReport:
    session_id: int
    files: dict[str, PipelineReport] = field(default_factory=dict)
    failures: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.failures


def find_media(folder: Path, settings: Settings) -> list[Path]:
    exts = {e.lower() for e in settings.video_extensions}
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts)


def ingest_folder(
    db: Session, folder: Path, settings: Settings, gate: GpuGate, project_name: str = "default"
) -> IngestReport:
    folder = folder.resolve()
    files = find_media(folder, settings)
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo de vídeo em {folder}")

    project = db.scalar(select(Project).where(Project.name == project_name))
    if project is None:
        project = Project(name=project_name)
        db.add(project)
        db.flush()

    session = db.scalar(select(RecordingSession).where(RecordingSession.folder == str(folder)))
    if session is None:
        session = RecordingSession(project_id=project.id, folder=str(folder))
        db.add(session)
        db.flush()

    report = IngestReport(session_id=session.id)
    for ordinal, path in enumerate(files):
        media = db.scalar(select(MediaFile).where(MediaFile.path == str(path)))
        if media is None:
            media = MediaFile(
                session_id=session.id, path=str(path), ordinal=ordinal, size_bytes=path.stat().st_size
            )
            db.add(media)
        db.commit()
        log_event("ingestao_iniciada", session_id=session.id, media_file_id=media.id, path=str(path))
        try:
            report.files[str(path)] = run_pipeline(db, media, ingest_stages(), settings, gate)
        except StageFailedError as exc:
            report.failures[str(path)] = str(exc)
    return report
