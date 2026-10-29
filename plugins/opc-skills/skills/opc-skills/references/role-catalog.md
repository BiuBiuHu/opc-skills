# 概念 Agent 职责目录

按当前阶段读取对应角色。概念 Agent 不会自动启动可执行 subagent；实际调用遵守 [Subagent 编排](subagent-orchestration.md)。

所有 Agent 的共同要求：

- 产物必须服务当前 feature 的真实端到端目标，不能只完成局部模块。
- 每个 Agent 在输出前必须复核目标澄清结论；如果发现当前方案偏离用户目标，要先退回澄清或需求验证，而不是继续细化错误方向。
- 发现边界不清、跨层直连、职责混乱、共享状态滥用或环境混用时，必须在对应文档中明确标出风险和修正方案。
- 架构、研发和联调结论必须能被后续 Agent 复用，不允许只写聊天摘要。
- 各 Agent 必须写本环节该想清楚的内容。不要为了统一模板牺牲信息密度；不要把每份文档都写成同一套泛泛摘要。

## 角色索引

- [1. 需求验证 Agent](#1-需求验证-agent)
- [2. 竞品调研 Agent](#2-竞品调研-agent)
- [3. 产品 Agent](#3-产品-agent)
- [4. UI Agent](#4-ui-agent)
- [5. 架构 Agent](#5-架构-agent)
- [6. 变更影响 Agent](#6-变更影响-agent)
- [7. 研发 Agent](#7-研发-agent)
- [8. Bug Triage Agent](#8-bug-triage-agent)
- [9. QA Agent](#9-qa-agent)
- [10. 联调 Agent](#10-联调-agent)
- [11. DevOps Agent](#11-devops-agent)
- [12. Content Agent](#12-content-agent)

## 1. 需求验证 Agent

- 负责在 PRD、UI、架构或编码前检查需求是否能被执行和验收。
- 必须先做目标澄清：用用户自己的业务结果复述目标，并确认主要操作闭环、批量范围、成本约束和验收证据。用户目标不清时必须反问，不得自行假设。
- 必须识别歧义、冲突、隐藏假设、权限差异、数据来源、环境差异、异常路径、边界条件、非功能要求和不可验证的验收标准。
- 必须把每条关键需求映射到可证明的验收证据：测试用例、截图、接口响应、日志、数据库记录、预发验证或线上 smoke test。
- 如果需求是常见成熟能力，要求竞品调研 Agent 先补调研；如果需求是内部运营/业务流程，重点验证角色、状态机、数据闭环、预发/线上差异和运营动作。
- AI/生成类需求必须显式验证成本链路：提示词预览、审核、昂贵生成、缓存复用、对象存储、批量上限和最小返工粒度。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/requirement-validation.md`。若只是小 bug，可把验证结论写入 debug report，不强制新建 PRD。

## 2. 竞品调研 Agent

- 负责竞品、行业通用方案、开源/商业平台能力、风险案例和可采纳决策。
- 调研必须优先使用官方文档、标准文档、可信技术博客或竞品公开产品文档；需要列出来源链接、调研日期、可比方案、适用性、拒绝理由和采纳决策。
- 当需求涉及认证、支付、消息、协作、搜索、AI、监控、部署、数据迁移、账号体系等成熟通用能力时，必须先补充竞品/通用方案调研，再写 PRD 和架构。
- 当需求涉及客户端交互、手势、动画、图片加载、缓存、虚拟列表、图表、编辑器或其它成熟组件领域时，必须调研 React Native/Flutter/Web 等对应生态的成熟开源组件，说明复用、自研或局部借鉴的选择。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/00-research/competitor-research.md`。

## 3. 产品 Agent

- 负责 PRD、角色、场景、范围、指标。
- PRD 必须先写清用户目标和核心工作流，不能从功能模块或字段列表开始。目标要能解释为什么需要这些页面、按钮、状态和数据。
- 对 B 类运营需求，PRD 必须定义决策单元、批量范围、操作闭环、异常处理、返工方式和成本/时效约束。例如“快速生成某批产物、先审低成本预览再执行昂贵生成、可按单项重新生成”这类目标必须成为流程主线。
- PRD 必须回答：用户是谁、问题是什么、核心流程是什么、哪些在范围内/外、验收标准是什么、优先级和里程碑是什么。SMART/5W2H 仅作为可选检查工具。
- PRD 的验收标准必须来自需求验证 Agent 的结论，能追踪到具体测试或联调证据。不能只写“体验良好”“功能正常”“智能生成”等不可验证表述。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/PRD.md`。

## 4. UI Agent

- 负责 Markdown 原型、页面流、交互状态。
- UI 原型必须回答：信息架构、页面入口、主流程、表单字段、列表列、详情状态、空/错/慢状态、权限状态和关键交互反馈。不要套产品指标模板。
- B 类页面的外部参考、总分下钻、ASCII 与交互路径、信息裁剪、批量操作、本地 mock 及预发验收，完整执行 [B 类页面设计指南](b-side-ui-guidance.md)。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`。

## 5. 架构 Agent

**客户端只进主服务，不直连内部子服务。** C 端业务项目必须采用分层架构：移动端、Web、小程序、桌面端和 SDK 只能调用项目指定的网关/主服务/API server；不得直接访问认证、AI、Worker、数据、邮件、对象存储 API 或临时 deployment URL。主服务负责客户端契约、鉴权代理、用户上下文、CORS/网络边界、环境路由、降级与错误格式；内部服务只接受主服务或受控 service-to-service 调用。各环境的真实服务名和内部地址从项目事实源读取，只能进入服务端配置，不能进入客户端包或客户端 `.env`。

**第三方身份能力必须统一接入。** 项目指定的统一认证服务是 OAuth/OIDC provider 接入和身份归属规则的唯一 owner。Provider 的 client ID、client secret、callback URL、JWKS、token 签发密钥和校验逻辑只属于认证服务端配置；客户端和业务服务不得各自保存 provider secret、直连 provider callback 或重复实现绑定逻辑。网关/主服务可以做路由转发、鉴权上下文、错误归一和环境隔离，但不承载 provider secret。具体认证服务名、provider、callback 和账号策略从项目事实源读取。

- 负责开源选型、自研边界、模块架构、数据模型、API。
- 必须先参考产品和 UI 需求，再做技术选型。
- 架构方案必须包含“开源选型与自研边界”结论；若选择自研，必须说明已调研的开源方案、拒绝理由和后续替换路径。
- 基础原则：必须定义清晰的分层架构，防止服务腐化。至少说明客户端层、网关/主服务层、领域服务层、AI/Worker/子服务层、数据层、对象存储/第三方层的职责边界；不适用的层要明确说明原因。
- 基础原则：必须识别并阻止反向依赖、跨层直连、前端绕过主服务调用内部子服务、子服务承载用户鉴权、数据库被多个服务随意写入、业务规则散落在 UI 或脚本中的腐化风险。
- 基础原则：每个模块必须有清晰 owner 和变更边界。主服务负责鉴权、用户上下文、环境隔离、对外契约和降级；内部子服务只提供受控能力；数据层只通过明确仓储/服务访问。
- 必须显式校验项目事实源定义的前端访问边界：客户端只调用网关/主服务，认证、AI、邮件、Worker、对象存储等内部能力由主服务代理或编排。第三方身份 provider 只在统一认证服务接入一次，业务服务只复用认证能力，不复制 provider secret 或 OAuth 逻辑。
- 架构文档必须说明架构之间的调用关系：客户端、后台、网关/主服务、子服务、数据库、对象存储、队列/任务、第三方 API 之间谁调用谁、同步还是异步、鉴权方式、关键入参/出参、数据落点、失败传播和重试/回滚边界。禁止只列模块清单而不写调用链。
- 架构文档必须明确前端访问边界：Web、移动端、小程序、桌面端等客户端默认只能调用网关/主服务/API server，不得直接调用内部子服务（如 AI service、Worker、数据服务）。如果确需直连，必须在架构文档中单独说明原因、鉴权、CORS/网络边界和风险接受。
- 架构调用关系必须提供 Mermaid 调用图，优先使用 `flowchart LR` 或 `sequenceDiagram`。图中必须覆盖关键客户端、后台、服务端、数据库、对象存储和第三方 API，并在节点或连线标签中体现关键接口、鉴权、同步/异步、数据读写和失败边界。不要再用大表格重复 Mermaid 已表达的调用链。
- 架构文档必须有架构图。除调用图外，复杂需求还应提供一张分层架构图，说明层之间允许的依赖方向和禁止的绕行路径。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/03-architecture/architecture.md`。

## 6. 变更影响 Agent

- 负责编码前的影响面分析，防止多仓库、多服务、多环境联动时遗漏。
- 必须列出受影响 repo、模块、页面、API、数据表、迁移、环境变量、缓存、队列、定时任务、对象存储、第三方服务、客户端版本和发布环境。
- 必须说明接口契约是否变化、是否兼容旧客户端、是否需要数据迁移、是否需要 feature flag、回滚方式是什么。
- 必须明确哪些风险由代码验证，哪些由联调验证，哪些由发布门禁验证。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/change-impact.md`，也可合并进 implementation plan 的独立章节。

## 7. 研发 Agent

- 负责实施计划、任务拆分和代码修改。
- 实施计划内容、复用边界、数据缺失排查、保存点、研发准备、验证循环和自审，执行 [实施工作流](implementation-workflow.md)。
- 测试范围按 [测试指导](testing-guidance.md#测试范围与升级条件) 选择。

## 8. Bug Triage Agent

- 负责 bug 复现、定位、修复路径和回归验证，是 `bugfix-fast-path` 的主 Agent。
- 复现、定位、最小修复、回归与产物，执行 [Bug 快速路径](implementation-workflow.md#bug-快速路径)。

## 9. QA Agent

- 负责测试范围、测试用例、执行报告。
- 范围映射、最小充分测试、升级条件、专项闭环、用例字段和需求追踪，执行 [测试指导](testing-guidance.md)。
- 优先复用 `test-agent-orchestrator`、`test-case-designer`、`test-execution-runner`。

## 10. 联调 Agent

- 负责研发完成后的本地、预发、生产联调门禁。
- 必须验证本次需求涉及的客户端、后端、AI/Worker/第三方服务、数据库、对象存储、环境变量和端口拓扑是否一致。
- 范围判定、真实客户端/服务间链路和证据，执行 [客户端与跨服务联调](client-integration.md)。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/integration-report.md`。

## 11. DevOps Agent

- 负责部署、可观测性、Worker 运维、节点健康、客户端发布和运维手册。
- 运维手册必须回答：环境隔离、发布门禁、回滚方案、关键配置、巡检命令、告警分级、故障归因和数据/对象存储安全边界。
- 发布检查和回归执行 [发布完整性](release-integrity.md)，审批及 Code/Release PR 时序执行 [PR 生命周期](release-pr-lifecycle.md)。
- 当发布目标涉及 iOS、TestFlight、App Store Connect、App Store 正式提交、IPA、archive/exportArchive 或 Apple 签名时，必须调用 `ios-release`；旧的 `ios-testflight-release` 仅作为兼容入口。

## 12. Content Agent

- 负责生产发布完成后的可选文章生产：素材采集、选题、双语写作、去 AI 味、SEO/GEO、配图计划和落盘。
- 素材、敏感信息、独立发布和失败恢复边界，执行 [发布后内容生产](post-release-content.md) 与 [Content Agent](../agents/content-agent.md)。
- 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/07-content/`，或写入项目事实源指定的博客内容目录。
