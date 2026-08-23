# OPC Skills

[中文说明](README.zh-CN.md) | [English README](README.en.md)

当前版本 / Current version: `v0.4.0`

`opc-skills` is a Codex Skill for delivering consumer-facing apps and their supporting operator consoles. It guides the main agent through goal clarification, PRD, UI, architecture, implementation, testing, integration, release review, and production verification.

`opc-skills` 是一套面向 C 端业务应用和配套 B 端工作台的 Codex Skill。它把目标澄清、PRD、UI、架构、实现、测试、联调、发布评审和生产回归串成可审查的交付流程。

This sync adds release-integrity gates, default-branch reconciliation, and worktree checks to the release flow.

本次同步补充了发布完整性门禁、默认分支归位和 worktree 校验。

## Quick Install

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

Then trigger it in Codex with:

```text
启动 OPC Skills
```

## 快速入口

- 中文文档：[README.zh-CN.md](README.zh-CN.md)
- English documentation: [README.en.md](README.en.md)
- Main skill rules: [SKILL.md](SKILL.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Release integrity reference: [references/release-integrity.md](references/release-integrity.md)
- Release integrity check: [scripts/check_release_integrity.sh](scripts/check_release_integrity.sh)

## License

MIT
