============================================================
PROJECT ATLAS
DOMAIN
============================================================

Document ID      : DOMAIN-004
Document Title   : Meeting Domain
Version          : 1.0.0
Status           : Draft (Architecture Review)
Document Owner   : Chief Domain Architecture Office
Product Owner    : Anil Kumar
Repository Path  : 02_Domains/DOMAIN-004_Meeting_Domain.md

============================================================
DOCUMENT PURPOSE
============================================================

This document defines the Meeting Domain of Project ATLAS.

The Meeting Domain is the primary operational intelligence source of the platform.

Unlike traditional meeting applications that simply record conversations, Project ATLAS transforms meetings into structured organizational knowledge by extracting transcripts, decisions, action items, SOP candidates, risks, insights, and AI-generated summaries.

Meetings become permanent organizational memory.

============================================================
DOCUMENT SCOPE
============================================================

This document defines:

• Meeting Aggregate

• Meeting Lifecycle

• Meeting Participants

• Meeting Recording

• Meeting Transcription

• AI Meeting Analysis

• Decisions

• Actions

• SOP Extraction

• Meeting Intelligence

• Business Rules

============================================================
AUDIENCE
============================================================

Applicable to

• Product Architects

• AI Engineers

• Backend Engineers

• Database Engineers

• Security Engineers

• DevOps Engineers

• Future AI Coding Agents

============================================================
DOCUMENT DEPENDENCIES
============================================================

Depends On

• MC-001
• MC-002
• MC-003
• MC-004
• MC-005

• ARCH-001
• ARCH-002
• ARCH-003
• ARCH-004
• ARCH-005

• DOMAIN-001 Organization

• DOMAIN-002 Identity & User

• DOMAIN-003 Project

Referenced By

• DOMAIN-005 Knowledge

• DOMAIN-006 Decision

• DOMAIN-007 SOP

• DOMAIN-008 Action

• DOMAIN-010 AI

• Meeting APIs

• AI Processing

============================================================
1. EXECUTIVE SUMMARY
============================================================

A Meeting represents a structured business collaboration event occurring within a Project.

Every Meeting is treated as an enterprise knowledge generation event.

Meetings are transformed into structured business intelligence through AI processing.

Generated outputs include

• Transcript

• AI Summary

• Decisions

• Actions

• SOP Candidates

• Knowledge Articles

• Risks

• Questions

• Follow-up Recommendations

============================================================
2. DOMAIN PURPOSE
============================================================

The Meeting Domain exists to

• Capture enterprise conversations

• Generate organizational knowledge

• Extract business decisions

• Identify action items

• Generate SOP candidates

• Build organizational memory

• Improve enterprise intelligence

Meetings are the primary source of organizational learning within Project ATLAS.

============================================================
3. MEETING AGGREGATE
============================================================

Aggregate Root

Meeting

Child Entities

• Recording

• Transcript

• AI Summary

• Participant

• Agenda

• Notes

Referenced Entities

• Organization

• Project

• User

Future Related Entities

• Knowledge

• Decision

• SOP

• Action

• AI Analysis

The Meeting aggregate owns every artifact produced during a meeting.

============================================================
4. MEETING ENTITY
============================================================

Core Attributes

• Meeting ID

• Organization ID

• Project ID

• Title

• Description

• Meeting Type

• Status

• Host

• Start Time

• End Time

• Duration

• Recording Enabled

• AI Processing Status

• Created Date

Business Rules

• Every Meeting belongs to exactly one Project.

• Every Meeting belongs to one Organization.

• Every Meeting has one Host.

• AI processing begins only after meeting completion unless Live AI Mode is enabled.

============================================================
5. MEETING LIFECYCLE
============================================================

Draft

↓

Scheduled

↓

Live

↓

Completed

↓

AI Processing

↓

Knowledge Extraction

↓

Archived

↓

Retention

↓

Deletion

Business Rules

• Only Completed meetings may enter AI Processing.

• Archived meetings become read-only.

• Deletion follows Organization retention policies.

============================================================
END OF PART 1
============================================================
============================================================
6. MEETING PARTICIPANTS
============================================================

Every Meeting consists of one or more Participants.

Participant Types

