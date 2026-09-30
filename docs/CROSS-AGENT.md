# 跨智能体接入 · 0.2.0

[English](./CROSS-AGENT.en.md) · [返回README](../README.md)

本版把同一套前端灵感工作流提供为 **Agent Skills、MCP stdio工具、CLI**。技能描述和工具说明帮助宿主按任务选择调用；实际是否自动调用由宿主决定。需要先安装技能或连接MCP，不需要新增模型账号。

## 选择入口

| 客户端/环境 | 推荐入口 | 安装位置或配置 | 验证情况 |
|---|---|---|---|
| Claude Code | Agent Skill；可选MCP | 项目`.claude/skills/frontend-inspiration-assistant/`；MCP在`.mcp.json` | 目录安装与完整运行包实测；配置按官方文档；客户端模型调用未测 |
| Cursor | Agent Skill；可选MCP | 项目`.cursor/skills/frontend-inspiration-assistant/`；`.cursor/mcp.json` | 目录安装与完整运行包实测；JSON配置校验；客户端UI未测 |
| Codex | 原插件模式或Agent Skill/MCP | 原本地市场；`.agents/skills/`；MCP配置TOML | 原0.1插件安装已测；0.2安装包、目录及TOML校验；现有私有实例不会自动升级 |
| Claude Desktop等MCP客户端 | MCP | 按该客户端的MCP设置合并生成的通用配置 | 官方SDK客户端实际发现和调用通过；具体客户端UI未测 |
| 自建智能体 | MCP或CLI | 启动stdio进程或调用Python脚本 | 现代与legacy握手、10个工具实际调用通过 |

## Agent Skill：按任务匹配

克隆仓库后，以下命令只写入明确指定的项目，不修改用户全局配置。把示例项目路径换成自己的**现有项目绝对路径**：

```bash
python plugin/scripts/install_skill.py --project "D:/Projects/my-site" --client claude
python plugin/scripts/install_skill.py --project "D:/Projects/my-site" --client cursor
python plugin/scripts/install_skill.py --project "D:/Projects/my-site" --client codex
```

选择当前客户端的一条执行即可；`--client agents`提供通用`.agents/skills/`布局。安装后该目录包含`SKILL.md`、完整脚本、三个内部技能和94个固定上游文件，复制或移动后仍能运行。已有同名目录时拒绝覆盖，先保留旧目录再按自己的升级流程处理。

安装后在支持技能发现的客户端开启项目或刷新技能列表，可直接说：

> 为这个网站的任务面板找至少20条UI与动效灵感，按项目相关度排序，保存完整Markdown和前五条真实截图，让我选择。

支持显式技能调用的客户端也可选择`frontend-inspiration-assistant`。自动调用的依据是技能description，不是常驻后台循环。

## MCP：让智能体调用工具

MCP需要Python 3.10+及[官方SDK](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.2.0)。先安装本版固定依赖，再用同一个Python生成配置。

Windows / PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r plugin/requirements-mcp.txt
.\.venv\Scripts\python.exe plugin/scripts/client_config.py --project "D:/Projects/my-site" --client cursor --output cursor.mcp.generated.json
```

macOS / Linux：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r plugin/requirements-mcp.txt
.venv/bin/python plugin/scripts/client_config.py --project "/absolute/path/to/my-site" --client cursor --output cursor.mcp.generated.json
```

将生成的`mcpServers`条目合并到目标项目的`.cursor/mcp.json`。Claude Code使用`--client claude`，合并到目标项目`.mcp.json`。`--client vscode`生成`servers`布局；`--client codex`生成TOML片段；`--client stdio`生成通用参考JSON。生成器保留当前解释器和插件绝对路径，`--python`可显式选择安装好依赖的解释器。已有输出文件拒绝覆盖；不要直接覆盖客户端已有服务器配置。

服务器由客户端启动，调用结束后由客户端管理进程，不需要开HTTP端口：

```bash
python plugin/scripts/mcp_server.py --project "/absolute/path/to/my-site"
```

