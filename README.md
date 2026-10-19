# OPC Skills

**语言 / Language:** [中文说明](README.zh-CN.md) · [English README](README.en.md)

当前版本 / Current version: `v0.4.0`

`opc-skills` is a Codex Skill for delivering consumer-facing apps and their supporting operator consoles. It guides the main agent through goal clarification, PRD, UI, architecture, implementation, testing, integration, release review, and production verification.

`opc-skills` 是一套面向 C 端业务应用和配套 B 端工作台的 Codex Skill。它把目标澄清、PRD、UI、架构、实现、测试、联调、发布评审和生产回归串成可审查的交付流程。

完整说明见语言页；规则以 [SKILL.md](SKILL.md) 为准。

Full docs live on the language pages; [SKILL.md](SKILL.md) is the source of truth for agent rules.

## Quick Install / 快速安装

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

Then trigger it in Codex with / 在 Codex 中用以下意图触发：

```text
启动 OPC Skills
```

## 延伸阅读 / Further reading

相关实践 / Related notes from One PC：

- [一个人，也可以做完一款产品：我的 OPC 软件研发实践](https://www.peak-lake.com/blog/opc-software-practice/) · [EN](https://www.peak-lake.com/en/blog/opc-software-practice/) — 一人公司如何把痛点做到发布；本仓库是其中的交付流程。 / Solo product loop; this repo is that delivery flow.
- [Loop Engineering 没有银弹](https://www.peak-lake.com/blog/mslj4f6g/) · [EN](https://www.peak-lake.com/en/blog/mslj4f6g/) — 垂直 Skills + spec/TDD，文中指向本仓库。 / Vertical Skills + spec/TDD; the post links here.

## Docs / 文档

- 中文：[README.zh-CN.md](README.zh-CN.md)
- English: [README.en.md](README.en.md)
- Main skill rules: [SKILL.md](SKILL.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Release integrity: [references/release-integrity.md](references/release-integrity.md)
- Release integrity check: [scripts/check_release_integrity.sh](scripts/check_release_integrity.sh)
- Post-release content: [references/post-release-content.md](references/post-release-content.md)

## License

MIT
