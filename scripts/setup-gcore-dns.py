#!/usr/bin/env python3
"""Switch keydesign.studio DNS to Gcore CDN via Cloudflare API.

Requires env CLOUDFLARE_API_TOKEN with Zone.DNS Edit permission.

Usage:
  CLOUDFLARE_API_TOKEN=... python3 scripts/setup-gcore-dns.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

ZONE_ID = "3deda2169b93891d12e6fdf96463164d"
GCORE_CNAME = "cl-glf1425f83.gcdn.co"
ORIGIN_IP = "92.53.96.132"
API = "https://api.cloudflare.com/client/v4"


def api(method: str, path: str, body: dict | None = None) -> dict:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not token:
        print("ERROR: set CLOUDFLARE_API_TOKEN (Zone.DNS Edit for keydesign.studio)", file=sys.stderr)
        sys.exit(1)

    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        print(f"API error {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)


def list_records() -> list[dict]:
    result = api("GET", f"/zones/{ZONE_ID}/dns_records?per_page=100")
    if not result.get("success"):
        print(result, file=sys.stderr)
        sys.exit(1)
    return result["result"]


def upsert_cname(name: str, target: str, records: list[dict]) -> None:
    existing = next((r for r in records if r["name"] == name and r["type"] in ("A", "CNAME")), None)
    payload = {
        "type": "CNAME",
        "name": name,
        "content": target,
        "proxied": False,
        "ttl": 300,
    }
    if existing:
        if existing["type"] == "CNAME" and existing["content"] == target and not existing.get("proxied"):
            print(f"OK  {name} already CNAME -> {target}")
            return
        api("PUT", f"/zones/{ZONE_ID}/dns_records/{existing['id']}", payload)
        print(f"UPD {name} -> CNAME {target}")
    else:
        api("POST", f"/zones/{ZONE_ID}/dns_records", payload)
        print(f"ADD {name} -> CNAME {target}")


def upsert_origin(records: list[dict]) -> None:
    name = f"origin.keydesign.studio"
    existing = next((r for r in records if r["name"] == name), None)
    payload = {
        "type": "A",
        "name": "origin",
        "content": ORIGIN_IP,
        "proxied": False,
        "ttl": 300,
    }
    if existing:
        if existing["type"] == "A" and existing["content"] == ORIGIN_IP and not existing.get("proxied"):
            print(f"OK  {name} already A -> {ORIGIN_IP}")
            return
        api("PUT", f"/zones/{ZONE_ID}/dns_records/{existing['id']}", payload)
        print(f"UPD {name} -> A {ORIGIN_IP}")
    else:
        api("POST", f"/zones/{ZONE_ID}/dns_records", payload)
        print(f"ADD {name} -> A {ORIGIN_IP}")


def main() -> None:
    records = list_records()
    upsert_origin(records)
    upsert_cname("www.keydesign.studio", GCORE_CNAME, records)
    upsert_cname("keydesign.studio", GCORE_CNAME, records)
    print("Done. Wait ~5 min for DNS, then test https://www.keydesign.studio/")


if __name__ == "__main__":
    main()
