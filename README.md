# OPC Skills

**Language:** [中文说明](README.zh-CN.md) · [Full English docs](README.en.md)

Current version: `v0.6.1`

`opc-skills` is a Codex Skill for shipping consumer-facing apps together with their B-side operator consoles. This hub is the short map. Full detail lives in [README.en.md](README.en.md) and [README.zh-CN.md](README.zh-CN.md). Agent rules are defined in [SKILL.md](SKILL.md); do not treat this page as a substitute.

## Install

One-liner (creates `~/.codex/skills` if needed):

```bash
npx opc-skills install
```

```bash
curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
```

`npx opc-skills update` refreshes the checkout. `npx opc-skills doctor` prints install paths, `VERSION`, and symlink health. Both the CLI and the curl script share `scripts/install.sh`. The script clones or fast-forwards [this repository](https://github.com/BiuBiuHu/opc-skills) into `~/.codex/skills/opc-skills`. If `~/.cursor/skills` or `~/.claude/skills` already exists, it also points those paths at the same checkout. It does not create those extra parent directories, and it does not read editor config or secrets. `git` is required.

Optional Codex Agent Plugin install (`codex plugin marketplace add BiuBiuHu/opc-skills`, then `codex plugin add opc-skills@opc-skills`) is documented in [docs/skills-hub.md](docs/skills-hub.md), together with `$skill-installer` prompts. `openai/skills` curated listing is deprecated; this repo is not in the public Plugins Directory.

Manual clone:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

Or clone elsewhere and symlink into `~/.codex/skills/opc-skills`.

## Deployment platforms

Vercel and Cloudflare are supported. For Pages, Workers Static Assets, or a frontend-only migration that keeps the backend in place, see [Cloudflare deployment](references/cloudflare-deployment.md). Hosting choice follows the user and project configuration.

## Trigger phrases

In Codex, use one of these intents:

```text
Start OPC Skills
Start the consumer app delivery workflow
Run the full consumer app + operator console loop
Use opc-skills to analyze this mobile requirement
Use opc-skills to design this consumer feature
Use opc-skills to design the matching ops console
Generate Chinese and English tech article drafts from this release
```

Chinese trigger phrases are listed in [README.zh-CN.md](README.zh-CN.md).

The main agent then reads `SKILL.md` and enters requirement validation, UI, architecture, implementation, testing, integration, release, or `post-release-content`.

## What it is

A reusable Codex Skill that walks the main agent through a reviewable delivery loop:

**clarify → PRD → UI → architecture → implement → test → integrate → release → optional post-release content**

It covers user-side App / Web / mini-program / desktop work, the matching ops, review, config, and support consoles, and the primary API / auth / worker path behind them. The skill keeps reusable methods, gates, templates, and role placeholders. Project names, accounts, domains, service aliases, and deployments stay in the project's own fact sources.

Default mode is `manual-gated`: documents and plans go to `awaiting-user-review` before implementation, migration, or deploy.

## Who it's for

- Solo builders and one-person companies (OPC) who need a complete path from a pain point to a shippable release
- Small teams that ship a consumer product and the operator console that keeps it running
- Work that needs evidence, not only a green build: real pages, real clients, staging, test reports, and production regression

## What you get

- Evidence-gated workflow: real pages and clients, staging, test report, code review, release-plan sign-off, production smoke, production-domain regression, then an observation window
- Templates under `templates/` for requirement validation, PRD, UI prototype, architecture, change impact, implementation plan, test strategy, release plan, evidence manifest, ops runbook, and post-release content
- Role files under `agents/` (Explorer, Frontend, Backend, QA, Integration, DevOps, Content). The skill does not call subagents itself; the main agent uses runtime tools only when the user explicitly allows it
- Release-integrity reference and `scripts/check_release_integrity.sh` for candidate commit, deployment commit, default-branch merge, and worktree reconciliation
- Chinese-default PRs: new Code / Release / docs PR titles, bodies, and checklists default to Chinese unless repo policy or the user says otherwise
- Optional bilingual post-release articles via Content Agent (`suggest` / `draft` / `publish`). Page release is never blocked by article work, and articles are not published silently
- Feature docs written to `docs/<FEATURE_NAME>/`; helpers include `scripts/start_rnd.sh`, `scripts/check_project_coupling.sh`, and `scripts/prepare_post_release_content.sh`

## Workflow snapshot

```text
goal clarification
  -> requirement validation / PRD
  -> consumer UI + B-side console prototype
  -> architecture + call graph + change impact
  -> implementation plan
  -> local mock / client automation
  -> staging + real API
  -> test report + code review
  -> release-plan review + related-system sign-off
  -> default-branch merge freeze
  -> production + smoke + domain regression
  -> worktree / integrity closeout
  -> optional bilingual post-release content
```

This is the map only. The language pages and [SKILL.md](SKILL.md) own the gates.

## Further reading

Related notes from One PC:

- [One Person Can Ship a Product Too: My OPC Software Development Practice](https://www.peak-lake.com/en/blog/opc-software-practice/) ([中文](https://www.peak-lake.com/blog/opc-software-practice/)) — How a solo builder runs the product loop; this repo is that delivery flow.
- [Loop Engineering Has No Silver Bullet: Vertical Skills + spec/TDD](https://www.peak-lake.com/en/blog/mslj4f6g/) ([中文](https://www.peak-lake.com/blog/mslj4f6g/)) — Vertical Skills + spec/TDD; the post links here.

## Docs

- Chinese: [README.zh-CN.md](README.zh-CN.md)
- English: [README.en.md](README.en.md)
- Main skill rules: [SKILL.md](SKILL.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Release integrity: [references/release-integrity.md](references/release-integrity.md)
- One-click install: [scripts/install.sh](scripts/install.sh)
- npm CLI: `npx opc-skills` ([package.json](package.json))
- Codex `$skill-installer`, Agent Plugin marketplace, and Hub notes: [docs/skills-hub.md](docs/skills-hub.md)
- Agent Plugin package: [plugins/opc-skills/](plugins/opc-skills/)
- Release integrity check: [scripts/check_release_integrity.sh](scripts/check_release_integrity.sh)
- Post-release content: [references/post-release-content.md](references/post-release-content.md)

## License

MIT
