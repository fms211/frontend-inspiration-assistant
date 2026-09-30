"""Portable, evidence-aware report/brief/audit utilities. Python 3 stdlib only."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import argparse
import copy
import hashlib
import json
import re
import struct
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.0"
PIN = "09170eec67eefd46a7ae85de61b40c194020f997"
SOURCES = ("https://reactbits.dev/", "https://github.com/DavidHDev/react-bits", "https://hepengwei.cn/", "https://ui.aceternity.com/")
DIRECTIONS = {"布局", "文字排版", "组件交互", "背景", "滚动动效", "动画", "3D"}
TIERS = {"高": 0, "中": 1, "低": 2}
VARIANTS = re.compile(r"\b(?:typescript|javascript|tsx|jsx|ts|js|tailwind|css)\b", re.I)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def filled(value):
    return value is not None and value != "" and value != [] and value != {}


def has_placeholder(value):
    if isinstance(value, dict):
        return any(has_placeholder(v) for v in value.values())
    if isinstance(value, list):
        return any(has_placeholder(v) for v in value)
    return isinstance(value, str) and bool(re.search(r"<[^>]*[\u4e00-\u9fff][^>]*>|\b(?:TODO|TBD)\b|^(?:适当|待定|更好看|同原来)$", value))


def require(obj, keys, label, errors):
    if not isinstance(obj, dict):
        errors.append(f"{label}: must be an object")
        return
    for key in keys:
        if not filled(obj.get(key)):
            errors.append(f"{label}.{key}: required")


def canonical_url(url):
    p = urlsplit(url)
    q = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith("utm_") and k.lower() not in {"ref"}]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/"), urlencode(sorted(q)), p.fragment))


def component_key(candidate):
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(candidate.get("component", "")))
    name = VARIANTS.sub("", re.sub(r"[-_/]", " ", name)).strip().lower()
    name = re.sub(r"\s+", " ", name)
    family = str(candidate.get("family", "")).lower()
    if family in {"reactbits", "react-bits-github", "github-react-bits"}:
        family = "react-bits"
    example = str(candidate.get("example", "")).strip().lower() if family == "hepengwei" else ""
    return family, name, example


def ranking(c):
    scores = c.get("fit_scores", {})
    return (TIERS.get(c.get("relevance"), 99), *(-scores.get(k, 0) for k in ("use", "style", "compatibility", "performance")))


def image_size(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b"\x89PNG\r\n\x1a\n") and raw[12:16] == b"IHDR" and b"IEND" in raw[-12:]:
        return struct.unpack(">II", raw[16:24])
    if raw.startswith(b"\xff\xd8") and raw.endswith(b"\xff\xd9"):
        pos = 2
        while pos + 4 <= len(raw):
            if raw[pos] != 0xff:
                break
            while raw[pos] == 0xff:
                pos += 1
            marker = raw[pos]
            pos += 1
            if marker in {0xd8, 0xd9, 0x01} or 0xd0 <= marker <= 0xd7:
                continue
            length = int.from_bytes(raw[pos:pos+2], "big")
            if length < 2 or pos + length > len(raw):
                break
            if marker in {0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf}:
                h, w = struct.unpack(">HH", raw[pos+3:pos+7])
                return w, h
            pos += length
    raise ValueError("not a supported complete PNG/JPEG screenshot")


def candidate_errors(data, base):
    errors = []
    require(data, ("project_root", "target", "context", "generated_at", "sources", "candidates", "top3_comparison", "combinations", "limitations"), "report", errors)
    source_records = data.get("sources", [])
    for url in SOURCES:
        matching = [s for s in source_records if canonical_url(s.get("entry", "")) == canonical_url(url)]
        if len(matching) != 1:
            errors.append(f"source entrance missing/duplicated: {url}")
        elif matching[0].get("status") not in {"visited", "failed"} or not matching[0].get("detail") or not matching[0].get("checked_at"):
            errors.append(f"source status/detail/time invalid: {url}")
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        return errors + ["candidates must be an array"]
    seen_keys, seen_locations, seen_ids = set(), set(), set()
    valid_browsed = 0
    fields = ("id", "name", "family", "component", "source_url", "directions", "relevance", "target_ui", "reason", "adaptation", "cost", "dependencies", "license", "verification", "fit_scores")
    for i, c in enumerate(candidates):
        label = f"candidate[{i}]"
        require(c, fields, label, errors)
        if not isinstance(c, dict):
            continue
        ident = c.get("id")
        if ident in seen_ids:
            errors.append(f"duplicate id: {ident}")
        seen_ids.add(ident)
        key = component_key(c)
        if key in seen_keys:
            errors.append(f"duplicate component/variant: {ident}: {key}")
        seen_keys.add(key)
        loc = (canonical_url(c.get("source_url", "")), str(c.get("example", "")).strip().lower())
        if loc in seen_locations:
            errors.append(f"same page/example counted twice: {ident}")
        seen_locations.add(loc)
        parsed = urlsplit(c.get("source_url", ""))
        if parsed.scheme != "https" or parsed.netloc not in {"reactbits.dev", "github.com", "hepengwei.cn", "ui.aceternity.com"}:
            errors.append(f"unsupported source URL: {ident}")
        if c.get("family") == "hepengwei" and not parsed.fragment:
            errors.append(f"SPA hash route missing: {ident}")
        if c.get("relevance") not in TIERS or not isinstance(c.get("directions"), list) or not set(c.get("directions", [])) <= DIRECTIONS:
            errors.append(f"invalid relevance/direction: {ident}")
        scores = c.get("fit_scores", {})
        if not isinstance(scores, dict) or any(type(scores.get(k)) is not int or not 0 <= scores[k] <= 5 for k in ("use", "style", "compatibility", "performance")):
            errors.append(f"fit_scores require four 0..5 integers: {ident}")
        verification = c.get("verification", {})
        require(verification, ("status", "checked_at", "actual_url", "interaction_observation", "evidence"), f"{label}.verification", errors)
        if isinstance(verification, dict) and verification.get("status") in {"browser-tested", "browser-viewed"}:
            evidence = base / str(verification.get("evidence", ""))
            if not evidence.is_file():
                errors.append(f"browser evidence file missing: {ident}")
            else:
                valid_browsed += 1
        else:
            errors.append(f"browser verification incomplete: {ident}")
        if i < 5:
            shot = base / str(c.get("screenshot", ""))
            try:
                w, h = image_size(shot)
                if w < 1 or h < 1:
                    raise ValueError("empty image dimensions")
            except (ValueError, OSError, struct.error, IndexError) as exc:
                errors.append(f"top-five screenshot missing/invalid: {ident}: {exc}")
    if len(seen_keys) < 20 or valid_browsed < 20:
        errors.append(f"minimum 20 unique browsed candidates not reached: unique={len(seen_keys)}, browsed={valid_browsed}")
    if all(isinstance(c, dict) and isinstance(c.get("fit_scores"), dict) and all(type(v) is int for v in c["fit_scores"].values()) for c in candidates):
        if [ranking(c) for c in candidates] != sorted(ranking(c) for c in candidates):
            errors.append("relevance/order invalid: high > medium > low; tie: use, style, compatibility, performance")
    return errors


def md(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def write_new(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)


def report_markdown(data, base, errors):
    lines = [f"# {data.get('target', '前端灵感')} · 灵感汇总", "", f"时间：{data.get('generated_at')}。状态：{'未达标' if errors else '浏览与报告校验通过'}。", "", data.get("context", ""), "", "## 四个入口", ""]
    for s in data.get("sources", []):
        lines.append(f"- [{s.get('entry')}]({s.get('entry')})：{s.get('status')}；{s.get('detail')}；{s.get('checked_at')}")
    if errors:
        lines += ["", "## 未达标原因", ""] + [f"- {e}" for e in errors]
    lines += ["", "## 完整候选表", "", "| 编号 | 名称与来源 | 方向 | 相关度 | 适用页面/UI | 贴合理由 | 需要怎样调整 | 成本 | 依赖与授权 | 浏览验证 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in data.get("candidates", []):
        v = c.get("verification", {})
        values = [c.get("id"), f"[{c.get('name')}]({c.get('source_url')})", "、".join(c.get("directions", [])), c.get("relevance"), c.get("target_ui"), c.get("reason"), c.get("adaptation"), c.get("cost"), f"{c.get('dependencies')}；{c.get('license')}", v.get("status")]
        lines.append("| " + " | ".join(md(x) for x in values) + " |")
    lines += ["", "## 前五条真实截图", "", "截图证明外观；触发动作和动效观察记录在下一节，原演示的未测时长/帧率不作推断。", ""]
    for c in data.get("candidates", [])[:5]:
        shot = base / str(c.get("screenshot", ""))
        if shot.is_file():
            lines += [f"### {c.get('id')} {c.get('name')}", "", f"![{c.get('name')}]({shot.resolve().as_posix()})", ""]
    lines += ["## 逐条浏览观察", ""]
    for c in data.get("candidates", []):
        v = c.get("verification", {})
        evidence = (base / str(v.get("evidence", ""))).resolve().as_posix()
        lines += [f"- **{c.get('id')}**：{v.get('interaction_observation')} 实际URL：[{v.get('actual_url')}]({v.get('actual_url')})；时间：{v.get('checked_at')}；[证据]({evidence})。"]
    lines += ["", "## 前三条比较", "", data.get("top3_comparison", ""), "", "## 可组合方向", "", data.get("combinations", ""), "", "## 验证边界", "", data.get("limitations", ""), "", "## 选择", "", "希望选择哪些编号？可以单选、多选、组合，或更换方向。选择后先生成逐元素方案；确认具体方案后才修改项目。", ""]
    return "\n".join(lines)


ELEMENT_KEYS = {
    "location": ("route", "region", "parent_ui", "visible_name", "position"),
    "text": ("current", "proposed", "font_family", "font_size", "font_weight", "line_height", "letter_spacing"),
    "layout": ("width", "height", "gap", "padding", "alignment", "hierarchy", "z_index", "mobile"),
    "visual": ("colors", "radius", "border", "opacity", "shadow"),
    "motion": ("trigger", "start", "end", "duration_ms", "delay_ms", "easing", "amplitude", "loop", "interruption", "reduced_motion"),
    "implementation": ("files", "component", "dependencies", "expected", "steps", "acceptance", "rollback"),
}


def brief_errors(data, candidates):
    errors = []
    require(data, ("target", "selected_ids", "selection_origin", "selection_text", "elements", "audit_summary"), "brief", errors)
    if has_placeholder(data):
        errors.append("brief contains unfilled template/vague parameters; concrete values or project tokens required")
    ids = {c.get("id") for c in candidates.get("candidates", [])}
    selected = data.get("selected_ids", [])
    if not isinstance(selected, list) or len(selected) != len(set(selected)) or any(i not in ids for i in selected):
        errors.append("selection contains missing/duplicate candidate IDs")
    if data.get("selection_origin") not in {"user", "test-fixture"}:
        errors.append("selection_origin must be user or test-fixture")
    for i, element in enumerate(data.get("elements", [])):
        require(element, ("candidate_ids", "observed_original", *ELEMENT_KEYS), f"element[{i}]", errors)
        if not set(element.get("candidate_ids", [])) <= set(selected):
            errors.append(f"element[{i}] refers to unselected candidates")
        for key, fields in ELEMENT_KEYS.items():
            require(element.get(key), fields, f"element[{i}].{key}", errors)
        for field in ("duration_ms", "delay_ms"):
            val = element.get("motion", {}).get(field)
            if type(val) not in (int, float) or val < 0:
                errors.append(f"element[{i}].motion.{field}: nonnegative milliseconds required")
    return errors


def brief_markdown(data):
    lines = [f"# {data['target']} · 待确认实施方案", "", f"选择来源：{data['selection_origin']}；编号：{', '.join(data['selected_ids'])}；原话：{data['selection_text']}", ""]
    if data["selection_origin"] == "test-fixture":
        lines += ["> 此文件仅验证候选→方案衔接。用户尚未选择，禁止实施。", ""]
    for i, element in enumerate(data["elements"], 1):
        lines += [f"## 元素 {i}：{element['location']['visible_name']}", "", f"候选：{', '.join(element['candidate_ids'])}；原效果：{element['observed_original']}", "", "| 项目 | 拟实施的具体参数 |", "|---|---|"]
        for key in ELEMENT_KEYS:
            content = "<br>".join(f"**{k}**：{md(v)}" for k, v in element[key].items())
            lines.append(f"| {key} | {content} |")
        lines.append("")
    lines += ["## 方案审计", "", data["audit_summary"], "", "## 实施确认", "", "请确认上述具体方案及修改范围。确认之前保持待实施状态；候选选择不等于修改项目的授权。", ""]
    return "\n".join(lines)


def audit_errors(data):
    errors = []
    require(data, ("stage", "target", "coverage", "limitations"), "audit", errors)
    if not isinstance(data.get("findings"), list):
        errors.append("audit.findings must be an array (empty allowed for a clean audit)")
        return errors
    if data.get("stage") not in {"candidates", "brief", "baseline", "implemented"}:
        errors.append("invalid audit stage")
    for i, f in enumerate(data.get("findings", [])):
        require(f, ("location", "issue", "priority", "evidence", "evidence_level", "skill", "parameters", "verification", "retest"), f"finding[{i}]", errors)
        if f.get("evidence_level") not in {"rule", "code", "browser"} or f.get("priority") not in {"P0", "P1", "P2", "P3"} or f.get("verification") not in {"proposed", "confirmed", "fixed", "not-tested"}:
            errors.append(f"invalid finding priority/evidence/status: {i}")
        if f.get("evidence_level") == "rule" and f.get("verification") in {"confirmed", "fixed"}:
            errors.append(f"rule-only finding cannot claim tested/fixed: {i}")
    return errors


def package_errors(root=ROOT):
    errors = []
    try:
        manifest = read_json(root / "plugin.json")
        if manifest.get("name") != "frontend-inspiration-assistant" or manifest.get("version") != VERSION:
            errors.append("plugin identity/version mismatch")
        if any(k in manifest for k in ("skills", "apps", "mcpServers", "interface")):
            errors.append("non-portable top-level manifest field")
        interface = manifest["extensions"]["com.openai"]["interface"]
        if len(interface["shortDescription"]) > 30:
            errors.append("shortDescription exceeds 30 characters")
        for key in ("logo", "composerIcon"):
            path = (root / interface[key]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
                errors.append(f"icon missing/outside/oversize: {key}")
                continue
            svg = ET.fromstring(path.read_text(encoding="utf-8"))
            w, h = float(svg.get("width", 0)), float(svg.get("height", 0))
            if w != h or w < 48:
                errors.append("icon must be square and >=48px")
        for name in ("frontend-inspiration", "frontend-audit", "ui-ux-pro-max"):
            skill = root / "skills" / name / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            if not text.startswith("---\n") or f"name: {name}\n" not in text or "\ndescription:" not in text:
                errors.append(f"invalid skill entry: {name}")
        audit_root = root / "skills/ui-ux-pro-max"
        record = read_json(audit_root / "UPSTREAM.json")
        if record.get("commit") != PIN or record.get("license") != "MIT":
            errors.append("upstream pin/license mismatch")
        for relative, expected in record.get("upstream_files", {}).items():
            path = (audit_root / relative).resolve()
            if not path.is_relative_to(audit_root.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f"upstream file missing/modified: {relative}")
        if len(list((audit_root / "data/stacks").glob("*.csv"))) != 22 or len(record.get("upstream_files", {})) < 90:
            errors.append("official runtime/data incomplete")
        if "MIT License" not in (audit_root / "LICENSE").read_text(encoding="utf-8"):
            errors.append("upstream MIT notice missing")
    except (OSError, ValueError, KeyError, ET.ParseError, TypeError) as exc:
        errors.append(f"package structure invalid: {exc}")
    return errors


def parse_rule_result(process):
    if process.returncode != 0:
        raise ValueError(f"audit command failed: {process.stderr.strip() or process.stdout.strip()}")
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"audit returned non-JSON/error output: {process.stdout[:300]}") from exc
    if not isinstance(result, dict):
        raise ValueError("audit returned unexpected JSON type despite exit code 0")
    if result.get("error") or type(result.get("count")) is not int or result["count"] < 1 or not result.get("results"):
        raise ValueError(f"audit returned error/empty result despite exit code 0: {result.get('error', 'no matches')}")
    return result


def audit_rules(query, domain=None, stack=None):
    errors = package_errors()
    if errors:
        raise ValueError("audit data integrity failed: " + "; ".join(errors))
    command = [sys.executable, str(ROOT / "skills/ui-ux-pro-max/scripts/search.py"), query, "--json", "-n", "3"]
    if domain:
        command += ["--domain", domain]
    if stack:
        command += ["--stack", stack]
    result = parse_rule_result(subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=45))
    return {"ok": True, "evidence_level": "rule", "browser_verified": False, "upstream_commit": PIN, "result": result}


def inspect_project(project):
    root = Path(project).resolve()
    package = read_json(root / "package.json") if (root / "package.json").exists() else {}
    deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    stack = next((s for d, s in (("react-native", "react-native"), ("next", "nextjs"), ("nuxt", "nuxtjs"), ("@angular/core", "angular"), ("vue", "vue"), ("svelte", "svelte"), ("astro", "astro"), ("react", "react")) if d in deps), "html-tailwind" if (root / "index.html").exists() else "unknown")
    documents = [str(root / n) for n in ("AGENTS.md", "PRODUCT.md", "DESIGN.md", "README.md", "package.json") if (root / n).is_file()]
    return {"ok": True, "project_root": str(root), "stack": stack, "name": package.get("name", root.name), "dependencies": deps, "context_documents": documents, "note": "只读识别；仍须阅读实际设计规范和目标页面。未知栈不默认React Native。"}


def stack_projection(data, stack):
    candidates = copy.deepcopy(data["candidates"])
    for c in candidates:
        react_web = c.get("family") in {"react-bits", "aceternity"}
        if react_web and stack not in {"react", "nextjs"}:
            c["fit_scores"]["compatibility"] = min(c["fit_scores"]["compatibility"], 2)
            if c["relevance"] == "高":
                c["relevance"] = "中"
            c["stack_note"] = "来源是React网页组件，不能直接用于此栈；仅借鉴模式，事件/状态/动画和依赖需重写。"
        elif react_web:
            c["stack_note"] = "React网页来源与当前栈匹配；Next.js交互放Client叶组件，新增依赖与SSR行为仍须核实。" if stack == "nextjs" else "React网页来源匹配，仍需核实依赖及实际版本。"
        else:
            c["stack_note"] = "HTML/CSS设计模式可跨网页栈借鉴；源码授权未知，自行实现并验收。"
        c["source_id"] = c["id"]
    candidates.sort(key=ranking)
    return {"ok": True, "stack": stack, "evidence_level": "rule", "browser_verified": False, "note": "兼容性投影；不是新一轮实时检索，也不覆盖用户/项目约束，最终排名仍结合用途和风格。", "candidates": candidates}


def safe_report_output(data, output):
    allowed = (Path(data["project_root"]).resolve() / "设计灵感").resolve()
    if not Path(output).resolve().is_relative_to(allowed):
        raise ValueError("report output must be inside current project's 设计灵感 directory")


def audit_markdown(data):
    lines = [f"# {data['target']} · {data['stage']}审计", "", "证据级别：rule规则建议 / code代码检查 / browser浏览器实测。", "", f"覆盖：{md(data['coverage'])}", "", "| 位置 | 问题 | 优先级 | 证据与技能 | 参数建议 | 验证与复测 |", "|---|---|---|---|---|---|"]
    for finding in data["findings"]:
        lines.append("| " + " | ".join(md(v) for v in (finding["location"], finding["issue"], finding["priority"], f"{finding['evidence_level']} / {finding['skill']} / {finding['evidence']}", finding["parameters"], f"{finding['verification']} / {finding['retest']}")) + " |")
    lines += ["", "验证边界：" + data["limitations"], ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("--project", required=True)
    for name in ("validate", "report", "brief", "audit-report"):
        p = sub.add_parser(name)
        p.add_argument("input")
        if name != "validate":
            p.add_argument("--output", required=True)
        if name == "report":
            p.add_argument("--allow-incomplete", action="store_true")
        if name == "brief":
            p.add_argument("--candidates", required=True)
    rules = sub.add_parser("audit-rules")
    rules.add_argument("query")
    group = rules.add_mutually_exclusive_group()
    group.add_argument("--domain")
    group.add_argument("--stack")
    rules.add_argument("--output")
    fit = sub.add_parser("stack-fit")
    fit.add_argument("input")
    fit.add_argument("--stack", required=True, choices=("react", "nextjs", "vue", "nuxtjs", "svelte", "astro", "html-tailwind", "react-native", "angular"))
    fit.add_argument("--output")
    sub.add_parser("package-check")
    pack = sub.add_parser("pack")
    pack.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            emit(inspect_project(args.project))
        elif args.command in {"validate", "report"}:
            source = Path(args.input).resolve()
            data = read_json(source)
            errors = candidate_errors(data, source.parent)
            if args.command == "report" and (not errors or args.allow_incomplete):
                safe_report_output(data, args.output)
                write_new(args.output, report_markdown(data, source.parent, errors))
            emit({"ok": not errors, "count": len(data.get("candidates", [])), "errors": errors})
            return 2 if errors else 0
        elif args.command == "brief":
            data = read_json(args.input)
            errors = brief_errors(data, read_json(args.candidates))
            if not errors:
                write_new(args.output, brief_markdown(data))
            emit({"ok": not errors, "status": "awaiting-confirmation", "errors": errors})
            return 2 if errors else 0
        elif args.command == "audit-report":
            data = read_json(args.input)
            errors = audit_errors(data)
            if not errors:
                write_new(args.output, audit_markdown(data))
            emit({"ok": not errors, "errors": errors})
            return 2 if errors else 0
        elif args.command == "audit-rules":
            result = audit_rules(args.query, args.domain, args.stack)
            if args.output:
                write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            emit(result)
        elif args.command == "stack-fit":
            result = stack_projection(read_json(args.input), args.stack)
            if args.output:
                write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            emit({"ok": True, "stack": args.stack, "candidates": [{"source_id": c["source_id"], "name": c["name"], "relevance":c["relevance"], "compatibility":c["fit_scores"]["compatibility"], "stack_note":c["stack_note"]} for c in result["candidates"]]})
        elif args.command in {"package-check", "pack"}:
            errors = package_errors()
            if not errors and args.command == "pack":
                destination = Path(args.output).resolve()
                if destination.is_relative_to(ROOT) or destination.exists():
                    raise ValueError("archive must be new and outside plugin root")
                destination.parent.mkdir(parents=True, exist_ok=True)
                package_name = read_json(ROOT / "plugin.json")["name"]
                with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as archive:
                    for path in sorted(ROOT.rglob("*")):
                        if path.is_symlink():
                            raise ValueError(f"symlinks are not portable: {path}")
                        if path.is_file() and not set(path.relative_to(ROOT).parts) & {"__pycache__", ".git", "node_modules"} and path.suffix != ".pyc":
                            archive.write(path, f"{package_name}/{path.relative_to(ROOT).as_posix()}")
                with zipfile.ZipFile(destination) as archive:
                    if archive.testzip() or len({n.split('/')[0] for n in archive.namelist()}) != 1:
                        raise ValueError("archive validation failed")
                emit({"ok": True, "archive": str(destination), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()})
            else:
                emit({"ok": not errors, "errors": errors})
            return 2 if errors else 0
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        emit({"ok": False, "error": str(exc)})
        return 2
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
