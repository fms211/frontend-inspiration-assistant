# UI UX Pro Max + impeccable 审计

本包包含UI UX Pro Max固定提交 `09170eec67eefd46a7ae85de61b40c194020f997`，MIT声明和原文件SHA256见相邻 `ui-ux-pro-max/UPSTREAM.json`。不改宿主全局技能。开始运行前执行 `inspiration.py package-check` 检查完整性。

先读本包UI UX Pro Max的完整SKILL.md。使用 `audit-rules` 包装器运行本包搜索，它同时检查退出码、JSON/error和实际count，防止官方脚本遇到文件缺失时exit0被误判：

```text
python <PLUGIN_ROOT>/scripts/inspiration.py audit-rules "keyboard focus contrast" --domain ux --output <REPORT_DIR>/ux-rules.json
python <PLUGIN_ROOT>/scripts/inspiration.py audit-rules "animation reduced motion" --domain ux --output <REPORT_DIR>/motion-rules.json
python <PLUGIN_ROOT>/scripts/inspiration.py audit-rules "client interaction accessibility" --stack nextjs --output <REPORT_DIR>/stack-rules.json
```

栈按当前项目识别。Vue使用vue，原生HTML用html-tailwind（无Tailwind时只采纳适用的HTML原则），未知不假定React Native。固定版本资料不保证所有框架API最新；代码实现查本项目真实版本与官方文档。搜索通常只需2–5个词，一次聚焦一种意图；无结果重试一次后标注无匹配。设计系统模式仅适用于新设计/整体调整，不为微交互强制改风格；不自动持久化覆盖项目设计规范。

审计分别发生在：候选筛选（适合与否/代价）、逐元素方案（参数/状态/减动效/验收）、实施后页面。impeccable负责结合项目产品/品牌上下文判断视觉一致性、阅读层次、布局和交互，UI UX Pro Max提供可访问性、栈、响应式、性能规则。用户约束优先；通用“避免渐变/默认某字体”等建议不能覆盖项目明确方向。

每项发现填写 `templates/audit.json`：精确位置、问题、优先级P0/P1/P2/P3、证据文件/描述、来源技能、证据级别、建议具体参数、验证状态和操作复测步骤。`evidence_level`仅取 `rule` / `code` / `browser`；`verification`仅取 `proposed` / `confirmed` / `fixed` / `not-tested`。规则建议没有现场证据时不写 confirmed/fixed。

覆盖视觉一致性、布局、反馈、可读性、可访问性、响应式、动效性能。实施后必测：桌面1440×900、手机390×844或项目断点；Tab/Shift+Tab/Enter/Space和Escape可见焦点与无陷阱；宿主支持的减动效模拟/系统设置；空、加载、失败、成功状态；长中文/文本放大；实际滚动/动画。按当前浏览器技能获得可用API，不编造viewport或emulateMedia支持。若宿主不支持模拟或页面没运行，明确 not-tested，不把代码存在当作通过。

性能需实际采样才能给FPS/耗时；未采样只写风险建议。截图是外观证据，不能独自证明动画、键盘、减动效通过。未发生项目实施时，实施后审计标“待用户确认实施后执行”；可审计当前基线，但不能改名为实施后验收。
