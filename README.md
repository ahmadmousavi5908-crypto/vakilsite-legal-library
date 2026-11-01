# Iranian Legal Research Library

A versioned, structured Persian-language legal research dataset for Iranian law.

## Version 1.0.0 scope

- **Registration and real estate:** priority area, including official and ordinary documents, title deeds, cadastral mapping, parcel identifiers, unregistered property, registration claims and property boundaries.
- **Cheques and commercial instruments:** included from the first version, including Sayad cheques, registration and transfer, non-payment certificates, promissory notes (سفته), required particulars and protest (واخواست).
- Civil law and civil procedure.
- General and specific criminal law, criminal procedure and criminology.

Initial content: 45 terms, 16 law records and 10 article summaries.

## Repository layout

- `terms/terms.json`: canonical terms, search titles, aliases, definitions and legal references.
- `laws/laws.json`: law metadata, source links and review status.
- `articles/articles.json`: article-level summaries linked to their parent law.
- `taxonomy/categories.json`: stable subject categories and educational tags.
- `relations/legal-content-links.json`: links between terms and legal provisions.
- `schema/record-contracts.json`: JSON Schema contracts for core records.
- `validation/validate_library.py`: local structural and reference validator.
- `reports/source-review.json`: source discovery and review limitations.
- `MANIFEST.json`: version, file inventory and record counts.

## Termux validation

Python 3 standard library only. No pip install, npm install, build step or website integration is required.

From the extracted repository directory, run:

```sh
python validation/validate_library.py
```

The validator checks JSON parsing, unique IDs, duplicate canonical terms and cross-references. It does **not** certify legal correctness, the current validity of legislation, completeness of amendments or the current operation of government systems.

## Legal review policy

- `verified_primary_source`: checked against an official primary publication for the stated point.
- `secondary_source_only`: located in a secondary legal source; primary-source confirmation remains necessary.
- `needs_legal_review`: legal or editorial review remains.
- `draft`: incomplete record.

A law's enactment date, publication date, effective date, amendments, transitional rules and implementing regulations are distinct facts. Do not infer one from another.

## Source policy

Primary-source verification must prioritize the Official Gazette and the National Laws and Regulations System. Secondary repositories are used for discovery and cross-checking, not as a substitute for official texts.

The current source-review report explicitly records the limitations of the initial research. In particular, cheque-law deadlines, criminal consequences, Sayad-system rules and the implementation timeline of the compulsory real-estate registration law are not presented as fully verified in this release.

## Safety and use

This repository is a research dataset, not legal advice and not a substitute for checking the current official text before advising a client, drafting a pleading or calculating a deadline. Similar concepts are kept separate unless their legal equivalence is established.

The repository is data-only and is not connected to the Vakilsite production website. Do not copy these files into the website project until a separate integration review is approved.
