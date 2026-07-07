# Project ATLAS

## Repository Purpose

This repository is the engineering source of truth for Project ATLAS. It stores approved documentation, architecture, standards, build packs, implementation packs, API contracts, database schemas, UI/UX specifications, testing strategies, and deployment procedures.

The repository reflects approved documents only. It does not generate product vision, business requirements, or architecture.

## Folder Structure

```
00_Master_Context           Master context documents and repository index
01_Architecture             System architecture and design decisions
02_Domains                  Domain models and bounded contexts
03_Engineering_Standards    Engineering standards, conventions, and guidelines
04_Build_Packs              Build pack specifications
05_Reference_Architecture   Reference implementation blueprints
06_Implementation_Packs     Implementation pack specifications
07_ADRs                     Architecture Decision Records
08_Templates                Repository document templates
09_Assets                   Repository assets
10_API                      API contracts and specifications
11_Database                 Database schemas and migration plans
12_UI_UX                    UI/UX specifications and design assets
13_Testing                  Testing strategies and test plans
14_Deployment               Deployment procedures and infrastructure
99_Reference                Reference materials
docs                        Supplementary documentation
```

The authoritative repository structure and navigation index is `00_Master_Context/MC-000_Repository_Index.md`.

## Current Status

Documentation Foundation — Reference Architecture Phase Preparation. Repository Version 0.2.0 (see `VERSION.md`).

## Documentation Workflow

1. The Product Architect (ChatGPT / CTO) authors and approves documents.
2. The Repository Manager saves approved documents to the correct folder.
3. Every document preserves its original wording and formatting.
4. Filenames follow the established naming convention.
5. Internal links are maintained across documents.
6. Version changes are recorded in `CHANGELOG.md` and `VERSION.md`.
7. Git commits are made only when explicitly instructed.
