---
name: opc-skills
description: 用于规划、设计、研发、测试、部署和运维 OPC/监测类平台。该 Skill 将产品、UI、架构、研发、QA、DevOps Agent 与项目内 Skills 串联成一键启动的研发工作流，适用于当前工作区内的具体项目。
---

# OPC Skills

这是 OPC/监测类平台项目的统一研发入口。使用时必须先识别本次用户指定或当前正在处理的项目根目录。

## 触发方式

当用户说出以下意图时，使用本工作流：

- `启动 OPC Skills`
- `启动监测平台研发流程`
- `一键启动 OPC 研发`
- `跑一遍监测平台全流程`
- 要求规划、设计、开发、测试、部署或运维 OPC/监测类平台
- 当本次需求明确涉及客户端应用时，要求对 OPC 平台做客户端联调、前后端联调、移动端联调、App 联调、真机或模拟器验证

## 核心规则

**先保存代码，再改代码。** 任何进入新一轮实现、重构、迁移、部署或批量修改前，必须先为当前工作区建立明确保存点。优先使用 Git commit；如果暂时不能提交，必须说明原因，并使用 stash、补丁文件或其它可回滚备份方式保存当前状态。禁止在未保存当前成果的情况下继续叠加新改动。

**目标澄清不可跳过。** 在 PRD、UI、架构、编码或部署前，必须先对齐用户真正想完成的业务结果，而不是只复述功能点。若目标、角色、操作闭环、时间范围、成本约束或验收方式不清楚，必须先用少量关键问题反问用户，直到双方对目标达成一致。目标澄清至少要回答：谁在什么场景下完成什么结果；核心工作单元是什么；一次操作面向单条、某天、某周、某月还是批量；成功标准是什么；哪些成本、时延、质量和环境约束不能突破；失败后如何重试、回滚或返工。未完成目标澄清时，不得把字段清单、接口清单或页面草图当成需求。

**AI/生成类需求必须成本分层。** 当需求涉及 LLM、生图、视频、批量生成、投放或审核时，必须先拆成低成本可审阶段和高成本执行阶段。默认顺序是：生成/预览提示词或计划 -> 人工或规则审核 -> 批量生成昂贵产物 -> 缓存/对象存储复用 -> 按最小粒度返工。不得默认每次查看、刷新、重新发布或客户端加载都重新生成昂贵产物。文档和 UI 必须明确缓存键、对象存储位置、幂等策略、单日/单条重生、批量生成上限和成本保护。

**B 类运营页面以效率为第一目标。** 管理后台、审核台、运营台、批量生成台等 B 类页面必须服务高效判断和高效操作，而不是展示数据库字段。B 类页面默认做减法：当前判断、比较、批量选择和下一步操作不需要的内容，不要展示；已由筛选条件、页面上下文或批量任务确定的信息，不要在每行重复展示；低频审计信息、原始 JSON、完整长文本、完整提示词、调试日志和说明性文案不得常驻在主流程里，必须收进抽屉、弹窗、hover、展开行或日志页。表格只保留决策字段和行动字段；图片、状态、异常、成本和进度应直接视觉化；hover/点击用于查看大图或长内容；详情抽屉只承载完整提示词、原始 JSON、错误日志等低频信息。长列表必须有分页、每页条数、总数、排序/筛选状态和加载/空/错态；数据量大或行高固定时必须评估服务端分页/排序/筛选或虚拟滚动。空值必须是可行动异常，例如“缺图片”“缺提示词”“未透传 contentSnapshot”，不能只显示 `-`。需要详细检查清单时读取 `references/b-side-ui-guidance.md`。

**B 类页面必须先用本地 mock 跑通交互，再部署 Vercel 预发。** 管理后台、运营台、审核台、批量生成台等 B 类页面在接真实预发环境前，必须先用本地 mock 数据或 Playwright route mock/MSW/dev fixture 做交互闭环。mock 数据要覆盖成功、空、慢、错、长文案、缺字段、多状态、批量范围和单条返工；验证目标不是“组件能渲染”，而是操作者能在一个连续工作流中高效完成任务：上下文不丢、下一步动作清楚、P0 决策信息不被藏进详情、行内可视对象可直接判断、昂贵操作不会被误触发。mock 验证失败时禁止部署到 Vercel；mock 验证通过后，必须提交代码，再部署预发，并用真实 API/数据库/对象存储复跑同一关键路径。mock 证据和预发证据都要写入测试报告。

**发布必须先预发、再线上，并且必须有测试报告和 Code Review。** 任何生产发布前必须完成以下门禁，缺一不可：

- 发布目标确认门禁：当用户只说“发布”“部署”“上线”“发一下”等，没有明确说明目标环境时，必须先停下来询问“发布到预发还是线上？”。禁止自行默认预发、默认线上或同时发布两个环境。只有用户明确指定目标环境后，才能执行对应部署流程。
- 禁止本地工作区直接部署：不支持、也不得执行“从未提交本地工作区直接打包部署”。无论预发还是线上，部署输入必须来自可追踪的 Git commit、PR/CR 分支、CI 构建产物或明确归档的构建包。工作区存在未提交改动时，必须先停止部署，要求完成 commit/CR 或选择明确的回滚/暂存策略。禁止用 `vercel deploy`、手动上传、压缩包等方式把未提交代码直接发布到任何共享环境。
- 代码保存门禁：发布前相关改动必须已经 commit，并能通过 commit hash、分支名、PR/CR 或构建产物追溯。若用户要求紧急修复，也必须先创建 hotfix 分支并提交，再按预发验证、CR/审批、生产发布执行；不得“先线上发布后补提交”。
- 预发门禁：必须先部署到预发环境，且确认预发项目、预发域名、预发 API、预发数据库/schema、预发下游服务没有混用生产环境。
- 测试报告门禁：预发通过后，必须产出或更新测试报告，记录测试环境、账号、版本/deployment、用例、命令、结果、失败项和证据路径。报告建议写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-report.md`；若项目已有固定测试报告路径，沿用项目路径。
- Code Review 门禁：生产发布前必须发起 CR/PR 或生成 code review 记录，说明变更范围、风险点、验证结果、回滚方案和 reviewer/审批状态。记录建议写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/code-review.md`；若使用 GitHub/GitLab PR，最终回复必须给出 PR/CR 链接。
- 线上发布门禁：只有预发验证通过、测试报告完成、CR/PR 已创建或已审核后，才能部署生产。生产部署后必须做线上 smoke test，并把生产 deployment、线上域名、验证结果和残留风险补回测试报告或运维记录。
- 环境隔离门禁：所有部署命令必须明确目标环境和目标项目。禁止在未确认 Vercel/云项目 link、deployment target、环境变量、数据库 host/schema 的情况下执行发布。预发与线上部署记录必须分别列出，不得用同一条结果混写。

