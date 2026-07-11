# 开源技术栈参考

## 编码前开源调研门禁

非平凡实现前必须先调研成熟开源项目、官方 SDK 或行业通用方案，尤其是 UI 交互、手势、动画、图片/视频、缓存、虚拟列表、编辑器、图表、地图、认证、支付、搜索、队列、监控和测试自动化。

调研必须记录：

- 需求对应的成熟能力是什么，不要只搜项目名。
- 候选方案的官方文档或维护者文档链接、仓库/包链接、当前调研日期。
- 维护状态：最近发布时间、Issue/PR 活跃度、是否有维护者风险。
- 兼容性：当前框架版本、运行时、Expo/RN/Node/Python/DB 版本、是否支持现有架构。
- 集成成本：是否引入 native 依赖、迁移成本、包体/性能影响、测试成本、回滚方式。
- 适配性：是否覆盖核心问题，是否会改变产品交互，是否能满足可访问性和错误态。
- 决策：直接复用、局部借鉴、自研、暂缓；拒绝方案必须写明理由。

产物位置：

- 完整需求：`<PROJECT_ROOT>/docs/<FEATURE_NAME>/00-research/competitor-research.md`
- bugfix fast-path：可写入 `04-engineering/debug-report.md` 或 `04-engineering/implementation-plan.md` 的“开源调研”章节

React Native / Expo 交互和图片类任务的默认候选：

- 图片渲染与缓存：优先查 `expo-image`、项目已有文件缓存、CDN/OSS 缓存头；不要重复生成图片。
- 分页/滑动：优先查 `react-native-pager-view`、`react-native-reanimated-carousel`、项目已有 `gesture-handler`/`Animated` 写法。
- 虚拟列表：优先查 `FlatList`、`SectionList`、`@shopify/flash-list`。
- 动画：优先查 `react-native-reanimated`，只有简单动画才使用 RN `Animated`。
- 维护风险明显的库，例如长期不更新、维护者明确求接手、依赖旧架构或旧 React 的库，只能作为参考，不应直接引入。

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
