from pathlib import Path
import platform


def get_app_data_dir() -> Path:
    home = Path.home()
    system = platform.system()

    if system == "Windows":
        return home / "AppData" / "Local" / "BookKeeper"

    if system == "Darwin":
        return home / "Library" / "Application Support" / "BookKeeper"
    
    return home / ".local" / "share" / "bookkeeper"


def ensure_data_dir() -> Path:
    path =get_app_data_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path