**零散想法先进入 Inbox，不直接开发。** 当用户说“先记下来”“后面再开发”或临时给出产品想法时，只记录到轻量草稿清单，不启动正式 PRD/架构/编码流程。当前任务完成后，再回看 Inbox：评估清单事项与当前工作、已提交代码和已完成任务的相关性；选择一个任务；然后按 OPC Skills 正式研发流程执行，包括开新分支、编写技术方案和测试方案、实施、端到端联调和测试用例。

**功能页证据闭环，不用间接证据替代验收。** 当本次改动涉及 UI、交互、客户端页面、移动端 Tab、Web 路由、弹窗、列表、表单、布局、图片、图表或可视状态时，完成标准必须包含“进入被改功能的真实页面并验证”。禁止用以下证据替代功能验收：仅类型检查通过、仅构建成功、仅安装成功、仅应用启动成功、停留在默认首页截图、停留在错误 Tab 截图、只看运行日志没有看页面、只验证相邻页面或抽象组件。改了哪个页面或交互，就必须导航到那个页面或交互状态；如果用户给了截图指出问题，必须在同一页面、同一状态、同类设备视口下截图对比。截图或运行时快照发现未修复时，必须继续修复，不得报告完成。

**验证码登录必须自动化闭环。** 当发布或修复涉及邮箱验证码登录、注册、OAuth 回跳后的 token 交换、登录态持久化或客户端登录入口时，发布前必须在真实客户端环境完成自动化端到端测试。移动端必须优先使用 iOS Simulator 或 Android Emulator 自动操作登录页，向项目约定测试邮箱（例如 `test@example.com`）发送验证码；验证码可从受控服务端日志、数据库中的验证码 hash、邮件服务日志或测试后门中取得，不得以“无法登录邮箱”为理由跳过验证。测试必须覆盖：发送验证码、冷却/Loading、输入正确验证码、verify、token exchange、userinfo/current user、进入登录后首页；失败时必须定位到客户端、网关、身份服务、数据库或第三方服务的具体层级，并修复后复验。只验证 curl、只看接口 2xx、只上传 TestFlight、只检查包内容，都不能替代客户端验证码登录闭环。

**客户端只进主服务，不直连内部子服务。** OPC/监测类项目必须采用分层架构：客户端层只能调用网关/主服务/API server。移动端、Web、小程序、桌面端和 SDK 默认只能调用 `main-api-service`；不得直接访问 `identity-service`、AI service、Worker、数据服务、邮件服务、对象存储 API 或任何生成的 preview/deployment URL。`main-api-service` 负责客户端契约、鉴权代理、用户上下文、CORS/网络边界、环境路由、降级与错误格式；内部服务只接受主服务或受控 service-to-service 调用。身份服务的环境命名应使用公开示例占位，例如 `staging-identity-service` 和 `identity-service`；这些内部地址只能出现在服务端配置中，不能出现在客户端包或客户端 `.env` 中。

**身份服务是统一身份中台。** 第三方身份能力必须在 `identity-service` 统一接入一次，业务侧通过 `main-api-service` 复用。Apple、GitHub、Google、Facebook 等 provider 的 client ID、client secret、callback URL、JWKS、token 签发密钥和 provider 校验逻辑只属于 `identity-service` 服务端配置；客户端和业务服务不得各自保存 provider secret、直连 provider callback 或重复实现 OAuth/provider 绑定逻辑。`main-api-service` 可以做路由转发、鉴权上下文、错误归一和环境隔离，但不承载 provider secret。

所有方案、架构决策、UI 原型、测试计划、评审结论都必须落盘到：

```text
<PROJECT_ROOT>/docs/<FEATURE_NAME>/
```

不要只把产品或技术决策留在聊天记录里。

`<PROJECT_ROOT>` 的判定规则：

- 如果用户明确指定项目目录，例如 `example-monitoring-platform`、`risk-review-console`，则以该目录为项目根目录。
- 如果用户没有指定项目目录，则以当前工作目录中最匹配本次任务的项目目录为项目根目录。
- 如果当前工作目录本身就是项目根目录，则直接使用当前目录。
- 不允许把文档写死到某个固定项目名下面；最终回复必须列出实际写入路径。

`<FEATURE_NAME>` 的判定规则：

