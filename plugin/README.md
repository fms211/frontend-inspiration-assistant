# 前端灵感与审美实施助手

跨项目、跨智能体复用的前端灵感插件，版本0.2.0。提供标准Agent Skill、可选MCP stdio工具和Python CLI。浏览由调用智能体真实可用的浏览器执行；frontend-design与impeccable可用时复用，缺失项如实记录。报告与规则CLI只需Python3标准库，MCP模式按requirements-mcp.txt安装官方SDK，不增加业务HTTP API。

[English](./README.en.md) · [中英文完整接入指南](https://github.com/fms211/frontend-inspiration-assistant/blob/HEAD/docs/CROSS-AGENT.md)

## 跨智能体接入

解压后的根目录含通用`SKILL.md`，可作为完整技能安装。以下命令从本文件所在目录执行，示例路径替换为自己的现有项目绝对路径；选择对应客户端的一条即可：

```bash
python scripts/install_skill.py --project "D:/Projects/my-site" --client claude
python scripts/install_skill.py --project "D:/Projects/my-site" --client cursor
python scripts/install_skill.py --project "D:/Projects/my-site" --client codex
```

MCP模式在当前选定的Python环境安装依赖，再生成客户端配置：

```bash
python -m pip install -r requirements-mcp.txt
python scripts/client_config.py --project "D:/Projects/my-site" --client cursor --output cursor.mcp.generated.json
```

将生成的服务器条目合并到客户端项目配置中，Claude Code可用`--client claude`，Codex可用`--client codex`生成TOML。可选`--with-browser`附加固定版本Playwright MCP配置，需要Node.js 18+和可用浏览器。安装器和配置生成器保留已有文件，不自动修改全局设置。

MCP提供10个工具、5个资源和1个prompt；服务器由客户端通过stdio启动。没有宿主浏览器时不虚构实测，没有impeccable时明确列出覆盖限制。模型是否自动选择由客户端决定；32项测试证明运行包与协议，具体客户端UI/模型调用仍待实测。

## 使用

启用插件后说：“为当前项目的任务面板搜集20条UI与动效灵感。”主入口为`frontend-inspiration`，单独审计入口为`frontend-audit`；`ui-ux-pro-max`为完整内置审计技能。

每轮检查React Bits、对应GitHub、hepengwei.cn、Aceternity UI，真实浏览预览并操作相关控件。按项目用途和方向排序高/中/低候选，官网/源码/语言样式版本去重。Markdown、Top5截图和浏览证据保存到当前项目`设计灵感/<日期时间>-<目标>/`，聊天展示完整候选表，等待你选择。

选定后提供路由、UI位置、当前/新文案、字体与布局、颜色/token、边框与阴影、完整动效参数、组件与依赖、操作验收及回退。**确认具体方案后才修改网站。**修改后做桌面/手机/键盘/减动效检查；未测试明确标出。

UI UX Pro Max官方提交：[`09170eec67eefd46a7ae85de61b40c194020f997`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/09170eec67eefd46a7ae85de61b40c194020f997)。本包保留官方脚本、22套技术栈数据、生成模板、MIT版权声明与SHA256记录。完整性失败时阻止审计运行。不覆盖宿主同名旧技能。源码网站组件授权需每轮核实，本插件MIT不代表那些组件也可自由再分发。

## 本地验证

在插件根目录运行（Windows用python）：

```text
python -m unittest discover -s tests -v
python scripts/inspiration.py package-check
python scripts/inspiration.py inspect --project <当前项目绝对路径>
python scripts/inspiration.py audit-rules "animation reduced motion" --domain ux
python scripts/inspiration.py stack-fit <候选.json> --stack vue
python scripts/inspiration.py pack --output <插件根目录之外的新ZIP绝对路径>
```

报告/方案/审计模板在templates，工作流在skills/frontend-inspiration/references。CLI失败输出`ok:false`并返回2，包括exit0的错误文本或JSON error，不能只看进程状态。`--allow-incomplete`仅保留明确未达标报告，仍返回非零；不会掩盖浏览失败。

`vendor_ui_ux.py`只用于维护者从指定官方提交重建副本，正常运行无需网络下载审计数据。工具不会自行执行网站源码。源码包不包含当前项目源码、账号数据、截图或密钥。
