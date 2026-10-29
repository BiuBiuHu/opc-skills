# 开源技术栈参考

## 编码前开源调研门禁

**编码前必须先查成熟开源方案。** 进入非平凡功能、交互、性能、基础设施、AI、认证、支付、搜索、图片/视频、缓存、队列、图表、编辑器、地图、上传下载、部署或测试自动化实现前，必须先搜索并评估可复用的开源项目、官方 SDK、成熟组件或行业通用方案。优先查看官方文档、GitHub/维护者文档、npm/包管理信息和现有项目依赖；对比维护状态、版本兼容、现有技术栈匹配、集成成本、性能、可访问性、回滚风险和自研替代成本。UI、手势、动画、图片加载、缓存和性能类问题禁止直接手写方案，除非调研后明确说明没有合适库或引入成本高于收益。调研结论写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/00-research/competitor-research.md`；bugfix fast-path 可写入 `04-engineering/debug-report.md` 或 `implementation-plan.md` 的开源调研小节。需要详细选型准则时读取 [open-source-stack.md](open-source-stack.md)。

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

应该自研项目差异化部分：

- 产品专属领域规则与状态机
- 无成熟方案可复用的第三方适配器
- 项目专属证据、审核与风控流程
- 产品核心交互和差异化体验

不应该自研：

- 浏览器运行时
- 工作流引擎
- 对象存储
- IAM 认证授权
- 指标和日志平台

## 通用技术取向


不要默认所有模块都自研。

默认技术取向：

- 浏览器自动化：Playwright / Crawlee
- MVP 任务队列：Postgres 任务队列
- 平台化工作流：Temporal 或 Kestra
- 结构化数据库：PostgreSQL
- 证据和文件存储：MinIO
- 可观测性：OpenTelemetry + Prometheus + Grafana + Loki
- 认证授权：Keycloak
- 后台 UI：Ant Design Pro / Refine

只自研项目差异化部分：

- 产品专属领域规则与状态机
- 无成熟方案可复用的第三方适配器
- 项目专属证据、审核与风控流程
- 产品核心交互和差异化体验


## 可复用 Skills


- `find-skills`：查找可借鉴的开源 agent skills；B 类页面、复杂交互、表格/筛选/批量操作和 UI 审计前优先使用
- `ui-ux-pro-max`：产品界面、设计系统、颜色、排版、响应式、可访问性和交互质量补充；B 类页面只能作为增强，不得替代效率目标和信息裁剪
- `ant-design`：Ant Design、Ant Design Pro、ProComponents、Table、Pagination、Form、权限路由和后台组件选型
- `ui-audit`：Web UI 发布前审计，覆盖可访问性、交互、表单、排版、布局、性能、动效和文案
- `test-agent-orchestrator`：测试工作流入口
- `test-case-designer`：测试计划和测试用例设计
- `test-execution-runner`：测试执行和报告
- `ios-release`：iOS 客户端发布，覆盖 TestFlight、App Store Connect、App Store 提审、签名、archive/exportArchive 和 IPA 上传；`ios-testflight-release` 只作为旧名称兼容入口
- `blog-writing`：文章素材采集、选题、双语写作、去 AI 味、SEO/GEO 和博客落盘；项目存在该 skill 时可复用，但必须先过滤项目专属路径和事实
- Cloudflare：用户选择 Cloudflare 时使用 [cloudflare-deployment.md](cloudflare-deployment.md)，按现有工具选择 Wrangler、API 或已登录浏览器
- `deploy-to-vercel` 或 `vercel-deploy`：当前端明确选择 Vercel 时使用，不覆盖用户的平台选择