- 每次新需求必须先定义一个稳定、可读、英文 kebab-case 的 feature name，例如 `evidence-review-workflow`。
- 如果用户明确给出 feature name，则使用用户给出的名称。
- 如果用户没有给出，Agent 必须根据需求内容自行命名，并在开始写文档前声明。
- 同一需求的 PRD、UI 原型、技术架构、实施计划、Backlog、测试策略、运维手册都必须写到同一个 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/` 目录下。
- 不允许把本次需求文档分散写入多个 feature 目录。

产品和技术文档必须遵守以下规则：

- 每类文档只保留一份主文档，不保留多份互相竞争的 PRD、架构方案或 UI 原型。
- 后续变化在主文档内部做版本化迭代。
- 每个版本必须说明：改了什么、为什么改、替代了哪个旧决策、影响是什么。
- 不再要求所有文档机械套用 SMART 和 5W2H。产品 PRD 可以用 SMART/5W2H 做快速校验；架构、UI、研发、测试、运维文档必须优先写清本环节真正需要的判断、边界、方案、证据和风险。
- 如果使用 SMART/5W2H，只能作为辅助检查，不能替代正文。禁止为了填模板写空泛表格。
- 旧文档只有在内容合并完成后才归档或删除。
- 每个主文档都必须优先基于 `templates/` 目录中的对应模板创建或更新。
- 文档生成或更新完成后，必须进入 `awaiting-user-review` 状态，等待用户审核。
- 用户审核通过前，不允许开始代码实现、数据库迁移、部署、删除、归档或破坏性清理。
- 只有用户明确说出“审核通过”“开始编码”“开始实施”“执行迁移”“部署”等批准语义，才能进入对应执行阶段。

## 工作模式

- `manual-gated`：默认模式。先产出文档和计划，文档完成后停在 `awaiting-user-review`，实施、迁移、部署、删除前等待用户确认。
- `full-auto`：仅当用户明确说 `全自动`、`full-auto`、`不需要确认` 时启用；但如果用户已要求“文档审核后才能编码”，则本次 feature 必须遵守审核关卡。
- `implementation-loop`：当需求、架构和验收标准已经明确，且用户要求“开始编码”“往下推进”“实现一下”时启用。跳过不必要的重新调研，但必须先做项目发现、变更影响分析、保存点、实现、验证、修复、复验和证据记录。
- `bugfix-fast-path`：当用户描述线上/预发/本地 bug、截图问题、报错、性能卡顿、交互异常或回归问题时启用。只要求完成复现、定位、修复、回归和证据闭环；除非 bug 暴露出产品或架构缺口，否则不强制补全完整 PRD/UI/架构流程。
- `validation-only`：当用户要求“验证一下”“review 需求”“看看能不能做”“只检查不改代码”时启用。只输出需求验证、实现验证或风险清单，不进入编码。
- `release-gated`：当用户要求预发、线上、发布、回滚、灰度、TestFlight 或运维检查时启用。只处理发布门禁、环境隔离、验证报告、回滚和线上 smoke test，不夹带无关功能开发。
- `architecture-review`：当用户要求检查架构、调用关系、分层、服务腐化或 Agent 产物质量时启用。重点审查依赖方向、服务边界、数据所有权、调用图和防腐化规则。

## Agent 角色

本工作流使用以下概念 Agent。只有当用户明确要求并行 Agent 工作时，才真正调用子 Agent。

所有 Agent 的共同要求：

- 产物必须服务当前 feature 的真实端到端目标，不能只完成局部模块。
- 每个 Agent 在输出前必须复核目标澄清结论；如果发现当前方案偏离用户目标，要先退回澄清或需求验证，而不是继续细化错误方向。
- 发现边界不清、跨层直连、职责混乱、共享状态滥用或环境混用时，必须在对应文档中明确标出风险和修正方案。
- 架构、研发和联调结论必须能被后续 Agent 复用，不允许只写聊天摘要。
- 各 Agent 必须写本环节该想清楚的内容。不要为了统一模板牺牲信息密度；不要把每份文档都写成同一套泛泛摘要。

1. 需求验证 Agent
   - 负责在 PRD、UI、架构或编码前检查需求是否能被执行和验收。
   - 必须先做目标澄清：用用户自己的业务结果复述目标，并确认主要操作闭环、批量范围、成本约束和验收证据。用户目标不清时必须反问，不得自行假设。
   - 必须识别歧义、冲突、隐藏假设、权限差异、数据来源、环境差异、异常路径、边界条件、非功能要求和不可验证的验收标准。
   - 必须把每条关键需求映射到可证明的验收证据：测试用例、截图、接口响应、日志、数据库记录、预发验证或线上 smoke test。
   - 如果需求是常见成熟能力，要求竞品调研 Agent 先补调研；如果需求是内部运营/业务流程，重点验证角色、状态机、数据闭环、预发/线上差异和运营动作。
   - AI/生成类需求必须显式验证成本链路：提示词预览、审核、昂贵生成、缓存复用、对象存储、批量上限和最小返工粒度。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/requirement-validation.md`。若只是小 bug，可把验证结论写入 debug report，不强制新建 PRD。

2. 竞品调研 Agent
   - 负责竞品、行业通用方案、开源/商业平台能力、风险案例和可采纳决策。
   - 调研必须优先使用官方文档、标准文档、可信技术博客或竞品公开产品文档；需要列出来源链接、调研日期、可比方案、适用性、拒绝理由和采纳决策。
   - 当需求涉及认证、支付、消息、协作、搜索、AI、监控、部署、数据迁移、账号体系等成熟通用能力时，必须先补充竞品/通用方案调研，再写 PRD 和架构。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/00-research/competitor-research.md`。

3. 产品 Agent
   - 负责 PRD、角色、场景、范围、指标。
   - PRD 必须先写清用户目标和核心工作流，不能从功能模块或字段列表开始。目标要能解释为什么需要这些页面、按钮、状态和数据。
   - 对 B 类运营需求，PRD 必须定义决策单元、批量范围、操作闭环、异常处理、返工方式和成本/时效约束。例如“快速生成某周/月的日历集、先审提示词再生成图片、可按某一天重新生成”这类目标必须成为流程主线。
   - PRD 必须回答：用户是谁、问题是什么、核心流程是什么、哪些在范围内/外、验收标准是什么、优先级和里程碑是什么。SMART/5W2H 仅作为可选检查工具。
   - PRD 的验收标准必须来自需求验证 Agent 的结论，能追踪到具体测试或联调证据。不能只写“体验良好”“功能正常”“智能生成”等不可验证表述。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/01-product/PRD.md`。

