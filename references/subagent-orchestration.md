# Subagent 编排执行准则

## 1. 最重要的结论

`SKILL.md` 不能直接调用 subagent。Skill 文件不是程序，不会执行 shell、hooks 或脚本。

正确链路是：

```text
用户请求
  -> 触发 opc-skills
  -> 主 Agent 读取 SKILL.md
  -> 主 Agent 按规则判断是否值得拆
  -> 主 Agent 读取 agents/<role>-agent.md
  -> 主 Agent 填写 templates/subagent-task-brief-template.md
  -> 主 Agent 调用 Codex Runtime 工具 multi_agent_v1.spawn_agent
  -> subagent 执行任务并返回结果
  -> 主 Agent 审查、集成、复验、汇报
```

所以“skills 中调用 subagent”的准确表达是：**skill 写强制规则，主 Agent 遵守规则并发起 Runtime tool call**。

## 2. 运行时工具

主 Agent 可使用的多 Agent 工具：

```text
multi_agent_v1.spawn_agent   启动 subagent
multi_agent_v1.wait_agent    等待 subagent 完成
multi_agent_v1.send_input    给已有 subagent 补充输入
multi_agent_v1.close_agent   关闭不再需要的 subagent
```

这些工具不是 shell 命令。不要写：

```bash
codex subagent run frontend-agent
```

也不要写：

```bash
npm run spawn-agent
```

## 3. 主 Agent 的实际执行步骤

1. 判断用户是否明确允许 subagent、多 Agent 或并行执行。
2. 判断任务是否值得拆：能并行提速、降低遗漏、提高审查质量或隔离专业上下文。
3. 选择角色文件，例如 `agents/frontend-agent.md`。
4. 使用 `templates/subagent-task-brief-template.md` 写任务包。
5. 调用 `multi_agent_v1.spawn_agent`。
6. 主 Agent 继续做不重叠工作，不要原地空等。
7. 需要结果时调用 `multi_agent_v1.wait_agent`。
8. 审查 subagent 输出，检查 ownership、无关改动、分层边界和验证证据。
9. 需要补充信息时用 `send_input`；任务完成后用 `close_agent`。

## 4. 具体调用例子

下面是主 Agent 在运行时发起的工具调用意图，不是放在仓库里的脚本：

```text
tool: multi_agent_v1.spawn_agent
input:
  agent_type: worker
  fork_context: false
  message: |
    你是 OPC Frontend Agent。你不是独自在代码库里工作，不要 revert 他人改动。

    业务目标：
    - 日历运营页生成本月提示词时覆盖整月，不只覆盖当前分页。
    - 单日抽屉允许编辑存量一句话，保存不触发生图。

    Ownership：
    - 可读：dida-admin/src, dida-admin/scripts, docs/calendar-ops-workbench
    - 可写：dida-admin/src/pages/CalendarOps.tsx, dida-admin/src/services/api.ts, dida-admin/scripts/calendar-ops-mock-gate.py
    - 禁止：dida-core/**, dida-ai-service/**, env 文件, Vercel 配置

    架构边界：
    - dida-admin 只能调用 dida-core admin API。
    - 禁止前端直连 dida-ai-service。

    验证：
    - npm run build
    - npm run test:run
    - npm run calendar:mock-gate

    输出：
    - 按 templates/subagent-result-template.md 返回。
```

等待结果时：

```text
tool: multi_agent_v1.wait_agent
input:
  targets: ["<spawn_agent 返回的 agent id>"]
  timeout_ms: 600000
```

继续补充约束时：

```text
tool: multi_agent_v1.send_input
input:
  target: "<agent id>"
  interrupt: false
  message: "补充约束：不要修改 CalendarOps 之外的页面；只汇报结果，不提交 git。"
```

关闭时：

```text
tool: multi_agent_v1.close_agent
input:
  target: "<agent id>"
```

## 5. 拆分判断

适合拆：

- 多仓库、多服务、多页面。
- B 类页面重做，涉及 UI、API、mock、测试和预发验证。
- 认证、AI/生成、缓存、队列、对象存储、发布等高风险链路。
- 可以按前端、后端、数据、测试、联调拆成不重叠 ownership。

不适合拆：

- 目标还没澄清。
- 单文件小修或很小 bug。
- 根因未知，尚不能确认归属层级。
- 多个 worker 会写同一文件。
- 需要生产发布、数据库迁移执行、环境变量修改、回滚或破坏性清理。

## 6. 主 Agent 不可下放的责任

- 目标澄清。
- 架构最终决策和跨层边界。
- 子任务拆分和 ownership。
- 结果审查、集成和复验。
- 预发/线上发布门禁。
- 最终对用户汇报。

subagent 是提高速度和覆盖面的执行单元，不是责任转移。
