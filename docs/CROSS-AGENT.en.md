# Cross-agent setup · 0.2.0

[简体中文](./CROSS-AGENT.md) · [README](../README.en.md)

One frontend inspiration workflow, delivered as **Agent Skills, MCP stdio tools, and a CLI**. Skill descriptions and tool metadata help the host select relevant capabilities. Automatic selection remains a host decision. Install the skill or connect the server first; no new model account is required.

## Choose an entry point

| Client/environment | Recommended entry | Project location/config | Evidence |
|---|---|---|---|
| Claude Code | Agent Skill; optional MCP | `.claude/skills/frontend-inspiration-assistant/`; `.mcp.json` | Directory installation and complete runtime tested; official config guidance; model invocation untested |
| Cursor | Agent Skill; optional MCP | `.cursor/skills/frontend-inspiration-assistant/`; `.cursor/mcp.json` | Directory installation/runtime and JSON validated; client UI untested |
| Codex | Original plugin or Skill/MCP | Source marketplace; `.agents/skills/`; MCP TOML | Original 0.1 installation tested; 0.2 bundle, directories and TOML validated; existing private instance does not update automatically |
| Claude Desktop/other MCP clients | MCP | Merge generated entries in the client's MCP settings | Actual official-SDK discovery and calls passed; specific client UI untested |
| Custom agents | MCP or CLI | Launch a stdio process or call Python scripts | Modern and legacy handshakes and all 10 tools tested |

## Agent Skills: task-based discovery

After cloning, choose one command for your client. Replace the example with an **existing project's absolute path**. The installer changes only that project, preserving global client settings:

```bash
python plugin/scripts/install_skill.py --project "/absolute/path/to/my-site" --client claude
python plugin/scripts/install_skill.py --project "/absolute/path/to/my-site" --client cursor
python plugin/scripts/install_skill.py --project "/absolute/path/to/my-site" --client codex
```

On Windows, use a path such as `D:/Projects/my-site`. `--client agents` provides the generic `.agents/skills/` layout. The installed skill includes its entry point, scripts, three internal skills and all 94 pinned upstream files. It remains runnable after relocation. An existing destination is preserved rather than overwritten; keep the old directory before following your upgrade process.

Open the project or refresh the host's skill list, then ask:

> Find at least 20 UI and motion inspirations for this website's task panel. Rank project relevance, save complete Markdown and five real screenshots, then let me choose.

Hosts with explicit skill invocation can also select `frontend-inspiration-assistant`. Discovery uses the skill description, not a continuous background loop.

## MCP: callable tools for agents

MCP requires Python 3.10+ and the pinned [official SDK](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.2.0). Generate settings using the same interpreter that has the dependencies installed.

Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r plugin/requirements-mcp.txt
.\.venv\Scripts\python.exe plugin/scripts/client_config.py --project "D:/Projects/my-site" --client cursor --output cursor.mcp.generated.json
```

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r plugin/requirements-mcp.txt
.venv/bin/python plugin/scripts/client_config.py --project "/absolute/path/to/my-site" --client cursor --output cursor.mcp.generated.json
```

Merge the generated `mcpServers` entries into the target project's `.cursor/mcp.json`. For Claude Code, use `--client claude` and the project's `.mcp.json`. `--client vscode` generates a `servers` layout; `--client codex` produces TOML; `--client stdio` produces generic reference JSON. The generator records interpreter and plugin paths; `--python` selects another interpreter explicitly. Existing output files are preserved. Merge entries without replacing other client servers.

The client starts and manages the server process. No HTTP port is required:

```bash
python plugin/scripts/mcp_server.py --project "/absolute/path/to/my-site"
```

This enters the stdio protocol, not an interactive menu. Tool input access is confined to the configured project; output must be a new file under its `设计灵感/` directory. No tool edits website source or supplies user confirmation.

### Ten tools

| Name | Result/action |
|---|---|
| `inspiration_get_workflow` | Workflow, four sources, browser requirements and confirmation boundaries |
| `inspiration_inspect_project` | Stack, dependencies and paths to project/design documents |
| `inspiration_get_template` | Candidate, element-level proposal or audit template |
| `inspiration_save_artifact` | Save supplied candidate/proposal/audit/browser-evidence JSON, explicitly not validated |
| `inspiration_validate_candidates` | Deduplication, minimum count, relevance order, source status, screenshots and evidence |
| `inspiration_write_report` | Save complete Markdown and return awaiting-selection status |
| `inspiration_write_proposal` | Validate and save a pending-confirmation plan; never authorizes website edits |
| `inspiration_audit_rules` | Bundled UI UX Pro Max rule and stack search |
| `inspiration_write_audit` | Audit report separating rule, code and browser evidence |
| `inspiration_stack_fit` | Stack compatibility projection, explicitly not a new browsing round |

An MCP-only client can use project/design previews and `inspiration_save_artifact` to submit filled templates or actual browser logs without another filesystem tool. Saving JSON does not validate browser authenticity.

Five readable resources cover workflow, sources, implementation, audit and host adaptation, with one starting prompt. Success provides structured JSON. Failures return MCP errors. Saving an explicitly requested incomplete diagnostic still returns an error rather than a successful 20-candidate check.

## Browser and design capabilities

Use the host's browser tools. Without them, `--with-browser` also generates a separate [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) entry, pinned to `@playwright/mcp@0.0.83`, with automatic screenshot output under the target project's `设计灵感/browser/`. Omit the screenshot filename to use this directory. This optional service needs Node.js 18+ and a usable browser. Follow its installation/tools instructions and actually click, scroll and capture screenshots. **This plugin's MCP server handles workflow, reports and audits; it does not call an LLM or replace the browser.**

Reuse `frontend-design` and `impeccable` when the host provides them. Otherwise the element-level workflow and complete bundled UI UX Pro Max remain available; report missing skills and untested coverage. Without a browser, continue rule/source inspection without inventing 20 browser-verified results.

## Validation limits and reproduction

32 automated tests passed: 17 original contracts, 9 portability tests and 5 actual MCP subprocess tests. Four skill installation layouts, full upstream integrity, JSON/TOML generation, modern/legacy handshakes, 10 tools, 5 resources, one prompt, report-to-pending-plan handoff and error flags were verified. MCP test inputs are clearly marked fixtures. The original [22-candidate actual research example](./FIRST_RUN.md) is preserved, not presented as a new 0.2 browsing round.

```bash
python -m pip install -r plugin/requirements-mcp.txt
python -m unittest discover -s plugin/tests -v
python plugin/scripts/inspiration.py package-check
python plugin/skills/ui-ux-pro-max/scripts/validate_data.py
```

Without optional MCP dependencies, six protocol tests skip; that is not a full 32-test pass. Specific Claude Code/Cursor UI and model-driven automatic selection remain untested. Post-implementation mobile, keyboard, reduced-motion and performance checks still require a real project.

References: [Agent Skills](https://agentskills.io/home), [MCP](https://modelcontextprotocol.io/docs/learn/architecture), [Claude Code Skills](https://code.claude.com/docs/en/skills), [Claude Code MCP](https://code.claude.com/docs/en/mcp), [Cursor Skills](https://cursor.com/docs/skills), [Cursor MCP](https://cursor.com/docs/mcp).
