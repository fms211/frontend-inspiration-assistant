# 0.2.0 · 跨智能体前端灵感与审美实施助手

同一套工作流新增三个入口：**Agent Skills、MCP stdio、CLI**。面向Claude Code、Cursor、Codex及兼容的智能体工具，技能描述和工具schema支持宿主按任务匹配与调用。

- 自包含技能安装器，支持`.claude/skills/`、`.cursor/skills/`、`.agents/skills/`，保留已有目录。
- 官方MCP SDK2.2.0：10个工具、5个参考资源、1个prompt，结构化结果和正确失败标记；现代与legacy握手通过。
- 客户端JSON/TOML配置生成，保留当前解释器与项目作用域；可选Playwright MCP浏览器配置。
- 继续保留至少20条不同候选、真实截图、完整Markdown、用户选择、逐元素方案和确认后实施。
- 32项测试通过；UI UX Pro Max94个官方文件原始哈希与22套栈数据保持完整。
- 中英文README、跨智能体安装指南及新版封面。

浏览行为由调用智能体真实执行，本插件MCP不调用LLM也不代替浏览器。`frontend-design`与`impeccable`按宿主可用性接入并记录覆盖。Claude Code/Cursor等实际客户端UI和模型自动选择未测；协议fixture不冒充新的真实网页检索。旧Codex私有实例不会自动升级。

安装包为完整运行包，解压根目录`frontend-inspiration-assistant/`带`SKILL.md`。纯CLI无需额外依赖；MCP需安装包内`requirements-mcp.txt`。源码和中英文安装指南在公开仓库中提供。

## English

One workflow, three interfaces: **Agent Skills, MCP stdio and CLI**, for compatible agent tools including Claude Code, Cursor and Codex.

A self-contained project skill installer, ten MCP tools, five resources, one prompt, client JSON/TOML generation and optional pinned Playwright MCP configuration. Modern and legacy handshakes and all 32 tests passed. All 94 pinned upstream UI UX Pro Max files and 22 stack datasets remain intact.

The calling agent performs actual browsing. The MCP server does not call an LLM or replace a browser. Optional host design skills are reported honestly. Specific client UI/model-driven selection remains untested; protocol fixtures are not new browser evidence. Existing private Codex installations do not automatically upgrade.

The portable archive has a `frontend-inspiration-assistant/` root with `SKILL.md`. CLI mode uses the standard library; MCP mode installs the included `requirements-mcp.txt`. Bilingual setup guides and editable source are in the public repository.

## Archive integrity

```text
ac528c72b462e5a732bfd8be87b5d777f2ec90338401f1458f0ff0f8e69a1825  frontend-inspiration-assistant-0.2.0.zip
```

124 files · 738328 bytes · CRC verified.
