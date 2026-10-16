---
description: 修构建错误：最小化改动让 make check 重新通过
---
# 构建修复

## 输入

$ARGUMENTS （报错信息或为空时自动运行 make check 收集错误）

## 流程

1. 运行 `make check`，完整收集报错
2. 逐个修复，遵守**最小改动原则**：只修让构建/测试通过所必需的内容，禁止顺手重构
3. 每修一处即重跑 `make check` 对应环节
4. 全部通过后：向用户报告修了什么、为什么这样修，并确认 `.harness/.check-passed` 已更新
5. 若发现错误的根因是之前某次改动引入，在 `docs/error-journal.md` 追加一条记录（现象 → 根因 → 修复 → 教训）
