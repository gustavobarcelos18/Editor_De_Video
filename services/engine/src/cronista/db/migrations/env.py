from __future__ import annotations

from alembic import context
from sqlalchemy import create_engine

from cronista.db.models import Base

config = context.config
target_metadata = Base.metadata


def run_migrations_online() -> None:
    url = config.attributes.get("connection_url") or config.get_main_option("sqlalchemy.url")
    if url is None:
        raise RuntimeError("URL do banco não informada ao Alembic")
    engine = create_engine(url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


run_migrations_online()
