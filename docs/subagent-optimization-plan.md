# OPC Skills Subagent 优化方案

## 0. 文档状态

- 状态：已应用到 `v0.2.0` 主规则；`v0.2.2` 根据 Dida 日历页实战补充批量确认、产物可用性状态、mock gate 和预发证据边界。
- 日期：2026-07-11
- 目标：在不重写 `opc-skills` 的前提下，引入可控的 subagent 编排能力，让复杂需求在执行速度和交付质量上都有可感知提升。
- 非目标：不把所有概念 Agent 都改成常驻 subagent；不引入自动发布、自动迁移或不可控并行写代码。

## 1. 当前判断

当前 `opc-skills` 已经有产品、UI、架构、研发、QA、联调、DevOps 等概念 Agent，也已经有一条基本约束：只有用户明确要求并行 Agent 工作时，才真正调用子 Agent。

因此本次优化不是重构，而是在现有工作流上补一层“可执行 subagent 编排规则”：

```text
opc-skills
  -> 定义目标澄清、分层架构、文档质量、发布门禁和 Agent 职责
  -> 决定什么时候允许拆分任务
  -> 由主 Agent 调用 subagent 执行明确子任务
  -> 主 Agent 审查、集成、验证并最终负责
```

## 2. 核心原则

1. Skill 是规则，不是执行器。
   - `SKILL.md` 只能约束主 Agent 的行为。
   - 真正触发 subagent 的动作由主 Agent 调用工具完成。

2. 拆分必须带来收益。
   - 启动 subagent 前必须说明预期收益：提速、降低遗漏、提高审查质量或隔离专业上下文。
   - 小 bug、单文件修改、目标不清晰或写范围重叠时，不应拆分。

3. 主 Agent 保留最终责任。
   - 目标澄清、架构最终决策、跨层边界、发布门禁和最终汇报不能下放。
   - subagent 的输出必须被主 Agent 审查后才能进入最终方案或代码。

4. 每个 subagent 必须有明确 ownership。
   - 可以读什么、可以改什么、不能改什么必须写清楚。
   - 多个 worker 不得修改同一批文件，除非主 Agent 明确安排顺序和合并策略。

5. 生产动作不交给 subagent。
   - subagent 不执行生产发布、数据库迁移、环境变量修改、回滚或破坏性清理。
   - release-gated 仍由主 Agent 严格执行。

## 3. 建议的 Agent 分层

### 3.1 概念 Agent

继续由 `opc-skills` 定义，用于说明职责、产物和质量门禁：

- 目标澄清 Agent
- 需求验证 Agent
- 产品 Agent
- UI Agent
- 架构 Agent
- 变更影响 Agent
- 研发 Agent
- Bug Triage Agent
- QA Agent
- 联调 Agent
- DevOps Agent

这些 Agent 不等于一定要启动 subagent。它们是方法论角色。

### 3.2 可执行 Subagent

当用户明确允许 subagent 或并行 Agent 工作，且任务满足拆分条件时，主 Agent 可以启动以下执行角色：

| Subagent | 类型 | 适用场景 | 可写范围 | 禁止事项 |
|----------|------|----------|----------|----------|
| Explorer Agent | explorer | 代码影响面、现有接口、数据模型、开源方案、历史文档扫描 | 默认只读 | 不直接改代码，不做最终决策 |
| Frontend Agent | worker | Web/RN UI、B 类页面、mock、Playwright、交互状态 | 明确页面、组件、前端测试文件 | 不改后端业务规则，不直连内部服务 |
| Backend Agent | worker | API、BFF、主服务契约、权限、幂等、分页、重试 | 明确服务端模块、路由、service、后端测试 | 不改前端交互，不绕过主服务边界 |
| Data/Migration Agent | worker | schema、索引、迁移、回滚脚本、数据修复 | 明确迁移文件和数据脚本 | 不直接执行生产迁移 |
| QA/Test Agent | explorer/worker | 测试策略、测试用例、自动化断言、失败路径 | 明确测试文件或文档 | 不把测试通过当成发布通过 |
| Integration Agent | explorer/worker | 前后端联调、环境拓扑、API contract、证据汇总 | 联调报告、证据清单、必要的轻量修复 | 不做生产发布，不跳过主 Agent 审查 |

## 4. 触发门禁

启动 subagent 前，主 Agent 必须回答：

```text
1. 用户是否明确允许 subagent / 多 Agent / 并行执行？
2. 这个子任务能否独立完成？
3. 这个子任务是否能并行，不阻塞主线程？
4. 文件 ownership 是否清楚？
5. 启动它的收益是什么：提速、质量、覆盖面还是专业上下文隔离？
6. 不启动它的主要风险是什么？
7. subagent 的输出如何验收？
```

任一问题答不清，不启动 subagent。

## 5. 任务拆分规则

### 5.1 适合拆分

- 多仓库、多服务、多页面的功能。
- B 类运营页重做，涉及 UI、API、mock、测试、部署。
- 认证、支付、AI 生成、缓存、队列、发布等高风险链路。
- 需要并行调研开源方案、现有代码、测试缺口和架构边界。
- 明确可按前端、后端、数据、测试分割文件 ownership。

### 5.2 不适合拆分

- 用户目标还没澄清。
- 单文件小修。
- 问题需要先定位根因，尚不知道归属层级。
- 多个子任务会改同一个文件或同一段逻辑。
- 需要生产发布、数据库迁移、环境变量修改或高风险操作。
- 子任务输出无法被主 Agent 快速验收。

