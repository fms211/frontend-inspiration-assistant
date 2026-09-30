import base64
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inspiration", ROOT / "scripts/inspiration.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Contracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        (self.base / "evidence.txt").write_text("fixture browser evidence", encoding="utf-8")
        (self.base / "shot.png").write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jD1sAAAAASUVORK5CYII="))
        self.data = {
            "project_root": str(self.base), "target": "fixture", "context": "fixture only", "generated_at": "2026-09-30T19:00:00+08:00",
            "sources": [{"entry": s, "status": "visited", "detail": "fixture", "checked_at": "fixture time"} for s in module.SOURCES],
            "top3_comparison": "fixture", "combinations": "fixture", "limitations": "fixture not live", "candidates": [],
        }
        for i in range(20):
            self.data["candidates"].append({
                "id": str(i), "name": f"Effect {i}", "family": "react-bits", "component": f"Effect {i}", "example": "",
                "source_url": f"https://reactbits.dev/components/effect-{i}", "directions": ["组件交互"], "relevance": "高",
                "target_ui": "fixture", "reason": "fixture", "adaptation": "fixture", "cost": "低", "dependencies": "none", "license": "fixture only",
                "fit_scores": {"use": 5, "style": 4, "compatibility": 4, "performance": 4}, "screenshot": "shot.png",
                "verification": {"status": "browser-tested", "checked_at": "fixture", "actual_url": "https://reactbits.dev/", "interaction_observation": "fixture", "evidence": "evidence.txt"},
            })

    def errors(self):
        return module.candidate_errors(self.data, self.base)

    def test_20_complete(self):
        self.assertEqual(self.errors(), [])

    def test_same_component_language_style_and_github_are_duplicate(self):
        duplicate = copy.deepcopy(self.data["candidates"][0])
        duplicate.update(id="extra", family="react-bits-github", component="Effect 0 TS Tailwind", source_url="https://github.com/DavidHDev/react-bits", example="misleading variant")
        self.data["candidates"].append(duplicate)
        self.assertTrue(any("duplicate component" in x for x in self.errors()))

    def test_19_fails(self):
        self.data["candidates"].pop()
        self.assertTrue(any("minimum 20" in x for x in self.errors()))

    def test_relevance_and_tie_sort(self):
        self.data["candidates"][0]["relevance"] = "中"
        self.assertTrue(any("order invalid" in x for x in self.errors()))
        self.data["candidates"][0]["relevance"] = "高"
        self.data["candidates"][1]["fit_scores"]["use"] = 4
        self.assertTrue(any("order invalid" in x for x in self.errors()))

    def test_missing_or_corrupt_screenshot(self):
        self.data["candidates"][3]["screenshot"] = "missing.jpg"
        self.assertTrue(any("top-five screenshot" in x for x in self.errors()))
        (self.base / "invalid.jpg").write_text("not an image")
        self.data["candidates"][3]["screenshot"] = "invalid.jpg"
        self.assertTrue(any("top-five screenshot" in x for x in self.errors()))

    def test_source_failure_retained_without_fake_count(self):
        self.data["sources"][3].update(status="failed", detail="browser crashed")
        self.assertEqual(self.errors(), [])
        self.assertIn("browser crashed", module.report_markdown(self.data, self.base, []))
        self.data["candidates"].pop()
        self.assertTrue(self.errors())

    def test_docs_only_does_not_pass_browser_count(self):
        self.data["candidates"][0]["verification"]["status"] = "docs-only"
        self.assertTrue(any("browser verification incomplete" in x for x in self.errors()))

    def test_spa_hash_is_preserved(self):
        self.assertNotEqual(module.canonical_url("https://hepengwei.cn/#/css/a"), module.canonical_url("https://hepengwei.cn/#/css/b"))

    def test_zero_exit_error_and_empty_fail(self):
        for stdout in ('Error: Stack file not found', '{"error":"missing","count":0}', '{"count":0,"results":[]}', '[]', 'null', '{"count":true,"results":[{}]}'):
            with self.subTest(stdout=stdout), self.assertRaises(ValueError):
                module.parse_rule_result(subprocess.CompletedProcess([], 0, stdout, ""))

    def test_official_data_missing_fails_closed(self):
        target = self.base / "package"
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (target / "skills/ui-ux-pro-max/data/stacks/nextjs.csv").unlink()
        self.assertTrue(any("nextjs.csv" in x or "incomplete" in x for x in module.package_errors(target)))

    def test_selection_to_brief_and_unknown_id(self):
        brief = {
            "target": "发送按钮fixture", "selected_ids":["0"], "selection_origin":"test-fixture", "selection_text":"fixture, not user choice", "audit_summary":"rule only; runtime pending",
            "elements":[{"candidate_ids":["0"],"observed_original":"fixture appearance only",
                "location":{"route":"/","region":"chat footer","parent_ui":"Composer","visible_name":"发送","position":"textarea right"},
                "text":{"current":"发送","proposed":"发送","font_family":"sans-serif","font_size":"14px","font_weight":500,"line_height":"20px","letter_spacing":"0px"},
                "layout":{"width":"44px","height":"44px","gap":"8px","padding":"8px","alignment":"center","hierarchy":"primary","z_index":10,"mobile":"390px: same 44px target"},
                "visual":{"colors":"var(--primary)","radius":"50%","border":"none","opacity":1,"shadow":"none"},
                "motion":{"trigger":"request starts","start":"opacity 1","end":"opacity 0.7","duration_ms":180,"delay_ms":0,"easing":"ease-out","amplitude":"0px","loop":False,"interruption":"replace with latest state","reduced_motion":"no animation"},
                "implementation":{"files":["Composer.tsx"],"component":"SendButton","dependencies":"none","expected":"loading feedback","steps":["bind loading state"],"acceptance":["keyboard activation once"],"rollback":"restore component"}}],
        }
        self.assertEqual(module.brief_errors(brief, self.data), [])
        self.assertIn("禁止实施", module.brief_markdown(brief))
        brief["selected_ids"] = ["missing"]
        self.assertTrue(module.brief_errors(brief, self.data))

    def test_unfilled_element_template_cannot_pass(self):
        template = json.loads((ROOT / "templates/implementation.json").read_text(encoding="utf-8"))
        self.assertTrue(any("unfilled template" in e for e in module.brief_errors(template, self.data)))

    def test_stack_detection_next_vue_and_html(self):
        for deps, expected in (({"next": "16", "react": "19"}, "nextjs"), ({"vue": "3"}, "vue")):
            (self.base / "package.json").write_text(json.dumps({"dependencies": deps}), encoding="utf-8")
            self.assertEqual(module.inspect_project(self.base)["stack"], expected)
        (self.base / "package.json").unlink()
        (self.base / "index.html").write_text("<main>fixture</main>")
        self.assertEqual(module.inspect_project(self.base)["stack"], "html-tailwind")

    def test_rule_cannot_claim_browser_confirmation(self):
        audit = json.loads((ROOT / "templates/audit.json").read_text(encoding="utf-8"))
        audit["findings"][0]["verification"] = "confirmed"
        self.assertTrue(any("rule-only" in x for x in module.audit_errors(audit)))

    def test_output_stays_in_project_design_folder(self):
        with self.assertRaises(ValueError):
            module.safe_report_output(self.data, self.base / "outside.md")

    def test_web_component_recommendation_changes_for_vue(self):
        react = module.stack_projection(self.data, "nextjs")
        vue = module.stack_projection(self.data, "vue")
        self.assertEqual(react["candidates"][0]["relevance"], "高")
        self.assertEqual(vue["candidates"][0]["relevance"], "中")
        self.assertLess(vue["candidates"][0]["fit_scores"]["compatibility"], react["candidates"][0]["fit_scores"]["compatibility"])
        self.assertEqual(self.data["candidates"][0]["relevance"], "高")

    def test_clean_audit_is_valid(self):
        audit = json.loads((ROOT / "templates/audit.json").read_text(encoding="utf-8"))
        audit["findings"] = []
        self.assertEqual(module.audit_errors(audit), [])


if __name__ == "__main__":
    unittest.main()
