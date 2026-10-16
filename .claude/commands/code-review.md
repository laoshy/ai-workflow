---
description: 通用代码复查：派发 code-reviewer 子 agent 审查本次改动
---
# 通用代码复查

## 复查范围

$ARGUMENTS （为空时：审查当前未提交的全部改动，用 git diff 确定）

## 流程

1. 用 `git diff` / `git status` 收集本次改动
2. 派发 **code-reviewer** 子 agent（Task 工具，subagent_type=code-reviewer），把 diff 和相关上下文交给它
3. 收到报告后向用户转述，按严重度分级：
   - 🔴 必须修：逻辑错误、边界遗漏、资源泄漏 → 当场修复并重跑 `make check`
   - 🟡 建议修：可读性、命名、重复代码 → 征求用户意见
   - 🟢 可忽略：风格偏好 → 仅记录
4. 修复后再次派发复查直至无 🔴 项，更新 `.harness/session-log.md` 记录复查结论