4. UI Agent
   - 负责 Markdown 原型、页面流、交互状态。
   - UI 原型必须先声明页面类型和效率目标。B 类运营页面默认采用“筛选上下文 + 高密度决策表 + 批量操作 + 详情抽屉”的信息结构；只有明确理由时才采用卡片流或展示型布局。
   - 对 B 类页面，禁止把 P0/P1 决策字段藏进详情。也禁止把非决策必需内容常驻展示：已筛选出来的上下文字段不要重复占列表列；完整提示词、原始 JSON、日志、长说明和低频审计字段默认进入抽屉、hover、展开行或独立详情页。图片等可视判断对象应直接出现在行内，支持 hover/点击大图；操作列固定在右侧；异常和缺字段要直接暴露。长列表原型必须包含分页/总数/每页条数；需要跨页选择或批量操作时必须说明选择保持、批量工具条、清空选择和失败回显。
   - 对 B 类交互，UI 原型必须包含本地 mock 验证场景：典型数据、空态、错误态、长内容、多状态、批量范围、单条返工和昂贵操作确认。原型要说明哪些状态在本地 mock 先验收，哪些状态必须到 Vercel 预发用真实接口复验。
   - UI 原型必须回答：信息架构、页面入口、主流程、表单字段、列表列、详情状态、空/错/慢状态、权限状态和关键交互反馈。不要套产品指标模板。
   - 需要时复用 `ui-ux-pro-max`。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`。

5. 架构 Agent
   - 负责开源选型、自研边界、模块架构、数据模型、API。
   - 必须先参考产品和 UI 需求，再做技术选型。
   - 基础原则：必须定义清晰的分层架构，防止服务腐化。至少说明客户端层、网关/主服务层、领域服务层、AI/Worker/子服务层、数据层、对象存储/第三方层的职责边界；不适用的层要明确说明原因。
   - 基础原则：必须识别并阻止反向依赖、跨层直连、前端绕过主服务调用内部子服务、子服务承载用户鉴权、数据库被多个服务随意写入、业务规则散落在 UI 或脚本中的腐化风险。
   - 基础原则：每个模块必须有清晰 owner 和变更边界。主服务负责鉴权、用户上下文、环境隔离、对外契约和降级；内部子服务只提供受控能力；数据层只通过明确仓储/服务访问。
   - 项目特例必须显式校验：客户端只能调用 `main-api-service`；身份、AI、邮件、Worker、对象存储等能力必须由 `main-api-service` 代理或编排。身份服务可按环境命名为 `staging-identity-service` 和 `identity-service`。第三方身份 provider 只在 `identity-service` 统一接入一次，业务服务只复用中台能力，不复制 provider secret 或 OAuth 逻辑。
   - 架构文档必须说明架构之间的调用关系：客户端、后台、网关/主服务、子服务、数据库、对象存储、队列/任务、第三方 API 之间谁调用谁、同步还是异步、鉴权方式、关键入参/出参、数据落点、失败传播和重试/回滚边界。禁止只列模块清单而不写调用链。
   - 架构文档必须明确前端访问边界：Web、移动端、小程序、桌面端等客户端默认只能调用网关/主服务/API server，不得直接调用内部子服务（如 AI service、Worker、数据服务）。如果确需直连，必须在架构文档中单独说明原因、鉴权、CORS/网络边界和风险接受。
   - 架构调用关系必须提供 Mermaid 调用图，优先使用 `flowchart LR` 或 `sequenceDiagram`。图中必须覆盖关键客户端、后台、服务端、数据库、对象存储和第三方 API，并在节点或连线标签中体现关键接口、鉴权、同步/异步、数据读写和失败边界。不要再用大表格重复 Mermaid 已表达的调用链。
   - 架构文档必须有架构图。除调用图外，复杂需求还应提供一张分层架构图，说明层之间允许的依赖方向和禁止的绕行路径。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/03-architecture/architecture.md`。

6. 变更影响 Agent
   - 负责编码前的影响面分析，防止多仓库、多服务、多环境联动时遗漏。
   - 必须列出受影响 repo、模块、页面、API、数据表、迁移、环境变量、缓存、队列、定时任务、对象存储、第三方服务、客户端版本和发布环境。
   - 必须说明接口契约是否变化、是否兼容旧客户端、是否需要数据迁移、是否需要 feature flag、回滚方式是什么。
   - 必须明确哪些风险由代码验证，哪些由联调验证，哪些由发布门禁验证。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/change-impact.md`，也可合并进 implementation plan 的独立章节。

7. 研发 Agent
   - 负责实施计划、任务拆分和代码修改。
   - 实施计划必须回答：改哪些仓库/模块/文件、迁移怎么做、接口契约怎么变、兼容策略、保存点、任务顺序、回滚点和每阶段退出条件。
   - 除非有明确理由，否则必须复用 `<PROJECT_ROOT>/` 中已有采集、爬虫、API、数据库和前端代码。
   - 当 UI 缺少关键数据时，必须先检查主服务/BFF/内部服务是否未透传字段，不能只在前端用占位符掩盖。AI/生成类实现必须保护昂贵操作，优先实现提示词预览、审核和缓存复用，再触发图片/视频等高成本生成。
   - B 类页面实现必须先建立本地 mock 验证入口。优先使用 Playwright route mock、MSW、dev fixture 或项目既有 mock 层构造稳定数据，不依赖真实预发数据边改边猜；mock 中必须包含正常、空、失败、长内容、缺字段、处理中和已完成状态。mock 验证通过前不得部署 Vercel。
   - 编码前必须完成项目发现：识别包管理器、启动命令、测试命令、lint/typecheck 命令、dev server、端口、环境变量样例、现有测试、当前分支和未提交改动。
   - 研发必须采用执行闭环：保存点 -> 小步修改 -> 运行最小验证 -> 读取失败 -> 修复 -> 复验 -> 更新证据。不能只改代码不验证，不能把构建通过当作功能通过。
   - 完成前必须做本地 diff 自审：检查无关改动、分层边界、权限/隐私、错误处理、性能风险、迁移安全、预发/线上配置差异和测试缺口。
   - 自动执行证据写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/evidence-manifest.md`；code review 自审写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/code-review.md`。

8. Bug Triage Agent
   - 负责 bug 复现、定位、修复路径和回归验证，是 `bugfix-fast-path` 的主 Agent。
   - 必须先记录：环境、版本/commit、账号/权限、操作步骤、期望结果、实际结果、截图/日志/API 响应、是否可稳定复现。
   - 必须定位归因层级：客户端、Web 前端、主服务/网关、内部子服务、数据库、缓存、对象存储、第三方、配置、发布环境或旧构建/缓存。
   - 能写自动化失败用例时，应先补失败测试；不能自动化时，必须写清人工复现步骤和最小证据。
   - 修复后必须验证原问题、相邻路径、回归风险和环境差异；UI/客户端 bug 必须进入真实功能页或同类设备状态截图验证。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/debug-report.md`。小 bug 可只产出 debug report、evidence manifest 和 test report。

