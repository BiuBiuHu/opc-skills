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

## 2. 对象定义

- **Code PR**：承载运行时代码、测试和实现文档。它的 merge 策略决定候选 commit 从 PR head 还是主分支 merge commit 构建。
- **Release PR**：承载 `release-plan.md`、测试报告、联调报告、evidence manifest 和部署核销证据。它不是运行时代码审核的替代品。
- **Release plan approval**：用户或 reviewer 对特定候选、范围、环境、顺序、迁移和回滚方案的明确 `approved`。它不是 PR merge。
- **Preview verification**：对已部署候选执行真实页面/API/DB/第三方闭环。`Ready` 不是验证通过。
- **Runtime entry inventory**：项目文档仓库中的真实入口清单，记录登录入口、BFF、Auth/service-only URL、provider callback、业务回跳、固定 alias 以及当前 deployment 快照。它是事实源；Release PR 只冻结本次候选，不把项目事实写进通用 skill。

## 3. 标准时序

1. 保存并验证代码，创建 Code PR。
2. 明确候选策略：
   - 若项目要求主分支候选，先 merge Code PR，再从同步后的主分支读取精确 merge commit。
   - 若项目允许 PR head Preview，在 release plan 中写明 head commit 和不先 merge Code PR 的理由。
   - 候选策略必须遵循项目级发布规范；若项目要求主分支候选，则使用精确的主分支 merge commit。
3. 从同步后的主分支创建 release 分支，创建 Release PR；初始 release plan 为 `awaiting-review`。
4. 读取并核对项目 runtime entry inventory，向用户展示候选 commit、真实登录/BFF/callback/回跳入口、目标环境、发布矩阵、数据动作、验证路径和回滚点，请求批准 release plan。不要请求 merge Release PR。
5. 用户明确批准后，把 release plan 更新为 `approved` 并提交到仍为 open 的 Release PR。
6. 从已提交、可追踪的候选部署 Preview，记录 deployment ID/URL；不要先 merge Release PR。
7. 在固定 Preview 入口执行真实 E2E、API、DB、日志和观察窗口验证，并持续回填同一个 Release PR。
8. Preview 全部通过后，明确告诉用户“Preview 已通过，可以 review/merge Release PR #N”；只有此时才考虑 merge Release PR。
9. Production 使用单独的 release plan 版本、审批、deployment、回归和核销。Preview 的批准不能自动授权 Production。
10. Production 低流量时执行无破坏性合成探针；仅有 `0` 条错误日志不算观察通过。
11. 最终核销真实用户验证、合成探针、DB after、日志窗口和 alias/deployment 漂移；适用证据完整后才 merge Release PR。
12. Release PR merge 后切回远端默认主分支，执行 `git pull --ff-only` 并确认本地与远端一致。

## 4. 失败分支

- Preview P0/P1 失败时立即按方案回滚固定 alias/流量，停止 Production。
- 把失败 deployment、日志、DB 证据、根因和回滚结果写回 Release PR；不得把失败方案标记为 `complete`。
- 候选代码变化时，原 release plan approval 失效。创建/合并新的 Code PR，基于新的精确候选更新 Release PR 或创建替代 Release PR，再请求批准。
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
| Preview 通过 | `Preview 已通过并完成证据回填，现在可以 review/merge Release PR #N` |
| Preview 失败 | `Preview P0/P1 失败，已回滚到 <id>；不要 merge Release PR #N，也不进入 Production` |
| Production 待审批 | `请批准 Production release plan vY；目标和回滚点为 <...>` |

禁止使用无法判断对象的表达：`先 merge`、`合并了继续`、`继续发布`、`方案好了`。如果用户只说“合并了”，先通过 GitHub/GitLab 状态确认是哪个 PR，再执行下一阶段。

## 6. 发布记录要求

Release PR 必须持续记录：

- Code PR、实现 commit、主分支 merge commit。
- Release PR 编号、release plan 版本和审批时间。
- runtime entry inventory 的路径/版本；本次实际登录入口、BFF、provider callback、业务回跳、固定 alias、deployment ID、commit 和 target 快照。
- Preview deployment、固定 alias、环境/schema、回滚 deployment。
- 真实 E2E、API、DB、日志、截图和观察窗口。
- 每个关联系统的发布/不发布核销。
- 失败、回滚、候选变化和 superseded PR。
- Production 独立审批、deployment、线上回归和最终状态。
- Production 真实用户验证、合成探针、DB after、日志观察窗口、callback/fixed alias 漂移检查和发布后默认主分支归位。
