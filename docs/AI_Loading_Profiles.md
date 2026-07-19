# Project ATLAS — AI Loading Profiles

| Field | Value |
|---|---|
| Document ID | AIL-001 |
| Title | Context-loading profiles per AI system and human role |
| Role | **Unique role:** *how much* of the corpus to load, per agent/role and task type. What to read is NAV-001/CTX-002; this document optimizes token budgets and workflow |
| Date | 2026-07-19 |

## 0. Universal rules (all profiles)

- **Tier definitions** — T0 law: CON-001 (§12+§17 minimum) + CTX-002. T1 depth: CTX-001 + REG-001 + current sprint log. T2 task chain: the IP/BP/DOMAIN/ES/RA sections for the task per CTX-001 §13. T3 background: audits, maturity, roadmap, MC/ARCH full texts.
- Never skip T0. Never load T3 before T2 — background displaces task context in small windows.
- Code context beats document context for implementation detail: `core/container.py` + the nearest analogous module answer "how do we do X here" faster than any prose.
- Documents are loaded by *section* where cited (e.g., "IP-001 §10"), not whole-file, when budget is tight.
- All AI profiles inherit the operating contract (CTX-002 §10): stage gates, stop-on-conflict, no invention, executed verification.

## 1. AI system profiles

| Profile | Required (load order) | Optional | Context size | Workflow & prompt strategy |
|---|---|---|---|---|
| **Claude Code** (agentic CLI/IDE; tools available) | T0 → T1 → T2 for the assigned stage. CLAUDE.md auto-loads; memory dir persists checkpoints | T3 on demand via file reads; audits when touching flagged areas | Large (≥200k): load T0–T2 fully | Work the stage-gate loop; verify by *executing* (run tests, curl endpoints, grep imports); update living docs at gates; recommend commits, never auto-commit. Prompts: one stage, explicit exclusions, "verify then report" |
| **Claude Sonnet** (chat, limited/no tools) | T0 + CTX-002 §8 + the *specific sections* under discussion | CTX-001 relevant §§, pasted code excerpts | Medium: rely on section-loading | Best for review/design discussion, not implementation. Prompts should paste evidence (file excerpts) rather than ask the model to assume; ask for output as unified diffs or full files for human application |
| **GPT (chat)** | Same as Claude Sonnet; additionally paste CON-001 §17 verbatim (non-negotiables travel poorly by reference) | MEM-001 as a one-shot primer | Medium | Same as Sonnet. Anchor every request with "authority: <doc §>"; require the model to cite which rule permits each choice — this repo's conventions differ from ecosystem defaults (e.g., envelopes, UUID v7, tenancy mixins) |
| **Codex / autonomous code agents** | T0 (§17 verbatim) + CTX-001 §3 invariants + §19 mistakes + the exact task chain + the target module's existing code | CTX-001 §13 recipe | Medium–large | Highest drift risk: constrain hard. One file-set per task; require imports of `shared/*` builders (never re-implement envelopes/errors/events/ids); CI/tests are the arbiter; human reviews against the Review Checklist (CTX-001 §17) |
| **Gemini** | As GPT profile | KG-001 for orientation (handles long single-doc context well — MEM-001 + CTX-001 in one load is viable) | Large | As GPT. If the full CTX-001 fits, prefer loading it whole over sectioning |
| **Cursor** | Index the repo; pin T0 docs + CTX-001 to the context; per-task, open the IP §§ + target module | `.cursorrules`-equivalent: distill CON-001 §12/§17 + CTX-001 §3 into the rules file (a follow-up task, not yet created) | IDE-managed | Keep chats task-scoped; re-pin T0 after context resets; never accept multi-file "fix-everything" applies without the checklist pass |
| **Windsurf** | As Cursor | Same rules-file distillation | IDE-managed | As Cursor; verify agentic multi-file edits stage-by-stage against the gate protocol |
| **VS Code agent (Copilot agent mode)** | As Cursor; `copilot-instructions.md`-equivalent from the same distillation | — | IDE-managed | Use for scoped edits and test authoring; route architectural choices to a full T0–T2 session (this class of agent sees the least context — give it the least discretion) |

## 2. Human role profiles

| Profile | Required | Optional | Time to productive | Workflow |
|---|---|---|---|---|
| **Human Architect** | CON-001 → AUD-002 (incl. strengths) → CTX-001 → KG-001 → ADRs → MAT-001/CERT-001 | Full chain browse via MC-000 + BP-ROADMAP; code tour from `core/container.py` | ~1 day | Owns ADR drafting, gate verification, chain-conflict rulings prep for PO; refreshes HD-001/MAT editions at audits |
| **Human Reviewer** | CON-001 §9–§11 + §17 → CTX-001 §17–§18 checklists → the stage's plan + verification report → the diff | REG-001 for decision context; AUD-002 for known-debt areas (don't re-flag registered debt) | ~2 hours | Review = checklist + evidence check: does every verification claim map to an executed command? Are frozen contracts untouched (BAS-001 §Immutability 3)? |
| **Human Developer** | CTX-002 → CON-001 (full once, §17 memorized) → CTX-001 §§2–5, 13, 19 → their task's IP §§ → the analogous existing module | Sprint log history; audits | ~half day | Build per the module recipe; run `scripts/dev-up.sh`; `uv run pytest` locally; follow the stage-gate loop; ask on any documentation conflict — the repo rewards asking |

## 3. Anti-patterns in context loading

Loading all 89 documents indiscriminately (T3 crowds out T2); trusting pre-2026-07-19 cross-references over CTX-001 §13; loading CTX-001 but skipping the *current* sprint log (state beats doctrine for "what do I do now"); treating this file's profiles as authority on rules (they are logistics — the rules live in CON-001).
