"""
Launcher for the C5.1 COUNTER Harvester.

This small file is the entry point used when the harvester is packaged
as a Windows .exe. It does three things before starting the real program:

1. Picks a fixed "data folder" (Documents\\COUNTER_Harvester_Data) and moves
   into it. The harvester saves everything (settings, providers.tsv, reports,
   database) relative to the current folder, so this keeps all the
   librarian's files in one place he can find, separate from the program.
   The program folder can then be replaced with a newer version without
   losing any data.
2. On first run, copies the starting settings files into that data folder.
3. If something goes wrong at startup, shows a pop-up with the error and
   saves the details to startup_error.txt, instead of closing silently.
"""

import os
import shutil
import sys
import traceback
from pathlib import Path

DATA_FOLDER_NAME = "COUNTER_Harvester_Data"
SEED_FILES = ("current_config.py", "default_config.py")


def bundle_dir() -> Path:
    """Folder where the packaged program's own files live."""
    if getattr(sys, "frozen", False):
        # PyInstaller puts bundled files here (the _internal folder).
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent


def documents_dir() -> Path:
    """The user's real Documents folder (handles OneDrive-redirected Documents)."""
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            CSIDL_PERSONAL = 5  # "My Documents"
            if ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf) == 0:
                return Path(buf.value)
        except Exception:
            pass
    return Path.home() / "Documents"


def prepare_data_folder() -> Path:
    """Create the data folder, copy starting settings into it, and move into it."""
    override = os.environ.get("COUNTER_HARVESTER_DATA")  # optional, for testing
    data_dir = Path(override) if override else documents_dir() / DATA_FOLDER_NAME
    data_dir.mkdir(parents=True, exist_ok=True)

    seed_dir = bundle_dir() / "seed"
    for name in SEED_FILES:
        target = data_dir / name
        source = seed_dir / name
        if not target.exists() and source.exists():
            shutil.copy2(source, target)

    os.chdir(data_dir)
    return data_dir


def redirect_missing_console(data_dir: Path) -> None:
    """A windowed .exe has no console, so send any printed text to a log file."""
    if sys.stdout is None or sys.stderr is None:
        log = open(data_dir / "console_output.txt", "w", encoding="utf-8", buffering=1)
        if sys.stdout is None:
            sys.stdout = log
        if sys.stderr is None:
            sys.stderr = log


def show_startup_error(details: str, data_dir: Path) -> None:
    """Save the error to a file and show a simple pop-up."""
    error_file = data_dir / "startup_error.txt"
    try:
        error_file.write_text(details, encoding="utf-8")
    except Exception:
        pass

    message = (
        "The COUNTER Harvester could not start.\n\n"
        f"Details were saved to:\n{error_file}\n\n"
        "Please send that file to your IT contact."
    )
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(None, message, "COUNTER Harvester", 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)
    print(details, file=sys.stderr)


def run() -> None:
    data_dir = Path.cwd()
    try:
        data_dir = prepare_data_folder()
        redirect_missing_console(data_dir)
        import main  # the harvester's own src/main.py

        main.main()
    except SystemExit:
        raise
    except Exception:
        show_startup_error(traceback.format_exc(), data_dir)
        sys.exit(1)


if __name__ == "__main__":
    run()
