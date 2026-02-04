from book_keeper.app_dirs import ensure_data_dir
from book_keeper.migrations_runner import run_migrations

def bootstrap():
    ensure_data_dir()
    run_migrations()
