# PROJECT_MANIFEST.md

---

## Document Information

| Field | Value |
|--------|--------|
| Document Title | Project Manifest — Repository Constitution |
| Version | 1.0.0 |
| Status | Active |
| Repository | Project ATLAS Engineering Repository |
| Owner | Repository Maintainer |
| Product Owner | Anil Kumar |
| Classification | Repository Governance |
| Last Updated | 2026-07-07 |

> This manifest summarizes repository governance only. It does **not** replace the Master Context documents (MC-001 to MC-005) or any Architecture Document. Where any conflict exists, the approved source documents take precedence.

---

## 1. Project Information

**Project Name**

Project ATLAS — an AI-Native Enterprise Knowledge Platform that transforms organizational conversations, meetings, documents, operational events, and business decisions into structured, governed, searchable, and continuously evolving enterprise knowledge (MC-001).

**Repository Purpose**

This repository is the engineering source of truth for Project ATLAS. It stores approved documentation, architecture, standards, build packs, implementation packs, API contracts, database schemas, UI/UX specifications, testing strategies, and deployment procedures. The repository reflects approved documents only. It does not generate product vision, business requirements, or architecture.

**Repository Version**

0.1.0 — Engineering Initialization (see `VERSION.md`).

---

## 2. Repository Mission

The repository exists to serve as the single authoritative source for all product, architecture, engineering, and implementation documentation of Project ATLAS (MC-004, Repository Governance).

Its mission is to ensure that documentation remains:

- Consistent
- Traceable
- Version-controlled
- Maintainable throughout the product lifecycle

Every document committed to the repository becomes part of the official engineering knowledge base.

---

## 3. Repository Philosophy

Derived from MC-004 and BP-000:

- **Single Source of Truth** — the repository is the authoritative record; no implementation may contradict approved documentation.
- **Documentation Before Implementation** — every major feature must have documentation before implementation begins.
- **Immutable Version History** — repository history must remain traceable.
- **Controlled Change Management** — all changes follow governed processes.
- **Traceable Engineering Decisions** — decisions are documented, never assumed.
- **Repository-wide Consistency** — no document may contradict a higher-authority document.

---

## 4. Repository Structure

The repository structure is fixed and defined by the approved architecture (README, BP-000). No new top-level folders may be added without formal approval.

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
99_Assets                   Repository assets
docs                        Supplementary documentation
```

Root files: `README.md`, `PROJECT_MANIFEST.md`, `VERSION.md`, `CHANGELOG.md`.

---

## 5. Documentation Hierarchy

The architectural hierarchy is mandatory (MC-004, Architecture Governance). No lower-level artifact may redefine responsibilities established by a higher-level artifact.

```
Master Context (MC Series)
        ↓
Architecture Documents
        ↓
Domain Documents
        ↓
Engineering Standards
        ↓
Build Packs
        ↓
Implementation Packs
        ↓
Source Code
        ↓
Testing
        ↓
Deployment
        ↓
