#!/usr/bin/env python3
"""PreToolUse hook: 单文件行数守卫（≤800 行）。
- Write：新写入内容超 800 行 → 拒绝
- Edit ：预估改后行数超 800 行 → 拒绝
通过标准输入接收 Claude Code 的 hook JSON。
"""
import json
import sys
from pathlib import Path

MAX_LINES = 800


def deny(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input", {}) or {}

    if tool == "Write":
        content = ti.get("content", "") or ""
        n = len(content.splitlines())
        if n > MAX_LINES:
            deny(
                f"[line_guard] 拒绝写入：文件将达 {n} 行，超过 {MAX_LINES} 行上限。\n"
                f"请拆分为多个模块（如 按 class/职责 拆文件），或把数据/常量外置。"
            )

    elif tool == "Edit":
        fp = ti.get("file_path", "")
        new = ti.get("new_string", "") or ""
        old = ti.get("old_string", "") or ""
        if fp:
            p = Path(fp)
            if p.is_file():
                try:
                    cur = len(p.read_text(encoding="utf-8", errors="ignore").splitlines())
                except Exception:
                    sys.exit(0)
                projected = cur - len(old.splitlines()) + len(new.splitlines())
                if projected > MAX_LINES:
                    deny(
                        f"[line_guard] 拒绝编辑：{p.name} 改后预计 {projected} 行，"
                        f"超过 {MAX_LINES} 行上限。请先拆分该文件再继续。"
                    )
    sys.exit(0)


if __name__ == "__main__":
    main()