• Host
• Co-Host
• Presenter
• Internal Participant
• External Guest
• AI Assistant (Future)

Participant Attributes

• Participant ID
• Meeting ID
• User ID (Optional)
• Display Name
• Email Address
• Organization
• Participant Type
• Join Time
• Leave Time
• Attendance Duration
• Speaking Duration
• Attendance Status

Attendance Status

• Invited
• Joined
• Left
• Absent

Business Rules

• Every Meeting must have one Host.
• External Guests shall have limited permissions.
• AI Assistants shall not be treated as human participants.

============================================================
7. MEETING RECORDING
============================================================

Meeting recording captures the raw meeting evidence.

Recording Attributes

• Recording ID
• Meeting ID
• Recording Status
• Recording Provider
• Recording Duration
• Recording Size
• Storage Location
• Recording Quality

Recording Status

• Scheduled
• Recording
• Completed
• Failed
• Archived

Recording Sources

• Zoom
• Microsoft Teams
• Google Meet
• Native Recording (Future)

Business Rules

• Recording requires Organization policy approval.
• Recording metadata shall remain immutable.
• Recording files follow Data Architecture retention policies.

============================================================
8. MEETING TRANSCRIPTION
============================================================

Every recorded Meeting may generate one or more transcripts.

Transcript Components

• Transcript ID
• Meeting ID
• Language
• Speaker Segments
• Timestamped Dialogue
• Confidence Score
• Processing Status

Transcript Processing

Recording

↓

Speech Recognition

↓

Speaker Identification

↓

Timestamp Alignment

↓

Transcript Validation

↓

Transcript Storage

↓

AI Processing

Business Rules

• Original transcripts shall remain immutable.
• Corrections shall be version-controlled.
• Multiple languages may be supported.

============================================================
9. AI MEETING PROCESSING
============================================================

After meeting completion, AI processing converts unstructured conversations into structured intelligence.

AI Processing Pipeline

Transcript

↓

Cleaning

↓

Segmentation

↓

Context Building

↓

Entity Extraction

↓

Decision Extraction

↓

Action Extraction

↓

Risk Detection

↓

Knowledge Extraction

↓

Summary Generation

↓

Embedding Generation

↓

Knowledge Graph Update

AI Processing Outputs

• Executive Summary
• Detailed Summary
• Decisions
• Action Items
• SOP Candidates
• Knowledge Objects
• Risks
• Questions
• AI Recommendations

============================================================
10. MEETING SUMMARY
============================================================

Project ATLAS shall generate structured summaries.

Summary Types

Executive Summary

• High-level overview

Operational Summary

• Detailed meeting outcomes

Technical Summary

• Technical discussions

Management Summary

• Strategic decisions

Custom Summary

• Organization-defined templates

Summaries shall reference supporting transcript evidence.

============================================================
11. MEETING ARTIFACTS
============================================================

Every Meeting generates one or more business artifacts.

Artifact Types

• Recording
• Transcript
• AI Summary
• Decisions
• Actions
• SOP Candidates
• Knowledge Articles
• Attachments
• Chat Messages
• Whiteboard Content (Future)

Artifacts remain linked to the originating Meeting.

============================================================
12. MEETING SEARCH
============================================================

Meetings shall be fully searchable.

Search Sources

• Title
• Participants
• Transcript
• Summary
• Decisions
• Actions
• Knowledge
• Attachments

Supported Search

• Keyword Search
• Semantic Search
• AI Search
• Speaker Search
• Timeline Search

Search shall respect Organization and Project permissions.

============================================================
13. MEETING GOVERNANCE
============================================================

Meeting governance ensures secure and compliant collaboration.

Governance Areas

• Recording Policies
• AI Processing Policies
• Participant Permissions
• Data Retention
• Transcript Retention
• Export Policies
• Compliance Monitoring
• Audit Logging

Meeting governance inherits Organization and Project policies.

============================================================
END OF PART 2
============================================================
============================================================
14. DECISION EXTRACTION
============================================================

Project ATLAS shall automatically identify business decisions discussed during meetings.

Decision Sources

• Explicit Decisions
• Approved Proposals
• Consensus Outcomes
• Management Directives
• Strategic Decisions
• Technical Decisions

