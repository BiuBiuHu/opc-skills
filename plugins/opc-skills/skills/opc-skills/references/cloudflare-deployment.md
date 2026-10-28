# Cloudflare 部署与迁移

适用于用户选择 Cloudflare（含 cloudfare 拼写）、官网/博客/SPA 静态托管，以及 Pages、Workers Static Assets 或边缘代理迁移。先读取本项目事实源与发布方案；真实账号、域名、仓库、项目名和凭据不能写入本参考。

## 平台与运行形态选择

| 情况 | 选择与约束 |
|---|---|
| 已有 Pages 项目 | 优先沿用；核对 Git integration / Direct Upload、生产分支和 Functions，迁移不是默认要求 |
| 新静态站点、频繁发布 | 评估 Workers Static Assets；可在本地或 CI 构建后由 Wrangler 上传，静态请求默认先命中资源 |
| SPA | 明确客户端路由 fallback；`single-page-application` 只能用于 SPA，不能用于博客和多页官网 |
| Astro/Vite 静态博客、MPA | 保留真实 404、canonical、尾斜杠策略、历史重定向、RSS/sitemap、robots/llms 和语言路径 |
| SSR / Node 后端 | 先验证框架适配、Node API、原生依赖、数据库、连接池、定时任务和 CPU 预算；不能把现有 Node 服务当成静态目录直接上传 |
| 用户只迁前端，保留后端 | 盘点 `/api/*`、OAuth、写作发布、评论、上传和观测路径；明确保留原后端的路由方式，禁止连带改部署或搬运服务端密钥 |

配额必须从执行当日官方文档核对。区分 Pages 构建次数、Workers Builds 构建分钟、上传/API 速率、静态请求与 Worker 调用、CPU、文件大小和数量；禁止宣称“免费无限部署”。外部 CI 只是把构建资源移出 Cloudflare，CI 自身和上传仍有额度。

## 发现与权限

- 识别账号、account ID、zone、站点、默认分支、当前生产版本、Wrangler 与 lockfile。优先使用已有 connector/API/CLI；需要已登录会话时使用可用浏览器 skill。
- 读取 DNS、proxy 状态、Worker Routes / Custom Domains / Pages custom domains、证书和原平台 alias。Cloudflare DNS/CDN 已代理不等于源站已迁到 Cloudflare。
- 优先使用现有受限部署凭据；需新增时只授予目标账号/zone 的必要权限，凭据写入 CI secret 或用户指定的安全位置，禁止输出到日志、提交或构建静态包。
- CI secret 通常使用 `CLOUDFLARE_API_TOKEN`，账号通过 `CLOUDFLARE_ACCOUNT_ID` 注入；真实值属于项目配置。GitHub token、写作口令和数据库密码继续留在所属服务端。
- Wrangler 固定到已验证版本，提交 lockfile；安装失败时读取依赖原因，选择可用的兼容版本，不能跳过校验发布。

## Route 和 Custom Domain 不能混用

| 形态 | 适用方式 |
|---|---|
| Worker 是完整源站 | Custom Domain；先检查现有 CNAME 冲突，记录 DNS 替换与证书验证、回滚 |
| 保留外部源站，Worker 在前面 | Worker Route + proxied DNS；保留原 CNAME，按路径回源现有后端 |
| Pages | 在项目绑定域名，按官方要求验证 CNAME；不能只改 DNS 就宣布绑定完成 |

Routes 的同 zone `fetch(request)` 会按 DNS 回到外部源站；Custom Domain 自身就是源站，同样的回源写法可能再次进入 Worker。设计回源时必须明确是哪种路由，避免循环。预览域名与生产域名不能盲目互相 fetch；必须验证实际线上路径。不能将受 Vercel Deployment Protection 保护的默认 deployment URL 当作公开后端而不测试，也不能擅自关闭原访问保护。

## 配置和构建

