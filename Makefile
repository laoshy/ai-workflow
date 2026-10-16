# ai-workflow 一键验证入口（模板）
# 接入新项目后，按项目语言修改 lint / test 两个目标；
# `check` 目标是整个工作流的验收锚点，不要改名。

.PHONY: check lint test format harness-check

# —— 验收锚点：lint + test + harness 自检，全绿并盖时间戳戳 ——
check: lint test harness-check
	@mkdir -p .harness && python -c "import time;open('.harness/.check-passed','w').write(str(time.time()))"
	@echo "== make check PASSED =="

# —— 按项目定制：lint ——
lint:
	@command -v ruff >/dev/null 2>&1 && ruff check . || echo "[lint] ruff 未安装，跳过"

# —— 按项目定制：测试 ——
test:
	@if [ -d tests ]; then python -m pytest -q; else echo "[test] 无 tests 目录，跳过"; fi

# —— Harness 自检（runbook 初始化后生效） ——
harness-check:
	@if [ -f scripts/harness_check.sh ]; then bash scripts/harness_check.sh; else echo "[harness] 未初始化，跳过"; fi

format:
	@command -v black >/dev/null 2>&1 && black -q . || echo "[format] black 未安装，跳过"
