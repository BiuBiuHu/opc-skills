# Agent 工作流

## 角色

- 文档治理 Agent：整理散落文档，合并到主文档，维护版本历史。
- 目标澄清 Agent：在 PRD、UI、架构和编码前对齐用户真正想完成的业务结果、操作闭环、成本约束和验收方式。
- 需求验证 Agent：检查需求歧义、冲突、隐藏假设、验收证据和是否可以进入后续阶段。
- 产品 Agent：负责 PRD、范围、角色、业务指标。
- UI Agent：负责 Markdown 原型、页面流程、交互状态。
- 架构 Agent：负责技术栈、模块、API、数据模型和自研边界。
- 变更影响 Agent：分析受影响 repo、模块、接口、数据、配置、环境、客户端版本和回滚路径。
- 研发 Agent：负责实施计划、任务拆分和代码修改。
- Bug Triage Agent：负责 bug 复现、定位、最小修复、回归验证和根因记录。
- QA Agent：负责测试用例、执行结果和测试报告。
- 联调 Agent：负责端到端联调门禁；仅当本次需求涉及客户端应用或用户明确要求时，启用客户端专项联调。
- DevOps Agent：负责部署、可观测性、运维手册和故障处理。

## 概念 Agent 与可执行 Subagent

`opc-skills` 默认定义的是概念 Agent，用来规定职责、产物和质量门禁。可执行 subagent 只能在用户明确允许 subagent、多 Agent 或并行执行时，由主 Agent 按任务边界启动。

Skill 文件不能直接调用 subagent。真实调用顺序必须是：主 Agent 读取 `references/subagent-orchestration.md`，读取对应 `agents/<role>-agent.md`，用 `templates/subagent-task-brief-template.md` 生成任务包，然后调用 Codex Runtime 工具 `multi_agent_v1.spawn_agent`。subagent 返回后，主 Agent 用 `templates/subagent-result-template.md` 审查结果。

启动 subagent 前必须回答：

- 是否能并行推进，或明显提高审查质量。
- ownership 是否清楚：可读范围、可写文件、禁止修改范围。
- 输出是否能被主 Agent 快速验收和集成。
- 不启动 subagent 的主要风险是什么。
- subagent 是否避开生产发布、数据库迁移、环境变量修改和破坏性清理。

推荐可执行 subagent：

- Explorer Agent：只读探索代码影响面、接口、数据模型、开源方案和历史文档。
- Frontend Agent：负责 Web/RN 页面、B 类表格、筛选、分页、抽屉、批量工具条、本地 mock 和前端测试。
- Backend Agent：负责主服务/BFF/API 契约、权限、分页、幂等、重试和后端测试。
- Data/Migration Agent：负责 schema、索引、迁移和回滚脚本设计；不得直接执行生产迁移。
- QA/Test Agent：负责测试策略、测试用例、自动化断言和失败路径。
- Integration Agent：负责前后端联调、环境拓扑、API contract 和证据汇总。

subagent 完成后，主 Agent 必须检查是否越权、是否引入无关改动、是否违反分层边界、是否有可复验证据，并记录实际收益、冲突和下次是否继续使用同类 subagent。

## 默认顺序

1. 文档治理 Agent 先确定 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，并声明本次文档目录。
2. 文档治理 Agent 先把同一 feature 下的散落文档合并到主文档。
3. 目标澄清 Agent 复述用户目标并反问关键问题，直到明确主要用户、核心闭环、批量范围、成本约束、返工粒度和验收证据。
4. 需求验证 Agent 更新 `docs/<FEATURE_NAME>/01-product/requirement-validation.md`。
5. 产品 Agent 更新 `docs/<FEATURE_NAME>/01-product/PRD.md`。
6. UI Agent 更新 `docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`。
7. 架构 Agent 更新 `docs/<FEATURE_NAME>/03-architecture/architecture.md`。
8. 变更影响 Agent 更新 `docs/<FEATURE_NAME>/04-engineering/change-impact.md`。
9. 研发 Agent 创建或更新实施计划、Backlog 和 evidence manifest。
10. QA Agent 创建或更新测试策略和测试用例。
11. 联调 Agent 创建或更新联调报告框架，声明本次是否启用客户端专项门禁；启用时补充客户端能力矩阵、验证工具和证据要求。
12. DevOps Agent 创建或更新运维手册和部署计划。
13. 如果本次已启用 subagent，主 Agent 追加 subagent 使用复盘：启动原因、预期收益、实际收益、产出文件、验证证据、冲突或重复工作。
14. 文档产出完成后进入 `awaiting-user-review`，等待用户审核。
15. 只有用户明确审核通过后，研发 Agent 才能开始代码实现，DevOps Agent 才能执行迁移或部署。

