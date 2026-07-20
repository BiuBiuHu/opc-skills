# Changelog

## Unreleased

### Added

- 增加 `agents/` 目录，定义 Explorer、Frontend、Backend、QA/Test、Integration 和 DevOps subagent 的角色、边界和输出格式。
- 增加 `templates/subagent-task-brief-template.md` 和 `templates/subagent-result-template.md`，用于主 Agent 生成任务包和验收 subagent 输出。
- 增加 `references/subagent-orchestration.md`，明确 skill 不能直接调用 subagent，必须由主 Agent 使用 Codex Runtime `multi_agent_v1.spawn_agent` 执行。

### Changed

- 更新 `SKILL.md`、`README.md`、`references/agent-workflow.md` 和 `docs/subagent-runtime-invocation-design.md`，补齐 “skill 规则 -> 主 Agent -> runtime tool call -> subagent” 的实际执行链路。

## v0.2.2 - 2026-07-11

### Added

- 增加昂贵批量操作规则：禁止“批量确认后逐条弹窗”的嵌套确认流，必须在一次确认中展示范围、成本、缓存、重试和覆盖策略。
- 增加产物可用性状态要求：生图任务成功但没有图片 URL 时必须显示“OSS 未命中/缺图片”，不能显示为已完成。
- 增加 B 类页面 mock gate 要求：优先沉淀可复跑 Playwright/MSW/dev fixture；临时脚本必须记录脚本、断言和不可复跑风险。
- 增加预发证据边界：能进入登录页或应用壳不能替代真实 API、OSS/数据库和功能页预发验收。

### Changed

- `VERSION` 更新为 `0.2.2`。
- README 当前版本更新为 `v0.2.2`。

## v0.2.1 - 2026-07-11

### Added

- 同步 README 到当前主规则，补充 subagent 适用边界与 B 类页面方法论提示。

### Changed

- `VERSION` 更新为 `0.2.1`。
- README 当前版本更新为 `v0.2.1`。

## v0.2.0 - 2026-07-11

### Added

- 将 Subagent 执行模型纳入 `SKILL.md` 主规则：Skill 定义规则，主 Agent 负责触发、审查、集成和最终负责。
- 在 `references/agent-workflow.md` 增加概念 Agent 与可执行 subagent 的区别。
- 增加 Explorer、Frontend、Backend、Data/Migration、QA/Test、Integration 等推荐 subagent 角色和边界。
- 增加 subagent 启动门禁：用户明确允许、任务可并行、ownership 清楚、可验收、不得涉及生产发布或破坏性操作。
- 增加 subagent 使用复盘要求：记录启动原因、预期收益、实际收益、产出文件、验证证据、冲突和后续是否继续使用。

### Changed

- README 当前版本更新为 `v0.2.0`。
- `docs/subagent-optimization-plan.md` 状态更新为已应用到 `v0.2.0` 主规则。

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
