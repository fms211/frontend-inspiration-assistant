"""Expose portable frontend research tools over MCP stdio for an explicit project."""
import argparse
import subprocess
import sys
from typing import Any, Literal
from agent_tools import AgentTools
import inspiration as core


def build_server(project):
    try:
        from mcp.server import MCPServer
        from mcp.server.mcpserver.exceptions import ToolError
    except ImportError as exc:
        raise RuntimeError("MCP SDK missing. Install this bundle's requirements-mcp.txt with the Python used by the client.") from exc
    tools = AgentTools(project)
    def invoke(method, *args):
        try:
            return method(*args)
        except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
            raise ToolError(str(exc)) from exc

    server = MCPServer("frontend-inspiration-assistant", version=core.VERSION,
                       instructions="For frontend design or motion inspiration, call inspiration_get_workflow first. Browse with the host's real browser tools; reports require 20 unique candidates and real evidence. Ask for user selection and concrete-plan confirmation before host implementation.")

    @server.tool(structured_output=True)
    def inspiration_get_workflow() -> dict[str, Any]:
        """Start a project-aware frontend/UI/motion inspiration workflow; discover constraints, sources, browser needs, and confirmation gates."""
        return invoke(tools.workflow)

    @server.tool(structured_output=True)
    def inspiration_inspect_project() -> dict[str, Any]:
        """Identify the configured project's stack, dependencies and design/context documents without editing the website."""
        return invoke(tools.inspect)

    @server.tool(structured_output=True)
    def inspiration_get_template(kind: Literal["candidates", "implementation", "audit"]) -> dict[str, Any]:
        """Get a report, element-level proposal, or evidence-aware audit template to fill from actual observations."""
        return invoke(tools.template, kind)

    @server.tool(structured_output=True)
    def inspiration_save_artifact(kind: Literal["candidates", "implementation", "audit", "browser-evidence"], payload: dict[str, Any], output_path: str) -> dict[str, Any]:
        """Save supplied structured candidate/proposal/audit/browser evidence JSON without requiring another filesystem tool. This does not validate evidence or authorize implementation."""
        return invoke(tools.save_artifact, kind, payload, output_path)

    @server.tool(structured_output=True)
    def inspiration_validate_candidates(input_path: str) -> dict[str, Any]:
        """Validate 20+ unique ranked candidates, all four source statuses, evidence files and five real screenshots. Invalid reports are MCP errors."""
        return invoke(tools.validate, input_path)

    @server.tool(structured_output=True)
    def inspiration_write_report(input_path: str, output_path: str, allow_incomplete: bool = False) -> dict[str, Any]:
        """Save full candidate Markdown in the project's 设计灵感 directory, then ask user selection. Incomplete diagnostics remain errors even if saved."""
        return invoke(tools.report, input_path, output_path, allow_incomplete)

    @server.tool(structured_output=True)
    def inspiration_write_proposal(input_path: str, candidates_path: str, output_path: str) -> dict[str, Any]:
        """Validate selected IDs and concrete element parameters; save a pending-confirmation proposal. Never authorizes website edits."""
        return invoke(tools.proposal, input_path, candidates_path, output_path)

    @server.tool(structured_output=True)
    def inspiration_audit_rules(query: str, domain: str | None = None, stack: str | None = None) -> dict[str, Any]:
        """Search bundled UI UX Pro Max rules and stack guidance; rule suggestions are not browser tests. Choose domain or stack."""
        return invoke(tools.rules, query, domain, stack)

    @server.tool(structured_output=True)
    def inspiration_write_audit(input_path: str, output_path: str) -> dict[str, Any]:
        """Validate and save audit findings distinguishing rule, code and browser evidence, including untested coverage."""
        return invoke(tools.audit, input_path, output_path)

    @server.tool(structured_output=True)
    def inspiration_stack_fit(input_path: str, stack: Literal["react", "nextjs", "vue", "nuxtjs", "svelte", "astro", "html-tailwind", "react-native", "angular"]) -> dict[str, Any]:
        """Project candidate compatibility onto another stack; explicitly returns rule-level guidance, not a new browser round."""
        return invoke(tools.fit, input_path, stack)

    @server.resource("inspiration://workflow")
    def workflow_resource() -> str:
        """Read the portable workflow and confirmation boundaries."""
        return tools.workflow()["instructions"]

    @server.resource("inspiration://sources")
    def source_resource() -> str:
        """Read source research and evidence requirements."""
        return (core.ROOT / "skills/frontend-inspiration/references/sources.md").read_text(encoding="utf-8")

    @server.resource("inspiration://implementation")
    def implementation_resource() -> str:
        """Read element-level proposal parameters and implementation confirmation requirements."""
        return (core.ROOT / "skills/frontend-inspiration/references/implementation.md").read_text(encoding="utf-8")

    @server.resource("inspiration://audit")
    def audit_resource() -> str:
        """Read audit coverage and rule/code/browser evidence requirements."""
        return (core.ROOT / "skills/frontend-inspiration/references/audit.md").read_text(encoding="utf-8")

    @server.resource("inspiration://host-adapters")
    def adapter_resource() -> str:
        """Read browser and optional design skill capability adaptation guidance."""
        return (core.ROOT / "skills/frontend-inspiration/references/host-adapters.md").read_text(encoding="utf-8")

    @server.prompt()
    def frontend_inspiration(target: str) -> str:
        """Start a 20+ candidate frontend inspiration round for a named project target."""
        return f"Research UI and motion inspiration for: {target}. Call inspiration_get_workflow, inspect the configured project, browse all four entrances with actual browser tools, record 20+ distinct ranked candidates and five real screenshots, save Markdown, then ask which IDs the user chooses. Prepare and audit a concrete element-level proposal; wait for confirmation before implementation."

    return server


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Project root; all tool file access is confined here")
    args = parser.parse_args(argv)
    try:
        server = build_server(args.project)
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
