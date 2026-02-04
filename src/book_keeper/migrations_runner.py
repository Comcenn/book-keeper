import os
from alembic.config import Config
from alembic import command


def run_migrations() -> None:
    dirname = os.path.dirname(__file__)
    cfg = Config(os.path.join(dirname, "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(dirname, "migrations"))
    command.upgrade(cfg, "head")