## 文档治理规则

- 每类文档只保留一份主文档。
- 每次需求必须有独立的 feature name，所有文档写入 `docs/<FEATURE_NAME>/`。
- 先合并有效内容，再归档或删除重复文档。
- 重大变更必须写入版本历史。
- 每份主文档必须写清本环节真正需要的判断、边界、方案、证据和风险。SMART/5W2H 只能作为可选校验，不得作为主结构或填空表格。
- 如果 PRD、UI 原型和技术架构不一致，不允许进入实施阶段。
- 如果目标澄清和后续 PRD/UI/架构不一致，不允许进入实施阶段；先回到目标澄清或需求验证。

## 目标澄清门禁

每个新需求都要先回答：

- 用户真正想完成的业务结果是什么，而不是要哪些控件或字段。
- 谁操作，操作频率如何，工作单元是单条、某天、某周、某月还是批量。
- 主要闭环是什么：创建、预览、审核、发布、返工、回滚或其它。
- 成本约束是什么，尤其是 LLM、生图、视频、第三方 API、批量任务。
- 最小返工粒度是什么，失败后怎么重试，哪些动作必须幂等。
- 什么证据能证明目标达成：截图、接口、数据、日志、预发 smoke 或人工验收。

如果任一项缺失，先反问用户。不要用字段清单、接口清单或页面草图代替目标澄清。

## B 类运营页面默认原则

- 筛选区和页面标题表达上下文，列表不重复展示已筛选信息。
- 主区域优先高密度表格，行内直接展示图片、状态、异常、进度和关键文案。
- 详情抽屉只放完整提示词、原始 JSON、错误日志、长文本和低频证据。
- 操作贴近数据行，批量操作贴近筛选上下文。
- 空值必须解释成可行动异常，不能只显示 `-`。
- 验收截图必须证明运营能在列表里完成主要判断。

## Bug 快速路径

当用户描述 bug、截图问题、报错、性能卡顿、交互异常或回归问题时，启用 `bugfix-fast-path`：

1. Bug Triage Agent 先记录复现步骤、环境、版本、实际结果和证据。
2. 定位归因层级，先排除旧构建、缓存、错误环境和配置混用。
3. 研发 Agent 做最小修复，必要时补失败测试。
4. QA/联调 Agent 验证原 bug、相邻路径和环境差异。
5. 结果写入 `debug-report.md`、`evidence-manifest.md` 和 `test-report.md`。

## 关卡

`manual-gated` 模式下，以下动作必须先等待用户确认：

- 文档产出后进入代码实现
- 删除或归档已有文档
- 代码实现
- 数据库迁移
- 部署
- 任何破坏性清理

## 客户端联调判定

仅当满足以下任一条件时启用客户端专项联调：

- 本次需求直接修改 Web、App、小程序、桌面端或 SDK。
- 本次后端/API/认证/存储/推送/轮询改动会影响客户端行为。
- 用户明确要求客户端、移动端、真机、模拟器、浏览器或前后端联调。

未启用时，联调报告只需写明“不适用”及原因，不得强制构建或启动无关客户端。

`full-auto` 模式只有在用户明确要求时才允许继续执行。

如果用户明确要求“文档生成后先审核”，即使处于 `full-auto` 意图，也必须以审核关卡优先。
