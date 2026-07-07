# Project ATLAS

## Repository Purpose

This repository is the engineering source of truth for Project ATLAS. It stores approved documentation, architecture, standards, build packs, implementation packs, API contracts, database schemas, UI/UX specifications, testing strategies, and deployment procedures.

The repository reflects approved documents only. It does not generate product vision, business requirements, or architecture.

## Folder Structure

```
00_Master_Context           Master context documents and repository index
01_Architecture             System architecture and design decisions
02_Domains                  Domain models and bounded contexts
03_Engineering_Standards    Coding standards, conventions, and guidelines
04_Build_Packs              Build pack specifications
05_Implementation_Packs     Implementation pack specifications
06_API                      API contracts and specifications
07_Database                 Database schemas and migration plans
08_UI_UX                    UI/UX specifications and design assets
09_Testing                  Testing strategies and test plans
10_Deployment               Deployment procedures and infrastructure
docs                        Supplementary documentation
```

## Current Status

Engineering Initialization. Repository Version 0.1.0.

## Documentation Workflow

1. The Product Architect (ChatGPT / CTO) authors and approves documents.
2. The Repository Manager saves approved documents to the correct folder.
3. Every document preserves its original wording and formatting.
4. Filenames follow the established naming convention.
5. Internal links are maintained across documents.
6. Version changes are recorded in `CHANGELOG.md` and `VERSION.md`.
7. Git commits are made only when explicitly instructed.
