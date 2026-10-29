# OPC 文档标准

产出产品、技术方案、架构、UI 原型、测试计划或评审结论时读取。所有这类决策必须落盘到 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/`，不能只留聊天记录；每类文档只保留一份当前主文档。

## 项目事实与文档位置

**通用 Skill 与项目事实必须隔离。** `opc-skills` 只保存跨项目可复用的方法、角色、门禁、模板和参数化示例，不保存任何具体业务项目的事实。项目名、真实仓库名或绝对路径、账号/邮箱、域名、云项目、服务别名、deployment ID、数据库 host/schema、密钥变量值、业务专用状态机和单一产品特例，必须写入对应项目仓库的 README、架构文档、runtime entry inventory、测试数据说明或运维手册。通用文档需要表达调用关系时，只使用 `<CLIENT_APP>`、`<PRIMARY_API>`、`<AUTH_SERVICE>`、`<WORKER>` 等角色占位符；需要真实值执行时，先读取项目事实源，禁止从 skill、历史聊天或示例猜测。

`<PROJECT_ROOT>` 的判定规则：

- 如果用户明确指定项目目录，则以该目录为项目根目录。
- 如果用户没有指定项目目录，则以当前工作目录中最匹配本次任务的项目目录为项目根目录。
- 如果当前工作目录本身就是项目根目录，则直接使用当前目录。
- 不允许把文档写死到某个固定项目名下面；最终回复必须列出实际写入路径。

`<FEATURE_NAME>` 的判定规则：

- 每次新需求必须先定义一个稳定、可读、英文 kebab-case 的 feature name，例如 `account-linking`。
- 如果用户明确给出 feature name，则使用用户给出的名称。
- 如果用户没有给出，Agent 必须根据需求内容自行命名，并在开始写文档前声明。
- 同一需求的 PRD、UI 原型、技术架构、实施计划、Backlog、测试策略、运维手册都必须写到同一个 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/` 目录下。
- 不允许把本次需求文档分散写入多个 feature 目录。

## 文档与模板索引

下表路径均相对 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/`；模板相对 skill 根目录。更新已有文档时沿用本 feature 主文档，不另建竞争版本。发布后内容仅在启用时创建。

| 文档 | 主文档路径 | 模板 |
|---|---|---|
| 竞品调研 | `00-research/competitor-research.md` | 按本环节要求及项目既有格式 |
| 需求验证 | `01-product/requirement-validation.md` | `templates/requirement-validation-template.md` |
| PRD | `01-product/PRD.md` | `templates/prd-template.md` |
| UI 原型 | `02-ui/markdown-prototype.md` | `templates/ui-prototype-template.md` |
| 架构 | `03-architecture/architecture.md` | `templates/architecture-template.md` |
| 变更影响 | `04-engineering/change-impact.md` | `templates/change-impact-template.md` |
| 实施计划 | `04-engineering/implementation-plan.md` | `templates/implementation-plan-template.md` |
| 调试报告 | `04-engineering/debug-report.md` | `templates/debug-report-template.md` |
| 证据清单 | `04-engineering/evidence-manifest.md` | `templates/evidence-manifest-template.md` |
| Code Review | `04-engineering/code-review.md` | 按本环节要求及项目既有格式 |
| Backlog | `04-engineering/backlog.md` | `templates/backlog-template.md` |
| 测试策略 | `05-testing/test-strategy.md` | `templates/test-strategy-template.md` |
| 结构化用例 | `05-testing/test-cases.json` | 按本环节要求及项目既有格式 |
| 测试报告 | `05-testing/test-report.md` | 按本环节要求及项目既有格式 |
| 联调报告 | `05-testing/integration-report.md` | 按本环节要求及项目既有格式 |
| 发布方案 | `06-ops/release-plan.md` | `templates/release-plan-template.md` |
| 运维手册 | `06-ops/ops-runbook.md` | `templates/ops-runbook-template.md` |
| 可选内容生产 | `07-content/content-production.md` | `templates/content-production-template.md` |

## 质量要求

所有主文档必须包含：

1. 版本历史
   - 版本号
   - 日期
   - 变更内容
   - 变更原因
   - 决策影响

2. 当前决策
   - 当前采用的方案
   - 被拒绝的替代方案
   - 未解决问题

3. 环节核心内容
   - 竞品调研：来源链接、对比维度、通用模式、适用性、采纳/拒绝决策和风险。
   - 需求验证：歧义、冲突、隐藏假设、状态机、权限、数据来源、环境差异、异常路径、边界条件和验收证据映射。
   - PRD：场景、范围、用户、流程、验收标准。
   - UI 原型：页面结构、入口、交互、状态、字段和权限。
   - 架构：分层、调用图、数据模型、API、边界、防腐化约束。
   - 变更影响：受影响 repo、模块、API、数据、配置、缓存、任务、客户端版本、环境、回滚和兼容策略。
   - 实施计划/Backlog：项目发现、改动清单、顺序、迁移、兼容、风险、退出条件和自动执行循环。
   - Bug 调试：复现、定位、归因、最小修复、回归、根因、证据和残余风险。
   - 证据清单：命令、页面、截图、接口响应、日志、数据库检查、设备/浏览器、结果和未执行原因。
   - 测试：用例、命令、数据、断言、截图/API/日志证据和失败路径。
   - 测试用例必须从“测什么、哪个系统测、怎么测、具体 case、证据是什么”五个维度写清楚，并覆盖成功路径、失败路径、边界路径和不能发生的副作用。
   - 运维：环境、配置、发布、回滚、巡检、告警和故障处理；发布方案还必须包含双向影响闭包、逐系统发布/不发布证据、候选与默认分支一致性、deployment 映射和 worktree 归位证据。

4. 架构调用关系
   - 适用于 `03-architecture/architecture.md`。
   - 必须包含分层架构图，使用 Mermaid 画出客户端层、主服务层、内部子服务层、数据层、对象存储/第三方层，以及允许的依赖方向。
   - 必须包含至少一个调用关系章节，说明用户操作或系统任务从入口到最终数据/副作用的完整链路。
   - 必须包含 Mermaid 调用图，使用 fenced code block：```` ```mermaid ````。调用图要画出主要模块和关键调用方向，不得只用文字或表格代替。
   - 每条关键链路必须在 Mermaid 图中体现调用方、被调用方、协议或接口、鉴权方式、同步/异步属性和核心数据对象；失败处理和可观测证据可用简短要点说明。避免使用“调用链表格”作为主要表达。
   - Mermaid 图必须画出前端访问边界：客户端 -> 网关/主服务 -> 内部子服务。不得把客户端直接连到内部子服务，除非该直连是明确设计决策并写明风险。
   - 如果存在 Web、移动端、后台、服务端、AI/Worker、数据库、对象存储或第三方 API，必须逐一纳入调用关系或明确说明不适用。

