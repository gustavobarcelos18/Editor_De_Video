from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from cronista.config import Settings
from cronista.db.session import open_db
from cronista.devtools.fixtures import make_fixtures

needs_ffmpeg = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None, reason="FFmpeg não instalado"
)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(env="test", data_dir=tmp_path / "data")


@pytest.fixture
def db(settings: Settings) -> Iterator[Session]:
    with open_db(settings.db_path) as session:
        yield session


@pytest.fixture(scope="session")
def fixture_folders(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Fixtures de vídeo geradas uma vez por execução dos testes (só com FFmpeg)."""
    if shutil.which("ffmpeg") is None:
        pytest.skip("FFmpeg não instalado")
    root = tmp_path_factory.mktemp("fixtures")
    return make_fixtures(Settings(env="test", data_dir=root), root)
