import os
from pathlib import Path
from alembic.config import Config
from alembic import command

from book_keeper.app_dirs import resource_path


def run_migrations() -> None:
    alembic_ini = resource_path("alembic.ini")
    migrations_dir = resource_path("migrations")

    cfg = Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(migrations_dir))

    command.upgrade(cfg, "head")
