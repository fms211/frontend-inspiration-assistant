---
name: frontend-audit
description: "用本插件内置UI UX Pro Max和宿主impeccable审计候选、逐元素实施方案或当前页面，记录位置、优先级、规则/代码/浏览器证据和验证状态。"
---

# 前端双重审计入口

先读 [审计流程](../frontend-inspiration/references/audit.md) 和本包 [UI UX Pro Max](../ui-ux-pro-max/SKILL.md)，再读当前项目规则、设计规范、实际目标页面，以及宿主impeccable技能。不要误用宿主缺少数据的同名旧UI UX技能。

按候选/方案/实施后页面区分阶段，覆盖视觉一致性、布局、交互反馈、可读性、可访问性、响应式和动效性能。模板位于插件根 `templates/audit.json`，输出Markdown并保存实际证据。没有实施或没有现场测试就标记待验证，绝不以规则命中冒充通过。只审计时不擅自修改页面。
