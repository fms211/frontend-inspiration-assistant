"""Project-scoped operations shared by MCP clients; browser evidence is supplied by the host."""
from pathlib import Path
import copy
import json
import inspiration as core


def checked(errors, **details):
    if errors:
        raise ValueError(json.dumps({"ok": False, "errors": errors, **details}, ensure_ascii=False))


class AgentTools:
    def __init__(self, project):
        self.project = Path(project).resolve(strict=True)
        if not self.project.is_dir():
            raise ValueError("project must be an existing directory")

    def path(self, value, *, output=False):
        path = Path(value)
        resolved = (path if path.is_absolute() else self.project / path).resolve()
        if not resolved.is_relative_to(self.project):
            raise ValueError("path must stay inside the configured project (including symlink targets)")
        relative = resolved.relative_to(self.project)
        if any(part in {".git", "node_modules"} or part.startswith(".env") for part in relative.parts):
            raise ValueError("secret/config/cache paths are not report inputs")
        if output and (not resolved.is_relative_to((self.project / "设计灵感").resolve()) or resolved.exists()):
            raise ValueError("output must be a new file inside this project's 设计灵感 directory")
        return resolved

    def document(self, value):
        path = self.path(value)
        if path.suffix != ".json" or path.stat().st_size > 5 * 1024 * 1024:
            raise ValueError("input must be a JSON report smaller than 5 MiB")
        data = core.read_json(path)
        if not isinstance(data, dict):
            raise ValueError("input JSON must be an object")
        return path, data

    def candidates(self, value):
        path, data = self.document(value)
        if Path(data.get("project_root", "")).resolve() != self.project:
            raise ValueError("candidate project_root must match the configured MCP project")
        if not isinstance(data.get("candidates"), list) or not isinstance(data.get("sources"), list):
            raise ValueError("candidates and sources must be arrays")
        if any(not isinstance(item, dict) for item in [*data["candidates"], *data["sources"]]):
            raise ValueError("candidate and source entries must be objects")
        for candidate in data["candidates"]:
            verification = candidate.get("verification", {})
            if not isinstance(verification, dict):
                raise ValueError("verification must be an object")
            for relative in (candidate.get("screenshot"), verification.get("evidence")):
                if relative:
                    self.path(str(path.parent / relative))
        errors = core.candidate_errors(data, path.parent)
        return path, data, errors

    def workflow(self):
        return {
            "ok": True, "version": core.VERSION, "project_root": str(self.project),
            "instructions": (core.ROOT / "SKILL.md").read_text(encoding="utf-8") + "\n\n" + (core.ROOT / "skills/frontend-inspiration/SKILL.md").read_text(encoding="utf-8"),
            "reference_resources": {name: f"inspiration://{name}" for name in ("sources", "implementation", "audit", "host-adapters")},
            "sources": list(core.SOURCES), "minimum_unique_candidates": 20,
            "browser_execution": "calling agent's actual browser tools; this server does not browse or call an LLM",
            "next_steps": ["inspect project and read its design constraints", "get candidates template", "browse four sources and save real evidence", "validate and write Markdown report", "ask user to choose", "write and audit element-level proposal", "wait for concrete proposal confirmation", "host implements and performs browser audit"],
            "implementation_authorized": False,
        }

    def inspect(self):
        self.path("package.json")
        result = core.inspect_project(self.project)
        result["context_previews"] = []
        for name in ("AGENTS.md", "PRODUCT.md", "DESIGN.md", "README.md"):
            path = self.path(name)
            if path.is_file():
                raw = path.read_bytes()[:65537]
                result["context_previews"].append({"name": name, "text": raw[:65536].decode("utf-8-sig", errors="replace"), "truncated": len(raw) > 65536})
        return result

    def save_artifact(self, kind, payload, output_path):
        if kind not in {"candidates", "implementation", "audit", "browser-evidence"} or not isinstance(payload, dict):
            raise ValueError("artifact kind and object payload required")
        data = copy.deepcopy(payload)
        if kind == "candidates":
            data["project_root"] = str(self.project)
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if len(text.encode("utf-8")) > 5 * 1024 * 1024:
            raise ValueError("artifact must be smaller than 5 MiB")
        output = self.path(output_path, output=True)
        if output.suffix != ".json":
            raise ValueError("artifact output must be a JSON file")
        core.write_new(output, text)
        return {"ok": True, "output_path": str(output), "kind": kind, "validation_status": "not-validated", "implementation_authorized": False}

    def template(self, kind):
        if kind not in {"candidates", "implementation", "audit"}:
            raise ValueError("unknown template kind")
        data = copy.deepcopy(core.read_json(core.ROOT / "templates" / f"{kind}.json"))
        if kind == "candidates":
            data["project_root"] = str(self.project)
        return {"ok": True, "template": data, "kind": kind, "note": "Fill with observed project and browser evidence; template placeholders are not verified results."}

    def validate(self, input_path):
        _, data, errors = self.candidates(input_path)
        checked(errors, count=len(data["candidates"]))
        return {"ok": True, "count": len(data["candidates"]), "errors": []}

    def report(self, input_path, output_path, allow_incomplete=False):
        source, data, errors = self.candidates(input_path)
        if errors and not allow_incomplete:
            checked(errors)
        output = self.path(output_path, output=True)
        markdown = core.report_markdown(data, source.parent, errors)
        core.write_new(output, markdown)
        # A deliberately saved diagnostic report still fails the MCP call.
        checked(errors, output_path=str(output), status="incomplete")
        return {"ok": True, "output_path": str(output), "markdown": markdown, "status": "awaiting-selection", "implementation_authorized": False}

    def proposal(self, input_path, candidates_path, output_path):
        _, data = self.document(input_path)
        _, candidates, errors = self.candidates(candidates_path)
        checked(errors)
        checked(core.brief_errors(data, candidates))
        output = self.path(output_path, output=True)
        markdown = core.brief_markdown(data)
        core.write_new(output, markdown)
        return {"ok": True, "output_path": str(output), "markdown": markdown, "status": "awaiting-confirmation", "selection_origin": data["selection_origin"], "implementation_authorized": False}

    def rules(self, query, domain=None, stack=None):
        if domain and stack:
            raise ValueError("choose domain or stack, not both")
        if len(query) > 4000:
            raise ValueError("query too long")
        return core.audit_rules(query, domain, stack)

    def audit(self, input_path, output_path):
        _, data = self.document(input_path)
        checked(core.audit_errors(data))
        output = self.path(output_path, output=True)
        markdown = core.audit_markdown(data)
        core.write_new(output, markdown)
        return {"ok": True, "output_path": str(output), "markdown": markdown}

    def fit(self, input_path, stack):
        _, data, errors = self.candidates(input_path)
        checked(errors)
        return core.stack_projection(data, stack)
