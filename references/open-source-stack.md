# 开源技术栈参考

## 推荐技术栈

MVP 阶段：

- 前端：React + Ant Design 或 Refine
- 后端：FastAPI
- 队列：Postgres `SKIP LOCKED`
- Worker：Python
- 浏览器：先复用现有 Selenium，再迁移到 Playwright / Crawlee
- 存储：Postgres + MinIO

平台化阶段：

- 工作流：Temporal 或 Kestra
- 浏览器：Playwright / Crawlee
- 可观测性：OpenTelemetry + Prometheus + Grafana + Loki
- 认证授权：Keycloak

## 自研边界

应该自研：

- 广告提取适配器
- 标准化广告模型
- 证据链关联
- 复核和 IB 核验流程
- 风险评分
- 国家优先级和节点策略

不应该自研：

- 浏览器运行时
- 工作流引擎
- 对象存储
- IAM 认证授权
- 指标和日志平台
