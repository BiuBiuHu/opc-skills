# Skills Hub, `$skill-installer`, and Agent Plugins

This is a distribution checklist, not a claim that `opc-skills` is listed in any official catalog or the public Plugins Directory.

Install order for this repo:

1. **Preferred:** `npx opc-skills` or `curl` (git checkout under `~/.codex/skills/opc-skills`)
2. **Inside Codex:** `$skill-installer` from this GitHub repository
3. **Agent Plugin:** add this repo as a marketplace, then install `opc-skills@opc-skills`
4. **Public Plugins Directory:** human + workspace portal submit later. Do not auto-submit.
5. **`openai/skills` curated:** deprecated. Do not open a PR into `skills/.curated`.

## 1. Preferred install: npx / curl

```bash
npx opc-skills install
```

```bash
curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
```

Those paths clone or fast-forward a git checkout into `~/.codex/skills/opc-skills`. Use `npx opc-skills update` / `doctor` afterwards. The skill **is the repository root** (`SKILL.md` at `/`). This is unchanged by the Agent Plugin packaging.

`npx opc-skills` on npm is currently `opc-skills@0.5.0`. The CLI only wraps `scripts/install.sh` and does not need a same-day publish for the plugin files in this repository. A later human publish can bump `package.json` to match `VERSION`.

## 2. Official Codex path: `$skill-installer` from GitHub

Codex ships a built-in system skill, `$skill-installer`. It installs into `$CODEX_HOME/skills` (normally `~/.codex/skills`) from a GitHub repo / path, including a repo whose `SKILL.md` is at the root.

`opc-skills` is that root-skill case. The installer helper aborts if the destination directory already exists, and it **copies files** (zip download, git sparse-checkout fallback). That copy is **not** a git checkout, so `npx opc-skills doctor` will report it as broken until you replace it with curl / npx. Prefer curl / npx when you want `update` to `git pull --ff-only`.

