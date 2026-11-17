"""Windows double-click / Desktop shortcut entry point for Buzz Drill."""
import contextlib
import ctypes
import datetime
import os
from pathlib import Path
import traceback


def main():
    import sys
    proj_dir = Path(__file__).resolve().parent
    os.chdir(proj_dir)
    if str(proj_dir) not in sys.path:
        sys.path.insert(0, str(proj_dir))
    log_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "BuzzDrill"
    log_path = log_dir / "app.log"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                try:
                    print("\nBuzz Drill started", datetime.datetime.now().isoformat(), flush=True)
                    from drill_server import main as run_drill

                    if run_drill(["--open"]):
                        raise RuntimeError("Startup failed. See the preceding message in the log.")
                except Exception:
                    traceback.print_exc()
                    raise
    except Exception as exc:
        ctypes.windll.user32.MessageBoxW(
            None,
            "Buzz Drill could not start.\n\n%s\n\nDetails: %s" % (exc, log_path),
            "Buzz Drill",
            0x10,
        )


if __name__ == "__main__":
    main()