9. QA Agent
   - 负责测试范围、测试用例、执行报告。
   - 测试文档必须回答：哪些行为要被证明、用什么证据证明、覆盖哪些失败路径、哪些环境要跑、哪些命令/截图/API 响应作为证据。不要只写测试类型清单。
   - QA 必须验证目标闭环，而不是只验证控件存在。B 类页面必须用截图或自动化断言证明：筛选上下文不冗余、关键决策字段列表可见、行内可视对象可直接判断、批量操作可用、单条返工可用、异常状态可行动。
   - B 类页面测试必须分两层：先本地 mock 交互验收，再预发真实链路验收。本地 mock 验收检查信息架构、状态流转、操作路径、错误/空/慢状态和昂贵操作保护；预发验收检查真实 API、数据库、对象存储、权限、环境隔离和缓存命中。两层证据缺一不可。
   - AI/生成类测试必须覆盖成本保护：提示词预览不触发昂贵生成，审核后才生成图片/视频，OSS/缓存命中不重复生成，按天/单条重生不会误触发整批重生。
   - 必须建立从需求到测试的追踪：每条 P0/P1 验收标准至少对应一个 test case 或联调证据；无法测试的验收标准必须退回需求验证 Agent 重写。
   - 测试文档必须按系统拆分说明怎么测：客户端、主服务/网关、领域/内部服务、数据层、第三方、运维/发布。没有涉及的系统要明确写“不适用”和原因。
   - 测试用例必须具备执行指导性。P0 case 必须写清 `id`、目标系统、优先级、前置数据、操作步骤、期望结果、不能发生的副作用、证据和自动化/人工方式。禁止只写“测试登录”“测试绑定”“测试接口正常”这类抽象条目。
   - 测试设计必须参考行业通用方法：风险驱动测试、需求到用例可追踪、等价类、边界值、决策表、状态迁移、错误猜测；认证/OAuth/API 类需求必须参考 OWASP ASVS 和 OAuth Security BCP 的安全验证思路。
   - 当需要编写或审查测试策略时，先读取 `references/testing-guidance.md`，并把适用规则落到 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-strategy.md`。
   - 优先复用 `test-agent-orchestrator`、`test-case-designer`、`test-execution-runner`。

10. 联调 Agent
   - 负责研发完成后的本地、预发、生产联调门禁。
   - 必须验证本次需求涉及的客户端、后端、AI/Worker/第三方服务、数据库、对象存储、环境变量和端口拓扑是否一致。
   - 只有当项目包含客户端应用且本次改动影响客户端，或用户明确要求客户端联调时，才启用客户端专项门禁。
   - 客户端包括 Web 控制台、移动端 App、桌面端或小程序；启用时必须按项目实际客户端类型选择联调路径。
   - 当客户端登录依赖邮箱验证码时，必须在模拟器/真机中自动完成至少一个测试邮箱的验证码登录闭环。验证码应从服务端可观测证据获取，例如 identity-service 对应环境数据库的验证码 hash 反查、受控日志或测试邮件平台；必须记录验证码来源、请求 URL、响应状态、登录后页面证据和失败层级。
   - 产物写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/integration-report.md`。

11. DevOps Agent
   - 负责部署、可观测性、Worker 运维、节点健康、客户端发布和运维手册。
   - 运维手册必须回答：环境隔离、发布门禁、回滚方案、关键配置、巡检命令、告警分级、故障归因和数据/对象存储安全边界。
   - 负责执行发布门禁：先预发部署，再预发测试报告，再 CR/PR 或 code review 记录，最后生产发布和线上 smoke test。
   - 生产发布前必须核对目标项目、域名、环境变量、数据库 host/schema、下游服务 URL 和回滚方案；发布后必须记录 deployment URL、固定域名、验证命令、验证账号、结果和残留风险。
   - 当发布目标涉及 iOS、TestFlight、App Store Connect、App Store 正式提交、IPA、archive/exportArchive 或 Apple 签名时，必须调用 `ios-release`；旧的 `ios-testflight-release` 仅作为兼容入口。

## 一键工作流

启动工作流后：

1. 识别并声明本次 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，然后读取当前项目材料：
   - `<PROJECT_ROOT>/README.md` 或项目说明文件
   - 当前 PRD
   - 当前 Markdown UI 原型
   - 当前技术架构
   - 当前开源选型与自研边界