## 6. Subagent 输入模板

主 Agent 启动 subagent 时，必须给出足够窄的任务说明：

```text
你是 <Frontend/Backend/QA/Integration> Agent。

目标：
- 本子任务要完成什么结果。

上下文：
- 业务目标摘要。
- 相关 feature/doc 路径。
- 已确认的架构边界和不能发生的副作用。

Ownership：
- 允许读取的目录。
- 允许修改的文件或模块。
- 禁止修改的文件或模块。

输出要求：
- 结论或改动摘要。
- 修改文件列表。
- 运行过的验证命令和结果。
- 未验证项和风险。

约束：
- 不要 revert 他人的改动。
- 不要扩大写入范围。
- 不要执行发布、迁移或破坏性命令。
```

## 7. Subagent 输出验收

subagent 完成后，主 Agent 必须检查：

- 输出是否回答了任务目标。
- 是否越过 ownership。
- 是否引入无关改动。
- 是否违反分层架构，例如前端直连内部服务。
- 是否有可复现验证证据。
- 是否留下未解释失败。
- 是否需要补充到 `evidence-manifest.md`、`test-report.md` 或 `code-review.md`。

主 Agent 不得把 subagent 结论原样当最终结论。最终方案、代码和发布判断必须由主 Agent 汇总后输出。

## 8. 收益评估

每次使用 subagent 后，必须记录实际收益：

```text
Subagent 使用复盘：
- 启动原因：
- 预期收益：
- 实际节省的时间：
- 发现的问题：
- 产出的文件：
- 验证证据：
- 是否有冲突或重复工作：
- 下次是否继续使用同类 subagent：
```

建议先用以下指标试运行：

- 复杂需求的代码影响面分析时间是否下降。
- UI/后端/测试是否能并行产出，减少等待。
- QA 或 UI 审计是否提前发现主 Agent 漏掉的问题。
- 集成阶段冲突数量是否可控。
- 最终返工轮数是否减少。

## 9. 风险与约束

| 风险 | 表现 | 约束 |
|------|------|------|
| 方向漂移 | subagent 局部正确，整体偏离用户目标 | 输入必须包含目标澄清摘要和不能发生的副作用 |
| 重复工作 | 多个 subagent 查同一问题 | 主 Agent 先定义问题清单和 ownership |
| 代码冲突 | 多个 worker 改同一文件 | worker 写范围必须不重叠 |
| 成本上升 | 小任务也并行，token 和时间变多 | 小 bug 和单文件修改默认不拆 |
| 质量幻觉 | subagent 说通过但证据不足 | 主 Agent 必须复验关键结论 |
| 生产风险 | subagent 执行发布或迁移 | subagent 禁止生产动作 |
| 上下文泄漏 | 把全部历史传给子任务导致污染 | 默认传最小上下文；需要完整上下文时说明原因 |

## 10. 对 `opc-skills` 的建议改造

### 10.1 第一阶段：只补规则，不改变执行流

修改范围建议：

- `SKILL.md`
  - 在 “Agent 角色” 前增加 “Subagent 执行模型”。
  - 明确 Skill 是规则，subagent 由主 Agent 触发。
  - 增加收益门禁、ownership 门禁和禁止事项。

- `references/agent-workflow.md`
  - 增加“概念 Agent 与可执行 subagent 的区别”。
  - 增加 Frontend、Backend、QA、Integration 的推荐拆分方式。

### 10.2 第二阶段：只在低风险任务试运行

优先使用：

- Explorer Agent 做代码影响面和开源调研。
- QA/Test Agent 做测试策略和失败路径审计。
- UI Audit Agent 做 B 类页面审计。

暂不启用：

- 多 worker 同时写代码。
- 数据库迁移 worker。
- 发布相关 subagent。

### 10.3 第三阶段：启用专业代码 Worker

当第一阶段复盘证明收益明显后，再启用：

- Frontend Worker
- Backend Worker
- Data/Migration Worker
- Integration Worker

启用条件：

- 文件 ownership 清楚。
- 主 Agent 已完成目标澄清和架构边界。
- 有最小验证命令。
- 有合并和复验计划。

## 11. 示例：Dida 日历运营页面

适合拆分：

```text
主 Agent：
- 目标澄清、信息架构、架构边界、最终集成。

Frontend Agent：
- 日历集总览、年度工作台、月度表格、单日抽屉。
- 本地 mock 和 Playwright 截图验证。

Backend Agent：
- 日历集 summary API、分页、状态统计、发布状态、OSS 状态透传。

QA/Test Agent：
- 提示词预览不触发生图。
- OSS 缓存命中不重复生成。
- 单日返工不重跑整月。
- 预发/线上发布门禁。

Integration Agent：
- 前端 -> dida-core/service -> AI/Worker -> OSS -> 数据库 的联调证据。
```

预期收益：

- 前端交互和后端契约可以并行推进。
- QA 能提前发现昂贵操作副作用。
- 主 Agent 专注跨层边界和最终验收。

## 12. 建议结论

建议采用“保守引入、收益复盘、逐步放开”的方案：

1. `opc-skills` 继续保留概念 Agent，作为方法论和质量门禁。
2. 新增 subagent 执行模型，但只在用户明确授权时启用。
3. 先启用 Explorer、QA、UI Audit 这类低风险 subagent。
4. 再逐步启用 Frontend、Backend、Integration worker。
5. 每次使用都记录收益和风险，只有证明能提速或提质，才保留该拆分模式。
