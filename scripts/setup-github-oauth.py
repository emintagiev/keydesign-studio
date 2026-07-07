#!/usr/bin/env python3
"""Serve setup form + callback on one port for browser automation."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRETS_FILE = ROOT / "oauth" / "oauth-secrets.php"
PORT = 5758
REDIRECT_URL = f"http://127.0.0.1:{PORT}/callback"
OAUTH_CALLBACK = "https://www.keydesign.studio/oauth/callback?provider=github"

MANIFEST = {
    "name": "Key Design Studio CMS",
    "url": "https://www.keydesign.studio",
    "redirect_url": REDIRECT_URL,
    "callback_urls": [OAUTH_CALLBACK],
    "public": False,
    "request_oauth_on_install": False,
    "default_permissions": {"contents": "write"},
    "default_events": [],
}


class Handler(BaseHTTPRequestHandler):
    manifest_code: str | None = None

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self._serve_form()
            return
        if parsed.path == "/callback":
            params = urllib.parse.parse_qs(parsed.query)
            code = (params.get("code") or [None])[0]
            if not code:
                self.send_error(400, "Missing code")
                return
            Handler.manifest_code = code
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>OK</h1><p>App created. Close tab.</p></body></html>")
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        self.send_error(404)

    def _serve_form(self):
        manifest_json = json.dumps(MANIFEST, separators=(",", ":"))
        escaped = (
            manifest_json.replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
        )
        html = f"""<!DOCTYPE html><html><body>
<form id="f" action="https://github.com/settings/apps/new" method="post">
<input type="hidden" name="manifest" value="{escaped}">
<button type="submit">Create App</button>
</form></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):  # noqa: A003
        return


def write_secrets(client_id: str, client_secret: str) -> None:
    SECRETS_FILE.write_text(
        f"""<?php
return [
    'client_id' => '{client_id}',
    'client_secret' => '{client_secret}',
    'base_url' => 'https://www.keydesign.studio/oauth',
];
""",
        encoding="utf-8",
    )
    SECRETS_FILE.chmod(0o600)


def main() -> int:
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Serving http://127.0.0.1:{PORT}/")
    thread.join(timeout=600)
    if not Handler.manifest_code:
        print("No callback received", file=sys.stderr)
        return 1
    result = subprocess.run(
        ["gh", "api", "-X", "POST", f"/app-manifests/{Handler.manifest_code}/conversions"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        return 1
    data = json.loads(result.stdout)
    write_secrets(data["client_id"], data["client_secret"])
    print("Saved oauth/oauth-secrets.php")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