Do **not** use a curated name-only install such as `$skill-installer opc-skills`. That used to look in [openai/skills](https://github.com/openai/skills) `skills/.curated`, which is deprecated and does not list this repo.

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

## 3. Agent Plugins marketplace

Official distribution for reusable Codex / ChatGPT packages is now [OpenAI Agent Plugins](https://developers.openai.com/plugins/build/plugins) (skills-only plugin is enough). This repo ships a portable package at `plugins/opc-skills/` plus a repo marketplace at `.agents/plugins/marketplace.json`.

The plugin is **skills-only**: root `plugin.json` uses the [Agent Plugins 1.0.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), OpenAI presentation lives under `extensions.com.openai.interface`, and there is no bundled MCP server or `apps` mapping.

### How to try marketplace add

From a machine with Codex CLI (marketplace commands need a recent Codex that supports `codex plugin marketplace`):

```bash
codex plugin marketplace add BiuBiuHu/opc-skills
codex plugin marketplace list
codex plugin add opc-skills@opc-skills
```

Pin a ref if you are testing a branch:

```bash
codex plugin marketplace add BiuBiuHu/opc-skills --ref main
```

Equivalent documented forms:

```bash
codex plugin marketplace add https://github.com/BiuBiuHu/opc-skills.git
codex plugin marketplace add /path/to/local/opc-skills
```

Then start a new Codex session. In ChatGPT desktop / Work mode: restart the app, open the Plugins Directory, choose the **OPC Skills** marketplace, and install **OPC Skills**. Codex caches marketplace plugins under `~/.codex/plugins/cache/opc-skills/opc-skills/`.

The marketplace entry points `source.path` at `./plugins/opc-skills` (resolved from the marketplace root, which is the repository root). Policy is `AVAILABLE` + `ON_INSTALL`. Category is `Developer Tools`.

This install is **in addition to**, not a replacement for, the curl / npx skill checkout. A plugin install does not create `~/.codex/skills/opc-skills`. Keep using curl / npx when you want `doctor` / `update` against a git checkout.

### Single source of truth

Canonical skill files stay at the repository root so the existing Codex skill install keeps working. `plugins/opc-skills/skills/opc-skills/` is a generated, self-contained copy for the plugin host (symlinks out of the plugin root would break after cache install).

```bash
scripts/sync-plugin-skill.sh          # refresh the copy + plugin.json version
scripts/sync-plugin-skill.sh --check  # fail if the copy drifted
```

Do not edit the generated payload by hand. See [plugins/opc-skills/README.md](../plugins/opc-skills/README.md).

## 4. Public Plugins Directory — later, do not auto-submit

A public listing is a **human + workspace** action through the [plugin submission portal](https://developers.openai.com/plugins/deploy/submission). This repository must not submit, upload a ZIP, or claim a directory listing.

When someone with an OpenAI organization, verified developer identity, and Apps Management Write (or org owner) is ready:

1. Confirm the plugin payload is current: `scripts/sync-plugin-skill.sh --check`.
2. Add a square listing icon (≥48×48, PNG/JPEG/WebP/SVG) under `plugins/opc-skills/assets/` and point `extensions.com.openai.interface.logo` (and `composerIcon` if Codex validation asks) at it. Skills-only metadata does not require privacy / terms / support URLs; add them only if you also attach an MCP server later.
3. Zip **the plugin root**, not the whole git repo:

   ```bash
   cd plugins/opc-skills
   zip -r ../../opc-skills-plugin.zip plugin.json skills README.md
   # add assets/ after you include a listing icon
   ```

   Keep secrets out of the ZIP. There should be none in this package.
4. Open ChatGPT **Plugins** and choose **Upload new or existing plugin**.
5. Select the verified Developer identity. The directory shows that identity’s name, not the `developerName` string alone.
6. Upload the ZIP. On the plugin detail page, wait for **Metadata & Skills** checks. Copy any findings, fix the package, and upload again.
7. This package is skills-only. Skip MCP connection, or choose **Skills only** if the portal offers that path. Do not add an MCP server to this ZIP unless you intend to keep one forever (adding MCP to an existing skills-only plugin is not currently supported).
8. Skills-only plugins do not need MCP review cases or a demo recording. Complete any remaining Review details the portal still asks for. Do not put reviewer credentials in the package.
9. Select the draft, **Submit for review**, and complete the policy attestations. Track **Review status**. Feedback arrives by email.
10. After approval, open the approved package version and choose **Publish plugin**. Only then may README say it is in the public directory.
11. Later skill or metadata changes need a new ZIP on the **same** plugin. Hosted MCP tool changes (if you ever add one) are scanned separately.

Workspace-only sharing (Admin → Plugins → import marketplace, or publish a local plugin to selected workspace roles) is also a human admin action. It is not a public directory listing.

## 5. `openai/skills` curated is deprecated

[openai/skills](https://github.com/openai/skills) marks itself deprecated in favor of Agent Plugins. Do **not** open a PR into `skills/.curated` or `skills/.experimental`.

Historical notes (do not follow unless the upstream repo is revived):

- Listing used to mean a human PR, starting in `skills/.experimental/`, then `skills/.curated/` after review.
- `SKILL.md` frontmatter still uses hyphen-case `name` (≤64 chars) and a `description`.
- Contributors typically needed the OpenAI CLA.
- A listing copy would have been a **subset** of this repo. GitHub `BiuBiuHu/opc-skills` stays canonical.

## Optional third-party registries

These are **optional** discovery surfaces. They are not required, not official Codex, and this repo is not listed there unless a later human publish says so.

| Surface | What it is | Why it is optional |
| --- | --- | --- |
| [skills-hub.ai](https://skills-hub.ai) / `@skills-hub-ai/cli` | Third-party catalog + `npx @skills-hub-ai/cli search\|install\|publish` | Publish needs a login. Do not auto-submit. |
| SkillHub (`@astron-team/skillhub`, iFlytek) | Self-hosted / enterprise registry | Team-private; not an official Codex listing. |
| `npx skills add owner/repo` / skills.sh | Community installer used by many skill packs | Different tool than `npx opc-skills`. |

Name collision: [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) is a **different** project (solopreneur marketing/research skills). Their one-liner is `npx skills add ReScienceLab/opc-skills`. Ours is `npx opc-skills install` (this package), the curl script above, or `codex plugin add opc-skills@opc-skills` after adding this repo’s marketplace.

## Follow-up

- Keep `scripts/install.sh` and `npx opc-skills` as the supported skill-checkout installers.
- Use `$skill-installer` + the copy-paste prompts when the user is already inside Codex and does not want curl/npx.
- Use `codex plugin marketplace add BiuBiuHu/opc-skills` when the user wants the Agent Plugin package.
- Public Plugins Directory submit is a later human + workspace step. Do not run it from this repository.
- Do not npm-publish from a packaging PR. Bump `package.json` only when a human is ready to publish a new CLI version.
- Do not open PRs against `openai/skills`.
