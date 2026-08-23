# Code PR 与 Release PR 生命周期

## 目录

1. 目标
2. 对象定义
3. 标准时序
4. 失败分支
5. 用户沟通契约
6. 发布记录要求

## 1. 目标

把代码评审、发布方案审批、共享环境部署、真实验证和发布证据合并拆成不同动作。任何时刻都要让用户知道：当前对象是哪一个 PR、目标环境是什么、现在需要批准还是 merge、完成后会发生什么。

发布前同时读取 `references/release-integrity.md`。Release PR 不仅核对主服务和客户端，还必须承载双向影响闭包、逐系统发布/不发布证据、默认分支 merge commit、deployment 映射和 worktree 归位结果。

## 2. 对象定义

- **Code PR**：承载运行时代码、测试和实现文档。Preview 可以按已审批方案从 PR head 构建；Production 候选必须先合并到仓库默认分支，并从精确 merge commit 或可证明映射关系的构建产物发布。
- **Release PR**：承载 `release-plan.md`、测试报告、联调报告、evidence manifest 和部署核销证据。它不是运行时代码审核的替代品。
- **Release plan approval**：用户或 reviewer 对特定候选、范围、环境、顺序、迁移和回滚方案的明确 `approved`。它不是 PR merge。
- **Preview verification**：对已部署候选执行真实页面/API/DB/第三方闭环。`Ready` 不是验证通过。
- **Runtime entry inventory**：项目文档仓库中的真实入口清单，记录登录入口、BFF、Auth/service-only URL、provider callback、业务回跳、固定 alias 以及当前 deployment 快照。它是事实源；Release PR 只冻结本次候选，不把项目事实写进通用 skill。

### PR 创建语言

- 新建 Code PR、Release PR、文档 PR 和其它 PR 时，标题与正文默认使用中文。
- 正文中的范围、验证、风险、回滚、发布状态和检查清单均使用中文；代码标识、命令、路径、commit hash、API 名称和产品专有名词保留原文即可。
- 仓库规范明确强制其它语言，或用户明确指定其它语言时才例外；创建前说明原因。
- 执行 `gh pr create` 或等价操作后立即回读 PR，检查标题、正文、base/head 和状态，修正遗留英文模板或无意义的中英混排。
- 不因本规则批量重命名历史 PR；只有用户要求或本次工作需要主动重写时才修改已有 PR。

## 3. 标准时序

1. 保存并验证代码，创建 Code PR。
2. 明确候选策略：
   - Preview 允许使用可追踪的 PR head，在 release plan 中写明 head commit、构建来源和不先 merge Code PR 的理由。
   - Production 必须先 merge 所有关联仓库的 Code PR，再从各自远端默认分支读取精确 merge commit。
   - Production deployment 必须与默认分支 merge commit 相同，或提供源码 commit、构建任务和产物摘要之间的可验证映射。
3. 从同步后的主分支创建 release 分支，创建 Release PR；初始 release plan 为 `awaiting-review`。
4. 读取并核对项目 runtime entry inventory，向用户展示候选 commit、真实登录/BFF/callback/回跳入口、目标环境、发布矩阵、数据动作、验证路径和回滚点，请求批准 release plan。不要请求 merge Release PR。
5. 用户明确批准后，把 release plan 更新为 `approved` 并提交到仍为 open 的 Release PR。
6. 从已提交、可追踪的候选部署 Preview，记录 deployment ID/URL；不要先 merge Release PR。
7. 在固定 Preview 入口执行真实 E2E、API、DB、日志和观察窗口验证，并持续回填同一个 Release PR。
8. Preview 全部通过后，把验证证据回填仍保持 open 的 Release PR，并明确进入 Production 候选冻结；此时需要 review/merge 的对象是各关联仓库的 Code PR，不是 Release PR。
9. Preview 通过后，将所有包含代码或配置候选的 Code PR 合并到各仓库默认分支，冻结精确 merge commit；merge 结果改变候选时更新 Production release plan 并重新审批。
10. Production 使用单独的 release plan 版本、审批、deployment、回归和核销。Preview 的批准不能自动授权 Production；按依赖优先顺序先部署内部服务和主服务，再发布或放量客户端。
11. Production 低流量时执行无破坏性合成探针；仅有 `0` 条错误日志不算观察通过。客户端产物完成但依赖服务或跨系统契约未核销时，Release Train 保持 open。
12. 最终核销每个仓库的默认分支 merge commit、deployment/产物 commit、真实用户验证、合成探针、DB after、日志窗口和 alias/deployment 漂移；适用证据完整后才 merge Release PR。
13. Release PR merge 后逐仓库确认远端默认分支包含候选 merge commit，运行 `scripts/check_release_integrity.sh`，再切回默认分支执行 `git pull --ff-only`，并核对 `git worktree list --porcelain`。默认分支 worktree 未与远端一致或有未提交改动时，保持 blocked；切换本地分支不能替代 Code PR 合并或部署版本核对。

