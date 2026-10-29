---
name: opc-skills
description: 用于规划、设计、研发、测试、部署和运维 C 端业务应用及配套 B 端工作台。支持 Vercel / Cloudflare 静态站与原生 Workers 服务端部署迁移，擅长 App/Web/小程序体验、主服务/API、认证、AI/生成、运营后台、联调、多仓库发布完整性、main/master 归并、worktree 同步门禁和发布后双语内容生产。
---

# OPC Skills

C 端业务应用与配套 B 端工作台的研发入口。先识别用户指定或当前最相关的项目根目录，再按任务选择模式和参考文件。

## 触发与范围

- 支持 `启动 OPC Skills`、`启动 C 端业务应用研发流程`、`一键启动 C 端应用研发`、`跑一遍 C 端应用和配套 B 端工作台全流程`。
- 处理 App/Web/小程序的规划、设计、研发、测试、发布、运维及配套配置、审核、运营、排错工作台。
- 客户端、前后端、真机/模拟器联调按本次影响范围启用；发布后文章与双语 SEO/GEO 内容是可选旁路。

## 工作模式

- `manual-gated`：默认模式。先产出文档和计划，文档完成后停在 `awaiting-user-review`，实施、迁移、部署、删除前等待用户确认。
- `full-auto`：仅当用户明确说 `全自动`、`full-auto`、`不需要确认` 时启用；但如果用户已要求“文档审核后才能编码”，则本次 feature 必须遵守审核关卡。
- `implementation-loop`：当需求、架构和验收标准已经明确，且用户要求“开始编码”“往下推进”“实现一下”时启用。跳过不必要的重新调研，但必须先做项目发现、变更影响分析、保存点、实现、验证、修复、复验和证据记录。
- `bugfix-fast-path`：当用户描述线上/预发/本地 bug、截图问题、报错、性能卡顿、交互异常或回归问题时启用。只要求完成复现、定位、修复、回归和证据闭环；除非 bug 暴露出产品或架构缺口，否则不强制补全完整 PRD/UI/架构流程。
- `validation-only`：当用户要求“验证一下”“review 需求”“看看能不能做”“只检查不改代码”时启用。只输出需求验证、实现验证或风险清单，不进入编码。
- `release-gated`：当用户要求预发、线上、发布、回滚、灰度、TestFlight 或运维检查时启用。只处理发布门禁、环境隔离、验证报告、回滚、线上 smoke、线上回归和观察窗口，不夹带无关功能开发。
- `post-release-content`：当页面或功能已经完成生产发布，且用户或项目配置启用文章生产时使用。只处理素材采集、选题、中文/英文稿、SEO/GEO、配图计划和文章落盘/发布，不重新执行页面发布门禁。
- `architecture-review`：当用户要求检查架构、调用关系、分层、服务腐化或 Agent 产物质量时启用。重点审查依赖方向、服务边界、数据所有权、调用图和防腐化规则。

## 关键约束

以下是入口摘要，执行细节按下一节读取；reference 中的既有要求仍然适用。

