# 本机安装、同步与诊断

安装需要 Git、Python 3.9+；npm CLI 还需 Node 18+。安装/更新是独立动作，不能因业务发布自动覆盖全局 skill。先按[授权规则](authorization.md)确认本次范围。

## 单一来源与多个安装入口

- 支持的安装入口是 `scripts/install.sh`，npm CLI 调用同一脚本，再进入 `scripts/sync-local-skills.py`。curl 无相邻 helper 时只在临时目录引导下载。
- 默认从 `~/.local/share/opc-skills/source` 的受校验 Git 仓库快进到 main，读取已提交插件 payload；不从脏工作区或未跟踪文件打包。
- 主安装位于 `${CODEX_HOME}/skills/opc-skills`，未设置时为 `~/.codex/skills/opc-skills`。已有 `~/.agents/skills`、`~/.cursor/skills`、`~/.claude/skills` 同步更新；不创建不存在的额外发现目录。
- 已指向主安装的别名保留；未知 symlink、其它仓库和共享 Git worktree 不自动接管。
- 每份安装记录 `.opc-install.json`：来源 commit、版本、文件 hash 与基线 ID。本地目录没有 `.git` 也可健康，不再仅因复制安装就报告 broken。

## 更新策略

1. 先校验来源、安装基线和全部目标，检查锁与并发修改。
2. 对有来源记录的安装使用“上次发布基线 / 当前本地内容 / 新发布内容”三方合并，保留各安装不同的本地规则及未知文件；不把版本号当成足够的基线证据。
3. 任一目标有内容、增删或权限冲突时，全部安装保持原样，只报告路径和原因，不输出文件内容。先审查冲突，再重试。
4. 全部准备成功后备份旧目录，原子替换每个目标；捕获到的异常会恢复已替换目标；进程强杀/断电后需按备份 manifest 审查恢复，不承诺跨进程自动恢复。备份与基线存于 `~/.local/state/opc-skills`，旧版本不会自动删除，备份内 manifest 记录目录编号与原目标，供审查后恢复。
5. doctor 校验来源、基线、入口、版本和各入口漂移；本地 override 单独列出，不把合法差异当成损坏。新 skill 在下一轮会话加载。

## 命令

```bash
npx opc-skills install
npx opc-skills update
npx opc-skills doctor
```

命令与新增 helper 需要包含本轮代码的 CLI 版本；PR 合并不等于 npm 已发布。npm 旧版本不具有新同步逻辑；也可从已核对的仓库运行 `bash scripts/install.sh`。

本地干净仓库或隔离配置：

```bash
bash scripts/install.sh update --source /path/to/clean/opc-skills --root /path/to/profile
bash scripts/install.sh doctor --root /path/to/profile
```

`--root` 隔离安装、缓存、基线和备份，显式设置时不读取真实 CODEX_HOME 目标，适合验证；不修改 HOME/CODEX_HOME。

## 首次接管旧安装

- 干净且来源匹配的旧 Git 安装可从其 HEAD 建立基线，完整备份（含 `.git`）后转为带来源的安装；脏仓库、关联 worktree 或其它 origin 会停止，不强制 reset。
- 复制安装没有基线时不能猜。根据原安装记录核对旧 commit，然后显式传入 `--base <prior-source-ref>`，先执行三方预检；来源不明先保留原目录，不自动覆盖。
- 对已有 managed 安装，缺失或损坏基线不能用 `--base` 绕过，需恢复正确状态。状态中的 lock 必须先确认对应进程已结束，不能自动删锁抢占。
- 冲突与本地规则的语义取舍不能由工具擅自裁决；同步器不把本地差异自动推广到公共仓库。
