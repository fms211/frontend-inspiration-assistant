"""Vendor the reviewed, pinned UI UX Pro Max runtime without executing it."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import urllib.request
import zipfile
import io

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "09170eec67eefd46a7ae85de61b40c194020f997"
REPOSITORY = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"


def main():
    url = f"https://codeload.github.com/nextlevelbuilder/ui-ux-pro-max-skill/zip/{COMMIT}"
    request = urllib.request.Request(url, headers={"User-Agent": "frontend-inspiration-assistant/0.1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read()
    target = ROOT / "skills" / "ui-ux-pro-max"
    target.mkdir(parents=True, exist_ok=True)
    hashes = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for item in archive.infolist():
            if item.is_dir():
                continue
            parts = PurePosixPath(item.filename).parts
            relative = None
            if parts[1:] == ("LICENSE",):
                relative = "LICENSE"
            elif len(parts) > 4 and parts[1:3] == ("src", "ui-ux-pro-max") and parts[3] in {"data", "scripts", "templates"}:
                relative = "/".join(parts[3:])
            if relative is None or "__pycache__" in parts or item.filename.endswith(".pyc"):
                continue
            if ".." in parts or ((item.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError(f"Unsafe runtime archive member: {item.filename}")
            destination = target / relative
            if not destination.resolve().is_relative_to(target.resolve()):
                raise ValueError("Extraction escaped target")
            blob = archive.read(item)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob)
            hashes[relative] = hashlib.sha256(blob).hexdigest()
    platform = json.loads((target / "templates/platforms/codex.json").read_text(encoding="utf-8"))
    base = (target / "templates/base/skill-content.md").read_text(encoding="utf-8")
    quick = (target / "templates/base/quick-reference.md").read_text(encoding="utf-8")
    rendered = base.replace("{{TITLE}}", platform["title"]).replace("{{DESCRIPTION}}", platform["description"])
    rendered = rendered.replace("{{QUICK_REFERENCE}}", quick).replace("{{SCRIPT_PATH}}", "<SKILL_DIR>/scripts/search.py")
    if "{{" in rendered:
        raise ValueError("Unresolved official template placeholder")
    frontmatter = "---\nname: ui-ux-pro-max\ndescription: " + json.dumps(platform["frontmatter"]["description"], ensure_ascii=False) + "\n---\n\n"
    note = (
        "<!-- Portable Codex package: resolve <SKILL_DIR> to this SKILL.md's directory. -->\n"
        "> 本副本由官方 Codex 模板生成。`<SKILL_DIR>` 指本 SKILL.md 所在目录，执行前请替换为实际绝对路径并正确引用。"
        "跨项目使用时遵循当前用户要求、项目规则与真实技术栈。上游建议不构成浏览器验收。\n\n"
    )
    (target / "SKILL.md").write_text(frontmatter + note + rendered, encoding="utf-8")
    record = {
        "repository": REPOSITORY, "commit": COMMIT, "license": "MIT",
        "archive_url": url, "archive_sha256": hashlib.sha256(raw).hexdigest(),
        "generated_skill": "Codex platform frontmatter + base template + quick reference; portable script path only",
        "upstream_files": hashes,
    }
    (target / "UPSTREAM.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "files": len(hashes), "stack_files": len(list((target / 'data/stacks').glob('*.csv'))), "commit": COMMIT}))


if __name__ == "__main__":
    main()
