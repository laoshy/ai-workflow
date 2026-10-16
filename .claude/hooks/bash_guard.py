#!/usr/bin/env python3
"""PreToolUse hook: 危险命令守卫。
拦截明确的破坏性命令（融合 Project Harness 的 safe_bash_guard 思路）。
误杀时可让用户临时放行（修改本文件或临时禁用 hook）。
"""
import json
import re
import sys

# (正则, 理由)  命中即拒绝
BLOCK_PATTERNS = [
    (r"rm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME|\.\.)", "递归删除根/家目录/上级目录"),
    (r"rm\s+-rf?\s+\*", "通配符递归删除"),
    (r"(?i)del\s+/[sq]\b.*\s+C:\\", "Windows 递归删除系统盘内容"),
    (r"(?i)(format|mkfs|diskpart)\s", "格式化磁盘类命令"),
    (r"git\s+push\s+.*--force\b(?!-with-lease)", "git push --force（如需强推请改用 --force-with-lease）"),
    (r"git\s+reset\s+--hard\s+origin", "硬重置丢弃本地全部改动"),
    (r"(?i)drop\s+(table|database)\s", "删除数据库表/库"),
    (r"(?i)(shutdown|reboot)\s*(-[fhr]+|\s/)", "关机/重启命令"),
    (r">\s*/dev/sd[a-z]", "直接写块设备"),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    cmd = (payload.get("tool_input", {}) or {}).get("command", "") or ""
    for pattern, reason in BLOCK_PATTERNS:
        if re.search(pattern, cmd):
            print(
                f"[bash_guard] 拒绝执行危险命令：{reason}\n命令：{cmd}\n"
                f"如确属必要，请拆分为更安全的步骤并向用户说明风险。",
                file=sys.stderr,
            )
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
