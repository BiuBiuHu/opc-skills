# 发布完整性与主干归位

本参考用于 `release-gated` 模式。它把“没有漏发关联系统”和“部署版本已经进入主干并能被其它 worktree 获取”定义为同一个可核验闭环。

## 0. 发布目标、环境与真实验证

先读取 [Code PR 与 Release PR 生命周期](release-pr-lifecycle.md)，按其顺序区分方案批准、预发、代码合并、生产和 Release PR 核销。以下为每次发布必须保留的执行检查。

- 发布目标确认门禁：当用户只说“发布”“部署”“上线”“发一下”等，没有明确说明目标环境时，必须先停下来询问“发布到预发还是线上？”。禁止自行默认预发、默认线上或同时发布两个环境。只有用户明确指定目标环境后，才能执行对应部署流程。
- 禁止本地工作区直接部署：不支持、也不得执行“从未提交本地工作区直接打包部署”。无论预发还是线上，部署输入必须来自可追踪的 Git commit、PR/CR 分支、CI 构建产物或明确归档的构建包。工作区存在未提交改动时，必须先停止部署，要求完成 commit/CR 或选择明确的回滚/暂存策略。禁止用 `vercel deploy`、手动上传、压缩包等方式把未提交代码直接发布到任何共享环境。
- 代码保存门禁：发布前相关改动必须已经 commit，并能通过 commit hash、分支名、PR/CR 或构建产物追溯。若用户要求紧急修复，也必须先创建 hotfix 分支并提交，再按预发验证、CR/审批、生产发布执行；不得“先线上发布后补提交”。
- 预发门禁：必须先部署到预发环境，且确认预发项目、预发域名、预发 API、预发数据库/schema、预发下游服务没有混用生产环境。
- 测试报告门禁：预发通过后，必须产出或更新测试报告，记录测试环境、账号、版本/deployment、用例、命令、结果、失败项和证据路径。报告建议写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/05-testing/test-report.md`；若项目已有固定测试报告路径，沿用项目路径。
- Code Review 门禁：生产发布前必须发起 CR/PR 或生成 code review 记录，说明变更范围、风险点、验证结果、回滚方案和 reviewer/审批状态。记录建议写入 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/04-engineering/code-review.md`；若使用 GitHub/GitLab PR，最终回复必须给出 PR/CR 链接。
- 线上发布门禁：只有预发验证通过、测试报告完成、CR/PR 已创建或已审核后，才能部署生产。生产部署后必须做线上 smoke test，并把生产 deployment、线上域名、验证结果和残留风险补回测试报告或运维记录。
- 环境隔离门禁：所有部署命令必须明确目标环境和目标项目。禁止在未确认 Vercel/云项目 link、deployment target、环境变量、数据库 host/schema 的情况下执行发布。预发与线上部署记录必须分别列出，不得用同一条结果混写。
- 真实入口清单门禁：项目真实域名、登录入口、主服务/BFF、Auth 服务入口、第三方 provider callback、业务回跳、固定 alias 和 deployment 快照不得写入通用 skill；必须从项目文档仓库的 `runtime-entry-inventory.md` 或等价入口清单读取。发布前逐项核对客户端实际入口、BFF URL、provider callback URL、callback alias、目标云项目、deployment ID、commit、target、DB/schema 和回滚点；每个 callback 域名必须单独 `inspect`，不能只检查同一项目的默认 Production alias。将本次候选复制到 `release-plan.md` 冻结；alias、deployment、commit 或入口变化后重新审批。若项目没有入口清单，先在项目文档仓库建立，不得把临时聊天记录当作长期事实源。
- 低流量生产观察门禁：当生产用户少、功能未开量或观察窗口内自然请求不足时，`0` 条错误日志只能说明“未观察到错误”，不能证明链路健康。必须使用受控、可重复、无破坏性的合成探针主动覆盖本次主链路和相邻高风险路径，同时检查 runtime 日志；探针不得重复触发付费、发送、绑定、解绑、迁移或其它不可逆副作用。探针账号、凭据和 token 不得写入仓库或报告。
- Release PR 最终核销门禁：涉及生产用户路径、数据写入或第三方回调时，最终核销至少包含真实用户或受控真实账号验证、合成探针、DB after/副作用检查、日志观察窗口和 alias/deployment 漂移检查。缺少任一适用证据时 Release PR 保持 open；不适用项必须写明理由，不能静默跳过。
- 线上失败暂停门禁：用户报告线上失败或 P0/P1 探针失败后，立即暂停 Release PR 合并、观察核销和后续切流。先从客户端实际 URL、请求 host、callback URL、runtime 日志和云平台 inspect 定位请求真实命中的 project/deployment/commit，再判断代码、环境、数据或第三方根因；禁止在未确认命中版本时继续改业务代码或宣布观察通过。