1. **保护已有成果。** 改代码、重构、迁移、部署或批量修改前先建立保存点。新需求从同步后的默认分支创建，逐受影响仓库核对；同步失败停止实现，不丢弃用户改动。详见[实施准备](references/implementation-workflow.md#保存点与分支准备)。
2. **从业务结果出发。** 目标、角色、核心闭环、批量范围、成本和验收不明确时先澄清，不以字段或页面清单替代目标。完整需求按[阶段工作流](references/agent-workflow.md)推进。
3. **沿用模式与审核关卡。** 默认 manual-gated；文档审核、实现、迁移、部署、删除等按现有模式执行。full-auto 需要明确授权，不能越过本 feature 已有审核要求；结构拆分不改变这些边界。
4. **隔离项目事实。** 本 skill 只放通用方法；真实仓库、域名、账号、部署与数据库配置从项目事实源读取，不带入通用 skill 或客户端包。所有方案、架构决策、UI 原型、测试计划和评审结论落盘到 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/`，按[文档标准](references/document-standard.md)维护唯一主文档。
5. **保持分层与身份归属。** 客户端只调用主服务/网关，内部服务走受控服务间调用；第三方 provider 与身份规则归统一认证服务。完整边界见[架构职责](references/role-catalog.md#5-架构-agent)。
6. **先调研、后实现、再验证。** 非平凡实现先查成熟方案；按保存点、小步修改、最小验证、失败归因、修复复验、自审和证据记录闭环。测试范围按调用链与风险选择，不默认全量。
7. **验证真实功能。** UI 改动进入被改页面和对应状态验收；认证覆盖真实客户端完整登录、持久化、冷启动和身份一致性。构建、安装、Ready、health 或接口 2xx 不替代业务闭环。
8. **保护高成本操作。** AI/生成先低成本预览、审核，再执行昂贵生成并复用缓存；B 类页面先本地 mock 验收，再预发真实链路；批量确认、跳过和返工约束不能省略。
9. **发布单独核销。** 明确目标环境与已提交来源，先预发、测试报告和 CR，再按批准方案上线。Production 候选先归并默认分支；发布矩阵、真实入口、回归、观察窗口和 worktree 归位缺项时不能宣告完整发布。失败停止切流及核销，按方案回滚。
10. **Subagent 按授权启动。** 概念角色不自动启动 subagent；仅用户明确允许且收益、ownership、验收清楚时由主 Agent 用 Runtime 工具调用，不能用 shell/hooks 启动。主 Agent 保留架构、集成、发布和最终汇报责任。
11. **PR 默认中文。** 创建或主动重写 PR 时按[PR 语言规则](references/release-pr-lifecycle.md#pr-创建语言)执行并回读；仓库规范或用户明确指定其它语言时才例外。
12. **任务与内容衔接保持原规则。** 零散想法先记 Inbox；任务完成后按[Inbox 与任务衔接](references/agent-workflow.md#inbox-与任务衔接)处理。生产完成时检查发布后内容配置，按可选内容旁路提供 suggest/draft/publish，不静默公开文章。

## 按需读取

先按模式读取对应章节，再按本次影响触发专项；不要预先打开所有 references、角色或模板。涉及下列条件时，对应文件是执行入口，不是可略过的推荐阅读。

| 当前任务或条件 | 读取内容 |
|---|---|
| 新需求、完整产品流程、目标不清 | [阶段工作流](references/agent-workflow.md)，再读[角色目录](references/role-catalog.md)中本阶段职责 |
| implementation-loop / full-auto 的研发阶段 | [实施工作流](references/implementation-workflow.md)，变更影响按[对应角色](references/role-catalog.md#6-变更影响-agent)核对 |
| bugfix-fast-path | [Bug 快速路径](references/implementation-workflow.md#bug-快速路径)；涉及认证再读认证专项 |
| validation-only | 只读取被验证领域的对应参考，输出验证/风险，不进入编码 |
| architecture-review、API 分层、身份或数据所有权 | [架构职责](references/role-catalog.md#5-架构-agent)与[架构文档质量](references/document-standard.md#质量要求) |
| 产出或整理产品/技术文档 | [文档标准及模板索引](references/document-standard.md)，只打开对应模板 |
| 设计或审查测试策略、用例、报告 | [测试指导](references/testing-guidance.md)，认证测试同时读下一行 |
| 登录、验证码、OAuth、绑定/解绑、token、持久化或认证故障 | [认证 E2E 与运行时前置排查](references/auth-login-e2e.md)；身份 owner 仍遵守架构职责 |
| 跨服务联调、改动影响客户端或明确要求客户端联调 | [联调范围、运行时、设备与功能页验收](references/client-integration.md) |
| B 类页面设计、实现、review 或验收 | [运营页面设计、批量确认、本地 mock 与预发](references/b-side-ui-guidance.md) |
| AI、生成、批量昂贵产物 | [成本分层](references/agent-workflow.md#ai生成成本)，涉及运营页面再读 B 类专项 |
| 非平凡实现、开源选型或组件复用 | [开源技术栈与可复用 Skills](references/open-source-stack.md) |
| release-gated、共享环境部署、回滚或发布核销 | [发布完整性](references/release-integrity.md)和[Code/Release PR 生命周期](references/release-pr-lifecycle.md)，两者都需读取 |
| 创建或主动重写 PR | [PR 创建语言](references/release-pr-lifecycle.md#pr-创建语言)；发布 PR 同时执行完整发布指引 |
| 获准使用可执行 subagent | [编排准则](references/subagent-orchestration.md)、对应 `agents/<role>-agent.md` 和任务包/结果模板 |
| post-release-content | [内容生产](references/post-release-content.md)与[Content Agent](agents/content-agent.md) |

角色文件用于职责与 prompt spec，不会自动运行；完整概念角色见目录，执行提示见 `agents/`。需要实现前后端时按实际角色选择，不把角色目录作为每次任务的必读整包。

## 部署平台选择

平台服从用户与项目事实源，支持 Vercel、Cloudflare 和已有环境，预发不默认限定 Vercel。

- Cloudflare（含 cloudfare 拼写）：读[部署与迁移](references/cloudflare-deployment.md)。静态站按情况选 Pages / Workers Static Assets；API、认证、邮件、AI 等后端再读[原生 Workers 服务端迁移](references/cloudflare-native-workers.md)。原来按请求运行的服务先验证原生 Workers，不默认改成常驻容器；数据库迁移单独决策。
- Vercel：明确选择 Vercel 的前端使用可用的 `deploy-to-vercel` / `vercel-deploy` skill，不覆盖用户的平台选择。
- 只迁前端时保留原后端、认证、数据库和客户端发布范围；任何共享环境发布仍执行上表发布指引。

## 最终回复格式

只返回：

- 模式
- 新增或更新的产物路径
- 关键决策
- 阻塞项
- 下一步动作

不要把长文档直接粘贴在聊天里。
