# OPC Testing Guidance

本参考用于 QA Agent 编写测试策略、测试用例和测试报告。目标是让测试文档具备执行指导性，而不是只列检查项。

## 行业参考

- ISO/IEC/IEEE 29119：测试过程、测试文档、测试设计和风险驱动测试。
- ISTQB：风险驱动测试、黑盒/白盒/经验型测试技术、等价类、边界值、状态迁移、决策表。
- OWASP ASVS：认证、会话、访问控制、API 安全的可验证安全要求。
- OAuth 2.0 Security BCP / RFC 9700：OAuth/OIDC 类登录、回调、token、redirect、state、PKCE、客户端与服务端边界的安全验证。

## 测试策略必须回答的问题

每份 `test-strategy.md` 必须明确回答：

1. 本次到底要证明什么行为正确。
2. 哪些系统参与，分别怎么测。
3. 哪些风险最高，为什么进入 P0。
4. 每条 P0 case 的前置数据、操作步骤、期望结果、副作用断言和证据是什么。
5. 哪些 case 自动化，哪些必须人工，人工验证需要什么截图、日志或录屏。
6. 失败后如何归因到客户端、主服务、子服务、数据库、配置或第三方。

## 系统分层测试地图

测试文档必须按系统拆分，不允许只写“一起联调”：

- 客户端：页面入口、状态展示、表单校验、按钮 loading、防重复点击、导航、错误提示、缓存清理、网络请求目标、截图证据。
- 主服务/网关：路由转发、鉴权上下文、CORS、环境隔离、错误码归一、超时、重试、内部服务 URL 不泄漏。
- 领域/内部服务：核心业务规则、状态迁移、幂等、事务、并发、审计日志、回滚边界。
- 数据层：唯一约束、索引、迁移、脏数据兼容、fixture 清理、跨环境隔离。
- 第三方：OAuth/provider callback、签名/JWKS、redirect URI、state/nonce、失败回调、供应商不可用。
- 运维/发布：构建产物、环境变量、deployment、日志、监控、回滚、预发和生产 smoke。

## 用例最小字段

每条可执行 case 必须包含：

- `id`：稳定编号，例如 `API-001`、`FE-001`、`ENV-001`。
- `title`：一句话说明要证明的行为。
- `system`：客户端、主服务、identity-service、数据库、第三方、运维。
- `priority`：P0/P1/P2。
- `scopeType`：changed-feature、impacted-regression、core-smoke、full-regression。
- `preconditions`：账号、数据、配置、登录态、provider mock。
- `steps`：可执行步骤，不写“测试一下”。
- `expectedResults`：直接结果。
- `sideEffects`：明确不能发生的副作用。
- `evidence`：截图、请求/响应、数据库状态、日志、构建输出、trace。
- `automation`：自动化入口、API、selector 或说明必须人工。

## 测试设计技术

按需求选择测试技术：

- 等价类：有效/无效输入、不同角色、不同环境。
- 边界值：分页、长度、频率、验证码冷却、token 过期时间。
- 决策表：多个条件组合，例如登录方式、邮箱是否一致、provider 是否返回 verified email。
- 状态迁移：登录、绑定、解绑、退出、token 刷新、账号合并状态。
- 错误猜测：历史 bug、跨环境 URL、旧缓存、重复点击、并发提交。
- 安全验证：鉴权绕过、越权访问、OAuth state/nonce、redirect URI、secret 泄漏。

## 输出要求

测试策略必须包含：

- 测试范围和不测范围。
- 风险分级依据。
- 测试数据约定。
- 系统分层测试地图。
- P0 场景矩阵。
- 具体 API/前端/环境用例。
- 执行顺序。
- 验证命令。
- 证据要求。
- 失败归因规则。

结构化用例建议额外写入：

```text
<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-cases.json
```

JSON 只作为执行索引，Markdown 必须保留完整说明。