**生产发布后必须完成线上回归，回归通过前禁止宣布发布完成。** 线上回归必须基于固定生产域名和受控生产测试账号，覆盖本次变更、所有已发布关联系统的契约、P0 核心用户路径、相邻高风险路径、环境隔离、数据库/队列副作用和关键失败路径；不能用 health check、构建 Ready 或单页 smoke 代替。测试用例、命令、结果、截图/API/日志证据必须写回 `05-testing/test-report.md` 和 `06-ops/release-plan.md`。任一 P0/P1 回归失败时，立即停止后续切流和发布核销，按发布方案回滚受影响系统，完成根因修复后重新走预发、发布评审、生产部署和线上回归。只有矩阵系统全部核销、线上回归通过并完成观察窗口，发布状态才能标记为 `complete`。

预发报告存在失败项时，先修复或由用户明确接受风险，不得把失败报告当发布通过。生产发布涉及数据库迁移时记录命令、目标 host/schema、结果与回滚；按依赖顺序先服务后客户端，不夹带未审批系统。iOS/TestFlight/App Store 目标按 `ios-release` 执行；旧名称只作兼容入口。

## 1. 发布状态机

每次共享环境发布都必须按以下状态推进，不能跳状态：

```text
discovered
-> impact-mapped
-> release-plan-awaiting-review
-> release-plan-approved
-> candidate-frozen
-> preview-verified
-> default-branch-merged
-> production-deployed
-> post-release-reconciled
-> worktrees-synchronized
-> complete
```

- `impact-mapped`：已从用户入口沿真实调用链完成依赖闭包盘点。
- `candidate-frozen`：所有候选仓库的实现 commit、配置快照、迁移和产物映射已写入发布方案；任何变化都会使审批失效。
- `default-branch-merged`：所有包含本次代码或生产配置候选的仓库，Code PR 已合入各自远端默认分支，并记录精确 merge commit。
- `post-release-reconciled`：矩阵每一行都有实际 deployment/产物、源码 commit、固定入口、验证、监控和回滚点。
- `worktrees-synchronized`：默认分支的远端和本地 worktree 已核对；其它 worktree 的落后或脏状态已处理或明确阻断。

`complete` 不是“主服务部署成功”的同义词。任一系统、默认分支、deployment 映射或 worktree 未核销，都必须保持 `blocked` 或 `partially-released`。

## 2. 依赖闭包盘点

**每次共享环境发布必须先完成发布方案评审，禁止只发布眼前仓库。** 任何预发、生产、灰度、TestFlight、Worker 或多服务发布，在执行部署前都必须创建或更新 `<PROJECT_ROOT>/docs/<FEATURE_NAME>/06-ops/release-plan.md`，并使用 `templates/release-plan-template.md`。发布方案必须读取 `references/release-integrity.md`，从用户入口沿真实调用链递归盘点客户端、主服务、认证、AI、邮件、Worker/Cron、后台、数据库、对象存储和第三方配置；同时从每个候选仓库的 `base...head` 变更反向扫描 API、事件、队列、Webhook、共享包、迁移、环境变量、部署/IaC 和定时任务，形成“关联系统发布矩阵”。“客户端不直连内部服务”不能作为排除主服务下游依赖的理由。矩阵中的每个系统都必须明确仓库、默认分支、云项目、域名、当前版本、实现/head commit、默认分支 merge commit、deployment/产物 commit、是否已归并默认分支、发布决策、判断依据、依赖、顺序、环境变量、数据迁移、验证和回滚；每个系统的决策只能是“发布”“不发布（证据）”“本次已在前置版本发布”或“阻断”，不能留空、待定或只写“依赖上游”。没有改动的系统也必须以“不发布 + 证据”记录，禁止因未列出而默认遗漏。发布前必须做一次从下游回到用户入口的反向闭包复核，孤立行、未确认 owner、未知调用方向或未知部署目标都阻断。评审状态只能为 `awaiting-review`、`approved` 或 `rejected`；未取得用户或指定 reviewer 的明确 `approved` 前禁止部署。候选 commit、系统范围、迁移、环境或发布顺序发生变化时，原审批失效，必须重新评审。部署完成后必须把实际 deployment、commit、smoke、监控和回滚点回填发布方案，并逐项核销矩阵，不能只报告客户端或主系统成功。


### 2.1 事实源和扫描顺序

发布前读取项目的 runtime entry inventory、架构调用图、部署配置、环境变量清单、API/事件契约和仓库依赖文件。不得只根据用户点名的仓库或当前打开的工作区判断范围。

从用户实际入口开始，按以下顺序递归追踪：

1. 客户端/Web/后台入口及其固定 API、认证回调和业务回跳。
2. 网关/主服务的同步调用、异步任务、队列、Cron、Webhook 和 service-to-service URL。
3. Auth、AI、邮件、Worker、数据服务、对象存储、数据库、第三方 provider 及其配置 owner。
4. 构建和部署依赖：共享包、镜像、基础设施、迁移、feature flag、缓存键和定时任务。

### 2.2 变更反查

