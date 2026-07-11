# OPC Skills

当前版本：`v0.1.0`

`opc-skills` 是一个面向 OPC/Dida 类产品研发的 Codex Skill，用于把需求澄清、产品设计、B 类运营页设计、架构治理、研发、测试、联调和发布门禁串成一套可复用工作流。

它的核心目标不是生成模板化文档，而是让 Agent 在复杂业务里持续做正确判断：先对齐目标，再设计信息结构和分层架构，然后小步实现、验证、联调和发布。

## 适用场景

- 规划、设计、研发、测试、部署 OPC 类监测平台。
- Dida 管理后台、移动端、主服务、AI/Worker、对象存储、认证和发布链路联动。
- B 类运营页面设计，例如审核台、批量生成台、运营工作台、长任务列表。
- 涉及 LLM、生图、缓存、OSS、预发/线上发布、回滚和成本保护的功能。
- 需要检查架构调用关系、分层边界和服务腐化风险的需求。

## 核心能力

- 目标澄清：在 PRD、UI、架构、编码前对齐业务结果、操作闭环、成本约束和验收证据。
- B 类页面方法论：默认采用高密度表格、总分下钻、批量操作、详情抽屉和本地 mock 验证。
- AI 成本分层：先生成和审核提示词，再触发昂贵生成；生成结果必须复用 OSS/缓存。
- 架构防腐化：客户端只调用主服务/API server，内部子服务不暴露给前端。
- 文档落盘：所有产品、UI、架构、研发、测试和运维结论写入项目内 `docs/<FEATURE_NAME>/`。
- 验证门禁：功能页必须进入真实页面验证；B 类页面先本地 mock，再预发真实链路复验。
- 发布门禁：生产发布必须经过预发、测试报告、Code Review 和线上 smoke test。
- Subagent 草案：已整理可执行 subagent 编排方案，用于后续提升复杂任务的并行速度和交付质量。

## 使用方式

将本目录放入 Codex 可发现的 skills 目录，例如：

```text
~/.codex/skills/opc-skills
```

在对话中使用以下意图即可触发：

```text
启动 OPC Skills
启动违规广告平台研发流程
跑一遍违规广告平台全流程
用 opc-skills 分析这个需求
用 opc-skills 设计这个 B 类页面
```

触发后，主 Agent 会读取 `SKILL.md`，并按当前任务类型进入需求验证、UI、架构、实现、测试、联调或发布模式。

## 工作流概览

```text
目标澄清
-> 需求验证
-> 产品 PRD
-> UI 原型和 ASCII 草图
-> 架构图和调用图
-> 变更影响分析
-> 实施计划
-> 本地 mock / 自动化验证
-> 预发联调
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
├── references/
│   ├── agent-workflow.md
│   ├── auth-login-e2e.md
│   ├── b-side-ui-guidance.md
│   ├── document-standard.md
│   ├── open-source-stack.md
│   └── testing-guidance.md
├── docs/
│   └── subagent-optimization-plan.md
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
    ├── test-strategy-template.md
    └── ui-prototype-template.md
```

## 关键原则

- 先保存代码，再改代码。
- 目标澄清不可跳过。
- B 类运营页面以效率为第一目标。
- 长列表必须有分页、总数、筛选和加载/空/错态。
- ASCII 草图必须和基础交互路径放在一起。
- AI/生成类需求必须先低成本预览，再高成本生成。
- 客户端不得直连内部子服务。
- 发布必须先预发、再线上，并且必须有测试报告和 Code Review。
- subagent 只能在用户明确允许、任务边界清楚、能证明提速或提质时使用。

## 版本发布

当前本地版本通过 `VERSION` 和 `CHANGELOG.md` 标记。若要开源发布，建议先把本目录迁入独立 Git 仓库，再补齐：

- `LICENSE`
- GitHub Releases
- 安装说明
- 示例任务和输出样例
- 版本 tag，例如 `v0.1.0`
