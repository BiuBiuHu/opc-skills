# Auth Login E2E Guidance

认证、验证码、OAuth、账号绑定和会话持久化是高风险链路。测试目标不是证明接口能返回 2xx，而是证明真实客户端能稳定进入登录后业务状态，并且用户身份、token 和数据归属一致。

## 适用场景

在以下任一场景必须使用本参考：

- 邮箱验证码登录、注册、验证码冷却、防刷或邮件发送链路。
- GitHub、Apple、Google、Facebook 等 OAuth 登录、绑定、解绑和回调。
- auth code、id token、access token、refresh token、userinfo/current user。
- 登录态持久化、冷启动恢复、token 刷新、退出登录、账号合并。
- 客户端、网关、auth-service、数据库或第三方 provider 任一层有改动。

## P0 闭环

必须按顺序验证并记录证据：

1. 客户端从清状态启动，确认目标环境标签、API baseURL 和构建版本正确。
2. 自动输入测试账号并触发登录或发送验证码；按钮 Loading 和冷却只作为过程证据。
3. 从服务端可观测来源获取验证码或 OAuth 结果，例如数据库 hash 反查、受控日志、测试邮件平台或 provider 测试账号。
4. 输入正确凭证并提交，记录 verify、token exchange、current user/userinfo 的请求结果。
5. 使用稳定业务断言证明登录成功，例如首页标题、用户头像、设置页账号信息或业务数据加载成功。禁止用“登录按钮消失”“Loading 出现/消失”“页面跳了一下”作为通过断言。
6. 检查客户端持久化：access token、refresh token、过期时间、login provider、当前环境作用域 key。不得输出完整 token 或 secret。
7. 终止并重启客户端，验证冷启动仍保持登录，并最终拿到同一个业务用户。
8. 验证用户身份一致性：token `sub`、core user id、业务数据 owner、头像/昵称显示不能在初次登录和冷启动之间分裂。
9. 验证服务端副作用：验证码被消费、attempts/冷却正确、identity 绑定状态正确、不会跨环境写库。
10. 将失败归因到客户端、网关/主服务、auth-service、数据库、第三方 provider、配置、旧构建/缓存或网络。

## 最小状态矩阵

认证测试至少覆盖以下状态。无法执行的项必须说明原因和风险：

| 状态 | 必测断言 | 证据 |
| --- | --- | --- |
| 发送验证码 | 格式校验、Loading、冷却、防重复点击 | 客户端截图、请求状态、验证码记录 |
| 验证码正确 | verify 成功、验证码被消费 | API 响应、DB 行删除或状态变化 |
| 验证码错误/过期 | 不签发 token、不进入首页、错误提示准确 | API 响应、截图、DB attempts |
| token exchange | access/refresh token 写入环境作用域 key | 脱敏 storage、JWT 非敏感 payload |
| current user | userinfo 失败时有明确 fallback 或失败策略 | API 状态、客户端日志、用户对象 |
| 冷启动 | 不回登录页，用户最终一致 | 重启截图、storage、current user 响应 |
| token 续期 | 快过期时 refresh，失败策略正确 | mock/接口响应、storage 更新 |
| OAuth 登录 | state/redirect 校验、回调换 token、用户一致 | provider 回调、API 响应、截图 |
| 绑定/解绑 | identity 状态正确，当前登录方式解绑后退出 | userinfo/DB、截图 |
| 跨环境 | 预发不打生产 API，生产不打预发 API | 网络日志、环境变量、构建产物 grep |

## 失败归因规则

- 客户端问题：按钮坐标/selector 错误、断言用了瞬时状态、旧 bundle、token 未持久化、错误地把可恢复 userinfo 失败当登录失败。
- 网关问题：CORS、路由前缀、环境 URL、Authorization 转发、错误码归一、fallback 契约缺失。
- auth-service 问题：验证码未写入/未消费、token 签发、userinfo 缺字段、provider identity 约束、redirect_uri/state 校验。
- 数据问题：账号缺 email identity、历史脏 identity、跨环境 schema、唯一约束或事务失败。
- 第三方问题：OAuth app 配置、callback URL、client id/secret、Apple team/key、GitHub scopes。
- 发布问题：TestFlight/生产包不是最新 commit、未清缓存、未记录 build number、从未提交工作区发布。

## 报告要求

`integration-report.md` 或 `test-report.md` 必须记录：

- 客户端类型、设备、系统版本、运行形态、构建号或 commit。
- 目标环境、API baseURL、网关域名、内部服务域名只允许出现在服务端配置。
- 测试账号、验证码来源、请求路径、状态码、关键响应字段和脱敏 token payload。
- 稳定业务断言截图、storage 检查、冷启动截图、服务端消费证据。
- 失败项、归因层级、修复点、复验结果和仍需服务端/配置处理的残余风险。
