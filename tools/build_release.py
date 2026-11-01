#!/usr/bin/env python3
"""Build a deterministic ZIP package and SHA-256 file for a tagged library release."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
MANIFEST_PATH = ROOT / "MANIFEST.json"
if not MANIFEST_PATH.is_file():
    raise SystemExit("Missing required MANIFEST.json")

MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
VERSION = MANIFEST.get("version")
if not isinstance(VERSION, str) or not VERSION.strip():
    raise SystemExit("MANIFEST.json has no valid version")

PACKAGE_NAME = f"vakilsite-legal-library-v{VERSION}.zip"
PACKAGE_PATH = OUTPUT / PACKAGE_NAME
ARCHIVE_ROOT = f"vakilsite-legal-library-v{VERSION}"

manifest_files = MANIFEST.get("files")
if not isinstance(manifest_files, list) or not manifest_files:
    raise SystemExit("MANIFEST.json files must be a non-empty array")

for name in manifest_files:
    if not isinstance(name, str):
        raise SystemExit(f"Invalid manifest file entry: {name!r}")
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise SystemExit(f"Unsafe manifest file path: {name}")

INCLUDED = ["README.md", "CHANGELOG.md", "MANIFEST.json"] + manifest_files
if len(INCLUDED) != len(set(INCLUDED)):
    raise SystemExit("Duplicate paths in package file inventory")

missing = [name for name in INCLUDED if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"Missing package files: {', '.join(missing)}")

OUTPUT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(PACKAGE_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name in sorted(INCLUDED):
        path = ROOT / name
        info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())

expected_entries = {f"{ARCHIVE_ROOT}/{name}" for name in INCLUDED}
with zipfile.ZipFile(PACKAGE_PATH, "r") as archive:
    actual_entries = set(archive.namelist())
    if actual_entries != expected_entries:
        raise SystemExit("Package contents do not match the declared file inventory")
    if f"{ARCHIVE_ROOT}/MANIFEST.json" not in actual_entries:
        raise SystemExit("MANIFEST.json is missing from the generated package")
    packaged_manifest = json.loads(archive.read(f"{ARCHIVE_ROOT}/MANIFEST.json").decode("utf-8"))
    if packaged_manifest != MANIFEST:
        raise SystemExit("Packaged MANIFEST.json does not match the source manifest")
    bad_member = archive.testzip()
    if bad_member:
        raise SystemExit(f"Corrupt ZIP member: {bad_member}")

digest = hashlib.sha256(PACKAGE_PATH.read_bytes()).hexdigest()
checksum_path = OUTPUT / f"{PACKAGE_NAME}.sha256"
checksum_path.write_text(f"{digest}  {PACKAGE_NAME}\n", encoding="ascii")
print(f"PACKAGE: {PACKAGE_PATH}")
print(f"FILES: {len(INCLUDED)}")
print(f"SHA256: {digest}")
print("PACKAGE BUILD PASSED")
