"""Install a self-contained Agent Skill into one explicitly selected project."""
from pathlib import Path
import argparse
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CLIENT_DIRS = {"claude": ".claude", "cursor": ".cursor", "codex": ".agents", "agents": ".agents"}


def install(project, client):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("project must be an existing directory")
    destination = (project / CLIENT_DIRS[client] / "skills" / "frontend-inspiration-assistant").resolve()
    if not destination.is_relative_to(project) or destination.is_relative_to(ROOT):
        raise ValueError("skill destination must stay inside the project and outside source runtime")
    if destination.exists():
        raise FileExistsError(f"existing skill preserved: {destination}")
    source_files = list(ROOT.rglob("*"))
    if any(path.is_symlink() for path in source_files):
        raise ValueError("source bundle contains symlinks; refusing a non-portable copy")
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".venv", ".git", "node_modules"))
    return {"ok": True, "client": client, "skill_root": str(destination), "discovery": "frontend-inspiration-assistant", "global_config_modified": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--client", choices=CLIENT_DIRS, required=True)
    args = parser.parse_args(argv)
    try:
        result = install(args.project, args.client)
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
