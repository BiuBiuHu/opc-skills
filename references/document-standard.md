# OPC 文档标准

所有产品和技术文档都必须使用本标准。

## 主文档

每次需求必须先确定一个独立的 `<FEATURE_NAME>`。每类文档只保留一份当前主文档，并且全部位于同一个 feature 目录：

- PRD：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/PRD.md`
- 需求验证：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/requirement-validation.md`
- UI 原型：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`
- 技术架构：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/03-architecture/architecture.md`
- 变更影响：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/change-impact.md`
- 实施计划：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/implementation-plan.md`
- 调试报告：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/debug-report.md`
- 证据清单：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/evidence-manifest.md`
- Backlog：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/backlog.md`
- 测试策略：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-strategy.md`
- 运维手册：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/06-ops/ops-runbook.md`

`<PROJECT_ROOT>` 必须按本次任务动态确定：

- 用户明确指定项目目录时，以用户指定目录为准。
- 用户没有指定项目目录时，以当前工作目录或当前任务最相关的项目目录为准。
- 不允许把文档写入无关项目的 `docs/` 目录。
- 最终回复必须列出实际写入的文档路径。

`<FEATURE_NAME>` 必须按本次需求动态确定：

- 使用英文 kebab-case，例如 `evidence-review-workflow`。
- 名称应表达业务能力，而不是临时动作，例如用 `evidence-review-workflow`，不要用 `update-docs`。
- 如果同一需求后续迭代，继续写入同一个 feature 目录，并在文档版本历史中追加版本。
- 如果是新需求，必须新建新的 feature 目录。

## 对应模板

- PRD：`templates/prd-template.md`
- 需求验证：`templates/requirement-validation-template.md`
- UI 原型：`templates/ui-prototype-template.md`
- 技术架构：`templates/architecture-template.md`
- 变更影响：`templates/change-impact-template.md`
- 实施计划：`templates/implementation-plan-template.md`
- 调试报告：`templates/debug-report-template.md`
- 证据清单：`templates/evidence-manifest-template.md`
- Backlog：`templates/backlog-template.md`
- 测试策略：`templates/test-strategy-template.md`
- 运维手册：`templates/ops-runbook-template.md`

## 必填章节

```md
# 标题

## 0. 版本历史

| 版本 | 日期 | 变更内容 | 变更原因 | 影响 |
|------|------|----------|----------|------|
| v0.1 | YYYY-MM-DD | 初始版本 | ... | ... |

## 1. 当前决策

## 2. 环节核心内容

不同文档必须写清本环节真正需要的内容：

- 需求验证：歧义、冲突、隐藏假设、状态机、权限、数据来源、环境差异、异常路径和验收证据映射。
- PRD：用户、问题、场景、范围、核心流程、验收标准、版本节奏。
- UI 原型：入口、信息架构、页面结构、字段、操作、状态、权限和终端范围。
- 架构：分层、调用图、数据模型、API、边界、防腐化约束、失败处理和回滚。
- 变更影响：受影响 repo、模块、API、数据、配置、缓存、任务、客户端版本、环境、回滚和兼容策略。
- 实施计划：项目发现、保存点、改动清单、执行顺序、最小验证、失败归因和复验方式。
- 调试报告：复现、定位、根因、最小修复、回归、证据和残余风险。
- 证据清单：命令、截图、API 响应、日志、数据库检查、设备/浏览器、结果和未执行原因。
- 测试：测试范围、测试数据、测试用例、断言、失败路径、证据和需求追踪。
- 运维：环境隔离、发布门禁、配置、巡检、告警、故障归因和回滚。

## 3. 未解决问题
```

## SMART 与 5W2H 的使用原则

SMART 和 5W2H 只能作为可选校验工具，不能作为每份文档的主结构。

正确用法：

1. PRD 可以用它们快速检查目标、用户、范围、指标和时间是否遗漏。
2. 架构、UI、研发、测试、运维文档优先写本环节的判断、边界、方案、证据和风险。
3. 禁止为了填满模板而写空泛表格。
4. 如果 SMART/5W2H 与具体环节内容冲突，以具体环节内容优先。

## 文档整理规则

当多个文档覆盖同一主题时：

1. 先确定 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`。
2. 再确定 feature 目录下的主文档目标。
3. 提取旧文档中的有效决策、数据、图示和约束。
4. 合并到 feature 目录下的主文档。
5. 在版本历史中记录本次合并。
6. 内容合并完成后，才能归档或删除重复文档。

## 审核关卡规则

每次 feature 文档生成或更新完成后：

1. Agent 必须停止在 `awaiting-user-review` 状态。
2. Agent 必须在最终回复列出待审核文档路径。
3. 用户审核通过前，不允许开始代码实现、数据库迁移、部署、删除或归档。
4. 如果用户提出修改意见，只更新同一 feature 目录下的文档并追加版本历史。
5. 只有用户明确批准后，才能进入实施阶段。