2. 在新增内容前，先把同一 feature 下的散落文档合并到主文档：
   - PRD：`docs/01-product/PRD.md`
   - 需求验证：`docs/01-product/requirement-validation.md`
   - UI 原型：`docs/02-ui/markdown-prototype.md`
   - 技术架构：`docs/03-architecture/architecture.md`
   - 实施计划：`docs/04-engineering/implementation-plan.md`
   - 变更影响：`docs/04-engineering/change-impact.md`
   - 调试报告：`docs/04-engineering/debug-report.md`
   - 证据清单：`docs/04-engineering/evidence-manifest.md`
   - Backlog：`docs/04-engineering/backlog.md`
   - 测试策略：`docs/05-testing/test-strategy.md`
   - 运维手册：`docs/06-ops/ops-runbook.md`
   - 竞品调研：`docs/00-research/competitor-research.md`

3. 更新或产出以下文档：
   - `docs/<FEATURE_NAME>/00-research/competitor-research.md`
   - `docs/<FEATURE_NAME>/01-product/requirement-validation.md`
   - `docs/<FEATURE_NAME>/01-product/PRD.md`
   - `docs/<FEATURE_NAME>/02-ui/markdown-prototype.md`
   - `docs/<FEATURE_NAME>/03-architecture/architecture.md`
   - `docs/<FEATURE_NAME>/04-engineering/change-impact.md`
   - `docs/<FEATURE_NAME>/04-engineering/implementation-plan.md`
   - `docs/<FEATURE_NAME>/04-engineering/debug-report.md`
   - `docs/<FEATURE_NAME>/04-engineering/evidence-manifest.md`
   - `docs/<FEATURE_NAME>/04-engineering/code-review.md`
   - `docs/<FEATURE_NAME>/04-engineering/backlog.md`
   - `docs/<FEATURE_NAME>/05-testing/test-strategy.md`
   - `docs/<FEATURE_NAME>/05-testing/test-cases.json`
   - `docs/<FEATURE_NAME>/05-testing/integration-report.md`
   - `docs/<FEATURE_NAME>/06-ops/ops-runbook.md`

   生成或更新这些文档时，必须优先使用以下模板：
   - `templates/prd-template.md`
   - `templates/requirement-validation-template.md`
   - `templates/ui-prototype-template.md`
   - `templates/architecture-template.md`
   - `templates/change-impact-template.md`
   - `templates/implementation-plan-template.md`
   - `templates/debug-report-template.md`
   - `templates/evidence-manifest-template.md`
   - `templates/backlog-template.md`
   - `templates/test-strategy-template.md`
   - `templates/ops-runbook-template.md`

4. 编码前必须执行研发准备门禁，并把结论写入 `docs/<FEATURE_NAME>/04-engineering/implementation-plan.md`、`change-impact.md` 或 `debug-report.md`：
   - 目标澄清：确认用户目标、核心工作流、批量范围、成本约束、返工粒度和验收证据已写入需求验证或 PRD；未确认时先反问用户。
   - 需求可执行性：验收标准必须可测试、可截图、可接口验证或可日志/数据验证；不可验证的表述必须先改写。
   - 项目发现：识别相关 repo、包管理器、启动命令、测试命令、lint/typecheck 命令、dev server、端口、环境变量样例、当前分支、未提交改动和已有测试。
   - 保存点：确认当前代码已有 commit、stash、补丁或其它可回滚保存点。
   - 变更影响：列出受影响模块、API、数据、缓存、任务、环境、客户端版本、预发/线上配置和回滚路径。
   - 任务切分：每个任务必须有明确文件/模块范围、验证方式、退出条件和失败后处理动作。
   - 自动执行循环：每轮实现后必须运行最小验证；失败时先读错误和日志，再修复并复验；不能在失败未解释时继续叠加无关改动。
   - 证据清单：每次关键命令、页面截图、接口响应、日志、数据库检查、模拟器/浏览器验证都必须记录到 evidence manifest；未能执行的验证必须说明原因和风险。

5. 当启用 `bugfix-fast-path` 时，执行以下 bug 修复门禁：
   - 复现门禁：记录环境、版本/commit、账号/权限、操作步骤、期望结果、实际结果、截图/日志/API 响应和复现稳定性。
   - 定位门禁：明确归因层级，先排除旧包、缓存、错误环境、配置混用和服务未重启，再判断代码问题。
   - 最小修复门禁：只修改与 bug 相关的代码和测试；需要扩大范围时必须说明原因。
   - 回归门禁：验证原 bug、相邻路径、失败路径和预发/线上差异；客户端/UI bug 必须进入真实功能页或同类设备状态截图验证。
   - 根因记录：`debug-report.md` 必须写清根因、修复点、验证证据、未覆盖风险和后续建议。

6. 研发完成后必须执行本地自审门禁：
   - 查看 diff，确认没有无关文件、临时日志、密钥、调试开关、错误环境 URL 或生成产物误入。
   - 检查分层边界，尤其是客户端不得直连内部子服务，内部子服务不得承载用户登录态判断。
   - 检查错误处理、权限、隐私、性能、缓存、迁移安全和兼容性。
   - 检查需求验收标准是否已映射到测试报告、联调报告或 evidence manifest。
   - 自审结论写入 `docs/<FEATURE_NAME>/04-engineering/code-review.md`；正式 PR/CR 可引用该文件。