Production
```

MC-001 is the constitutional authority. If any future document conflicts with MC-001, MC-001 takes precedence until formally amended through version control.

---

## 6. Naming Convention

Filenames follow the established repository naming convention (README):

- **Master Context documents:** `MC-XXX_Document_Title.md` (e.g., `MC-001_Project_Vision_and_Product_Charter.md`)
- **Build Packs:** `BP-XXX_Document_Title.md` (e.g., `BP-000_Engineering_Foundation.md`)
- **Folders:** two-digit numeric prefix followed by an underscore-separated name (e.g., `04_Build_Packs`)
- Document titles within filenames use `Title_Case_With_Underscores`
- Every document declares its Document ID, Title, Version, Status, Owner, and Repository Path in its header

---

## 7. Versioning Policy

Versioning follows the change classification defined in MC-004 (Change Management):

| Change Type | Examples | Version Increment |
|-------------|----------|-------------------|
| Editorial Changes | Grammar, formatting, clarifications | Patch (e.g., 1.0.1) |
| Functional Improvements | Additional capabilities, new workflows, new documentation sections | Minor (e.g., 1.1.0) |
| Breaking Strategic Changes | Product vision, platform architecture, business model, multi-tenant strategy changes | Major (e.g., 2.0.0) |

- Major version changes require architecture review and formal approval.
- Repository-level version changes are recorded in `CHANGELOG.md` and `VERSION.md`.
- Every document maintains its own Version History section.

---

## 8. Repository Rules

- The repository reflects approved documents only.
- Every document preserves its original wording and formatting when saved.
- Documents are saved to the correct folder per the fixed repository structure.
- Internal links are maintained across documents.
- No document shall exist without an identified owner (MC-004, Document Ownership).
- No document may skip lifecycle review stages (MC-004, Document Lifecycle).
- Failure to comply with governance is treated as a repository governance violation requiring formal review before implementation proceeds.

---

## 9. Documentation Rules

Documentation is the authoritative source of truth (MC-004, Documentation Governance):

- Documentation precedes implementation.
- Documentation must remain synchronized with the platform.
- Breaking changes require documentation updates.
- Repository history must remain traceable.
- Documentation is version controlled.

Minimum ownership fields for every document: Document Owner, Technical Reviewer, Business Reviewer, Approval Authority, Current Version, Repository Location.

Before approval, every document must satisfy the Quality Gates defined in MC-004: Business Quality, Architecture Quality, Engineering Quality, and Documentation Quality.

---

## 10. Git Workflow

Defined by README (Documentation Workflow) and BP-000 (Git Rules):

1. The Product Architect authors and approves documents.
2. The Repository Manager saves approved documents to the correct folder.
3. Version changes are recorded in `CHANGELOG.md` and `VERSION.md`.
4. Git commits are made **only when explicitly instructed**.
5. Every approved Build Pack must be committed separately.
6. Engineering commits must remain atomic.

Recommended commit format for documentation:

```
docs(bp-xxx): add build pack
```

---

## 11. Architecture Decision Record (ADR) Policy

Every significant business or technical decision shall be documented (MC-004, Decision Governance). Each decision record should include:

- Decision Identifier
- Decision Summary
- Business Context
- Alternatives Considered
- Final Decision
- Business Justification
- Technical Impact
- Risks
- Approval Authority
- Decision Date

Project ATLAS values traceability over undocumented assumptions. Architecture and design decisions are stored under `01_Architecture`.

---

## 12. AI Coding Agent Rules

Derived from MC-004 (AI Coding Governance) and BP-000 (AI Development Rules):

- AI assistants are engineering tools.
- AI must never invent business requirements.
- AI may propose improvements, but implementation requires repository approval.
- No AI may silently change architecture; all architectural changes require versioned documentation.
- All AI-generated code must satisfy the same engineering standards as manually written code.

AI-generated output must:

- Follow repository standards
- Follow architecture
- Follow naming conventions
- Include documentation
- Pass testing
- Pass code review

AI must never become an exception to engineering discipline.

---

## 13. Engineering Workflow

Derived from BP-000 (Coding Rules) and MC-004 (Architecture Governance):

1. Documentation is authored and approved first (Master Context → Architecture → Domains → Engineering Standards → Build Packs → Implementation Packs).
2. Implementation begins only after the required Build Packs are complete.
3. No production code without approved engineering documentation.
4. No undocumented feature may enter production.
5. Testing, security review, and deployment follow implementation per the Definition of Done.

Every major deliverable undergoes structured review (MC-004, Review Governance):

```
Level 1: Author Review
Level 2: Peer Review
Level 3: Architecture Review
Level 4: Product Approval
Level 5: Repository Freeze
```

---

## 14. Branch Strategy

A formal branch strategy has not yet been defined in the approved repository documents. Until an approved Engineering Standard defines branching:

- Work is performed on the main repository line.
- Git commits are made only when explicitly instructed (README, Documentation Workflow).
- Commits remain atomic, with each approved Build Pack committed separately (BP-000, Git Rules).

This section shall be updated when the corresponding Engineering Standard is approved.

---

## 15. Definition of Done

**Feature-level Definition of Done (MC-004):** a feature is complete only when all of the following are satisfied:

- Business: Approved
- Architecture: Approved
- Engineering: Completed
- Implementation: Completed
- Testing: Passed
- Security Review: Completed
- Documentation: Updated
- Repository: Committed
- Deployment: Successful
- Monitoring: Enabled

Anything less is considered incomplete.

**Build Pack Definition of Done (BP-000):** a Build Pack is complete only when:

- Documentation approved
- Repository updated
- Git committed
- Dependencies verified
- No unresolved engineering conflicts remain

---

## 16. Repository Governance

Approval authority is distributed as follows (MC-004, Approval Authority):

| Authority | Role |
|-----------|------|
| Business Authority | Product Owner |
| Architecture Authority | Chief Architect / Architecture Board |
| Engineering Authority | Engineering Lead |
| Repository Authority | Repository Maintainer |
| Production Authority | Release Manager |

Governance pillars (MC-004): Enterprise First, AI Native, Human Governed, Security by Design, Documentation First, Continuous Evolution.

The Repository Manager maintains repository documentation exactly as approved and does not redesign product, architecture, business model, repository structure, or engineering standards.

---

## 17. Change Management

All changes follow controlled governance (MC-004, Change Management):

- Editorial changes → patch version increment.
- Functional improvements → minor version increment.
- Breaking strategic changes → major version increment, requiring architecture review and formal approval.

Any strategic change requires (MC-001, Governance):

1. Product Review
2. Architecture Review
3. Repository Update
4. Version Increment
5. Formal Approval

Breaking changes additionally require product approval, architecture approval, version increment, and migration documentation (MC-004, Backward Compatibility Principles).

---

## 18. Contribution Guidelines

All contributors — human or AI — must:

1. Read this manifest and the Master Context documents (MC-001 to MC-005) before working on the repository.
2. Follow the documentation hierarchy; never allow a lower-level artifact to redefine a higher-level artifact.
3. Preserve original wording and formatting of approved documents.
4. Follow the established naming convention and folder structure.
5. Maintain internal links across documents.
6. Record version changes in `CHANGELOG.md` and `VERSION.md`.
7. Pass all applicable Quality Gates before a document is approved.
8. Commit to Git only when explicitly instructed.
9. Never modify approved documents outside the formal change management process.

---

## 19. Repository Freeze Policy

Derived from MC-001 and MC-004 (Architecture Freeze Declarations and Document Lifecycle):

- Every document follows the lifecycle: Draft → Internal Review → Architecture Review → Approved → Architecture Freeze → Amendment (if required) → Archived Version.
- Repository Freeze is the final review level (Level 5) after Product Approval.
- Upon approval, the frozen elements of MC-001 (Product Vision, Mission, Philosophy, Positioning, Principles, Boundaries, Strategic Objectives, Success Metrics, Governance Rules) and MC-004 (Product Principles, Engineering Principles, AI Governance, Security Principles, Privacy Principles, Repository Governance, Documentation Governance, Architecture Governance, Definition of Done, Change Management, Review Process) are immutable unless amended through formal repository governance.
- Frozen content may be changed only through a formally versioned amendment with architecture review and formal approval.

---

## 20. Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-07-07 | Initial release of PROJECT_MANIFEST.md — repository constitution summarizing approved governance from the MC Series, README, and BP-000. |

---

# End of Document
