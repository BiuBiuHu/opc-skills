# Subagent 编排执行准则

概念 Agent 和角色文件不会自行运行。主 Agent 只有在用户明确允许、子任务收益与 ownership 清楚时，才使用当前会话提供的工具；授权复用见[授权规则](authorization.md)。

## 1. 发现当前能力

读取当前会话暴露的工具名称、说明、参数 schema、并发限制和结果通道，不从历史工具名推断接口。

- 核对创建、观察/等待、通信/继续及必要时中断能力；不同宿主的 namespace、参数、返回 ID 和等待语义可能不同。
- 不依赖旧固定 namespace，不用 shell、hooks、npm 或伪 CLI 启动子代理。缺少创建或结果获取能力时主 Agent 独立完成并说明限制，不重复调用不存在的接口。
- 没有公开 close 能力就不虚构关闭接口；中断不能当成关闭/删除，是否需要回收按真实说明处理。
- 工具可用不等于获得授权。讨论接口、角色或测试方案不自动允许实际派生子代理。
- 只传 schema 支持的模型、reasoning、fork/context 或 agent type 参数；默认沿用会话模型设置，最小化上下文，不搬运旧字段。

### collaboration 工具的条件示例

仅当当前会话实际暴露以下工具和字段时使用；其它宿主映射到自己的 schema。

| 目的 | 工具示例 | 语义 |
|---|---|---|
| 创建独立任务 | `collaboration.spawn_agent` | 使用实际 task_name/message 等字段，保存返回的真实 ID |
| 补充执行中任务 | `collaboration.send_message` | 发送约束，不假定会启动空闲代理 |
| 让已有代理继续 | `collaboration.followup_task` | 按说明启动/恢复新一轮任务 |
| 等待通知 | `collaboration.wait_agent` | 读取随后真实消息/结果，等待结束不等于任务成功 |
| 查询状态 | `collaboration.list_agents` | 按需查询，不高频轮询 |
| 中断当前执行 | `collaboration.interrupt_agent` | 不冒充关闭或删除 |

上述 schema 确实可用且用户已授权时，任务包可以映射为：

```json
{
  "task_name": "frontend_review",
  "fork_turns": "none",
  "message": "按角色说明审查指定页面。任务包给出可读/可写范围、禁止事项、输出和验证；不执行发布、迁移或环境变量修改。"
}
```

这是参数形状示例，不是自动脚本，也不保证所有宿主都有这些字段。

## 2. 启动前检查

1. 复用本会话已明确的 Subagent 授权，没有授权不启动。
2. 子任务独立，能够并行提速、降低遗漏、提高审查质量或隔离专业上下文。
3. 按任务读取 `agents/<role>-agent.md`，用 `templates/subagent-task-brief-template.md` 写清目标、最小上下文、ownership、禁止事项、输出、验证和预期收益。
4. 可读/可写范围与其它 worker 不重叠，输出可快速验收集成。
5. 不分派生产发布、生产回滚、迁移执行、环境变量修改或破坏性清理；Data/Migration 只设计脚本，不执行生产迁移。
6. 使用实际 schema 发起调用，保存返回 ID；不编造类型、额度或未返回的代理。

小 bug、单文件小修、目标或根因不清、写入范围重叠、产出无法验收时不拆分；复杂任务也必须先满足以上条件。

## 3. 协作与结果复核

- 主 Agent 继续不重叠工作，只在依赖结果时等待；超时参数和沟通频率按宿主约束，不复制旧示例。
- 创建成功、状态通知和等待返回不代替完成证据。通过实际消息、结果或游标分清完成、失败、仍运行和需要输入。
- 补充信息使用通信能力，继续任务使用真正的继续能力；方向错误时再调用中断工具。
- 按 `templates/subagent-result-template.md` 检查目标、ownership、无关改动、分层边界、验证命令、失败解释和风险，再集成复验。
- 主 Agent 保留目标澄清、架构最终决策、跨层边界、发布、集成、复验和最终汇报责任。
- 记录预期/实际收益、冲突或重复工作及下次是否继续使用同类子任务。

## 官方依据与边界

[OpenAI Multi-agent 文档](https://developers.openai.com/api/docs/guides/responses-multi-agent) 描述派生、通信、继续、等待、状态和中断等动作；具体工具仍以当次宿主 schema 为准。本文不创建 API 请求、不启用额外功能，也不扩大执行权限。
