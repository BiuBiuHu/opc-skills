# opc-skills Agent Plugin

Skills-only [Agent Plugin](https://developers.openai.com/plugins/build/plugins) wrapper around the canonical `opc-skills` Codex skill.

This folder is the plugin root (`plugin.json` + `skills/`). It does **not** replace the existing Codex skill install:

- `npx opc-skills install` / `curl …/scripts/install.sh` still clone the **repository root** into `~/.codex/skills/opc-skills`
- the plugin host loads `skills/opc-skills/` from this directory after a marketplace install

## Single source of truth

Do not edit `skills/opc-skills/` by hand.

| Path | Role |
| --- | --- |
| Repository root `SKILL.md`, `agents/`, `references/`, `templates/`, selected `scripts/` and `docs/` | Canonical skill |
| `plugins/opc-skills/plugin.json` | Portable Agent Plugins manifest |
| `plugins/opc-skills/skills/opc-skills/` | Generated copy for the plugin host |
| `.agents/plugins/marketplace.json` | Repo marketplace catalog |

Refresh the copy after changing a canonical skill file:

```bash
scripts/sync-plugin-skill.sh
```

Check for silent drift:

```bash
scripts/sync-plugin-skill.sh --check
```

The copy is self-contained on purpose. Symlinks back to the repo root would break after Codex caches the plugin under `~/.codex/plugins/cache/`.

## Marketplace install

Documented in [docs/skills-hub.md](../../docs/skills-hub.md). Short form:

```bash
codex plugin marketplace add BiuBiuHu/opc-skills
codex plugin add opc-skills@opc-skills
```

This plugin is **not** listed in the public Plugins Directory until a human submits it through the OpenAI portal.
