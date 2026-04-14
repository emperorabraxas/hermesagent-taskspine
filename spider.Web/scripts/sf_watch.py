#!/usr/bin/env python3
"""
Open a *visible* CamouFox browser session into a Salesforce org using the local `sf` CLI session.

Goal: let you "watch" UI validation in a real browser window (not API-only checks).

Usage:
  cd spider.Web
  ./.venv/bin/python scripts/sf_watch.py --target-org joedev --path /lightning/o/Opportunity/list
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import urllib.parse


def _sf_org_display(target_org: str) -> dict:
    # `sf` sometimes prints plugin warnings before the JSON payload.
    # Extract the first JSON object from the combined output.
    out = subprocess.check_output(
        ["sf", "org", "display", "-o", target_org, "--json"],
        stderr=subprocess.STDOUT,
        text=True,
    )
    # `sf` sometimes prints JS-ish objects (single quotes) in plugin warnings that contain `{`.
    # The real payload starts at the JSON object with the "status" key.
    start = out.find('{\n  "status"')
    if start == -1:
        start = out.find('{"status"')
    if start == -1:
        raise RuntimeError(out[:800] or "sf org display produced no JSON payload")
    decoder = json.JSONDecoder()
    data, _end = decoder.raw_decode(out[start:])
    if data.get("status") != 0:
        raise RuntimeError(out[:800])
    return data["result"]


async def _run(target_org: str, path: str, wait_seconds: int) -> int:
    try:
        from camoufox.async_api import AsyncCamoufox
    except Exception:
        print("CamouFox is not installed in this venv. Run: pip install camoufox", file=sys.stderr)
        return 2

    org = _sf_org_display(target_org)
    instance_url = org["instanceUrl"].rstrip("/")
    access_token = org["accessToken"]

    nav_path = path if path.startswith("/") else f"/{path}"
    login_url = (
        f"{instance_url}/secur/frontdoor.jsp?"
        + urllib.parse.urlencode({"sid": access_token, "retURL": nav_path})
    )

    print(f"[sf_watch] org={target_org} instance={instance_url}")
    print(f"[sf_watch] opening: {nav_path}")
    print("[sf_watch] Close the browser window or press Ctrl+C here to exit.")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1600, "height": 950})
        await page.goto(login_url, wait_until="networkidle", timeout=60000)
        # Give Lightning time to hydrate.
        await page.wait_for_timeout(wait_seconds * 1000)
        # Keep session alive for interactive/manual testing.
        await asyncio.Event().wait()

    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--target-org", default="joedev")
    p.add_argument("--path", default="/lightning/page/home")
    p.add_argument("--wait-seconds", type=int, default=8)
    args = p.parse_args()

    try:
        return asyncio.run(_run(args.target_org, args.path, args.wait_seconds))
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