对每个候选仓库执行 `git diff <base>...<head>` 或等价的 PR 变更扫描，并检查：

- 源码 import/调用、API route、OpenAPI/schema、事件 topic 和队列消费者；
- `package`/lock、镜像、构建脚本、部署配置、IaC 和运行时入口；
- 环境变量名、数据库 migration、缓存/对象存储键、Cron/Webhook 配置；
- 客户端 base URL、provider callback、共享类型或协议版本。

扫描结果必须回填发布方案的“变更来源与影响面”表。发现无法确认 owner、调用方向、兼容性或部署目标时，结论只能是 `blocked`，不能用“暂不确定”当作“不发布”。

### 2.3 每个系统必须有决策

关联系统矩阵的每一行都必须填写：`发布`、`不发布（证据）`、`本次已在前置版本发布` 或 `阻断`。不允许空白、`待定` 或只写“依赖上游”。

“不发布”必须给出可复核证据，例如：候选前后 commit/config/API/事件 schema 无变化，且当前线上版本满足兼容约束。只写“看起来不影响”“客户端不直连”不算证据。

发布前由主 Agent 做一次反向复核：从矩阵中的每个下游系统反查是否能回到用户入口；无法回到入口的孤立行、未列出的下游或只有口头说明的依赖都要重新核对。

## 3. 部署前候选冻结

- 共享环境部署输入必须是已提交且可追踪的 commit、Code PR、CI 构建产物或归档包；工作区有未提交改动时阻断。
- Preview 可以使用已审批的 PR head，但必须写明候选 head commit 和不先合并的理由。
- Production 必须先合并所有代码/生产配置候选的 Code PR，再部署精确 merge commit 或可验证映射的构建产物。不得“先线上发布，之后再补 main/master”。
- 候选 commit、矩阵系统、迁移、环境、发布顺序、固定 alias 或构建映射变化后，原审批立即失效，重新从 `impact-mapped` 开始。
- 部署命令执行前再次运行 `scripts/check_release_integrity.sh`（或项目等价检查），并把输出摘要写入 evidence manifest。

## 4. 部署后主干与 worktree 归位

对每个受影响仓库分别执行，不得只检查当前仓库：

1. 用 `git merge-base --is-ancestor <merge-commit> origin/<default-branch>` 证明远端默认分支包含候选 merge commit。
2. 用云平台/CI inspect 证明 production deployment 的源码 commit 与该 merge commit 一致；只有产物摘要、deployment URL 或“Ready”不够。
3. 列出 `git worktree list --porcelain`。所有位于默认分支的 worktree 必须 `git pull --ff-only` 后与远端默认分支同一 HEAD，且无未提交改动。
4. feature/hotfix worktree 不得被强制覆盖。若它有未提交改动，先保存并记录；若它落后于本次默认分支，下一次开发前必须 rebase/merge 或重新从同步主分支创建，不能直接继续叠加。
5. 记录仓库、默认分支、远端 HEAD、本地 HEAD、deployment commit、每个 worktree 的路径/分支/HEAD/脏状态和处理结果。

默认分支未合并、deployment 映射不一致、默认分支 worktree 落后/脏、或无法确认远端状态时，发布状态保持 `blocked`，并明确下一动作；禁止以切换本地分支、刷新页面或重新部署掩盖问题。

## 5. 失败处理

- 发现漏发系统：暂停后续切流和 Release PR 核销，补齐矩阵，重新审批候选和顺序；已发布系统按回滚方案处理。
- 发现部署 commit 不在默认分支：不得直接在默认分支补一个无关 merge。先判断是否应回滚线上版本；修复后重新走 Code PR、候选冻结、部署和核销。
- 发现 worktree 有用户改动：不执行 `reset`、`checkout`、强制覆盖或删除。先建立 commit/stash/补丁保存点，之后再同步。
- 线上 P0/P1 失败：停止核销，按方案回滚受影响系统；修复后重新经过预发、审批、生产部署和线上回归。

## 6. 最小证据

发布方案和 evidence manifest 至少保存：

- 依赖闭包来源、扫描命令、候选 base/head commit 和矩阵逐行决策；
- 每个仓库的 Code PR、默认分支 merge commit、deployment/产物 commit 和映射证据；
- 每个环境的 project、固定域名/alias、target、数据库/schema 和实际 deployment；
- `check_release_integrity.sh` 输出、worktree 列表、`git pull --ff-only` 结果和脏状态处理；
- 漏发/漂移/失败时的阻断、回滚、修复和复验记录。

## 7. 最终汇报

发布最终回复必须列出发布方案及审批状态、关联系统核销、各仓库默认分支 merge commit 与 deployment/产物 commit、预发 deployment、测试报告、CR/PR 或自审路径、生产 deployment、线上 smoke、完整线上回归、跨仓库归位、观察窗口和残余风险。发布后内容生产另按 [可选旁路](post-release-content.md) 判定，不改变页面发布状态。