Decision Attributes

• Decision ID
• Meeting ID
• Project ID
• Organization ID
• Decision Title
• Decision Description
• Decision Category
• Decision Maker(s)
• Decision Timestamp
• Confidence Score
• Approval Status
• Linked Transcript References

Business Rules

• Every extracted decision shall reference transcript evidence.

• AI-generated decisions require user review before publication unless Organization policy allows automatic approval.

============================================================
15. ACTION EXTRACTION
============================================================

Project ATLAS shall identify actionable commitments from meeting discussions.

Action Sources

• Assigned Tasks
• Commitments
• Follow-up Activities
• Customer Requests
• Risk Mitigation Tasks
• Escalations

Action Attributes

• Action ID
• Meeting ID
• Assigned User
• Due Date
• Priority
• Status
• Confidence Score
• Supporting Transcript

Action Lifecycle

Detected

↓

Validated

↓

Assigned

↓

In Progress

↓

Completed

↓

Archived

Business Rules

• Actions may be reassigned.

• Every Action shall reference its originating Meeting.

============================================================
16. SOP EXTRACTION
============================================================

Meetings frequently contain repeatable operational procedures.

Project ATLAS shall identify potential SOP candidates.

Extraction Sources

• Repeated Procedures
• Standard Instructions
• Operational Workflows
• Customer Processes
• Compliance Activities

Generated SOP Candidate

↓

AI Review

↓

Human Review

↓

Approval

↓

Published SOP

↓

Knowledge Repository

SOP candidates shall remain linked to their originating Meetings.

============================================================
17. KNOWLEDGE EXTRACTION
============================================================

Knowledge extraction converts conversations into reusable enterprise knowledge.

Knowledge Categories

• Business Knowledge
• Technical Knowledge
• Customer Knowledge
• Product Knowledge
• Process Knowledge
• Operational Knowledge
• Lessons Learned
• Best Practices

Knowledge Processing

Transcript

↓

Topic Detection

↓

Concept Extraction

↓

Relationship Discovery

↓

Knowledge Object Creation

↓

Embedding Generation

↓

Knowledge Graph Update

Knowledge shall remain searchable across the Organization according to access permissions.

============================================================
18. MEETING INTELLIGENCE GRAPH
============================================================

Every Meeting contributes to the Enterprise Intelligence Graph.

Meeting

↓

Participants

↓

Topics

↓

Knowledge

↓

Decisions

↓

Actions

↓

SOPs

↓

Projects

↓

AI Memory

The graph continuously expands as new meetings are processed.

The Intelligence Graph enables semantic search, relationship discovery, contextual AI assistance, and organizational memory.

============================================================
19. AI CONFIDENCE & HUMAN REVIEW
============================================================

Every AI-generated artifact shall include confidence metadata.

Confidence Levels

High

• Automatic publication permitted if Organization policy allows.

Medium

• Human review recommended.

Low

• Human approval required before publication.

AI-generated outputs shall always preserve links to supporting evidence.

============================================================
20. DOMAIN EVENTS
============================================================

The Meeting Domain publishes the following events.

Meeting Events

• Meeting Scheduled
• Meeting Started
• Meeting Ended
• Meeting Archived

Recording Events

• Recording Started
• Recording Completed
• Recording Failed

AI Events

• Transcript Generated
• Summary Generated
• Decision Extracted
• Action Extracted
• SOP Candidate Generated
• Knowledge Generated
• Embeddings Created

Consumer Domains

• Knowledge Domain
• Decision Domain
• SOP Domain
• Action Domain
• AI Domain
• Analytics Domain

Domain events shall be immutable and fully auditable.

============================================================
END OF PART 3
============================================================
============================================================
21. DOMAIN CONSTRAINTS
============================================================

The Meeting Domain enforces the following constraints.

Organization

• Every Meeting belongs to exactly one Organization.

• Cross-Organization Meetings are prohibited unless explicitly supported by future federation capabilities.

Project

• Every Meeting belongs to exactly one Project.

• Meetings cannot be transferred between Projects after AI processing has begun.

Participants

• Every internal Participant must belong to the Meeting Organization.

• External Guests shall have restricted permissions.

