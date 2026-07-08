# OPC Skills

OPC Skills 是一套面向 OPC/监测类平台的 Codex skill 模板，用于把需求验证、产品、UI、架构、研发、测试、联调、DevOps 串成一个有门禁的研发工作流。

> English summary: an open Codex skill template for agentic product, engineering, QA, and release workflows in monitoring-style platforms.

## 适合场景

- 多服务、多客户端、多环境的监测平台研发。
- 需要把 PRD、UI、架构、测试、联调和发布证据落盘的团队。
- 需要约束 Agent 不跳过保存点、测试报告、Code Review 和发布门禁的项目。
- 需要沉淀模板化研发文档，而不是只把决策留在聊天记录里的项目。

## 不适合场景

- 一次性脚本或很小的单文件修改。
- 不需要文档门禁、测试证据或发布流程的小型个人项目。
- 已经有完整内部研发流程，且不希望 Agent 介入流程治理的团队。

## 目录结构

```text
.
├── SKILL.md
├── templates/
├── references/
├── scripts/
│   └── start_rnd.sh
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── SECURITY.md
```

## 安装

克隆到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/BiuBiuHu/opc-skills.git ~/.codex/skills/opc-skills
```

也可以先克隆到任意目录，再复制或软链到 `~/.codex/skills/opc-skills`。

## 使用方式

在 Codex 中说：

```text
启动 OPC Skills
```

或描述一个监测平台相关需求，例如：

```text
启动监测平台研发流程，帮我规划证据复核工作流
```

Skill 会先识别 `<PROJECT_ROOT>` 和 `<FEATURE_NAME>`，然后按默认 `manual-gated` 模式产出文档并停在用户审核状态。

## 工作模式

- `manual-gated`：默认模式。先产出文档和计划，实施、迁移、部署、删除前等待确认。
- `full-auto`：用户明确要求时启用，但生产发布仍保留预发、测试报告和 Code Review 门禁。
- `implementation-loop`：需求和验收标准明确后，进入保存点、实现、验证、修复、复验循环。
- `bugfix-fast-path`：用于线上、预发、本地 bug 的复现、定位、最小修复和回归。
- `release-gated`：用于预发、线上、回滚、灰度、客户端发布等发布门禁。
- `architecture-review`：用于检查分层、调用关系、服务边界和腐化风险。

## 核心原则

- 先保存代码，再改代码。
- 产品、技术、测试和运维决策必须落盘到 `docs/<FEATURE_NAME>/`。
- 客户端默认只调用网关/主服务，不直连内部子服务。
- 生产发布必须先预发、再测试报告、再 Code Review、最后线上 smoke test。
- UI 或客户端改动必须进入真实功能页验证，不能只用构建通过替代验收。

## 初始化文档目录

```bash
./scripts/start_rnd.sh /path/to/project evidence-review-workflow
```

脚本会基于 `templates/` 创建 feature 文档骨架。

## 开源安全说明

本仓库中的服务名、邮箱、项目名和环境名均为公开示例占位。使用时请替换成你自己的项目约定，但不要把真实密钥、内部服务地址、客户数据、生产数据库信息或私有部署 URL 提交到仓库。

## License

MIT
