"""Shared database selection and input validation for StockFisher interfaces."""
import re
import sqlite3
from pathlib import Path

from . import anki, store


def _validate_range(value, label, low, high, named=None):
    if not value:
        return
    valid = True
    for piece in value.lower().split(","):
        piece = piece.strip()
        if named and piece in named:
            continue
        if not re.fullmatch(r"\d+|\d+-\d*|-\d+", piece):
            valid = False
            break
        ends = piece.split("-")
        nums = [int(n) for n in ends if n]
        if any(n < low or n > high for n in nums) or (len(nums) == 2 and nums[0] > nums[1]):
            valid = False
            break
    if not valid:
        example = "6-9, 8, or college (levels 1–10)" if label == "Difficulty" else "2018-, 2015-2020, or 2024"
        raise ValueError("%s: use %s, or leave it blank." % (label, example))



def connect_database(path):
    """Validate and select an existing mirror. The database is opened read-only."""
    db_path = Path(path).expanduser().resolve()
    if not db_path.is_file():
        raise FileNotFoundError("Database not found. Choose an existing qbreader.sqlite file.")
    con = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True, timeout=10)
    try:
        tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")}
        if not {"u", "q", "f", "sets", "meta"}.issubset(tables):
            raise ValueError("This file does not have the expected StockFisher mirror tables.")
        units = con.execute("SELECT count(*) FROM u").fetchone()[0]
        sets = con.execute("SELECT count(*) FROM sets").fetchone()[0]
        synced = store.meta("synced", con=con)
        facets = store.meta("facets", {}, con=con)
    finally:
        con.close()

    if store._CON is not None:
        store._CON.close()
        store._CON = None
    store.PATH = str(db_path)
    anki.CACHE = str(db_path.parent / "anki_index.json")
    return {"path": str(db_path), "units": units, "sets": sets, "synced": synced,
            "categories": sorted({v for values in facets.values() for v in values})}

