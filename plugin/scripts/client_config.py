"""Generate client-specific MCP configuration; never changes a global client setting."""
from pathlib import Path
import argparse
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAYWRIGHT_PACKAGE = "@playwright/mcp@0.0.83"


def configuration(project, client, python=sys.executable, with_browser=False):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("project must be an existing directory")
    servers = {"frontend-inspiration": {
        "type": "stdio", "command": str(python),
        "args": [str(ROOT / "scripts/mcp_server.py"), "--project", str(project)],
        "env": {"PYTHONUTF8": "1"},
    }}
    if with_browser:
        servers["playwright"] = {"type": "stdio", "command": "npx.cmd" if os.name == "nt" else "npx",
                                  "args": ["-y", PLAYWRIGHT_PACKAGE, "--output-dir", str(project / "设计灵感/browser")]}
    if client == "codex":
        lines = []
        for name, settings in servers.items():
            lines += [f"[mcp_servers.{json.dumps(name)}]", f"command = {json.dumps(settings['command'])}",
                      f"args = {json.dumps(settings['args'], ensure_ascii=False)}"]
            if settings.get("env"):
                lines += [f"[mcp_servers.{json.dumps(name)}.env]", 'PYTHONUTF8 = "1"']
            lines.append("")
        return "\n".join(lines)
    return json.dumps({"servers" if client == "vscode" else "mcpServers": servers}, ensure_ascii=False, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--client", choices=("claude", "cursor", "stdio", "vscode", "codex"), required=True)
    parser.add_argument("--python", default=sys.executable, help="Python interpreter with requirements-mcp.txt installed")
    parser.add_argument("--with-browser", action="store_true", help="Also include the optional pinned Playwright MCP")
    parser.add_argument("--output", help="Create a new config file; existing files are preserved")
    args = parser.parse_args(argv)
    try:
        text = configuration(args.project, args.client, args.python, args.with_browser)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("x", encoding="utf-8") as handle:
                handle.write(text)
            print(json.dumps({"ok": True, "output": str(output.resolve()), "client": args.client}, ensure_ascii=False))
        else:
            print(text, end="")
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
