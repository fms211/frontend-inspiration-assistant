"""Actual MCP subprocess/client tests; fixtures are explicitly not live browser research."""
import json
from pathlib import Path
import sys
import unittest

import test_contracts as fixtures
from test_portable import proposal_fixture

try:
    from mcp import Client, StdioServerParameters
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(HAS_MCP, "Install requirements-mcp.txt to run actual MCP protocol tests")
class MCPStdio(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.fixture = fixtures.Contracts("test_20_complete")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.base = self.fixture.base
        (self.base / "candidates.json").write_text(json.dumps(self.fixture.data), encoding="utf-8")
        (self.base / "package.json").write_text('{"name":"stdio-fixture","dependencies":{"next":"16"}}', encoding="utf-8")
        (self.base / "DESIGN.md").write_text("fixture design: readable UI, restrained animation", encoding="utf-8")
        self.params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "scripts/mcp_server.py"), "--project", str(self.base)], env={"PYTHONUTF8": "1"})

    async def test_discovery_resources_prompts_and_rule_search(self):
        async with Client(self.params, read_timeout_seconds=40) as client:
            tools = await client.list_tools()
            self.assertEqual(len(tools.tools), 10)
            workflow = await client.call_tool("inspiration_get_workflow")
            self.assertFalse(workflow.is_error)
            self.assertEqual(workflow.structured_content["minimum_unique_candidates"], 20)
            self.assertFalse(workflow.structured_content["implementation_authorized"])
            inspect = await client.call_tool("inspiration_inspect_project")
            self.assertEqual(inspect.structured_content["stack"], "nextjs")
            self.assertIn("readable UI", inspect.structured_content["context_previews"][0]["text"])
            template = await client.call_tool("inspiration_get_template", {"kind": "candidates"})
            self.assertEqual(template.structured_content["template"]["project_root"], str(self.base))
            resources = await client.list_resources()
            self.assertEqual(len(resources.resources), 5)
            resource = await client.read_resource("inspiration://workflow")
            self.assertIn("具体方案", resource.contents[0].text)
            for name in workflow.structured_content["reference_resources"]:
                reference = await client.read_resource(f"inspiration://{name}")
                self.assertGreater(len(reference.contents[0].text), 100)
            prompts = await client.list_prompts()
            self.assertEqual(len(prompts.prompts), 1)
            prompt = await client.get_prompt("frontend_inspiration", {"target": "fixture panel"})
            self.assertIn("fixture panel", prompt.messages[0].content.text)
            rules = await client.call_tool("inspiration_audit_rules", {"query": "animation reduced motion", "domain": "ux"})
            self.assertFalse(rules.is_error)
            self.assertFalse(rules.structured_content["browser_verified"])

    async def test_structured_submission_needs_no_extra_filesystem_tool(self):
        async with Client(self.params, read_timeout_seconds=30) as client:
            saved = await client.call_tool("inspiration_save_artifact", {"kind": "browser-evidence", "payload": {"observation": "fixture only"}, "output_path": "设计灵感/submitted/evidence.json"})
            self.assertFalse(saved.is_error)
            self.assertEqual(saved.structured_content["validation_status"], "not-validated")
            payload = dict(self.fixture.data)
            payload["project_root"] = "caller value overridden by configured project"
            payload["candidates"] = [dict(item, screenshot="../../shot.png", verification={**item["verification"], "evidence": "../../evidence.txt"}) for item in self.fixture.data["candidates"]]
            submitted = await client.call_tool("inspiration_save_artifact", {"kind": "candidates", "payload": payload, "output_path": "设计灵感/submitted/candidates.json"})
            self.assertFalse(submitted.is_error)
            valid = await client.call_tool("inspiration_validate_candidates", {"input_path": "设计灵感/submitted/candidates.json"})
            self.assertFalse(valid.is_error)
            self.assertEqual(valid.structured_content["count"], 20)
            invalid = await client.call_tool("inspiration_save_artifact", {"kind": "browser-evidence", "payload": {}, "output_path": "site.json"})
            self.assertTrue(invalid.is_error)
            self.assertFalse((self.base / "site.json").exists())

    async def test_legacy_client_initialization_and_tool_call(self):
        async with Client(self.params, mode="legacy", read_timeout_seconds=30) as client:
            result = await client.call_tool("inspiration_inspect_project")
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content["stack"], "nextjs")

    async def test_real_report_to_proposal_handoff(self):
        (self.base / "brief.json").write_text(json.dumps(proposal_fixture()), encoding="utf-8")
        async with Client(self.params, read_timeout_seconds=30) as client:
            validated = await client.call_tool("inspiration_validate_candidates", {"input_path": "candidates.json"})
            self.assertFalse(validated.is_error)
            self.assertEqual(validated.structured_content["count"], 20)
            report = await client.call_tool("inspiration_write_report", {"input_path": "candidates.json", "output_path": "设计灵感/fixture/report.md"})
            self.assertFalse(report.is_error)
            self.assertEqual(report.structured_content["status"], "awaiting-selection")
            proposal = await client.call_tool("inspiration_write_proposal", {"input_path": "brief.json", "candidates_path": "candidates.json", "output_path": "设计灵感/fixture/brief.md"})
            self.assertFalse(proposal.is_error)
            self.assertFalse(proposal.structured_content["implementation_authorized"])
            self.assertEqual(proposal.structured_content["status"], "awaiting-confirmation")

    async def test_stack_projection_and_evidence_aware_audit(self):
        data = {"stage": "baseline", "target": "fixture", "coverage": {"desktop": "not-tested"}, "limitations": "fixture, not browser-tested", "findings": []}
        (self.base / "audit.json").write_text(json.dumps(data), encoding="utf-8")
        async with Client(self.params, read_timeout_seconds=30) as client:
            fit = await client.call_tool("inspiration_stack_fit", {"input_path": "candidates.json", "stack": "vue"})
            self.assertFalse(fit.is_error)
            self.assertFalse(fit.structured_content["browser_verified"])
            self.assertEqual(fit.structured_content["candidates"][0]["relevance"], "中")
            audit = await client.call_tool("inspiration_write_audit", {"input_path": "audit.json", "output_path": "设计灵感/fixture/audit.md"})
            self.assertFalse(audit.is_error)
            self.assertIn("not-tested", audit.structured_content["markdown"])
            data["findings"] = [{"location": "fixture button", "issue": "fixture only", "priority": "P2", "evidence": "rule only", "evidence_level": "rule", "skill": "ui-ux-pro-max", "parameters": "16px", "verification": "confirmed", "retest": "browser untested"}]
            (self.base / "audit.json").write_text(json.dumps(data), encoding="utf-8")
            invalid = await client.call_tool("inspiration_write_audit", {"input_path": "audit.json", "output_path": "设计灵感/fixture/invalid-audit.md"})
            self.assertTrue(invalid.is_error)
            self.assertFalse((self.base / "设计灵感/fixture/invalid-audit.md").exists())

    async def test_invalid_incomplete_and_outside_inputs_are_mcp_errors(self):
        self.fixture.data["candidates"].pop()
        (self.base / "candidates.json").write_text(json.dumps(self.fixture.data), encoding="utf-8")
        async with Client(self.params, read_timeout_seconds=30) as client:
            invalid = await client.call_tool("inspiration_validate_candidates", {"input_path": "candidates.json"})
            self.assertTrue(invalid.is_error)
            incomplete = await client.call_tool("inspiration_write_report", {"input_path": "candidates.json", "output_path": "设计灵感/fixture/incomplete.md", "allow_incomplete": True})
            self.assertTrue(incomplete.is_error)
            self.assertTrue((self.base / "设计灵感/fixture/incomplete.md").exists())
            outside = await client.call_tool("inspiration_validate_candidates", {"input_path": "../outside.json"})
            self.assertTrue(outside.is_error)


if __name__ == "__main__":
    unittest.main()
