# Changelog

## Unreleased

### Added

- 增加中英文 README：根 `README.md` 作为语言入口，中文说明迁移到 `README.zh-CN.md`，新增 `README.en.md`。
- 增加 `references/release-integrity.md`，固化双向依赖闭包、发布状态机、候选冻结、deployment 与默认分支一致性和 worktree 归位门禁。
- 增加 `scripts/check_release_integrity.sh`，只读检查候选 commit 是否已进入远端默认分支、deployment commit 是否匹配，并核对默认分支 worktree。
- 发布方案模板新增变更来源、逐系统决策、漏发复核、完整性检查和逐 worktree 归位证据。
- 增加任务自动衔接规则：当前任务完成后，若未命中硬门禁，主 Agent 自动回看 Inbox/Todo 并继续下一项，不再等待用户单独说“继续”。
- 增加项目级 runtime entry inventory 门禁：真实登录入口、BFF、OAuth callback、业务回跳、固定 alias 和 deployment 快照记录在项目文档仓库，不写入通用 skill；发布前必须逐个 callback alias inspect 并将候选快照冻结到 release plan。
- 增加低流量生产合成探针、Release PR 五项最终核销证据、线上失败暂停与命中 deployment 定位、发布后切回同步默认主分支门禁。
- 增加 PR 中文门禁：新建 Code PR、Release PR、文档 PR 的标题、正文和检查清单默认使用中文，并在创建后回读核对。

### Changed

- 增加通用 Skill 与项目事实隔离规则，并将项目名、固定服务、测试账号、仓库路径和业务专用示例改为角色占位符或通用示例。
- 发布与 DevOps 规则改为：未知依赖、未知 owner、未知 deployment 映射、默认分支未合并或 worktree 未同步时阻断；禁止先部署线上再补 main/master。
- 强化研发和 QA 的测试范围选择规则：每轮验证先按改动文件、调用链、共享契约和风险选择最小充分测试集，全量测试仅在发布门禁、公共基础设施变更、影响范围不可可靠切分或用户明确要求时升级。
- `VERSION` 和 README 当前版本更新为 `0.4.0`。

## v0.3.2 - 2026-08-08

### Added

- 增加新需求分支准备门禁：保存当前工作区，切回远端默认主分支并 `git pull --ff-only`，确认同步后再创建需求分支。
- 多仓库需求按仓库分别记录分支保存点、主分支同步结果和新需求分支；同步失败时禁止开始实现。

### Changed

- 同步 `SKILL.md`、README 和 `references/agent-workflow.md` 的研发顺序与编码前门禁。

## v0.3.1 - 2026-08-06

### Added

- 增加生产发布后的强制线上回归门禁，覆盖 P0/P1、关联系统契约、相邻高风险路径和失败路径。

### Changed

- 发布完成条件改为：全部系统核销、线上回归通过且观察窗口完成；health/smoke 不再能单独证明发布完成。
- P0/P1 回归失败必须停止核销、回滚并重新走预发和发布评审流程。
- 同步 `release-gated` 模式、README、QA Agent 和 DevOps Agent，避免执行入口仍以 smoke 作为发布终点。
- `VERSION` 更新为 `0.3.1`。

## v0.3.0 - 2026-08-06

### Added

- 增加强制发布方案评审门禁：每次共享环境发布前必须形成关联系统发布矩阵并获得明确批准。
- 增加 `templates/release-plan-template.md`，覆盖系统范围、候选版本、部署顺序、环境、迁移、验证、监控和回滚核销。

### Changed

- 生产发布流程增加方案变更重新评审和发布后逐系统核销，防止只发布主仓库而漏发关联服务。
- DevOps Agent 和运维模板同步关联系统矩阵要求。
- `VERSION` 更新为 `0.3.0`。

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
- 纳入通用分层架构原则：客户端只调用主服务/API server，内部子服务不暴露给前端。
- 纳入 AI/生成类成本保护：先提示词预览和审核，再昂贵生成，复用 OSS/缓存。
- 增加 `docs/subagent-optimization-plan.md` 草案，用于后续引入 Frontend、Backend、QA、Integration 等专业执行角色。

### Notes

- 本版本是本地 Skill 发布标记，不包含 Git tag 或远端 release。
- `docs/subagent-optimization-plan.md` 仍是草案，尚未合并为 `SKILL.md` 主规则。
