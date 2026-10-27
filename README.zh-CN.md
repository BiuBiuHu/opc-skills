# OPC Skills

[English hub](README.md) | [English README](README.en.md)

当前版本：`v0.5.0`

`opc-skills` 是一套面向 C 端业务研发的 Codex Skill，擅长开发用户侧 App/Web/小程序，以及配套的 B 端运营工作台。主要给一人公司（OPC）和需要同时交付用户产品与运营工作台的小团队用。

它覆盖完整交付链路：目标澄清 → PRD → UI → 架构 → 实现 → 测试 → 联调 → 发布，以及可选的发布后中英文内容。先对齐用户目标和核心路径，再设计 C 端体验、服务接口和 B 端操作闭环，最后用真实页面、真实客户端、预发验证和测试报告证明功能可上线。入口短文见 [README.md](README.md)；完整规则以 [SKILL.md](SKILL.md) 为准。

## 安装

一键安装（会创建 `~/.codex/skills`）：

```bash
npx opc-skills install
```

```bash
curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
```

`npx opc-skills update` 会快进更新；`npx opc-skills doctor` 会检查安装路径、`VERSION` 和 symlink。CLI 与 curl 脚本共用 `scripts/install.sh`。脚本会把本仓库克隆或快进更新到 `~/.codex/skills/opc-skills`。若本机已有 `~/.cursor/skills` 或 `~/.claude/skills`，会再指向同一目录，方便 Cursor / Claude Code 发现。脚本不会凭空创建这些额外目录，也不会读取编辑器配置或密钥。安装需要本机已有 `git`。Codex `$skill-installer` 的可粘贴提示见 [docs/skills-hub.md](docs/skills-hub.md)；本 skill 尚未进入 openai curated 列表。

手动安装：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

也可以克隆到其它位置，再软链到 `~/.codex/skills/opc-skills`。

## 触发语

在对话中使用以下意图即可触发：

```text
启动 OPC Skills
启动 C 端业务应用研发流程
跑一遍 C 端应用和配套 B 端工作台全流程
用 opc-skills 分析这个移动端需求
用 opc-skills 设计这个 C 端功能
用 opc-skills 设计配套运营工作台
按这次发布生成中英文技术文章草稿
```

触发后，主 Agent 会读取 `SKILL.md`，并按当前任务类型进入需求验证、UI、架构、实现、测试、联调、发布或 `post-release-content` 模式。

## 延伸阅读

相关实践，来自 One PC：

