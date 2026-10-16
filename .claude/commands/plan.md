---
description: 实现规划：产出计划文档并停在确认门，等待用户批准
---
# 实现规划阶段

## 需求输入

$ARGUMENTS

## 流程

1. 确定需求来源：若存在 `.claude/prds/` 中最近的 PRD 则以其为准；否则以 $ARGUMENTS 为需求
2. 若项目已初始化 Harness，先读 `AGENTS.md`、`docs/architecture.md`、`current-task.md`
3. 通读相关代码后，产出 `.claude/plans/<slug>.plan.md`，必须包含：
   - 目标（对应 PRD 哪些验收标准）
   - 改动文件清单：每个文件**一行一个改动要点**
   - 实施步骤（可勾选的 checklist）
   - 验证方式：完成后用哪条命令验证、预期看到什么（最终汇总到 `make check`）
   - 回滚方式
4. **停在确认门**：向用户列出计划要点，等待明确批准。批准前禁止修改任何代码。

## 批准协议

- 用户回复"批准，用 tdd-workflow 实施" → 加载 tdd-workflow 技能，按计划严格 TDD 实施
- 用户仅回复 yes / 批准（未指定方式）→ 按计划实施，不强制 TDD
- 用户提出修改意见 → 修订计划，重新停在确认门
