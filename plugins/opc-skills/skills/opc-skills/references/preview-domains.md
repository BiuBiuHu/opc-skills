# 预发入口与命名

预发使用部署平台原生域名，不绑定业务自有域名或新增业务域名DNS/Custom Domain。若当前任务明确要求例外，遵循用户的具体指令，并在项目发布方案中记录；不要把历史遗留自定义域名当成本次默认授权。

## 选择地址

- 名称表达项目与环境，采用短小的英文或拼音、连字符及`preview`；避免把日期、任务ID、完整分支路径或随机hash作为给用户的唯一入口。冲突时使用有意义的短后缀，不改账户全局域名来缩短一个项目地址。
- Cloudflare Workers：命名为`<project>-preview`，使用实际返回的`<project>-preview.<account-subdomain>.workers.dev`。Pages：使用专属预发项目的`<project>-preview.pages.dev`或平台生成的可读分支别名。不得为了名称好记改用业务自定义域名。
- Vercel：使用`.vercel.app`，优先可读且稳定的分支URL或平台支持的别名。可缩短项目名与预发分支名；保留唯一deployment URL作为版本证据。不要凭格式编造可访问地址，也不要为缩短URL而启用付费自定义后缀。

## 核对环境

域名包含`preview`不证明环境隔离。核对实际项目、deployment target、commit、绑定、变量与数据库/schema，并回读固定入口指向的deployment。Vercel原生域名也可能指向Production；不得通过`--prod`或promote获得好记的预发URL。Worker默认服务环境字段也不代替项目级预发隔离判断。

保留既有Access或Deployment Protection。新入口先配置必要的保护，再对外提供，并分别验证匿名访问限制、授权页面/API、静态资源和实际业务路径。回调、CORS或采集地址受影响时，只更新本次范围内的配置，不关闭保护解决连通问题。

## 替换已有入口

盘点该入口的所有者、DNS/Custom Domain、证书、访问策略、回调与采集调用方。先发布并验证新的原生入口，再切换项目文档和测试脚本；按用户授权移除旧自定义绑定及本次专属DNS/证书，复核无残留。未获授权时不批量迁移其它项目或清理共享策略。

记录主入口、实际deployment URL/ID、源码commit、环境、保护方式与回滚路径。新旧原生地址需要兼容时可保留受保护的旧入口，但不再将难读的旧地址作为主入口。

官方依据（执行时核对当前平台行为）：[Cloudflare workers.dev](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/)、[Pages预览](https://developers.cloudflare.com/pages/configuration/preview-deployments/)、[Vercel生成URL](https://vercel.com/docs/deployments/generated-urls)。
