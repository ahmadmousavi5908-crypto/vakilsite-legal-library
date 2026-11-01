# Iranian Legal Research Library

A versioned, structured Persian-language legal research dataset for Iranian law.

## Scope of v1

- Real-estate registration and property transactions (priority)
- Cheques and promissory notes (included in v1)
- Civil law and civil procedure
- General and specific criminal law
- Criminal procedure and criminology

## Design principles

1. Data only: no runtime, npm dependencies, build step, or website integration.
2. Stable identifiers; canonical terms are separate from aliases and search phrases.
3. Every legal proposition records its source and review status.
4. Unverified legal content is explicitly marked and must not be presented as definitive advice.
5. Similar legal concepts are not merged merely because users search for them interchangeably.
6. Persian text is UTF-8; JSON uses two-space indentation.

## Repository layout

- `terms/`: canonical terms, aliases, search phrases and short definitions.
- `laws/`: law metadata and source references.
- `articles/`: article-level records and cautious summaries.
- `taxonomy/`: stable subject taxonomy.
- `relations/`: links between terms, laws and articles.
- `schema/`: JSON Schema contracts.
- `validation/`: validation policy and Termux-friendly validator.
- `reports/`: review and duplicate reports.

## Termux validation

Python 3 standard library only; no pip install required.

```sh
python validation/validate_library.py
```

The validator checks JSON parsing, required fields, unique IDs, duplicate canonical terms, and references between records. It does not certify the legal correctness or current force of a law.

## Legal review policy

- `verified_primary_source`: checked against an official primary publication for the stated point.
- `secondary_source_only`: located in a secondary legal source; requires primary-source confirmation.
- `needs_legal_review`: editorial or legal review remains.
- `draft`: incomplete record.

A law's enactment date, publication date, effective date, amendments, transitional rules and implementing regulations are distinct facts. Do not infer one from another.

## Sources and research

Primary-source discovery should prioritize the Official Gazette and the National Laws and Regulations System. Secondary repositories are used for discovery and cross-checking, not as a substitute for the official text.

Initial discovery references:
- Official Gazette issue metadata for the Law on Compulsory Official Registration of Transactions Concerning Immovable Property: https://www.irancodify.com/b/قانون_الزام_به_ثبت_رسمی_معاملات_اموال_غیرمنقول_مصوب_1401-09-06
- Law text and registration-law materials: https://law-ir.ir/law/cat/2036/
- Civil Code, document provisions (Arts. 1284 onward): https://adlio.ir/law/قانون-مدنی-مصوب-1307-02-18/
- Commercial Code, promissory note provisions (Arts. 307-309): https://adlio.ir/law/قانون-تجارت-مصوب-1311-02-13/
- Cheque law research entry point: https://lawlex.ir/

The initial source list is a research log, not a representation that every law has been fully consolidated as of the release date.

## Version

Initial structured foundation: 1.0.0