- [一个人，也可以做完一款产品：我的 OPC 软件研发实践](https://www.peak-lake.com/blog/opc-software-practice/)（[EN](https://www.peak-lake.com/en/blog/opc-software-practice/)）— 一人公司如何把痛点做到发布；opc-skills 是其中的交付流程。
- [Loop Engineering 没有银弹：垂直场景的 Skills + spec/TDD 落地实践](https://www.peak-lake.com/blog/mslj4f6g/)（[EN](https://www.peak-lake.com/en/blog/mslj4f6g/)）— 垂直 Skills + spec/TDD，文中指向本仓库。

## 最近更新

- 增加 `npx opc-skills` CLI（`install` / `update` / `doctor` / `path`），与 `scripts/install.sh` 共用安装规则。
- 增加 `docs/skills-hub.md`，记录 Codex `$skill-installer` 可粘贴安装方式；尚未进入 openai curated 列表。
- 增加 `scripts/install.sh` 一键安装，并把安装说明提前到引言之后。
- 将 README 与 `SKILL.md` 的主规则对齐，补充 subagent 的适用边界。
- 新增 `agents/`、`templates/subagent-task-brief-template.md`、`templates/subagent-result-template.md` 和 `references/subagent-orchestration.md`，明确 skill 不能直接调用 subagent，必须由主 Agent 使用 Runtime 工具执行。
- 强化 B 类页面、本地 mock、Mermaid 调用图、预发/线上门禁的阅读提示。
- 补充昂贵批量操作的确认规则：禁止嵌套确认，必须展示成本、缓存、重试和覆盖策略。
- 明确预发证据不能只停留在登录页，必须验证真实 API、OSS/数据库和功能页路径。
- 增加发布方案评审、关联系统核销和生产发布后线上回归门禁；线上 smoke 不能替代 P0/P1 回归。
- 增加新需求分支准备门禁：保存当前工作区，切回远端默认主分支并 `git pull --ff-only`，再从同步后的主分支创建需求分支。
- 隔离通用 Skill 与项目事实：具体项目名、账号、域名、服务别名和 deployment 只保存在项目事实源中，通用材料使用角色占位符。
- 增加 PR 中文门禁：新建 Code PR、Release PR、文档 PR 默认用中文标题、正文和检查清单。
- 强化测试范围规则：按改动文件、调用链、共享契约和风险选择最小充分测试集，不默认执行无关全量测试。
- 增加发布完整性门禁：发布方案必须完成双向影响闭包、逐系统发布/不发布证据、候选冻结和漏发复核。
- Production 部署必须来自远端默认分支 merge commit，或提供可验证的源码 commit、构建任务和产物映射；禁止先部署线上再补 main/master。
- 增加 `references/release-integrity.md` 和 `scripts/check_release_integrity.sh`，用于核对候选 commit、deployment commit 和 worktree 归位状态。
- 当前任务完成后，若未命中硬门禁，主 Agent 会自动回看 Inbox/Todo 并继续下一项，不再等待用户额外说“继续”。
- 增加发布后可选内容生产：通过 `Content Agent` 从 Git、代码、测试和发布证据中生成中文/英文文章草稿，并提供选题、落盘、审核和发布状态机。

## 适用场景

- C 端应用：移动 App、Web App、小程序、桌面端、登录注册、内容浏览、创建编辑、支付订阅、分享通知、离线缓存。
- C 端体验：导航、表单、弹窗、列表、媒体、手势、动画、性能、空/错/慢状态和真实设备验证。
- B 端工作台：运营台、审核台、内容生成台、配置台、客服排错台、发布台和数据修复台。
- 全栈闭环：客户端、主服务/API、认证、AI/Worker、数据库、对象存储、第三方服务、预发/线上发布和回滚。
- 发布后内容：技术文章、发布复盘、中文/英文双稿、SEO/GEO、Mermaid 图和脱敏配图计划。

## 核心能力

- C 端优先：先明确用户、场景、入口、核心路径和成功标准。
- B 端配套：工作台服务配置、审核、生成、排错、返工和发布，不做字段堆砌。
- 全栈契约：客户端只调用主服务/API server，内部服务由主服务编排。
- 成本保护：AI/生成类能力先预览审核，再执行昂贵生成，并复用缓存/对象存储。
- 证据闭环：真实页面、真实客户端、预发环境、测试报告和发布门禁缺一不可。
- 文档落盘：产品、UI、架构、研发、测试、联调和运维结论写入 `docs/<FEATURE_NAME>/`。
- 内容生产旁路：发布完成后可选生成 `suggest`、`draft` 或 `publish` 内容，不阻塞页面发布，默认不静默公开。
- Subagent 编排：只有在用户明确允许、任务边界清楚、能证明提速或提质时，才拆分 Explorer、Frontend、Backend、QA/Test、Integration 等子任务。

## 工作流概览

```text
目标澄清
-> 需求验证
-> 产品 PRD
-> C 端体验设计 / B 端工作台原型
-> 架构图和调用图
-> 变更影响分析
-> 实施计划
-> 本地 mock / 客户端自动化验证
-> 预发联调和真实 API 复验
-> 测试报告和 Code Review
-> 发布方案评审和关联系统核销
-> 默认分支 merge commit 冻结
-> 生产发布和线上 smoke test
-> 固定生产域名线上回归
-> worktree 归位和发布完整性核销
-> 观察窗口完成后发布核销
-> 可选：选题 / 中英文草稿 / 内容审核 / 文章发布
```

默认模式是 `manual-gated`：文档和方案完成后进入 `awaiting-user-review`，用户审核通过后才进入实现、迁移或部署。

发布后内容生产有三个独立模式：

- `suggest`：输出 3-5 个基于一手素材的候选选题。
- `draft`：生成中文和英文两版，写入 `docs/<FEATURE_NAME>/07-content/` 或项目事实源指定的博客目录。
- `publish`：内容审核通过后，按项目事实源指定的博客构建和发布流程执行。

可先准备本次发布的素材清单：

```bash
./scripts/prepare_post_release_content.sh \
  /path/to/project feature-name <base-commit> <head-commit>
```

文章发布默认需要单独批准，不能把页面发布完成自动解释为文章已公开。

## 目录结构

```text
opc-skills/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── VERSION
├── CHANGELOG.md
├── package.json
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── bin/
│   └── opc-skills.js
├── agents/
│   ├── explorer-agent.md
│   ├── frontend-agent.md
│   ├── backend-agent.md
│   ├── qa-agent.md
│   ├── integration-agent.md
│   ├── devops-agent.md
│   └── content-agent.md
├── references/
│   ├── agent-workflow.md
│   ├── auth-login-e2e.md
│   ├── b-side-ui-guidance.md
│   ├── document-standard.md
│   ├── open-source-stack.md
│   ├── post-release-content.md
│   ├── release-integrity.md
│   ├── release-pr-lifecycle.md
│   ├── subagent-orchestration.md
│   └── testing-guidance.md
├── docs/
│   ├── skills-hub.md
│   ├── subagent-optimization-plan.md
│   └── subagent-runtime-invocation-design.md
├── scripts/
│   ├── install.sh
│   ├── check_release_integrity.sh
│   ├── prepare_post_release_content.sh
│   ├── check_project_coupling.sh
│   └── start_rnd.sh
└── templates/
    ├── architecture-template.md
    ├── backlog-template.md
    ├── change-impact-template.md
    ├── content-production-template.md
    ├── debug-report-template.md
    ├── evidence-manifest-template.md
    ├── implementation-plan-template.md
    ├── ops-runbook-template.md
    ├── prd-template.md
    ├── release-plan-template.md
    ├── requirement-validation-template.md
    ├── subagent-result-template.md
    ├── subagent-task-brief-template.md
    ├── test-strategy-template.md
    └── ui-prototype-template.md
```

## 关键原则

- 先保存代码，再改代码。
- 通用 Skill 不保存具体项目的账号、域名、服务名、部署标识或业务专用规则。
- 目标澄清不可跳过。
- C 端核心用户路径优先，不能只堆功能点或字段。
- 配套 B 端工作台服务运营闭环，不是数据库字段展示页。
- B 类运营页面以效率为第一目标。
- 长列表必须有分页、总数、筛选和加载/空/错态。
- ASCII 草图必须和基础交互路径放在一起。
- AI/生成类需求必须先低成本预览，再高成本生成。
- 客户端不得直连内部子服务。
- 发布必须先预发、再线上，并且必须有测试报告和 Code Review。
- 生产发布后必须完成线上回归；全部系统核销、回归通过且观察窗口完成后才能宣布发布完成。
- 发布完整性和主干归位是同一条硬门禁；Production 候选必须先进入远端默认分支，并能和实际 deployment/产物 commit 对上。
- 发布后必须核对受影响仓库的默认分支、merge commit、deployment commit 和 worktree 状态；默认分支 worktree 未同步或脏时保持阻断。
- 发布后文章必须来自 Git、代码和验证证据；默认同时产出中英文稿，且必须通过敏感信息检查和独立内容审核。
- 文章发布失败不回滚页面发布；文章公开发布必须有独立目标、预览、deployment 和回滚记录。
- 创建 PR 默认使用中文；除非仓库规范或用户明确要求其它语言。
- 测试范围必须按改动影响选择；全量测试只作为明确触发条件下的升级选项。
- subagent 只能在用户明确允许、任务边界清楚、能证明提速或提质时使用；skill 只写规则，主 Agent 通过 `multi_agent_v1.spawn_agent` 执行调用。

## 常用命令

安装或检查本 skill：

```bash
npx opc-skills install
npx opc-skills update
npx opc-skills doctor
```

从模板初始化 feature 文档：

```bash
./scripts/start_rnd.sh /path/to/project account-linking
```

发布前检查通用 skill 是否混入项目专属事实：

```bash
./scripts/check_project_coupling.sh
```

核对发布候选、deployment commit 和 worktree 归位：

```bash
./scripts/check_release_integrity.sh /path/to/repo <candidate-commit> [default-branch] [deployment-commit]
```

准备发布后文章素材：

```bash
./scripts/prepare_post_release_content.sh \
  /path/to/project feature-name <base-commit> <head-commit>
```

## 版本发布

当前版本通过 `VERSION` 和 `CHANGELOG.md` 标记。本次发布版本为 `v0.5.0`。

开源发布建议：

- 为稳定版本创建 GitHub Release。
- 补充示例任务和输出样例。
- 为版本创建 tag，例如 `v0.5.0`。
- npm 包名 `opc-skills` 当前可用，但不要在未明确要求时发布到 npm。
