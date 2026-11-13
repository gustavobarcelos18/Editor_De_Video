from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from cronista.db.models import Base


def test_migration_creates_all_tables_and_no_day_number(db: Session) -> None:
    inspector = inspect(db.get_bind())
    tables = set(inspector.get_table_names())
    assert {t.name for t in Base.metadata.sorted_tables} <= tables
    for table in tables - {"alembic_version"}:
        assert "day_number" not in {c["name"] for c in inspector.get_columns(table)}
