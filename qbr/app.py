"""Local StockFisher app. Run with python -m qbr.app; no notebook is required.

One request thread owns the engine's SQLite connection. The server only binds to
loopback, serves an explicit asset list, and authenticates API calls from its UI.
"""
import argparse
import hmac
import json
import os
import secrets
import sqlite3
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from urllib.request import urlopen

import qbr
from . import find, store
from .ui import _validate_range, connect_database

ASSETS = Path(__file__).with_name("web")


def _text(data, key, maximum=500, required=False):
    value = data.get(key, "")
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError("%s must be text of at most %s characters." % (key.capitalize(), maximum))
    value = value.strip()
    if required and not value:
        raise ValueError("Enter %s first." % key.replace("_", " "))
    return value


def _integer(data, key, default, low, high):
    value = data.get(key, default)
    if isinstance(value, bool) or not str(value).isdigit() or not low <= int(value) <= high:
        raise ValueError("%s must be between %s and %s." % (key.capitalize(), low, high))
    return int(value)


def _filters(data):
    category = _text(data, "category")
    difficulty = _text(data, "difficulty", 100)
    year = _text(data, "year", 100)
    _validate_range(difficulty, "Difficulty", 1, 10, find.LEVELS)
    _validate_range(year, "Years", 1, 2100)
    return {"cat": category or None, "diff": difficulty or None, "year": year or None}


class Application:
    def status(self):
        try:
            info = connect_database(store.PATH)
            return dict(info, connected=True)
        except (OSError, ValueError, sqlite3.Error) as exc:
            return {"connected": False, "path": store.PATH, "error": str(exc), "categories": []}

    def query(self, action, data):
        if action == "database":
            return dict(connect_database(_text(data, "path", 4096, required=True)), connected=True)
        filters = _filters(data)
        if action == "profile":
            name = _text(data, "query", required=True)
            ranking = data.get("ranking", "spec")
            if ranking not in ("spec", "n", "pyramid"):
                raise ValueError("Choose specificity, frequency, or clue position.")
            for key in ("exact", "anki"):
                if key in data and not isinstance(data[key], bool):
                    raise ValueError("%s must be true or false." % key)
            return qbr.profile(name, sort=ranking, top=_integer(data, "limit", 20, 1, 100),
                               exact=data.get("exact", False), anki=data.get("anki", False),
                               exclude=[s.strip() for s in _text(data, "exclude").split(",") if s.strip()],
                               **filters)
        if action == "search":
            return qbr.search(_text(data, "query", required=True), n=20,
                              offset=_integer(data, "offset", 0, 0, 1000000), **filters)
        if action == "check":
            return qbr.verify_clue(_text(data, "answer", required=True),
                                   _text(data, "clue", 4000, required=True), **filters)
        raise ValueError("Unknown action.")


class AppServer(HTTPServer):
    allow_reuse_address = sys.platform != "win32"
    request_queue_size = 64

    def __init__(self, port=8766, application=None):
        super().__init__(("127.0.0.1", port), Handler)
        self.app = application or Application()
        self.token = secrets.token_urlsafe(32)
        self.origin = "http://127.0.0.1:%s" % self.server_port

    def serve_forever(self, poll_interval=0.25):
        try:
            super().serve_forever(poll_interval)
        finally:
            if store._CON is not None:
                store._CON.close()
                store._CON = None


