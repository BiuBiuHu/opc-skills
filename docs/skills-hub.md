# Skills Hub and Codex `$skill-installer`

This is a follow-up checklist, not a claim that `opc-skills` is listed in any official catalog.

**Preferred install for this repo remains our own tools:**

```bash
npx opc-skills install
```

```bash
curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
```

Those paths clone or fast-forward a git checkout into `~/.codex/skills/opc-skills`. Use `npx opc-skills update` / `doctor` afterwards. Do not treat a Hub listing as a prerequisite.

`opc-skills` is **not** currently listed under [openai/skills](https://github.com/openai/skills) `skills/.curated`. `$skill-installer` can still install it from this GitHub repository.

## Official Codex path: `$skill-installer`

Codex ships a built-in system skill, `$skill-installer`. It installs into `$CODEX_HOME/skills` (normally `~/.codex/skills`) from:

1. the curated list at `openai/skills` → `skills/.curated` (name-only install)
2. any other GitHub repo / path, including a repo whose `SKILL.md` is at the root

`opc-skills` is case (2). The skill **is the repository root** (`SKILL.md` lives at `/`, not under `skills/<name>`).

The installer helper aborts if the destination directory already exists, and it **copies files** (zip download, git sparse-checkout fallback). That copy is **not** a git checkout, so `npx opc-skills doctor` will report it as broken until you replace it with our curl / npx installer. Prefer curl / npx when you want `update` to `git pull --ff-only`.

### Copy-paste prompt (English)

Paste this into Codex:

```text
$skill-installer install from github.com/BiuBiuHu/opc-skills

The skill is the repository root (SKILL.md is at the root, not in a subdirectory).
Install it as opc-skills into ~/.codex/skills/opc-skills.
Use the helper with --path . and --name opc-skills.
```

Shorter variant:

```text
Use $skill-installer to install github.com/BiuBiuHu/opc-skills (repo root is the skill; SKILL.md at root; dest name opc-skills).
```

### Copy-paste prompt (中文)

在 Codex 里粘贴：

```text
用 $skill-installer 从 github.com/BiuBiuHu/opc-skills 安装。
这个 skill 在仓库根目录（根上就是 SKILL.md，不是子目录）。
安装名为 opc-skills，目标路径 ~/.codex/skills/opc-skills。
helper 请使用 --path . --name opc-skills。
```

### Exact helper command

If Codex (or you) runs the bundled installer script directly:

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo BiuBiuHu/opc-skills \
  --path . \
  --name opc-skills
```

`$CODEX_HOME` defaults to `~/.codex` when unset. `--path .` is required because the skill is the repo root; `--name opc-skills` is required because the path basename of `.` is not a valid skill name. After install, restart Codex (or start a new turn) so it picks up the skill.

Do **not** use a curated name-only install such as `$skill-installer opc-skills` — that looks in `openai/skills` `skills/.curated`, where this repo is not listed.

## Curated listing checklist (do not auto-submit)

No official, automatable “submit this skill to the Hub” API was found. `$skill-installer` only **reads** the GitHub tree of `openai/skills` `skills/.curated` (and optionally `.experimental`). Listing still means a human PR (or a future Plugins flow), not a POST.

As of this writing, [openai/skills](https://github.com/openai/skills) marks itself deprecated in favor of the OpenAI Plugins / skill-only plugin guide. Confirm the current intake path before opening a PR.

If curated listing is still wanted later:

1. Confirm whether intake is still `openai/skills` or has moved to Plugins.
2. Do **not** claim `opc-skills` is curated until a listing actually lands.
3. Historical skills-repo path: start in `skills/.experimental/`, validate, then move to `skills/.curated/` after review.
4. `SKILL.md` frontmatter must keep `name` in hyphen-case (≤64 chars) and a `description` (≤256 chars if that validator is still in use).
5. Contributors typically need the OpenAI CLA.
6. A listing copy would be a **subset** of this repo, not a second source of truth. Keep GitHub `BiuBiuHu/opc-skills` canonical; do not fork install rules away from `scripts/install.sh`.
7. After any listing, keep README honest: “install from GitHub / npx / curl” first; “also available via `$skill-installer` by repo URL” second; “curated name-only” only once it is true.

Do not run third-party publish CLIs from CI or from this repo’s install path.

## Optional third-party registries

These are **optional** discovery surfaces. They are not required, not official Codex, and this repo is not listed there unless a later human publish says so.

| Surface | What it is | Why it is optional |
| --- | --- | --- |
| [skills-hub.ai](https://skills-hub.ai) / `@skills-hub-ai/cli` | Third-party catalog + `npx @skills-hub-ai/cli search\|install\|publish` | Publish needs a login. Do not auto-submit. |
| SkillHub (`@astron-team/skillhub`, iFlytek) | Self-hosted / enterprise registry | Team-private; not an official Codex listing. |
| `npx skills add owner/repo` / skills.sh | Community installer used by many skill packs | Different tool than `npx opc-skills`. |

Name collision: [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) is a **different** project (solopreneur marketing/research skills). Their one-liner is `npx skills add ReScienceLab/opc-skills`. Ours is `npx opc-skills install` (this package) or the curl script above.

## Follow-up

- Keep `scripts/install.sh` and `npx opc-skills` as the supported installers.
- Use `$skill-installer` + the copy-paste prompts when the user is already inside Codex and does not want curl/npx.
- Revisit curated / Plugins listing only after the intake path is confirmed. Do not auto-submit anywhere from this repository.
