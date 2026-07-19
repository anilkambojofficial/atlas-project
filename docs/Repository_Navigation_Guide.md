# Project ATLAS — Repository Navigation Guide

| Field | Value |
|---|---|
| Document ID | NAV-001 |
| Title | Repository Navigation Guide |
| Role | **Unique role:** where each role *starts* and in what order they read — for humans primarily (AI logistics: AIL-001; metadata: MAN-001; relationships: KG-001) |
| Date | 2026-07-19 |

## Starting points by role

| Role | Start here | Then | First hands-on step |
|---|---|---|---|
| **New developer** | `docs/AI_Continuation_Pack.md` (CTX-002 — 10-minute state) | `docs/Repository_Constitution.md` (full, once; §17 memorized) → `docs/AI_Future_Context_Pack.md` §§2–5, 13, 19 → your task's IP sections | `scripts/dev-up.sh infra` → `cd backend && uv run pytest` → read `core/application.py` + `core/container.py` top to bottom (~400 lines: the whole runtime) |
| **AI model / agent** | CTX-002 → CON-001 §12 + §17 | Per its loading profile in AIL-001 | Verify preconditions in CTX-002 §8 before implementing anything |
| **Architect** | CON-001 → AUD-002 (findings *and* strengths) | CTX-001 → KG-001 → `07_ADRs/` → MAT-001/HD-001 | Walk one decision end-to-end through REG-001 → ADR → code to internalize the decision flow |
| **Reviewer** | CON-001 §9–§11 + §17 | CTX-001 §17 (review checklist) + §18 (verification checklist) → the stage's plan + verification report | Review the diff *against the checklist*, and each verification claim against its executed command |
| **Implementation (starting a stage)** | Current sprint log → the stage's approved plan | The stage's IP §§ per CTX-001 §13 mapping → the nearest analogous existing module | Confirm Definition of Ready (CON-001 §13) is met before writing code |
| **Product Owner (returning)** | CTX-002 §5 (risks) + REG-001 Standing Obligations | RMB-001 (roadmap state) → HD-001 (traffic lights) → anything Proposed awaiting ratification | The pending-decisions list at the top of REG-001's obligations table |

## Mandatory vs optional

| Tier | Documents | Who |
|---|---|---|
| **Mandatory for everyone** | CON-001 · CTX-002 | All roles, all sessions |
| **Mandatory before writing code** | CTX-001 (esp. §3 invariants, §13 mapping, §19 mistakes) · current sprint log · the task's IP/BP sections | Developers, AI agents |
| **Mandatory for decision-makers** | REG-001 · relevant ADRs · AUD-002 · POL-001 | Architects, reviewers, PO |
| **Optional (depth/background)** | Full MC/ARCH/DOMAIN texts (consult by section) · RA full texts · AUD-001 (superseded analysis — read AUD-002 instead) · MAT-001 detail · CERT-001 · KG-001 · historical sprint logs | As needed |

## Reading order by role (condensed)

- **Developer:** CTX-002 → CON-001 → CTX-001 (§§2–5,13,19) → sprint log → task IP → analogous code. (~half day to productive.)
- **Architect:** CON-001 → AUD-002 → CTX-001 → ADRs → KG-001 → MAT-001. (~1 day.)
- **Reviewer:** CON-001 §9–11,17 → CTX-001 §17–18 → stage plan/report → diff. (~2 hours per review.)
- **AI:** per AIL-001 tiers T0→T1→T2; T3 on demand.

## Common navigation mistakes

1. **Starting with the 68-document chain instead of the context layer.** The chain is the law library, not the orientation; CTX-002 → CTX-001 first, then the chain *by section, on demand*.
2. **Trusting raw BP/IP cross-references for module routing.** The off-by-one defects are real and documented; the corrected mapping is CTX-001 §13 — always route through it.
3. **Reading AUD-001 as current.** AUD-002 re-validated, corrected, and reclassified it; AUD-001 is the frozen adversarial record, AUD-002 is the operative truth.
4. **Treating a Proposed ADR as Accepted.** Check the status header and `07_ADRs/README.md`; ratification state gates what you may build (CTX-002 §4).
5. **Looking for "where are we" in doctrine documents.** State lives in the sprint log + CTX-002 + git; doctrine documents are timeless by design.
6. **Assuming empty folders are abandoned.** `08–14, 99_Reference, agents/, infrastructure/` are reserved by the plan (MAN-001 stats cover what's real today).
7. **Searching for business code.** There is none yet — `apps/` is intentionally empty until Sprint-002; the platform foundation is the entire codebase.
8. **Fixing documentation defects encountered while navigating.** They are registered tripwires (CTX-001 §15.4); fixing them is a governed editorial batch, not a drive-by edit (POL-001 §5).