7. 研发完成后必须执行联调门禁，并把结果写入 `docs/<FEATURE_NAME>/05-testing/integration-report.md`。联调门禁至少包含：
   - 客户端范围判定：先判断本次需求是否涉及 Web 控制台、移动 App、桌面端、小程序或外部 SDK；若不涉及，报告中明确写“客户端专项门禁不适用”及原因。
   - 客户端能力矩阵：启用客户端专项门禁时，先列出客户端类型、运行方式、目标环境、关键用户路径、依赖 API、认证方式、缓存/离线/推送/深链等受影响能力。
   - 进程和端口拓扑：确认每个服务只保留一份有效进程，端口无冲突，客户端配置指向正确 API。
   - 环境变量：确认本地、预发、生产的服务 URL、API key、模型名、数据库连接、schema、CORS/ATS/网络安全配置完整且不交叉。
   - 客户端网关边界：确认客户端环境变量、运行时配置、网络日志和构建产物中没有内部子服务 URL 或生成的 Vercel deployment URL；客户端所有业务 API 都必须指向网关/主服务。
   - 数据库和迁移：确认目标数据库、schema、表、索引、幂等约束存在，写入路径不会污染其它环境。
   - service-to-service：验证客户端到主服务、主服务到 AI/Worker 服务、AI/Worker 到第三方 API 的链路。
   - 第三方 API：用最小请求验证路径、鉴权、模型/渠道、超时和错误格式，区分代码错误、配置错误、供应商不可用。
   - Web 客户端 smoke test：仅当本次需求涉及 Web 控制台时执行，验证关键页面能打开、登录态有效、主流程能触发、轮询/等待动画/错误态可见。
   - Web B 类页面 smoke test：必须先在本地 dev server 使用 mock 数据完成同一页面、同一状态、同一主流程的截图/断言验收；通过后再部署或检查 Vercel 预发，并用真实 API 复跑关键路径。不得用预发真实数据不可控作为跳过本地交互验证的理由。
   - 移动端客户端 smoke test：仅当本次需求涉及 React Native、Expo、iOS、Android、Flutter 或小程序客户端时执行，必须构建或启动对应客户端，验证 API baseURL、登录态、核心页面、主流程、加载态、错误态、缓存/离线队列和环境切换；iOS 优先使用模拟器构建安装验证，React Native/Expo 优先复用 `react-native-dev`，小程序优先复用对应小程序 skill。
   - 客户端契约验证：客户端专项门禁启用时，必须核对接口字段、错误码、分页/轮询/超时、鉴权刷新、schema 兼容和空/错/慢三类状态，避免只验证 happy path。
   - 客户端发布形态：仅在客户端专项门禁启用时执行，区分 Metro/dev server、Debug 包、Release 包、TestFlight/灰度包或生产包，确认用户看到的是最新构建而不是旧缓存。若发布或验证目标包含 iOS/TestFlight/App Store，使用 `ios-release` 执行签名、归档、导出、上传和 App Store Connect/TestFlight 配置检查。
   - 客户端证据：仅在客户端专项门禁启用时要求，联调报告必须记录客户端类型、运行方式、设备/浏览器、版本号或构建号、API 环境、验证命令、关键截图或日志路径。
   - 功能页截图验收：仅在客户端专项门禁启用且本次改动涉及 UI/交互时执行。必须先列出本次实际修改的页面、Tab、路由或弹窗，再逐一进入对应功能页截图或采集运行时 UI 快照。验收截图必须覆盖用户指出的问题状态，例如指定 Tab、指定日期、指定列表项、指定空态/错误态/加载态、指定表单字段或指定底部安全区。若截图不在目标功能页，或截图无法证明问题已修复，则该项为失败，必须继续修复。
   - 失败归因：每个失败项必须给出归因层级（前端、主服务、子服务、数据库、配置、第三方、沙箱/网络）和下一步处理动作。

