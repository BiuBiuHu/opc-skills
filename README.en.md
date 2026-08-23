# OPC Skills

[中文说明](README.zh-CN.md)

Current version: `v0.4.0`

`opc-skills` is a Codex Skill for delivering consumer-facing apps, Web apps, mini programs, and their supporting operator consoles. It is designed for full delivery loops: clarify the user goal, define the core journey, design the user experience and service contracts, implement in controlled steps, verify with real pages and real clients, and release only after staging evidence, review, and production regression.

## Recent Updates

- Aligned README with the main rules in `SKILL.md` and clarified when subagents are appropriate.
- Added `agents/`, `templates/subagent-task-brief-template.md`, `templates/subagent-result-template.md`, and `references/subagent-orchestration.md`.
- Clarified that a skill cannot call subagents directly; the main agent must use runtime tools when the user explicitly allows multi-agent work.
- Strengthened guidance for B-side pages, local mocks, Mermaid call graphs, staging gates, and production release gates.
- Added confirmation rules for expensive batch operations, including cost, cache, retry, and overwrite strategies.
- Added runtime entry inventory gates so project-specific domains, accounts, service aliases, deployment IDs, and callback URLs stay in project documentation instead of the generic skill.
- Added Release PR lifecycle guidance, production synthetic probes, deployment drift checks, and post-release default-branch reset gates.
- Added a Chinese-by-default PR rule for new Code PRs, Release PRs, documentation PRs, titles, bodies, and checklists.
- Refined testing scope rules: choose the smallest sufficient test set from changed files, call chains, shared contracts, and risk; full test runs are an explicit escalation, not the default.
- Added release-integrity gates for bidirectional impact closure, per-system release decisions, candidate freezing, and missed-system review.
- Production deployments must come from a remote default-branch merge commit, or from a traceable build artifact that maps back to source commit and build job.
- Added `references/release-integrity.md` and `scripts/check_release_integrity.sh` for candidate, deployment commit, and worktree reconciliation checks.

## When To Use It

- Consumer apps: mobile apps, Web apps, mini programs, desktop apps, sign-in, browsing, creation, payments, sharing, notifications, and offline flows.
- Consumer experience work: navigation, forms, dialogs, lists, media, gestures, animation, performance, empty/error/loading states, and real-device verification.
- B-side operator consoles: operations, review, content generation, configuration, customer-support debugging, release control, and data repair tools.
- Full-stack delivery: client, primary API/BFF, authentication, AI/worker services, database, object storage, third-party services, staging, production, and rollback.

## Core Capabilities

- Consumer journey first: start from users, scenarios, entry points, core paths, and success criteria.
- Operator console support: design configuration, review, generation, troubleshooting, rework, and release workflows without turning the UI into a database viewer.
- Full-stack contracts: clients call only the primary API or API server; internal services are orchestrated behind that boundary.
- Cost protection: preview and review AI/generative work before expensive batch generation; reuse cache and object storage.
- Evidence loop: real pages, real clients, staging validation, test reports, code review, production regression, and observation windows.
- Documentation persistence: product, UI, architecture, engineering, testing, integration, and operations decisions are written to `docs/<FEATURE_NAME>/`.
- Subagent orchestration: split work only when the user explicitly allows it and the task boundaries are clear enough to improve speed or review quality.

## Installation

Clone this repository into a Codex-discoverable skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

Or clone it elsewhere and symlink it into `~/.codex/skills/opc-skills`.

## Usage

Use one of these intents in Codex:

```text
启动 OPC Skills
启动 C 端业务应用研发流程
跑一遍 C 端应用和配套 B 端工作台全流程
用 opc-skills 分析这个移动端需求
用 opc-skills 设计这个 C 端功能
用 opc-skills 设计配套运营工作台
```

After activation, the main agent reads `SKILL.md` and enters the relevant mode: requirement validation, UI, architecture, implementation, testing, integration, or release.

## Workflow

```text
Goal clarification
-> Requirement validation
-> Product PRD
-> Consumer experience design / B-side console prototype
-> Architecture diagram and call graph
-> Change impact analysis
-> Implementation plan
-> Local mock / client automation verification
-> Staging integration and real API verification
-> Test report and code review
-> Release plan review and related-system sign-off
-> Default-branch merge commit freeze
-> Production release and smoke test
-> Production-domain regression
-> Worktree reconciliation and release-integrity closeout
-> Observation window and release closeout
```

The default mode is `manual-gated`: the agent writes documents and plans first, then waits in `awaiting-user-review` before implementation, migration, or deployment.

## Repository Structure

```text
opc-skills/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── VERSION
├── CHANGELOG.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── agents/
├── docs/
├── references/
├── scripts/
│   ├── check_release_integrity.sh
│   ├── check_project_coupling.sh
│   └── start_rnd.sh
└── templates/
```

## Key Principles

- Save the current code state before editing.
- Generic skill files must not store project-specific accounts, domains, service names, deployment IDs, or one-off business rules.
- Goal clarification is mandatory.
- Consumer-facing work follows the core user journey, not a field list.
- B-side operator pages optimize decision speed and operational flow.
- Long lists need pagination, total counts, filters, loading states, empty states, and error states.
- ASCII sketches must stay close to the interaction flow they describe.
- AI/generative features must preview cheaply before expensive generation.
- Clients must not call internal services directly.
- Production release requires staging, a test report, code review, release plan review, production smoke, production regression, and an observation window.
- Release integrity and default-branch reconciliation are one hard gate: production candidates must be merged into the remote default branch and mapped to the actual deployment or artifact commit.
- After production closeout, affected repositories must record default branch, merge commit, deployment commit, local/remote HEAD, and worktree state.
- New PRs default to Chinese unless repository policy or the user explicitly requires another language.
- Test scope must be selected from impact and risk; full test suites are used only when the escalation criteria are met.
- Subagents are used only when explicitly allowed by the user and when ownership boundaries are clear.

## Useful Commands

Initialize feature documents from templates:

```bash
./scripts/start_rnd.sh /path/to/project account-linking
```

Check for project-specific coupling before publishing generic skill changes:

```bash
./scripts/check_project_coupling.sh
```

Check release candidate ancestry, deployment commit mapping, and worktree reconciliation:

```bash
./scripts/check_release_integrity.sh /path/to/repo <candidate-commit> [default-branch] [deployment-commit]
```

## Security

This repository intentionally avoids project-specific facts. Real project names, paths, accounts, domains, cloud projects, deployment IDs, database hosts, schema names, credential values, and business-specific state machines should live in the relevant project documentation, not in this generic skill.

See [SECURITY.md](SECURITY.md) for reporting and handling sensitive information.

## License

MIT