class Handler(BaseHTTPRequestHandler):
    server_version = "StockFisher"

    def log_message(self, _format, *_args):
        pass

    def _send(self, status, content, mime="application/json; charset=utf-8"):
        payload = content.encode("utf-8") if isinstance(content, str) else content
        self.close_connection = True
        self.send_response(status)
        self.send_header("Connection", "close")
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; "
                         "img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; "
                         "frame-ancestors 'none'; form-action 'self'")
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, status, value):
        self._send(status, json.dumps(value, ensure_ascii=False))

    def _allowed(self, api=False):
        host = urlsplit(self.server.origin).netloc
        if self.headers.get("Host") != host or self.headers.get("Origin", self.server.origin) != self.server.origin:
            self._json(403, {"error": "This app only accepts local requests from its own window."})
            return False
        if api and not hmac.compare_digest(self.headers.get("X-StockFisher-Token", ""), self.server.token):
            self._json(403, {"error": "Reload StockFisher to reconnect."})
            return False
        return True

    def do_GET(self):
        url = urlsplit(self.path)
        if not self._allowed(api=url.path.startswith("/api/")):
            return
        if url.path == "/health":
            return self._json(200, {"app": "StockFisher", "version": 1, "root": str(Path(__file__).resolve().parent)})
        if url.path == "/":
            page = (ASSETS / "index.html").read_text(encoding="utf-8").replace("__SESSION_TOKEN__", self.server.token)
            return self._send(200, page, "text/html; charset=utf-8")
        assets = {"/app.js": ("app.js", "text/javascript"), "/app.css": ("app.css", "text/css"),
                  "/favicon.svg": ("favicon.svg", "image/svg+xml")}
        if url.path in assets:
            name, mime = assets[url.path]
            return self._send(200, (ASSETS / name).read_bytes(), mime + "; charset=utf-8")
        try:
            if url.path == "/api/status":
                return self._json(200, self.server.app.status())
            if url.path == "/api/question":
                uid = parse_qs(url.query).get("uid", [""])[0]
                if not uid.isdigit():
                    raise ValueError("Choose a source question from the results.")
                result = qbr.show(int(uid))
                return self._json(200 if result else 404, result or {"error": "Source question not found."})
            self._json(404, {"error": "Page not found."})
        except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
            self._json(400, {"error": str(exc)})

    def do_POST(self):
        if not self._allowed(api=True):
            return
        action = urlsplit(self.path).path.removeprefix("/api/")
        if action == "shutdown":
            self._json(200, {"closed": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        if action not in ("profile", "search", "check", "database"):
            return self._json(404, {"error": "Unknown action."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536 or self.headers.get_content_type() != "application/json":
                raise ValueError("Send a small JSON request.")
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object.")
            self._json(200, self.server.app.query(action, data))
        except sqlite3.OperationalError as exc:
            message = ("The search could not be parsed. Try a plain phrase or check your quotation marks."
                       if "fts5" in str(exc).lower() or "syntax" in str(exc).lower() else str(exc))
            self._json(400, {"error": message})
        except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
            self._json(400, {"error": str(exc)})


def open_window(url):
    """Use an app-style browser window when available, otherwise the default browser."""
    if sys.platform == "win32":
        for base, relative in (("PROGRAMFILES", "Google/Chrome/Application/chrome.exe"),
                               ("PROGRAMFILES(X86)", "Microsoft/Edge/Application/msedge.exe")):
            executable = Path(os.environ.get(base, "")) / relative
            if executable.is_file():
                subprocess.Popen([str(executable), "--app=" + url, "--new-window", "--window-size=1280,900"])
                return
    webbrowser.open(url)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")

    raw_args = sys.argv[1:] if argv is None else argv
    explicit_port = any(a == "--port" or a.startswith("--port=") for a in raw_args)
    ports = [args.port] if explicit_port else [args.port, 8767, 8768, 8769, 8770]

    server = None
    for port in ports:
        try:
            server = AppServer(port)
            break
        except OSError:
            url = "http://127.0.0.1:%s" % port
            try:
                with urlopen(url + "/health", timeout=2) as response:
                    health = json.load(response)
                if health.get("app") == "StockFisher" and health.get("root") == str(Path(__file__).resolve().parent):
                    if not args.no_browser:
                        open_window(url)
                    return 0
            except (OSError, ValueError):
                pass
            continue

    if server is None:
        print("Port %s is in use. Try --port with another number." % args.port, file=sys.stderr)
        return 1
    print("StockFisher is ready at %s" % server.origin, flush=True)
    if not args.no_browser:
        open_window(server.origin)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
