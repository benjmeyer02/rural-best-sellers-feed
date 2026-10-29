#!/usr/bin/env python3
"""Publish the six products shown in each homepage Best Sellers tab."""

import datetime as dt
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
COLLECTIONS = {"men": "mens-best-sellers", "women": "womens-best-sellers"}


def fetch_ids(handle):
    url = f"https://ruraloutfitters.store/collections/{handle}/products.json?limit=6"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; RuralBestSellersFeed/1.0)",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"{handle}: HTTP {response.status}")
        body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise RuntimeError(f"{handle}: response too large")
    products = json.loads(body)["products"]
    ids = [str(product["id"]) for product in products]
    if len(ids) != 6 or len(set(ids)) != 6 or any(not value.isdecimal() for value in ids):
        raise RuntimeError(f"{handle}: expected six distinct product IDs")
    return ids


feed = {tab: fetch_ids(handle) for tab, handle in COLLECTIONS.items()}
if set(feed["men"]) & set(feed["women"]):
    raise RuntimeError("The two homepage tabs overlap")
feed["generated_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
(ROOT / "best-sellers.json").write_text(json.dumps(feed, indent=2) + "\n")
