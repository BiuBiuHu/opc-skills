# 发布完整性与主干归位

本参考用于 `release-gated` 模式。它把“没有漏发关联系统”和“部署版本已经进入主干并能被其它 worktree 获取”定义为同一个可核验闭环。

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
