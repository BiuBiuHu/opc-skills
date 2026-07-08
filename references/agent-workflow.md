# Agent 工作流

## 角色

- 文档治理 Agent：整理散落文档，合并到主文档，维护版本历史。
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

## 默认顺序

1. 文档治理 Agent 先确定 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，并声明本次文档目录。
2. 文档治理 Agent 先把同一 feature 下的散落文档合并到主文档。
3. 需求验证 Agent 更新 `docs/<FEATURE_NAME>/01-product/requirement-validation.md`。
4. 产品 Agent 更新 `docs/<FEATURE_NAME>/01-product/PRD.md`。
5. UI Agent 更新 `docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`。
6. 架构 Agent 更新 `docs/<FEATURE_NAME>/03-architecture/architecture.md`。
7. 变更影响 Agent 更新 `docs/<FEATURE_NAME>/04-engineering/change-impact.md`。
8. 研发 Agent 创建或更新实施计划、Backlog 和 evidence manifest。
9. QA Agent 创建或更新测试策略和测试用例。
10. 联调 Agent 创建或更新联调报告框架，声明本次是否启用客户端专项门禁；启用时补充客户端能力矩阵、验证工具和证据要求。
11. DevOps Agent 创建或更新运维手册和部署计划。
12. 文档产出完成后进入 `awaiting-user-review`，等待用户审核。
13. 只有用户明确审核通过后，研发 Agent 才能开始代码实现，DevOps Agent 才能执行迁移或部署。

## 文档治理规则

- 每类文档只保留一份主文档。
- 每次需求必须有独立的 feature name，所有文档写入 `docs/<FEATURE_NAME>/`。
- 先合并有效内容，再归档或删除重复文档。
- 重大变更必须写入版本历史。
- 每份主文档必须写清本环节真正需要的判断、边界、方案、证据和风险。SMART/5W2H 只能作为可选校验，不得作为主结构或填空表格。
- 如果 PRD、UI 原型和技术架构不一致，不允许进入实施阶段。

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
