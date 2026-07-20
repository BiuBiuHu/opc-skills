# OPC Skills

当前版本：`v0.2.2`

`opc-skills` 是一套面向 C 端业务研发的 Codex Skill，擅长开发用户侧 App/Web/小程序，以及配套的 B 端运营工作台。

它关注完整交付链路：先对齐用户目标和核心路径，再设计 C 端体验、服务接口和 B 端操作闭环，最后通过真实页面、真实客户端、预发验证和测试报告证明功能可上线。

## 最近更新

- 将 README 与 `SKILL.md` 的主规则对齐，补充 subagent 的适用边界。
- 新增 `agents/`、`templates/subagent-task-brief-template.md`、`templates/subagent-result-template.md` 和 `references/subagent-orchestration.md`，明确 skill 不能直接调用 subagent，必须由主 Agent 使用 Runtime 工具执行。
- 强化 B 类页面、本地 mock、Mermaid 调用图、预发/线上门禁的阅读提示。
- 补充昂贵批量操作的确认规则：禁止嵌套确认，必须展示成本、缓存、重试和覆盖策略。
- 明确预发证据不能只停留在登录页，必须验证真实 API、OSS/数据库和功能页路径。

## 适用场景

- C 端应用：移动 App、Web App、小程序、桌面端、登录注册、内容浏览、创建编辑、支付订阅、分享通知、离线缓存。
- C 端体验：导航、表单、弹窗、列表、媒体、手势、动画、性能、空/错/慢状态和真实设备验证。
- B 端工作台：运营台、审核台、内容生成台、配置台、客服排错台、发布台和数据修复台。
- 全栈闭环：客户端、主服务/API、认证、AI/Worker、数据库、对象存储、第三方服务、预发/线上发布和回滚。

## 核心能力

- C 端优先：先明确用户、场景、入口、核心路径和成功标准。
- B 端配套：工作台服务配置、审核、生成、排错、返工和发布，不做字段堆砌。
- 全栈契约：客户端只调用主服务/API server，内部服务由主服务编排。
- 成本保护：AI/生成类能力先预览审核，再执行昂贵生成，并复用缓存/对象存储。
- 证据闭环：真实页面、真实客户端、预发环境、测试报告和发布门禁缺一不可。
- 文档落盘：产品、UI、架构、研发、测试、联调和运维结论写入 `docs/<FEATURE_NAME>/`。
- Subagent 编排：只有在用户明确允许、任务边界清楚、能证明提速或提质时，才拆分 Explorer、Frontend、Backend、QA/Test、Integration 等子任务。

## 使用方式

将本目录放入 Codex 可发现的 skills 目录，例如：

```text
~/.codex/skills/opc-skills
```

在对话中使用以下意图即可触发：

```text
启动 OPC Skills
启动 C 端业务应用研发流程
跑一遍 C 端应用和配套 B 端工作台全流程
用 opc-skills 分析这个移动端需求
用 opc-skills 设计这个 C 端功能
用 opc-skills 设计配套运营工作台
```

触发后，主 Agent 会读取 `SKILL.md`，并按当前任务类型进入需求验证、UI、架构、实现、测试、联调或发布模式。

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
-> 生产发布和线上 smoke test
```

默认模式是 `manual-gated`：文档和方案完成后进入 `awaiting-user-review`，用户审核通过后才进入实现、迁移或部署。

## 目录结构

```text
opc-skills/
├── SKILL.md
├── README.md
├── VERSION
├── CHANGELOG.md
├── agents/
│   ├── explorer-agent.md
│   ├── frontend-agent.md
│   ├── backend-agent.md
│   ├── qa-agent.md
│   ├── integration-agent.md
│   └── devops-agent.md
├── references/
│   ├── agent-workflow.md
│   ├── auth-login-e2e.md
│   ├── b-side-ui-guidance.md
│   ├── document-standard.md
│   ├── open-source-stack.md
│   ├── subagent-orchestration.md
│   └── testing-guidance.md
├── docs/
│   ├── subagent-optimization-plan.md
│   └── subagent-runtime-invocation-design.md
├── scripts/
│   └── start_rnd.sh
└── templates/
    ├── architecture-template.md
    ├── change-impact-template.md
    ├── debug-report-template.md
    ├── evidence-manifest-template.md
    ├── implementation-plan-template.md
    ├── ops-runbook-template.md
    ├── prd-template.md
    ├── requirement-validation-template.md
    ├── subagent-result-template.md
    ├── subagent-task-brief-template.md
    ├── test-strategy-template.md
    └── ui-prototype-template.md
```

## 关键原则

- 先保存代码，再改代码。
- 目标澄清不可跳过。
- C 端核心用户路径优先，不能只堆功能点或字段。
- 配套 B 端工作台服务运营闭环，不是数据库字段展示页。
- B 类运营页面以效率为第一目标。
- 长列表必须有分页、总数、筛选和加载/空/错态。
- ASCII 草图必须和基础交互路径放在一起。
- AI/生成类需求必须先低成本预览，再高成本生成。
- 客户端不得直连内部子服务。
- 发布必须先预发、再线上，并且必须有测试报告和 Code Review。
- subagent 只能在用户明确允许、任务边界清楚、能证明提速或提质时使用；skill 只写规则，主 Agent 通过 `multi_agent_v1.spawn_agent` 执行调用。

## 版本发布

当前本地版本通过 `VERSION` 和 `CHANGELOG.md` 标记。本次发布版本为 `v0.2.2`。若要开源发布，建议先把本目录迁入独立 Git 仓库，再补齐：

- `LICENSE`
- GitHub Releases
- 安装说明
- 示例任务和输出样例
- 版本 tag，例如 `v0.2.2`
