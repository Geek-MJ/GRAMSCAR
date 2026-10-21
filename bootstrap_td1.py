#!/usr/bin/env python3
"""Restore the official ESILV TD1 runtime files without touching group results."""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

ARCHIVE_URL = (
    "https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/"
    "next-generation-ai/latest/downloads/esilv-student-2026-10-18.zip"
)
ARCHIVE_SHA256 = "e14ebfb4437ca6a54a4c6d0edf7a1f65ec028d01764b884b2b6e46880dd78cb4"
FILES = (
    "skeleton-multi-llm-en.py",
    "sandbox_sqlite.py",
    "verify-data.py",
    "check_access.py",
    "atelier-vote.py",
    "atelier-routage.py",
    "schema.sql",
    "questions-td1.json",
    "modeles-autorises.json",
    "data/boutique.sqlite",
    "data/product.csv",
    "data/customers.csv",
    "data/orders.csv",
    "data/manifest.json",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, help="Local copy of the official kit ZIP (offline setup)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.zip:
        raw = args.zip.read_bytes()
    else:
        with urllib.request.urlopen(ARCHIVE_URL, timeout=60) as response:
            raw = response.read()
    if hashlib.sha256(raw).hexdigest() != ARCHIVE_SHA256:
        raise SystemExit("Student kit SHA-256 differs from the verified 2026-10-18 archive.")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for relative in FILES:
            original = archive.read("kit-td1/" + relative)
            destination = root / relative
            if destination.exists():
                if destination.read_bytes() != original:
                    if relative == "modeles-autorises.json":
                        print("Keeping repository modeles-autorises.json")
                        continue
                    raise SystemExit(f"Different local file: {relative} (not overwritten)")
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(original)
            print(f"Restored {relative}")
    print("Done. Verify with: python verify-data.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
