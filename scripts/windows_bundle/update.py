"""update.py -- bring this QBCards folder up to the latest windows-app release. The Start ... launchers run it first.

The release carries version.txt ("<commit> <sha256 of QBCards-Windows.zip>"). When it differs from the copy here, the
ZIP is downloaded, checked against that hash, and the app code in it replaces the code here. Never touched: data/
(Buzz Drill results), qbr/data/ (StockFisher's question index), runtime/ (the Python running this) and the launchers.
Offline, or on any error, the current version simply starts.
"""
import hashlib
import io
import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

RELEASE = os.environ.get("QBCARDS_RELEASE", "https://github.com/tygerthelyon/qbcards/releases/download/windows-app/")
HERE = Path(__file__).resolve().parent
TOP = "QBCards/"
KEEP = ("data/", "qbr/data/", "runtime/")                 # local data and the running Python
SKIP_SUFFIXES = (".cmd",)                                  # a batch file must not change while cmd is reading it
UA = {"User-Agent": "QBCards updater"}


def fetch(name, timeout):
    req = urllib.request.Request(RELEASE + name, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    mine = (HERE / "version.txt").read_text(encoding="utf-8").split() if (HERE / "version.txt").is_file() else []
    try:
        latest = fetch("version.txt", 5).decode("utf-8").split()
    except Exception:
        return 0                                           # offline or GitHub unreachable: run what is here
    if len(latest) != 2 or latest[:1] == mine[:1]:
        return 0
    print("Updating to the latest version...", flush=True)
    try:
        blob = fetch("QBCards-Windows.zip", 120)
        if hashlib.sha256(blob).hexdigest() != latest[1]:
            raise ValueError("download did not match its checksum")
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            names = [n for n in z.namelist() if n.startswith(TOP) and not n.endswith("/")]
            if TOP + "drill_server.py" not in names:
                raise ValueError("unexpected download contents")
            for name in names:
                rel = name[len(TOP):]
                if rel.startswith(KEEP) or rel.endswith(SKIP_SUFFIXES) or rel == "version.txt":
                    continue
                target = HERE / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(name) as src, open(target, "wb") as out:
                    shutil.copyfileobj(src, out)
        (HERE / "version.txt").write_text(" ".join(latest) + "\n", encoding="utf-8")
        print("Updated.", flush=True)
    except Exception as e:
        print("Could not update (%s); starting the current version." % e, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
