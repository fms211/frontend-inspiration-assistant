import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

import test_contracts as fixtures

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from agent_tools import AgentTools
import client_config
import install_skill
import inspiration as core


def proposal_fixture():
    element = {"candidate_ids": ["0"], "observed_original": "fixture only"}
    for group, fields in core.ELEMENT_KEYS.items():
        element[group] = {field: "fixture value 16px" for field in fields}
    element["motion"].update(duration_ms=160, delay_ms=0)
    return {"target": "fixture", "selected_ids": ["0"], "selection_origin": "test-fixture", "selection_text": "fixture; not a real user selection", "elements": [element], "audit_summary": "fixture rules only"}


class Portable(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.Contracts("test_20_complete")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.base = self.fixture.base
        self.tools = AgentTools(self.base)
        self.source = self.base / "candidates.json"
        self.save()

    def save(self):
        self.source.write_text(json.dumps(self.fixture.data), encoding="utf-8")

    def test_project_scoping_rejects_escape_and_wrong_root(self):
        with self.assertRaises(ValueError):
            self.tools.path("../outside.json")
        with self.assertRaises(ValueError):
            self.tools.path(".env.json")
        self.fixture.data["project_root"] = str(self.base.parent)
        self.save()
        with self.assertRaises(ValueError):
            self.tools.validate("candidates.json")

    def test_candidate_evidence_cannot_escape_project(self):
        self.fixture.data["candidates"][0]["verification"]["evidence"] = "../outside.txt"
        self.save()
        with self.assertRaises(ValueError):
            self.tools.validate("candidates.json")

    def test_skill_install_cannot_recurse_into_source_runtime(self):
        with self.assertRaises(ValueError):
            install_skill.install(ROOT, "agents")
        self.assertFalse((ROOT / ".agents/skills/frontend-inspiration-assistant").exists())

    def test_report_writes_once_and_asks_selection(self):
        result = self.tools.report("candidates.json", "设计灵感/fixture/report.md")
        self.assertEqual(result["status"], "awaiting-selection")
        self.assertFalse(result["implementation_authorized"])
        self.assertIn("希望选择哪些编号", result["markdown"])
        with self.assertRaises(ValueError):
            self.tools.report("candidates.json", "设计灵感/fixture/report.md")
        with self.assertRaises(ValueError):
            self.tools.report("candidates.json", "site.md")

    def test_19_result_diagnostic_still_fails(self):
        self.fixture.data["candidates"].pop()
        self.save()
        output = "设计灵感/fixture/incomplete.md"
        with self.assertRaises(ValueError):
            self.tools.report("candidates.json", output)
        self.assertFalse((self.base / output).exists())
        with self.assertRaises(ValueError):
            self.tools.report("candidates.json", output, True)
        self.assertIn("未达标", (self.base / output).read_text(encoding="utf-8"))

    def test_proposal_never_authorizes_implementation(self):
        (self.base / "brief.json").write_text(json.dumps(proposal_fixture()), encoding="utf-8")
        result = self.tools.proposal("brief.json", "candidates.json", "设计灵感/fixture/brief.md")
        self.assertEqual(result["status"], "awaiting-confirmation")
        self.assertFalse(result["implementation_authorized"])
        self.assertIn("禁止实施", result["markdown"])

    def test_self_contained_skill_install_for_four_clients(self):
        for client in ("claude", "cursor", "codex", "agents"):
            project = self.base / client
            project.mkdir()
            result = install_skill.install(project, client)
            destination = Path(result["skill_root"])
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertEqual(core.package_errors(destination), [])
            run = subprocess.run([sys.executable, str(destination / "scripts/inspiration.py"), "package-check"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(run.returncode, 0, run.stdout)
            self.assertTrue(json.loads(run.stdout)["ok"])
            with self.assertRaises(FileExistsError):
                install_skill.install(project, client)

    def test_generated_configs_preserve_paths_and_parse(self):
        for client in ("claude", "cursor", "stdio", "vscode"):
            config = json.loads(client_config.configuration(self.base, client, sys.executable, True))
            servers = config["servers" if client == "vscode" else "mcpServers"]
            self.assertEqual(servers["frontend-inspiration"]["args"][-1], str(self.base))
            self.assertEqual(servers["frontend-inspiration"]["command"], sys.executable)
            self.assertIn(client_config.PLAYWRIGHT_PACKAGE, servers["playwright"]["args"])
            self.assertEqual(servers["playwright"]["args"][-1], str(self.base / "设计灵感/browser"))
        if sys.version_info >= (3, 11):
            import tomllib
            config = tomllib.loads(client_config.configuration(self.base, "codex", sys.executable, True))
            self.assertEqual(config["mcp_servers"]["frontend-inspiration"]["args"][-1], str(self.base))

    def test_archive_is_named_for_skill_not_source_directory(self):
        archive_path = self.base / "portable.zip"
        run = subprocess.run([sys.executable, str(ROOT / "scripts/inspiration.py"), "pack", "--output", str(archive_path)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout)
        with zipfile.ZipFile(archive_path) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual({name.split("/")[0] for name in archive.namelist()}, {"frontend-inspiration-assistant"})
            self.assertIn("frontend-inspiration-assistant/SKILL.md", archive.namelist())
            self.assertFalse(any("__pycache__" in name for name in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
