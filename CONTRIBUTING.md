# Contributing

欢迎贡献 issue、文档改进、模板优化和工作流建议。

## 基本要求

- 保持内容通用，不写入私有项目名、客户名、内部服务名或真实环境地址。
- 不提交密钥、token、账号密码、数据库连接串、生产日志、客户数据或私有部署 URL。
- 修改 `SKILL.md` 时，优先保持规则可执行、可验证、可落盘。
- 修改模板时，避免空泛字段，确保 Agent 可以按模板产出可执行文档。

## 提交流程

1. Fork 本仓库。
2. 创建 feature branch。
3. 修改后运行敏感词扫描。
4. 提交 PR，并说明变更范围、使用场景和兼容影响。

建议扫描命令：

```bash
rg -n -i "secret|token|password|api[_-]?key|apikey|private|credential|prod|production|staging|数据库|schema|host|客户|内部" .
```

扫描结果需要人工判断。命中通用文档词不一定是问题，但真实值必须删除。
