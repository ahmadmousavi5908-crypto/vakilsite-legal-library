#!/usr/bin/env python3
"""Build a deterministic ZIP package and SHA-256 file for a tagged library release."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
MANIFEST = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
VERSION = MANIFEST["version"]
PACKAGE_NAME = f"vakilsite-legal-library-v{VERSION}.zip"
PACKAGE_PATH = OUTPUT / PACKAGE_NAME
ARCHIVE_ROOT = f"vakilsite-legal-library-v{VERSION}"
INCLUDED = ["README.md", "CHANGELOG.md"] + MANIFEST["files"]

OUTPUT.mkdir(parents=True, exist_ok=True)
missing = [name for name in INCLUDED if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"Missing package files: {', '.join(missing)}")

with zipfile.ZipFile(PACKAGE_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name in sorted(set(INCLUDED)):
        path = ROOT / name
        info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())

digest = hashlib.sha256(PACKAGE_PATH.read_bytes()).hexdigest()
checksum_path = OUTPUT / f"{PACKAGE_NAME}.sha256"
checksum_path.write_text(f"{digest}  {PACKAGE_NAME}\n", encoding="ascii")
print(f"PACKAGE: {PACKAGE_PATH}")
print(f"SHA256: {digest}")
print("PACKAGE BUILD PASSED")
