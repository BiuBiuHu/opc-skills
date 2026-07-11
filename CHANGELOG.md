# Changelog

## v0.1.0 - 2026-07-11

首个可发布版本。

### Added

- 增加 `README.md`，说明适用场景、核心能力、使用方式、目录结构和关键原则。
- 增加 `VERSION`，标记当前本地版本为 `0.1.0`。
- 增加 `CHANGELOG.md`，记录版本发布内容。
- 纳入 B 类运营页面方法论：总分下钻、ASCII 草图与交互路径合并、本地 mock 验证、分页和行内可判断。
- 纳入 Dida/OPC 分层架构原则：客户端只调用主服务/API server，内部子服务不暴露给前端。
- 纳入 AI/生成类成本保护：先提示词预览和审核，再昂贵生成，复用 OSS/缓存。
- 增加 `docs/subagent-optimization-plan.md` 草案，用于后续引入 Frontend、Backend、QA、Integration 等专业执行角色。

### Notes

- 本版本是本地 Skill 发布标记，不包含 Git tag 或远端 release。
- `docs/subagent-optimization-plan.md` 仍是草案，尚未合并为 `SKILL.md` 主规则。
