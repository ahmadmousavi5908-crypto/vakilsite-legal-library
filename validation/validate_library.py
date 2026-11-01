#!/usr/bin/env python3
"""Validate JSON structure and cross-references using Python's standard library."""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
JSON_FILES = sorted(ROOT.rglob("*.json"))


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


def normalize(value):
    value = unicodedata.normalize("NFKC", value).replace("ي", "ی").replace("ك", "ک")
    return re.sub(r"[\u200c\s]+", " ", value).strip()


data = {p.relative_to(ROOT).as_posix(): read_json(p) for p in JSON_FILES}
terms = data.get("terms/terms.json", {}).get("records", [])
laws = data.get("laws/laws.json", {}).get("records", [])
articles = data.get("articles/articles.json", {}).get("records", [])
ids = {}
for group in (terms, laws, articles):
    for record in group:
        key = record.get("id")
        if not key:
            ERRORS.append("A record has no id")
        elif key in ids:
            ERRORS.append(f"Duplicate id: {key}")
        else:
            ids[key] = record

canonical = {}
for term in terms:
    key = normalize(term.get("canonical", ""))
    if not key:
        ERRORS.append(f"Empty canonical term: {term.get('id')}")
    elif key in canonical:
        ERRORS.append(f"Duplicate canonical term: {term.get('id')} and {canonical[key]}")
    else:
        canonical[key] = term.get("id")
    if term.get("review_status") not in {"verified_primary_source", "secondary_source_only", "needs_legal_review", "draft"}:
        ERRORS.append(f"Invalid review status: {term.get('id')}")
    for ref in term.get("law_refs", []):
        if ref not in {item.get("id") for item in laws}:
            ERRORS.append(f"Unknown law reference {ref} in {term.get('id')}")
    for ref in term.get("article_refs", []):
        if ref not in {item.get("id") for item in articles}:
            ERRORS.append(f"Unknown article reference {ref} in {term.get('id')}")

law_ids = {item.get("id") for item in laws}
for article in articles:
    if article.get("law_id") not in law_ids:
        ERRORS.append(f"Unknown law for article {article.get('id')}")

for relation in data.get("relations/legal-content-links.json", {}).get("relations", []):
    for endpoint in ("from", "to"):
        if relation.get(endpoint) not in ids:
            ERRORS.append(f"Unknown relation endpoint: {relation.get(endpoint)}")

report = {
    "json_files": len(JSON_FILES),
    "terms": len(terms),
    "laws": len(laws),
    "articles": len(articles),
    "errors": ERRORS,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
if ERRORS:
    sys.exit(1)
print("VALIDATION PASSED")
