from __future__ import annotations

from pathlib import Path

import pytest

from cronista.config import find_repo_root, load_settings


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_local_overrides_versioned(tmp_path: Path) -> None:
    cfg = tmp_path / "config"
    _write(cfg / "dev.yaml", "env: dev\ndata_dir: data\nproxy_height: 360\n")
    _write(cfg / "dev.local.yaml", "proxy_height: 240\ndata_dir: D:/midia\n")
    settings = load_settings("dev", cfg)
    assert settings.proxy_height == 240
    assert settings.data_dir == Path("D:/midia")


def test_relative_data_dir_is_resolved_from_repo_root(tmp_path: Path) -> None:
    cfg = tmp_path / "config"
    _write(cfg / "dev.yaml", "env: dev\ndata_dir: data\n")
    assert load_settings("dev", cfg).data_dir == (tmp_path / "data").resolve()


def test_unknown_key_is_rejected(tmp_path: Path) -> None:
    cfg = tmp_path / "config"
    _write(cfg / "dev.yaml", "env: dev\ndata_dir: data\nchave_errada: 1\n")
    with pytest.raises(ValueError):
        load_settings("dev", cfg)


def test_repo_configs_load_and_have_no_personal_paths() -> None:
    root = find_repo_root(Path(__file__))
    for env in ("dev", "prod"):
        settings = load_settings(env, root / "config")
        assert settings.env == env
        text = (root / "config" / f"{env}.yaml").read_text(encoding="utf-8")
        assert "C:\\Users" not in text
        assert "/home/" not in text