8. 如果用户要求“发布”“上线”“部署线上”“准备发布”或类似生产发布意图，必须执行生产发布门禁：
   - 先确认目标环境：如果用户没有明确说预发、线上、production、prod、preview、staging 等目标环境，必须先询问用户，不得执行部署命令。
   - 确认代码保存状态：列出当前分支、commit、工作区是否干净。若存在未提交改动，必须停止发布并先要求提交、暂存或回滚；禁止从本地未提交工作区部署。
   - 确认 CR 状态：若尚未发 CR/PR，先创建或生成 code review 记录；未经用户明确授权，不得跳过。
   - 部署预发：明确预发项目、预发域名、预发 API、预发数据库/schema 和预发下游服务；部署完成后记录 deployment URL。
   - 执行预发测试：至少覆盖本次变更涉及的核心路径、失败路径和环境隔离检查；输出 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-report.md` 或项目既有测试报告。
   - 评审测试结果：若测试报告存在失败项，必须先修复或由用户明确接受风险；不得把失败报告当作发布通过。
   - 部署生产：明确生产项目、生产域名、生产 API、生产数据库/schema 和生产下游服务；部署完成后记录 deployment URL。
   - 线上 smoke test：验证线上关键页面/API/后台任务可用；若生产发布包含数据库迁移，必须记录迁移命令、目标 host/schema、迁移结果和回滚方式。
   - 最终回复必须列出：预发 deployment、测试报告路径、CR/PR 或 code review 路径、生产 deployment、线上验证结果、未解决风险。

### 客户端专项联调方案

只有当客户端专项门禁启用时，联调 Agent 执行以下步骤：

1. 识别客户端形态：Web、React Native/Expo、原生 iOS、原生 Android、Flutter、小程序、桌面端或 SDK。
2. 识别运行形态：dev server、Debug 包、Release 包、TestFlight/灰度包、生产包、浏览器会话或真机。
3. 识别环境绑定：API baseURL、WebSocket/SSE 地址、对象存储域名、认证回调、CORS/ATS/网络安全策略和 feature flags。
4. 设计最小闭环：登录/鉴权、核心列表或详情、创建/更新/删除、长任务触发与轮询、错误态、空态、加载态、缓存或离线恢复。
5. 选择验证工具：Web 优先 Playwright 或浏览器自动化；React Native/Expo 优先 `react-native-dev`；iOS 优先 XcodeBuildMCP 模拟器构建安装；小程序优先对应小程序 skill；无法自动化时必须记录人工验证步骤和证据。
6. 输出联调矩阵：每个客户端类型一行，包含环境、入口、命令、设备、版本、验证路径、结果、证据和失败归因。
7. 确认新旧构建：客户端问题必须先排除旧 bundle、旧包、错误环境、缓存登录态和代理配置，再归因到业务代码。
8. 执行功能页验收：对每个被改功能执行“导航到目标页面/状态 -> 截图或快照 -> 对照验收点 -> 不通过继续修复”的闭环。不得把默认首页、错误 Tab、构建日志、安装成功或非目标页面截图记为通过证据。

9. 在 `manual-gated` 模式下，实施代码、迁移数据库、部署、删除或归档文档前必须等待用户确认。

10. 文档产出完成后，最终回复必须明确当前状态为 `awaiting-user-review`，并列出待用户审核的文档路径。

11. 在 `full-auto` 模式下，可以继续完成实施、验证和报告，但仍需记录所有产物路径；如果本次需求已有审核关卡约束，则不得越过用户审核。即使是 `full-auto`，生产发布仍必须保留预发测试报告和 CR/code review 记录；不得从未提交本地工作区直接部署，也不得先发布后补 CR。

## 文档质量规则

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
   - 运维：环境、配置、发布、回滚、巡检、告警和故障处理。

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
   - 每条 P0/P1 需求必须有稳定 ID，例如 `REQ-EVIDENCE-REVIEW-001`。
   - PRD 验收标准、测试用例、联调报告和证据清单必须引用这些 ID。
   - 如果某条需求无法映射到可执行测试或证据，必须退回需求验证阶段重写，不能靠“人工感觉通过”验收。

7. 自动开发执行质量
   - 适用于 `implementation-loop`、`full-auto` 和用户明确要求直接开发的场景。
   - 必须先发现项目命令和现有约束，再修改代码。
   - 必须小步提交验证证据：每次关键变更后至少运行一个与变更相关的最小验证命令或功能页验证。
   - 失败必须归因后再改；禁止在没有解释失败的情况下继续增加新代码。
   - 最终报告必须说明哪些验证通过、哪些没跑、为什么没跑、残余风险是什么。

8. Bug 修复质量
   - 适用于 `bugfix-fast-path`。
   - 必须先复现或说明无法复现的原因和替代证据。
   - 必须区分代码 bug、配置问题、旧构建/缓存、环境混用、第三方异常和数据问题。
   - 修复必须有回归证据，UI/客户端问题必须有真实功能页截图或运行时快照。
   - Debug report 必须能让后续 Agent 不看聊天记录也理解问题、根因、修复和验证结果。

主文档应简洁但完整。历史决策放在版本历史里，不要散落到重复文档中。

## 模板规则

所有主文档都必须对应一个模板。

Agent 在读写文档时：

1. 先读取对应模板。
2. 再读取当前主文档。
3. 判断主文档是否缺少模板中的约束项。
4. 缺项时优先补齐，而不是自由发挥新增结构。

如果用户没有特别要求，不要随意改变主文档的顶层结构。

## 可复用 Skills

- `ui-ux-pro-max`：产品界面和 UI/UX 设计
- `test-agent-orchestrator`：测试工作流入口
- `test-case-designer`：测试计划和测试用例设计
- `test-execution-runner`：测试执行和报告
- `ios-release`：iOS 客户端发布，覆盖 TestFlight、App Store Connect、App Store 提审、签名、archive/exportArchive 和 IPA 上传；`ios-testflight-release` 只作为旧名称兼容入口
- `deploy-to-vercel` 或 `vercel-deploy`：当前端需要部署到 Vercel 时使用

## 开源策略

不要默认所有模块都自研。

默认技术取向：

- 浏览器自动化：Playwright / Crawlee
- MVP 任务队列：Postgres 任务队列
- 平台化工作流：Temporal 或 Kestra
- 结构化数据库：PostgreSQL
- 证据和文件存储：MinIO
- 可观测性：OpenTelemetry + Prometheus + Grafana + Loki
- 认证授权：Keycloak
- 后台 UI：Ant Design Pro / Refine

只自研：

- 搜索广告适配器
- 风险规则
- 证据链模型
- 复核流程
- 国家优先级和节点策略
- 产品专属控制台体验

## 文档命名

统一使用以下主文档结构：

```text
<PROJECT_ROOT>/docs/<FEATURE_NAME>/
├── 00-research/competitor-research.md
├── 01-product/requirement-validation.md
├── 01-product/PRD.md
├── 02-ui/markdown-prototype.md
├── 03-architecture/architecture.md
├── 04-engineering/change-impact.md
├── 04-engineering/implementation-plan.md
├── 04-engineering/debug-report.md
├── 04-engineering/evidence-manifest.md
├── 04-engineering/code-review.md
├── 04-engineering/backlog.md
├── 05-testing/test-strategy.md
├── 05-testing/test-cases.json
├── 05-testing/test-report.md
├── 05-testing/integration-report.md
└── 06-ops/ops-runbook.md
```

除非用户明确要求创建附录或历史归档，否则不要新增顶层产品方案、技术架构方案或 UI 原型文档。

示例：

```text
example-monitoring-platform/docs/evidence-review-workflow/
├── 00-research/competitor-research.md
├── 01-product/requirement-validation.md
├── 01-product/PRD.md
├── 02-ui/markdown-prototype.md
├── 03-architecture/architecture.md
├── 04-engineering/change-impact.md
├── 04-engineering/implementation-plan.md
├── 04-engineering/debug-report.md
├── 04-engineering/evidence-manifest.md
├── 04-engineering/code-review.md
├── 04-engineering/backlog.md
├── 05-testing/test-strategy.md
├── 05-testing/test-cases.json
├── 05-testing/test-report.md
├── 05-testing/integration-report.md
└── 06-ops/ops-runbook.md
```

## 最终回复格式

只返回：

- 模式
- 新增或更新的产物路径
- 关键决策
- 阻塞项
- 下一步动作

不要把长文档直接粘贴在聊天里。