此命令进入stdio协议服务，不是交互命令行菜单。服务器读取限定项目内的报告、清单和规范预览，并读取本包固定资源；生成文件必须是该项目`设计灵感/`中的新文件。工具没有修改网站源码或代用户确认方案的入口。

### 10个工具

| 名称 | 返回或动作 |
|---|---|
| `inspiration_get_workflow` | 完整流程、四个来源、浏览能力需求和确认边界 |
| `inspiration_inspect_project` | 技术栈、依赖与待阅读的项目规范路径 |
| `inspiration_get_template` | 候选、逐元素方案或审计模板 |
| `inspiration_save_artifact` | 直接保存结构化候选、方案、审计或浏览证据JSON，状态为未验证 |
| `inspiration_validate_candidates` | 去重、20条计数、排序、来源状态、截图与证据校验 |
| `inspiration_write_report` | 保存完整Markdown并返回待用户选择状态 |
| `inspiration_write_proposal` | 校验并保存待确认方案；不授权修改网站 |
| `inspiration_audit_rules` | 内置UI UX Pro Max规则和技术栈搜索 |
| `inspiration_write_audit` | 按规则/代码/浏览器证据生成审计报告 |
| `inspiration_stack_fit` | 不同技术栈的兼容性投影，明确不算新浏览轮次 |

仅有MCP、没有其他文件工具的客户端，也可通过项目规范预览理解上下文，用`inspiration_save_artifact`保存填写好的模板或实际浏览日志，再调用校验和报告工具。保存JSON本身不验证浏览真实性。

另提供5个可读取资源（流程、来源、实施参数、审计和宿主适配）及1个启动prompt。成功调用返回结构化JSON；失败以MCP错误返回。允许保存未达标诊断报告时，调用仍标记错误，不能当成20条验收成功。

## 浏览器和审计能力

使用宿主现有浏览器；没有时可在生成配置时增加`--with-browser`，附带独立的[微软Playwright MCP](https://github.com/microsoft/playwright-mcp)配置，固定`@playwright/mcp@0.0.83`，自动截图输出目录设为目标项目的`设计灵感/browser/`。截图时不传文件名即可使用该目录。该可选服务需要Node.js 18+及可用浏览器；按其工具说明安装浏览器并实际执行点击、滚动和截图。**本插件MCP自身负责流程、报告和审计，不会自主调用LLM或代替浏览器。**

`frontend-design`与`impeccable`在宿主可用时复用；缺失时本包逐元素流程和完整UI UX Pro Max仍可运行，并列明缺失技能及未测项。没有浏览器时只能继续规则与源码核实，不能虚构20条浏览结果。

## 验证边界与复现

32项自动测试通过，包含17项原契约、9项可移植性与6项实际MCP进程测试。四种技能目录安装、依赖数据完整性、JSON/TOML配置、现代和legacy协议、10工具/5资源/1prompt、候选→待确认方案、错误状态均已验证。MCP测试数据是明确标记的fixture；原22条真实浏览案例保留在[案例](./FIRST_RUN.md)，不冒充0.2新增浏览轮次。

```bash
python -m pip install -r plugin/requirements-mcp.txt
python -m unittest discover -s plugin/tests -v
python plugin/scripts/inspiration.py package-check
python plugin/skills/ui-ux-pro-max/scripts/validate_data.py
```

未安装可选MCP依赖时，6项MCP进程测试会跳过，不能宣称完整32项通过。Claude Code/Cursor等客户端UI和模型自动选择尚未实测，页面实施后的移动端、键盘、减动效及性能也需在真实项目中验证。

规范依据：[Agent Skills](https://agentskills.io/home)、[MCP](https://modelcontextprotocol.io/docs/learn/architecture)、[Claude Code Skills](https://code.claude.com/docs/en/skills)、[Claude Code MCP](https://code.claude.com/docs/en/mcp)、[Cursor Skills](https://cursor.com/docs/skills)、[Cursor MCP](https://cursor.com/docs/mcp)。
