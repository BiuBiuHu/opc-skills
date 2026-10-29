# Agent 工作流

用于完整需求的阶段推进及模式/审核关卡查询。概念职责按需读取 [角色目录](role-catalog.md) 的当前阶段；可执行 subagent 另读 [编排准则](subagent-orchestration.md)，不会因角色存在而自动启动。

## 目标澄清门禁

**目标澄清不可跳过。** 在 PRD、UI、架构、编码或部署前，必须先对齐用户真正想完成的业务结果，而不是只复述功能点。若目标、角色、操作闭环、时间范围、成本约束或验收方式不清楚，必须先用少量关键问题反问用户，直到双方对目标达成一致。目标澄清至少要回答：谁在什么场景下完成什么结果；核心工作单元是什么；一次操作面向单条、某天、某周、某月还是批量；成功标准是什么；哪些成本、时延、质量和环境约束不能突破；失败后如何重试、回滚或返工。未完成目标澄清时，不得把字段清单、接口清单或页面草图当成需求。

**C 端业务以用户路径为主线。** C 端需求必须先定义用户、入口、场景、核心路径、完成结果和失败恢复，而不是先拆页面或字段。若需要配套 B 端工作台，必须说明工作台如何支撑配置、审核、生成、发布、排错或返工。

## AI/生成成本

**AI/生成类需求必须成本分层。** 当需求涉及 LLM、生图、视频、批量生成、投放或审核时，必须先拆成低成本可审阶段和高成本执行阶段。默认顺序是：生成/预览提示词或计划 -> 人工或规则审核 -> 批量生成昂贵产物 -> 缓存/对象存储复用 -> 按最小粒度返工。不得默认每次查看、刷新、重新发布或客户端加载都重新生成昂贵产物。文档和 UI 必须明确缓存键、对象存储位置、幂等策略、最小重生粒度、批量生成上限和成本保护。

## 项目材料

识别并声明本次 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，然后读取当前项目材料：

- `<PROJECT_ROOT>/README.md` 或项目说明文件
- 当前 PRD
- 当前 Markdown UI 原型
- 当前技术架构
- 当前开源选型与自研边界

## 默认顺序

1. 文档治理 Agent 先确定 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，并声明本次文档目录。
2. 按 [保存点与分支准备](implementation-workflow.md#保存点与分支准备) 逐仓库准备，失败则停止实现。
3. 文档治理 Agent 先把同一 feature 下的散落文档合并到主文档。
4. 目标澄清 Agent 复述用户目标并反问关键问题，直到明确主要用户、核心闭环、批量范围、成本约束、返工粒度和验收证据。
5. 需求验证 Agent 更新 `docs/<FEATURE_NAME>/01-product/requirement-validation.md`。
6. 产品 Agent 更新 `docs/<FEATURE_NAME>/01-product/PRD.md`。
7. UI Agent 更新 `docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`。
8. 架构 Agent 更新 `docs/<FEATURE_NAME>/03-architecture/architecture.md`。
9. 变更影响 Agent 更新 `docs/<FEATURE_NAME>/04-engineering/change-impact.md`。
10. 研发 Agent 创建或更新实施计划、Backlog 和 evidence manifest。
11. QA Agent 创建或更新测试策略和测试用例。
12. 联调 Agent 创建或更新联调报告框架，声明本次是否启用客户端专项门禁；启用时补充客户端能力矩阵、验证工具和证据要求。
13. DevOps Agent 创建或更新运维手册和部署计划。
14. 生产发布进入 `complete` 后，如果用户或项目事实源启用发布后内容生产，Content Agent 进入 `suggest`、`draft` 或 `publish` 模式；文章生产不改变页面发布状态。
15. 如果本次已启用 subagent，主 Agent 追加 subagent 使用复盘：启动原因、预期收益、实际收益、产出文件、验证证据、冲突或重复工作。
16. 文档产出完成后进入 `awaiting-user-review`，等待用户审核。
17. 只有用户明确审核通过后，研发 Agent 才能开始代码实现，DevOps Agent 才能执行迁移或部署。

文档位置、模板映射及整理规则统一见 [文档标准](document-standard.md)。需要编码时按 [实施工作流](implementation-workflow.md) 执行；需要联调时按 [客户端与跨服务联调](client-integration.md) 执行；发布按 [完整性](release-integrity.md) 和 [PR 生命周期](release-pr-lifecycle.md) 执行。

## Bug 快速路径

按 [Bug 快速路径](implementation-workflow.md#bug-快速路径) 完成复现、定位、最小修复、回归与证据；除暴露产品/架构缺口外，不强制完整 PRD/UI/架构流程。

## 关卡

`manual-gated` 模式下，以下动作必须先等待用户确认：

- 文档产出后进入代码实现
- 删除或归档已有文档
- 代码实现
- 数据库迁移
- 部署
- 任何破坏性清理

`full-auto` 只有用户明确要求时启用；用户已有“文档生成后先审核”等关卡时仍优先遵守。即使 full-auto，生产发布仍保留预发报告和 CR/code review，不从未提交工作区部署，不先发布后补 CR。

## Inbox 与任务衔接

**零散想法先进入 Inbox，不直接开发。** 当用户说“先记下来”“后面再开发”或临时给出产品想法时，只记录到轻量草稿清单，不启动正式 PRD/架构/编码流程。当前任务完成后，如果没有命中必须停下的硬门禁，必须立刻回看 Inbox/Todo：评估清单事项与当前工作、已提交代码和已完成任务的相关性；选择一个后续任务；然后按 OPC Skills 正式研发流程继续执行，包括开新分支、编写技术方案和测试方案、实施、端到端联调和测试用例。不得等待用户再说“继续”。只有当下一步会进入用户审核、迁移、部署、删除或其它明确确认关卡时才暂停。

## 发布后内容生产

按 [发布后内容生产](post-release-content.md) 的入口检查和 suggest/draft/publish 模式执行；详细角色见 [Content Agent](../agents/content-agent.md)。
