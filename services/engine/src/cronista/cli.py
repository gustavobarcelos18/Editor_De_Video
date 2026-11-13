"""CLI: `cronista ingest <pasta>`, `cronista status`, `cronista fixtures`."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from sqlalchemy import select

from cronista.config import load_settings
from cronista.db.models import Job, MediaFile, Project, RecordingSession
from cronista.db.session import open_db
from cronista.devtools.fixtures import make_fixtures
from cronista.ingest.service import ingest_folder
from cronista.logging_setup import setup_logging
from cronista.pipeline import AlwaysFreeGate, recover_orphans

app = typer.Typer(help="Cronista: gameplay do OBS → timeline do Resolve.", no_args_is_help=True)


@app.command()
def ingest(
    folder: Annotated[Path, typer.Argument(help="Pasta da sessão de gravação")],
    project: Annotated[str, typer.Option(help="Nome do projeto (série)")] = "default",
) -> None:
    """Ingere uma sessão: valida, remuxa se preciso, gera proxy e WAVs. Retoma de onde parou."""
    settings = load_settings()
    setup_logging(settings.log_level)
    with open_db(settings.db_path) as db:
        recovered = recover_orphans(db)
        if recovered:
            typer.echo(f"{recovered} job(s) interrompido(s) voltaram para a fila.")
        report = ingest_folder(db, folder, settings, AlwaysFreeGate(), project)
    for path, result in report.files.items():
        typer.echo(f"{path}: executadas={result.executed} em_cache={result.cached}")
        for stage in result.results.values():
            for warning in stage.warnings:
                typer.echo(f"  aviso: {warning}")
    for path, error in report.failures.items():
        typer.echo(f"FALHOU {path}: {error}", err=True)
    raise typer.Exit(0 if report.ok else 1)


@app.command()
def status() -> None:
    """Mostra projetos, sessões e o estado dos jobs."""
    settings = load_settings()
    with open_db(settings.db_path) as db:
        for project in db.scalars(select(Project)):
            typer.echo(f"Projeto {project.name}")
            for session in project.sessions:
                typer.echo(f"  Sessão {session.id}: {session.folder}")
                for media in session.media_files:
                    typer.echo(f"    {Path(media.path).name}")
                    for job in db.scalars(select(Job).where(Job.media_file_id == media.id).order_by(Job.id)):
                        extra = f" ({job.error})" if job.error else ""
                        typer.echo(f"      {job.stage}: {job.status}{extra}")
        if db.scalar(select(RecordingSession.id)) is None and db.scalar(select(MediaFile.id)) is None:
            typer.echo("Nada ingerido ainda.")


@app.command()
def fixtures(
    out: Annotated[Path | None, typer.Option(help="Pasta de saída (padrão: data/fixtures)")] = None,
) -> None:
    """Gera as fixtures sintéticas de vídeo (FFmpeg) para testar sem gravação real."""
    settings = load_settings()
    target = out or settings.data_dir / "fixtures"
    for name, path in make_fixtures(settings, target).items():
        typer.echo(f"{name}: {path}")