Recording

• Recording follows Organization policy.

• Recording may be disabled for confidential meetings.

AI Processing

• AI processing shall preserve the original transcript.

• AI-generated artifacts shall never modify the source transcript.

Knowledge

• Every extracted artifact maintains a permanent reference to its originating Meeting.

Compliance

• Meeting retention follows Organization policy.

• Audit history cannot be deleted outside approved retention procedures.

============================================================
22. BUSINESS RULES
============================================================

The Meeting Domain enforces the following business rules.

• Every Meeting has exactly one Host.

• Meetings belong to one Organization.

• Meetings belong to one Project.

• AI processing starts only after meeting completion unless Live AI Mode is enabled.

• AI-generated artifacts remain linked to the Meeting.

• Meeting artifacts inherit Project permissions.

• Meeting artifacts inherit Organization governance.

• Search results respect Organization, Project, and User permissions.

• Deleted Meetings follow enterprise retention policies.

============================================================
23. DOMAIN SUCCESS CRITERIA
============================================================

The Meeting Domain is considered complete when:

✓ Meeting Aggregate is defined.

✓ Meeting lifecycle is documented.

✓ Participant model is established.

✓ Recording model is defined.

✓ Transcript model is documented.

✓ AI processing pipeline is defined.

✓ Decision extraction is documented.

✓ Action extraction is documented.

✓ SOP extraction is documented.

✓ Knowledge extraction is documented.

✓ Intelligence Graph integration is defined.

✓ Domain events are documented.

✓ Business rules are complete.

============================================================
24. DOMAIN DECISIONS
============================================================

| Decision | Status | Rationale |
|----------|--------|-----------|
| Meeting as Intelligence Source | Accepted | Meetings become enterprise knowledge assets |
| AI-First Meeting Processing | Accepted | Structured intelligence from conversations |
| Immutable Transcript Preservation | Accepted | Auditability and evidence integrity |
| Human Review for AI Artifacts | Accepted | Enterprise governance and quality control |
| Intelligence Graph Integration | Accepted | Organization-wide knowledge discovery |
| Event-Driven Processing Pipeline | Accepted | Loose coupling and scalability |

Future changes require an approved Architecture Decision Record (ADR).

============================================================
25. VERSION HISTORY
============================================================

Version 1.0.0

Initial Meeting Domain

Major Deliverables

• Meeting Aggregate
• Meeting Lifecycle
• Participant Model
• Recording Architecture
• Transcript Processing
• AI Processing Pipeline
• Decision Extraction
• Action Extraction
• SOP Extraction
• Knowledge Extraction
• Meeting Intelligence Graph
• Domain Events
• Business Rules

============================================================
26. CROSS REFERENCES
============================================================

Related Documents

• DOMAIN-001 Organization Domain
• DOMAIN-002 Identity & User Domain
• DOMAIN-003 Project Domain

• ARCH-002 Multi-Tenant Architecture
• ARCH-003 AI Architecture
• ARCH-004 Data Architecture
• ARCH-005 Security Architecture

Future Related Documents

• DOMAIN-005 Knowledge Domain
• DOMAIN-006 Decision Domain
• DOMAIN-007 SOP Domain
• DOMAIN-008 Action Domain
• DOMAIN-010 AI Domain

• BP-004 Meeting

• ES-005 AI Engineering Standards

============================================================
27. DOMAIN FREEZE DECLARATION
============================================================

Upon approval, this document becomes the authoritative Meeting Domain for Project ATLAS.

The following domain elements are considered frozen until amended through formal repository governance:

• Meeting Aggregate

• Meeting Lifecycle

• Participant Model

• Recording Model

• Transcript Model

• AI Processing Pipeline

• Decision Extraction

• Action Extraction

• SOP Extraction

• Knowledge Extraction

• Meeting Intelligence Graph

• Domain Relationships

• Domain Events

• Business Rules

All future APIs, database schemas, Engineering Standards, Build Packs, Implementation Packs, AI workflows, and production code shall conform to this domain model.

Changes affecting meeting intelligence, AI processing, or extracted business artifacts require formal architectural approval and an Architecture Decision Record (ADR).

============================================================
END OF DOCUMENT
============================================================
