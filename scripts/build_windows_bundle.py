"""build_windows_bundle.py -- make QBCards-Windows.zip: Buzz Drill and StockFisher with Python built in.

Downloads the official Windows embeddable Python (checked against its SHA-256), adds the two apps and the launchers in
scripts/windows_bundle/, and zips everything under one QBCards/ folder, so a user extracts it and double-clicks
"Start Buzz Drill" without installing anything. GitHub Actions runs this on every push that changes the apps and
publishes the ZIP to the windows-app release (.github/workflows/windows-bundle.yml).

    python scripts/build_windows_bundle.py              writes dist/QBCards-Windows.zip
"""
import argparse
import hashlib
import io
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON = "3.14.6"
SHA256 = "df901e84a896ff1ee720ad03377e0c8d8c2244fda79808aeeaff6316df1cb75c"
URL = "https://www.python.org/ftp/python/%s/python-%s-embed-amd64.zip" % (PYTHON, PYTHON)
APP = ["LICENSE", "drill_server.py", "stockfisher.ico", "drill", "qbr"]
SKIP_DIRS = {"__pycache__", "data"}          # qbr/data holds a local mirror; data/ holds a user's buzzes
LAUNCHERS = ROOT / "scripts" / "windows_bundle"
TOP = "QBCards/"


def embeddable(cache):
    """The embeddable Python ZIP, downloaded once into `cache` and verified."""
    path = cache / Path(URL).name
    if not path.is_file():
        cache.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL, timeout=120) as r:
            path.write_bytes(r.read())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SHA256:
        path.unlink()
        raise SystemExit("checksum mismatch for %s: got %s" % (URL, digest))
    return path


def app_files():
    for name in APP:
        p = ROOT / name
        if p.is_file():
            yield p
            continue
        for f in sorted(p.rglob("*")):
            if f.is_file() and not SKIP_DIRS & set(f.relative_to(ROOT).parts[:-1]):
                yield f


def crlf(data):
    return data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


def build(out):
    py_zip = embeddable(out / "cache")
    out.mkdir(parents=True, exist_ok=True)
    target = out / "QBCards-Windows.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        with zipfile.ZipFile(py_zip) as src:
            for info in src.infolist():
                data = src.read(info)
                if info.filename.endswith("._pth"):
                    # the embeddable Python only searches the folders listed here; ".." is the QBCards folder
                    data = data.rstrip(b"\r\n") + b"\r\n..\r\n"
                z.writestr(TOP + "runtime/" + info.filename, data)
        for f in app_files():
            z.write(f, TOP + f.relative_to(ROOT).as_posix())
        for f in sorted(LAUNCHERS.iterdir()):
            if f.suffix in (".cmd", ".txt"):
                z.writestr(TOP + f.name, crlf(f.read_bytes()))
    return target


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    args = ap.parse_args(argv)
    target = build(args.out.resolve())
    with zipfile.ZipFile(target) as z:
        count = len(z.namelist())
    print("%s: %d files, %.1f MB (Python %s)" % (target, count, target.stat().st_size / 1e6, PYTHON))


if __name__ == "__main__":
    main()
