# Subagent Task Brief

> 主 Agent 在调用 `multi_agent_v1.spawn_agent` 前填写。本文件是模板，不会自动启动 subagent。

## 角色

- 目标 subagent：`Explorer | Frontend | Backend | QA/Test | Integration | DevOps`
- Runtime 类型：`explorer | worker | default`

## 为什么要拆

- 用户是否明确允许 subagent/多 Agent/并行执行：
- 预期收益：`并行提速 | 降低遗漏 | 提高审查质量 | 隔离专业上下文`
- 不拆的风险：
- 是否有不适合拆分的因素：

## 业务目标

- 用户真正要完成的结果：
- 不能发生的副作用：
- 当前 feature/doc 路径：

## 当前上下文

- 项目根目录：
- 当前分支/commit：
- 已确认的目标澄清结论：
- 已确认的架构边界：

## Ownership

- 可读范围：
- 可写范围：
- 禁止修改范围：
- 不能执行的命令或动作：

## 任务

1. 
2. 
3. 

## 验证要求

- 必须运行的命令：
- 必须提供的截图/API/日志/数据库/对象存储证据：
- 可以不验证的内容及原因：

## 输出格式

使用 `templates/subagent-result-template.md` 的格式返回。

## spawn_agent 消息骨架

```text
你是 OPC <ROLE> Agent。你不是独自在代码库里工作，不要 revert 他人改动。

业务目标：
- 

预期收益：
- 

当前上下文：
- 

Ownership：
- 可读：
- 可写：
- 禁止：

架构边界：
- 客户端只能调用主服务/API server。
- 内部服务只接受受控 service-to-service 调用。
- AI/生成类能力必须先低成本预览和缓存复用，再触发昂贵生成。

任务：
- 

验证：
- 

输出要求：
- 按 subagent-result-template 返回。
```
