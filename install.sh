#!/usr/bin/env bash
# ai-workflow 安装脚本：把工作流接入当前项目
# 用法：
#   bash /path/to/ai-workflow/install.sh          # 复制模式（默认）
#   bash /path/to/ai-workflow/install.sh --link   # 软链模式（工作流升级全局生效，推荐个人使用）
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$(pwd)"

if [ "$SRC" = "$DST" ]; then
  echo "错误：请在目标项目目录中运行本脚本，而不是模板仓库内。"; exit 1
fi

MODE="copy"
[ "${1:-}" = "--link" ] && MODE="link"

install_item() {
  local rel="$1"
  local target="$DST/$rel"
  if [ -e "$target" ] && [ "$rel" = "CLAUDE.md" ]; then
    echo "  跳过 $rel（已存在，请手动合并项目特有规则）"; return
  fi
  if [ "$MODE" = "link" ]; then
    mkdir -p "$(dirname "$target")"
    ln -sfn "$SRC/$rel" "$target"
  else
    cp -r "$SRC/$rel" "$target"
  fi
  echo "  安装 $rel ($MODE)"
}

echo "接入 ai-workflow → $DST ($MODE 模式)"
for item in .claude CLAUDE.md Makefile project_harness_initialization_runbook.md; do
  install_item "$item"
done

echo ""
echo "完成。下一步："
echo "  1. 按项目语言修改 Makefile 的 lint/test 目标"
echo "  2. 打开 Claude Code，说：读取 project_harness_initialization_runbook.md，按 Standard 档在当前仓库初始化 Project Harness"
echo "  3. 把项目领域约束补进 CLAUDE.md / AGENTS.md"
echo "  4. 运行 make check 确认验收通道畅通"