5. 架构防腐化检查
   - 适用于 `03-architecture/architecture.md`，必要时也写入 `04-engineering/implementation-plan.md`。
   - 必须列出至少 3 条本 feature 的防腐化约束，例如“前端不得直连内部子服务”“主服务是唯一外部契约入口”“内部子服务不持有用户登录态判断”“跨环境 URL 不得兜底到生产”“临时脚本不得成为业务入口”。
   - 每条约束必须能在代码、配置、测试或联调报告中被验证。

6. 需求到验证追踪
   - 适用于 `01-product/requirement-validation.md`、`01-product/PRD.md`、`05-testing/test-cases.json`、`05-testing/test-report.md` 和 `04-engineering/evidence-manifest.md`。
   - 每条 P0/P1 需求必须有稳定 ID，例如 `REQ-FEATURE-001`。
   - PRD 验收标准、测试用例、联调报告和证据清单必须引用这些 ID。
   - 如果某条需求无法映射到可执行测试或证据，必须退回需求验证阶段重写，不能靠“人工感觉通过”验收。

实现验证与 Bug 修复质量执行 [实施与 Bug 工作流](implementation-workflow.md)；对应要求不因移出本文件而省略。

主文档应简洁但完整。历史决策放在版本历史里，不要散落到重复文档中。

## 标准章节与可选检查

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

## 散落文档归并

当多个文档覆盖同一主题时：

1. 先确定 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`。
2. 再确定 feature 目录下的主文档目标。
3. 提取旧文档中的有效决策、数据、图示和约束。
4. 合并到 feature 目录下的主文档。
5. 在版本历史中记录本次合并。
6. 内容合并完成后，才能归档或删除重复文档。

同一 feature 的旧文档可能散落在以下旧目录，先查找并合并有效内容，再归档或删除，不能将其误认成新文档目标：

- `docs/01-product/PRD.md`
- `docs/01-product/requirement-validation.md`
- `docs/02-ui/markdown-prototype.md`
- `docs/03-architecture/architecture.md`
- `docs/04-engineering/implementation-plan.md`
- `docs/04-engineering/change-impact.md`
- `docs/04-engineering/debug-report.md`
- `docs/04-engineering/evidence-manifest.md`
- `docs/04-engineering/backlog.md`
- `docs/05-testing/test-strategy.md`
- `docs/06-ops/ops-runbook.md`
- `docs/00-research/competitor-research.md`

PRD、UI 原型、架构或目标澄清结论不一致时，先退回澄清/需求验证，不进入实现。文档有版本化变更时写清改动、原因、替代的旧决策和影响。

## 模板使用

所有主文档都必须对应一个模板。

Agent 在读写文档时：

1. 先读取对应模板。
2. 再读取当前主文档。
3. 判断主文档是否缺少模板中的约束项。
4. 缺项时优先补齐，而不是自由发挥新增结构。

如果用户没有特别要求，不要随意改变主文档的顶层结构。

## 审核关卡规则

每次 feature 文档生成或更新完成后：

1. Agent 必须停止在 `awaiting-user-review` 状态。
2. Agent 必须在最终回复列出待审核文档路径。
3. 用户审核通过前，不允许开始代码实现、数据库迁移、部署、删除或归档。
4. 如果用户提出修改意见，只更新同一 feature 目录下的文档并追加版本历史。
5. 只有用户明确批准后，才能进入实施阶段。
