from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def _default_inbox() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "hermes-agent" / "webhooks" / "inbox"


def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def _verify_sig(secret: bytes, body: bytes, sig_header: str) -> bool:
    # GitHub sends: "sha256=<hex>"
    if not sig_header or not sig_header.startswith("sha256="):
        return False
    got = sig_header.split("=", 1)[1].strip()
    mac = hmac.new(secret, msg=body, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, got)


@dataclass
class StoredEvent:
    filename: str
    event: str
    delivery: str
    ts: str

    def __str__(self) -> str:
        return f"{self.ts} {self.event} {self.delivery} {self.filename}"


def serve(*, host: str, port: int, path: str, inbox_dir: Optional[Path] = None) -> None:
    inbox = _ensure_dir((inbox_dir or _default_inbox()).expanduser().resolve())
    secret = os.environ.get("HERMES_GITHUB_WEBHOOK_SECRET", "").encode("utf-8")
    if not secret:
        raise SystemExit("HERMES_GITHUB_WEBHOOK_SECRET is required (non-empty)")

    webhook_path = path if path.startswith("/") else ("/" + path)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa: N802
            p = urlparse(self.path).path
            if p != webhook_path:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"not found")
                return

            length = int(self.headers.get("Content-Length", "0") or "0")
            body = self.rfile.read(length) if length > 0 else b""

            sig = self.headers.get("X-Hub-Signature-256", "")
            if not _verify_sig(secret, body, sig):
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"invalid signature")
                return

            event = self.headers.get("X-GitHub-Event", "unknown")
            delivery = self.headers.get("X-GitHub-Delivery", "unknown")

            try:
                payload = json.loads(body.decode("utf-8"))
            except Exception:
                payload = {"_raw": body.decode("utf-8", errors="replace")}

            ts = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{ts}__{event}__{delivery}.json"
            (inbox / filename).write_text(json.dumps({
                "event": event,
                "delivery": delivery,
                "received_at": ts,
                "headers": {
                    "X-GitHub-Event": event,
                    "X-GitHub-Delivery": delivery,
                },
                "payload": payload,
            }, indent=2))

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "stored": filename}).encode("utf-8"))

        def log_message(self, format, *args):  # noqa: A002
            # Keep it quiet; receiver should be safe for systemd logs.
            return

    httpd = HTTPServer((host, port), Handler)
    print(f"Hermes webhook receiver listening on http://{host}:{port}{webhook_path}")
    print(f"Inbox: {inbox}")
    httpd.serve_forever()


def list_events(*, inbox_dir: Optional[Path] = None, limit: int = 20) -> list[StoredEvent]:
    inbox = _ensure_dir((inbox_dir or _default_inbox()).expanduser().resolve())
    files = sorted([p for p in inbox.glob("*.json")], key=lambda p: p.name, reverse=True)
    out: list[StoredEvent] = []
    for p in files[: max(0, limit)]:
        parts = p.name.split("__", 2)
        ts = parts[0] if parts else "?"
        event = parts[1] if len(parts) > 1 else "?"
        delivery = (parts[2].rsplit(".", 1)[0] if len(parts) > 2 else "?")
        out.append(StoredEvent(filename=p.name, event=event, delivery=delivery, ts=ts))
    return out


def read_event(*, filename: str, inbox_dir: Optional[Path] = None) -> str:
    inbox = _ensure_dir((inbox_dir or _default_inbox()).expanduser().resolve())
    p = (inbox / filename).resolve()
    if inbox not in p.parents:
        raise ValueError("invalid filename")
    return p.read_text()

