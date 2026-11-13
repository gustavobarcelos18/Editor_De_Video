"""Tabelas da Fase 1. Sem `day_number`: o número do dia é da edição (plano mestre, seção 4)."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    game: Mapped[str | None] = mapped_column(String(200), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    sessions: Mapped[list[RecordingSession]] = relationship(back_populates="project")


class RecordingSession(Base):
    """Uma gravação de duração variável (pode ter vários arquivos, por divisão automática do OBS)."""

    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    folder: Mapped[str] = mapped_column(String(1000), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    project: Mapped[Project] = relationship(back_populates="sessions")
    media_files: Mapped[list[MediaFile]] = relationship(
        back_populates="session", order_by="MediaFile.ordinal"
    )


class MediaFile(Base):
    __tablename__ = "media_file"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"))
    path: Mapped[str] = mapped_column(String(1000), unique=True)
    ordinal: Mapped[int] = mapped_column(Integer, default=0)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)

    session: Mapped[RecordingSession] = relationship(back_populates="media_files")


class Job(Base):
    """Um job por (arquivo, etapa), atualizado no lugar. Estados: pending, running, done, failed."""

    __tablename__ = "job"
    __table_args__ = (UniqueConstraint("media_file_id", "stage"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    media_file_id: Mapped[int] = mapped_column(ForeignKey("media_file.id"))
    stage: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    cache_key: Mapped[str | None] = mapped_column(String(64), default=None)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, default=None)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)


class Artifact(Base):
    """Saída de uma etapa, identificada pela chave de cache (hash de entrada + parâmetros + versão)."""

    __tablename__ = "artifact"
    __table_args__ = (UniqueConstraint("media_file_id", "stage"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    media_file_id: Mapped[int] = mapped_column(ForeignKey("media_file.id"))
    stage: Mapped[str] = mapped_column(String(100))
    cache_key: Mapped[str] = mapped_column(String(64))
    result_path: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Marker(Base):
    """Marcador de hotkey (usado na 1B). Tempo em segundos de mídia dentro do arquivo."""

    __tablename__ = "marker"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"))
    media_file_id: Mapped[int | None] = mapped_column(ForeignKey("media_file.id"), default=None)
    marker_id: Mapped[str] = mapped_column(String(64))  # o `id` de `tipo|id`
    kind: Mapped[str] = mapped_column(String(40))
    media_time_s: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(20), default="journal")  # journal | file
    warning: Mapped[str | None] = mapped_column(Text, default=None)