- 检查 `assets.directory`、`binding`、`compatibility_date`、`main`、`workers_dev` 与显式环境。预览配置不携带生产 routes/custom domains；生产域名切换只在预览验证之后执行。
- 静态资源优先，不要为所有请求设置 `run_worker_first: true`。仅 `/api/*` 等确需动态处理的路径进入 Worker；代理接口和敏感响应禁止缓存。
- `vercel.json` 的 redirects、rewrites、headers、functions 和 cron 不会自动迁移。逐项分类：静态规则转换、边缘适配、继续回源或明确不适用。不能把所有 rewrite 都当成重定向。
- 保留 URL、query、HTTP 方法、body、必要鉴权、响应状态和 Location；跨源重定向默认手动处理，避免将凭据自动转发到未知目标。
- 代理 origin 固定在服务端配置，不能让请求参数指定任意上游。预览若必须读保留的生产后端，要在方案中声明只读例外并拦截写请求；不能用真实发布、删文章或新增评论试探链路。
- 平台专属 analytics、Speed Insights 和函数入口要逐项适配。保留 GA 等独立观测；不能用 SDK “不报错”代替确认采集成功。
- 部署输入必须来自已提交版本。记录 source commit、构建任务、产物摘要、Worker version/deployment ID 和入口；版本指纹不能包含密钥。`wrangler deploy --dry-run` 只验证打包，不等于已经部署。

## 发布与验收

沿用本 skill 的发布完整性、测试、Code Review 和现有授权规则。用户已明确要求将指定现网站点迁移到 Cloudflare 时，先完成可逆准备、构建、审查和回滚方案；不要因改用 Cloudflare 增加重复平台选择或额外确认。出现范围扩大、付费升级、无法回滚或缺少访问权限时，再说明具体缺口。不要把静态站点迁移扩展为后端、数据库或移动/桌面客户端发布。

1. 备份旧 DNS/proxy、route、alias、部署版本与构建配置，建立保存点。
2. 从可追踪 commit 构建，先 dry-run，再发布隔离预览。预览开启 `noindex`，关闭生产 telemetry 和写操作。
3. 验证首页、各语言、深链接、刷新、静态图片/字体/CSS/JS、404、历史文章跳转、canonical/hreflang、robots、sitemap、RSS，以及保留 API 的只读健康/未授权失败响应。
4. 代码按既有门禁进入默认分支，冻结精确生产 commit 和构建映射。按批准范围设置生产 route/domain/proxy；不要修改无关域名、后端项目、数据库、R2 或第三方回调。
5. 用生产固定域名复测，读取平台 version/deployment、检查实际 source commit。`Server: cloudflare` 只能说明经过 CDN，不能单独证明迁移成功。
6. 核验后续发布链路：写作提交、默认分支 push 或指定 CI 确实发布到 Cloudflare。若原平台仍自动构建，按范围停掉前端重复构建，保留旧部署和 API；停止自动构建与删除项目是不同动作。
7. 持续回填同一份发布方案和测试报告，逐行说明已迁前端、保留后端、配额及回滚状态。

## 回滚

- Route 模式：撤销本次新增的站点 Route，保留原 CNAME；需要时恢复原 proxy 值。先验证原站点/API，之后再暂停 Cloudflare CI。
- Custom Domain / Pages 模式：按旧 DNS 和 alias 快照恢复入口，等解析与证书生效；不能只删除 Worker 让域名失效。
- 保留最近稳定 Worker 版本，可按官方 Wrangler/API 回滚；版本回滚不能代替错误 DNS、绑定或后端状态的修复。
- 未完成生产域名和自动发布验证时，报告“已准备/已预览”，不得写“迁移完成”。

## 官方资料

执行时重新核对（本参考校验于 2026-10-28）：

- [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/)
- [静态资源计费](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/)
- [Workers Builds 额度](https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/)
- [Pages 限制](https://developers.cloudflare.com/pages/platform/limits/)
- [Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [HTML 路径策略](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/)
- [Worker Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
