#!/usr/bin/env python3
"""PostToolUse hook: 写入后自动格式化（宽容模式：工具缺失则静默跳过）。"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    fp = (payload.get("tool_input", {}) or {}).get("file_path", "") or ""
    if not fp:
        sys.exit(0)
    p = Path(fp)
    if not p.is_file():
        sys.exit(0)

    try:
        if p.suffix == ".py" and shutil.which("black"):
            subprocess.run(["black", "-q", str(p)], timeout=30,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif p.suffix == ".go" and shutil.which("gofmt"):
            subprocess.run(["gofmt", "-w", str(p)], timeout=30,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # 格式化失败不影响主流程
    sys.exit(0)


if __name__ == "__main__":
    main()
