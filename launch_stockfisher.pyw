"""Windows double-click entry point; keep startup errors visible without a console."""
import contextlib
import ctypes
import datetime
import os
from pathlib import Path
import traceback


def main():
    import sys
    proj_dir = Path(__file__).resolve().parent
    if not (proj_dir / "qbr").is_dir():
        proj_dir = Path(r"C:\QB\qbcards")
    os.chdir(proj_dir)
    if str(proj_dir) not in sys.path:
        sys.path.insert(0, str(proj_dir))
    log_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "StockFisher"
    log_path = log_dir / "app.log"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                try:
                    print("\nStockFisher started", datetime.datetime.now().isoformat(), flush=True)
                    from qbr.app import main as run_app

                    if run_app():
                        raise RuntimeError("Startup failed. See the preceding message in the log.")
                except Exception:
                    traceback.print_exc()
                    raise
    except Exception as exc:
        ctypes.windll.user32.MessageBoxW(
            None,
            "StockFisher could not start.\n\n%s\n\nDetails: %s" % (exc, log_path),
            "StockFisher",
            0x10,
        )


if __name__ == "__main__":
    main()
