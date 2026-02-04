from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_keeper.app_dirs import ensure_data_dir


db_dir = ensure_data_dir()
db_path = db_dir / "bookkeeper.db"


engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=True)

sessionLocal = sessionmaker(bind=engine)
