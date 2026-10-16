#!/usr/bin/env python3
"""Stop hook: 完成前验证门（配合 Makefile 的 check 目标）。
规则：项目已初始化 Harness 且存在 Makefile check 目标时，
若 .harness/.check-passed 标记缺失或早于最新源码改动 → 阻止结束，要求先跑 `make check`。
"""
import json
import sys
import time
from pathlib import Path

SRC_GLOBS = ["src/**/*.py", "lib/**/*.py", "tests/**/*.py", "*.py", "src/**/*.ts", "app/**/*.kt"]


def main() -> None:
    root = Path.cwd()
    harness = root / ".harness"
    makefile = root / "Makefile"
    if not harness.is_dir() or not makefile.is_file():
        sys.exit(0)  # 未初始化 harness 的项目不打扰
    if "check" not in makefile.read_text(encoding="utf-8", errors="ignore"):
        sys.exit(0)

    marker = harness / ".check-passed"
    if not marker.is_file():
        block("尚未运行过验证。请先执行 `make check`，通过后再结束。")
        return

    marker_mtime = marker.stat().st_mtime
    newest_src = 0.0
    for pattern in SRC_GLOBS:
        for f in root.glob(pattern):
            if ".harness" in f.parts or "node_modules" in f.parts or ".venv" in f.parts:
                continue
            try:
                newest_src = max(newest_src, f.stat().st_mtime)
            except Exception:
                pass
    if newest_src > marker_mtime:
        block("检测到验证之后又有代码改动。请重新执行 `make check` 再结束。")
        return
    sys.exit(0)


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
