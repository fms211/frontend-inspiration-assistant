# Frontend Inspiration Assistant · 0.2.0

[简体中文](./README.md) · [Full cross-agent guide](https://github.com/fms211/frontend-inspiration-assistant/blob/HEAD/docs/CROSS-AGENT.en.md)

A self-contained frontend research and audit runtime with **Agent Skills, optional MCP stdio tools, and CLI**. Python 3.10+ is required. CLI/report helpers use the standard library; MCP installs the pinned official SDK from `requirements-mcp.txt`.

## Install as an Agent Skill

The archive root includes `SKILL.md`. From this directory, choose one command and replace the example with an existing project's absolute path:

```bash
python scripts/install_skill.py --project "/absolute/path/to/my-site" --client claude
python scripts/install_skill.py --project "/absolute/path/to/my-site" --client cursor
python scripts/install_skill.py --project "/absolute/path/to/my-site" --client codex
```

On Windows, a path such as `D:/Projects/my-site` is supported. `--client agents` targets `.agents/skills/`. Existing destinations are preserved and global settings are unchanged. The skill, scripts, templates and complete UI UX Pro Max data remain together after installation.

## Connect MCP

Install dependencies in the Python environment you choose for the client, then generate configuration using that interpreter:

```bash
python -m pip install -r requirements-mcp.txt
python scripts/client_config.py --project "/absolute/path/to/my-site" --client cursor --output cursor.mcp.generated.json
```

Merge the generated entries into the project's `.cursor/mcp.json`. `--client claude` targets Claude Code's `.mcp.json` format; `--client codex` generates TOML; `--client vscode` generates the `servers` format. Use `--python` to choose another interpreter explicitly. `--with-browser` adds optional pinned Playwright MCP configuration, requiring Node.js 18+ and a usable browser.

The host starts `scripts/mcp_server.py --project <project-root>` over stdio. Ten tools, five resources and one starting prompt are available. File inputs remain within that project; report outputs must be new files under `设计灵感/`. There is no website-editing or user-confirmation tool.

## Workflow and browser evidence

Inspect project purpose, design rules and stack; browse React Bits, its GitHub source, hepengwei.cn and Aceternity UI. Produce at least 20 distinct ranked candidates, real Top5 screenshots, complete Markdown, a Top3 comparison and combinations. Ask the user to select IDs, prepare concrete element-level parameters, audit the proposal, and wait for confirmation before host implementation.

Browsing is performed by the calling agent's actual browser tools. The MCP server does not browse or call an LLM. Reuse host frontend-design/impeccable when available; otherwise report missing coverage while using the bundled workflow and complete UI UX Pro Max. Rule suggestions and code inspection are not browser tests.

## CLI and checks

```bash
python scripts/inspiration.py --help
python scripts/inspiration.py inspect --project "/absolute/path/to/my-site"
python scripts/inspiration.py audit-rules "animation reduced motion" --domain ux
python scripts/inspiration.py package-check
python skills/ui-ux-pro-max/scripts/validate_data.py
python -m unittest discover -s tests -v
```

32 tests passed with the optional MCP dependency installed: 17 original contracts, nine portability checks and six actual MCP subprocess tests. Modern/legacy handshakes and all tools/resources/prompt passed. Without the SDK, six protocol tests skip. Specific client UI/model selection and post-implementation browser acceptance remain untested. See [validation](./VALIDATION.md).

UI UX Pro Max retains all 94 pinned upstream files at commit `09170eec67eefd46a7ae85de61b40c194020f997`, its [MIT notice](./skills/ui-ux-pro-max/LICENSE), and [hash record](./skills/ui-ux-pro-max/UPSTREAM.json). Original code uses [MIT](./LICENSE); source-site component licenses must be checked separately.
