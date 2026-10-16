# ai-workflow

给 coding agent 的工程执行轨道：**命令管入口、skill 管过程、子 agent 管分工、hooks 管硬拦、Harness 管记忆、`make check` 管验收**。

融合了 [Project Harness](https://github.com/Bow-Lin/project-harness)（MIT）的 runbook 作为状态层。

## 结构

```
ai-workflow/
├── .claude/
│   ├── commands/            # 入口命令
│   │   ├── plan-prd.md      #   /plan-prd      需求定义（what/why）
│   │   ├── plan.md          #   /plan          实施计划 + 确认门
│   │   ├── code-review.md   #   /code-review   派 code-reviewer 复查
│   │   ├── security-scan.md #   /security-scan 派 security-reviewer 复查
│   │   ├── build-fix.md     #   /build-fix     最小化修构建
│   │   └── pr.md            #   /pr            验证 + 提交 + 开 PR
│   ├── agents/              # 专业子 agent
│   │   ├── code-reviewer.md
│   │   └── security-reviewer.md
│   ├── skills/tdd-workflow/ # TDD 技能（RED→GREEN→重构→覆盖率）
│   └── hooks/               # 强制护栏（见下表）
├── CLAUDE.md                # 通用硬约束
├── Makefile                 # 一键验证：make check（验收锚点）
├── install.sh               # 接入脚本
└── project_harness_initialization_runbook.md   # 状态层初始化协议
```

## Hooks（强制护栏）

| Hook | 时机 | 作用 |
|---|---|---|
| `line_guard.py` | Write/Edit 前 | 单文件 ≤800 行，超限拒绝 |
| `bash_guard.py` | Bash 前 | 拦截 rm -rf、force push、DROP TABLE 等危险命令 |
| `stop_gate.py` | 会话结束前 | 代码有改动而 `make check` 未通过 → 阻止收工 |
| `format.py` | 写入后 | 自动格式化（black/gofmt，缺工具则静默跳过） |

## 新项目使用

```bash
git clone https://github.com/<你>/ai-workflow.git my-project
cd my-project && rm -rf .git && git init
```

然后 4 步：
1. `bash ../ai-workflow/install.sh --link` （或模板自带则跳过）
2. 改 `Makefile` 的 lint/test 目标适配项目语言
3. 对 Claude Code 说：**读取 project_harness_initialization_runbook.md，按 Standard 档初始化 Project Harness**，再把领域约束补进 AGENTS.md
4. `make check` 确认全绿

## 存量项目接入

```bash
cd old-project && bash /path/to/ai-workflow/install.sh --link
```

初始化 Harness 时强调"这是存量项目，先通读代码再生成 architecture.md"。
TDD 只跟改动走（改动处补测试），不回填存量代码。

## 日常循环

```
/start → (/plan-prd) → /plan → 批准(+tdd-workflow) → 写码
      → /code-review (敏感加 /security-scan) → /commit → /handoff
小改动直接做，不必走全流程。
```

## 升级路径

- 起步：软链模式（--link），改模板全局生效
- 稳定后：本仓库注册为私有 plugin marketplace，各项目 `/plugin install`
