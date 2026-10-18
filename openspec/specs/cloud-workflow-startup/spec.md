# Cloud workflow startup

## Purpose

Make reviewed development skills and project workflow readiness explicit at cloud
startup without mistaking installation for enforced agent behavior.

## Requirements

### Requirement: Complete reviewed skill installation
Setup SHALL install or verify the canonical development-team package and model
router including its Codex model profile and runtime references. It MUST refuse
conflicting installed content without overwriting user work.

#### Scenario: Fresh installation and repeat
- **WHEN** setup runs twice against empty then identical installation paths
- **THEN** both packages and router profile exist and the second run changes no content

#### Scenario: Existing modified installation
- **WHEN** an installation differs from the reviewed package
- **THEN** setup fails clearly and preserves the differing files

### Requirement: Workspace startup instructions
Setup SHALL add one managed section to the workspace AGENTS.md while preserving
unmanaged text. The section MUST require the router/profile before any delegation,
explicit supported model/effort choices with fresh context, and the development
team plus project-specific OpenSpec discovery before code changes.

#### Scenario: Existing instructions and repeated setup
- **WHEN** setup encounters unrelated instructions or its identical managed section
- **THEN** unrelated text remains byte-for-byte intact and managed instructions are not duplicated

#### Scenario: Edited or malformed managed instructions
- **WHEN** the managed section differs or its boundaries are malformed
- **THEN** setup refuses to replace it and preserves the existing document

#### Scenario: Read-only delegation
- **WHEN** work delegates read-only analysis without implementation
- **THEN** startup instructions require routing skill use without inventing an apply change

### Requirement: Read-only readiness verification
Verification SHALL check installed content, managed instructions and the expected
OpenSpec executable version without installing packages, changing projects or
contacting model APIs. Missing or incompatible prerequisites MUST fail clearly.

#### Scenario: Missing skill or executable
- **WHEN** a required skill, profile, instruction section or executable is absent
- **THEN** verification returns nonzero with the missing prerequisite identified

### Requirement: Project-specific OpenSpec preflight
Preflight SHALL use the selected executable in the actual project directory to
resolve OpenSpec context. Apply preflight MUST require a selected change and
inspect its status and apply instructions. Failed, malformed or missing context
MUST remain a failure; preflight MUST NOT initialize or migrate projects.

#### Scenario: Valid selected change
- **WHEN** the selected project command resolves a root and a change with ready apply instructions
- **THEN** preflight reports the actual context and selected change

#### Scenario: Separate project wrapper
- **WHEN** a project selects a different executable or version from the installed environment
- **THEN** preflight verifies the unchanged environment and runs the selected project command in that project

#### Scenario: Missing or blocked apply context
- **WHEN** no root or change resolves, or apply instructions report a blocked state
- **THEN** apply preflight fails without changing project files

### Requirement: Honest persistence and routing claims
Documentation SHALL distinguish installed files, startup instruction discovery,
accepted model override requests, actual execution identity and environment
publication. It MUST NOT claim that Markdown enforces tool calls or that local
installation publishes an environment.

#### Scenario: Hosted verification handoff
- **WHEN** setup is installed in a running workspace
- **THEN** delivery identifies fresh-session and environment-publication checks separately