## 4. 失败分支

- Preview P0/P1 失败时立即按方案回滚固定 alias/流量，停止 Production。
- 把失败 deployment、日志、DB 证据、根因和回滚结果写回 Release PR；不得把失败方案标记为 `complete`。
- 候选代码、默认分支 merge commit 或构建产物发生变化时，原 release plan approval 失效。创建/合并新的 Code PR，基于新的精确候选更新 Release PR 或创建替代 Release PR，再请求批准。
- 旧 Release PR 若已被新候选替代，应关闭并说明 superseded-by PR；保留历史，不删除证据。
- 不通过删除、移动、合并 identity，清理生产数据或修改环境 secret 来伪造验证通过。
- 用户报告线上失败或 P0/P1 探针失败时，立即暂停 Release PR merge 和观察核销；先从实际 host、callback 和 runtime 日志定位请求命中的 deployment/commit，再决定回滚或修复。

## 5. 用户沟通契约

每次只给一个明确动作，并包含对象、编号、环境和后果：

| 阶段 | 必须使用的表达 |
|------|----------------|
| Code PR 待处理 | `请 review/merge Code PR #N；合并后候选将固定为 <commit>` |
| Release plan 待审批 | `请批准 Preview release plan vX；这是部署授权，不是 merge Release PR #N` |
| Preview 已部署 | `Preview deployment <id> 已切到固定入口，请执行 <完整路径>` |
| Preview 验证中 | `Release PR #N 保持 open，正在回填 <API/DB/E2E/观察窗口>` |
| Preview 通过 | `Preview 已通过并完成证据回填；Release PR #N 保持 open，现在请 review/merge 关联 Code PR，并冻结 Production merge commit` |
| Preview 失败 | `Preview P0/P1 失败，已回滚到 <id>；不要 merge Release PR #N，也不进入 Production` |
| Production 待审批 | `请批准 Production release plan vY；目标和回滚点为 <...>` |

禁止使用无法判断对象的表达：`先 merge`、`合并了继续`、`继续发布`、`方案好了`。如果用户只说“合并了”，先通过 GitHub/GitLab 状态确认是哪个 PR，再执行下一阶段。

## 6. 发布记录要求

Release PR 必须持续记录：

- 每个关联仓库的 Code PR、默认分支、实现/head commit、默认分支 merge commit、deployment/产物 commit 和构建映射证据。
- Release PR 编号、release plan 版本和审批时间。
- runtime entry inventory 的路径/版本；本次实际登录入口、BFF、provider callback、业务回跳、固定 alias、deployment ID、commit 和 target 快照。
- Preview deployment、固定 alias、环境/schema、回滚 deployment。
- 真实 E2E、API、DB、日志、截图和观察窗口。
- 每个关联系统的发布/不发布核销；单个客户端或服务产物完成不能替代完整 Release Train 核销。
- 失败、回滚、候选变化和 superseded PR。
- Production 独立审批、deployment、线上回归和最终状态。
- Production 真实用户验证、合成探针、DB after、日志观察窗口、callback/fixed alias 漂移检查，以及所有受影响仓库的远端默认分支与本地工作区归位。
