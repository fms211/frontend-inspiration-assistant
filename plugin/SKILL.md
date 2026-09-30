---
name: frontend-inspiration-assistant
description: "Research frontend/UI design and motion inspiration for a website project, compare 20+ relevant candidates with real browser evidence, prepare element-level plans, and audit UX. 用于前端设计灵感、UI动效参考、页面审美实施与审计。"
---

# Frontend Inspiration Assistant · 前端灵感与审美实施助手

用于支持 Agent Skills 的智能体，不绑定特定模型或编辑器。优先使用用户指定语言，默认中文。用户调用后可检索、保存报告和审计；选择候选只授权拟定方案，确认具体方案后才能修改网站。

## 按任务调用

- **找灵感、比较 UI 或动效**：读取 [检索技能](skills/frontend-inspiration/SKILL.md)；遵循项目用途、技术栈与设计规范，每轮至少20条不同候选、高→中→低排序、前五条真实截图、完整Markdown、前三条比较，再询问选择。
- **选定灵感、准备实施**：读取 [逐元素方案](skills/frontend-inspiration/references/implementation.md)，给出位置、文字、布局、视觉与动效的具体参数。先审计方案，等待用户确认。
- **审计候选、方案或页面**：读取 [审计技能](skills/frontend-audit/SKILL.md)，调用完整内置 [UI UX Pro Max](skills/ui-ux-pro-max/SKILL.md)。区分规则、代码与实际浏览器证据。

## 工具发现与调用

技能根目录是本文件所在目录。脚本与数据使用相对关系解析；实际执行时根据客户端提供的技能目录定位绝对路径，禁止使用作者机器路径。

1. 若连接了本插件 MCP，先调用 `inspiration_get_workflow`，再按返回步骤使用项目识别、模板、报告、方案和审计工具。MCP作用域为启动时指定的项目。
2. 若未连接 MCP，使用 `python <SKILL_ROOT>/scripts/inspiration.py --help`。报告与审计CLI只依赖Python3标准库。
3. 浏览、点击、滚动与截图使用当前智能体真实可用的浏览器工具。按 [宿主适配](skills/frontend-inspiration/references/host-adapters.md) 判断能力，不把HTTP抓取或代码阅读当成实际浏览。
4. `frontend-design` 和 `impeccable` 可用时读取并复用。缺失时由当前智能体结合项目规范和内置审计完成能进行的步骤，在报告中明确该技能未参与；不得假称完成 impeccable 审计。

自动匹配由宿主根据技能描述或MCP工具说明决定。工具接入不等于自动获得浏览器、网站登录或修改授权；没有浏览器时记录限制，不伪造20条“实测”候选。
