---
description: 收尾：确认验证通过、规范提交，并可选开 PR
---
# 收尾 / PR

## 输入

$ARGUMENTS （可选：PR 标题或补充说明）

## 流程

1. 运行 `make check`，必须全绿；失败则转 `/build-fix`
2. 若启用了 Harness：确认 `.harness/session-log.md` 已记录本次工作与验证证据
3. 提交：按 conventional commits 写信息（feat/fix/refactor/docs/test/chore），
   正文说明"做了什么 + 为什么 + 验证证据（make check 输出摘要）"
4. 用户要求开 PR 时：
   - push 分支，用 `gh pr create` 开 PR
   - PR 描述包含：变更摘要、验证方式与结果、风险点
5. 提醒用户：如本次有新经验/约定，考虑运行 `/retro` 沉淀进 AGENTS.md
