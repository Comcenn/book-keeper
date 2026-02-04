from pathlib import Path
import sys
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
    path = get_app_data_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def resource_path(relative: str | Path) -> Path:
    """
    Resolve a resource path both in development and when frozen by PyInstaller.

    - In development: returns <project-root>/<relative>
    - In PyInstaller: returns <_MEIPASS>/<relative>
    """

    relative = Path(relative)

    if hasattr(sys, "_MEIPASS"):
        # Running inside a PyInstaller bundle
        return Path(sys._MEIPASS) / relative  # type: ignore

    return Path(__file__).resolve().parent.parent.parent / relative
