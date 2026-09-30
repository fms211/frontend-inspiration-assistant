# 0.2.0 跨智能体验证 / Cross-agent validation

2026-09-30（Asia/Shanghai）：Windows、Python3.11.9、官方MCP SDK2.2.0。32项自动测试全部通过，无跳过。

- 17项原契约、9项可移植性、6项实际stdio子进程测试。
- 现代协议及legacy初始化、10工具成功/失败分支、5资源和1prompt实际调用。
- 四种技能安装目录中完整运行包可直接执行；JSON/TOML解析、已有目录/文件保留及标准ZIP根目录验证。
- 报告不足20条、项目路径越界、规则冒充实测等返回MCP错误；允许保存未达标诊断时仍不返回成功。
- 方案保持awaiting-confirmation，工具没有网站修改入口；fixture选择不代表用户选择。
- 官方UI UX Pro Max的94个原始文件未修改，固定提交与22套技术栈数据继续完整。

**实测边界：** Claude Code、Cursor等应用UI和模型自动选择未实际运行；安装目录与标准协议通过不等于这些客户端已完成端到端验收。原22条网页浏览案例属于0.1实际研究，本次协议fixture不冒充新浏览。0.1私有Codex实例不由GitHub发布自动升级。实际页面修改后仍需桌面、移动、键盘、减动效及性能验证。

English: all 32 tests passed with no skips, including six actual MCP subprocess tests; Client UI/model selection is untested, and protocol fixtures are not new browser evidence. Existing private installations do not auto-update from GitHub. See [setup and evidence](./CROSS-AGENT.en.md).

---

# 0.1.0 历史验收 / Historical validation

日期 / Date: 2026-09-30 · Runtime: 0.1.0

| 检查 / Check | 结果 / Result |
|---|---|
| 插件契约 / Plugin contracts | 17 tests passed locally |
| 官方数据 / Official datasets | 12 domains, 22 stacks, ui-reasoning.csv validated |
| 上游完整性 / Upstream integrity | 94 original files recorded by SHA256; commit 09170eec67eefd46a7ae85de61b40c194020f997 |
| 清单与资产 / Manifest and assets | Agent Plugins schema, three skill entries, 128px icon, MIT and package checks passed |
| 浏览 / Browsing | Four entrances visited; 22 unique candidates; real Top5 screenshots |
| 方案衔接 / Proposal handoff | Explicit test-fixture; no actual user selection or implementation |
| 跨栈 / Cross-stack | Next.js context plus Vue/HTML compatibility projections |
| 宿主 / Host | Installed private plugin, three enabled skills, synchronized runtime and rule search verified |

## 错误分支 / Failure cases

官网/源码/语言/样式重复、19条不足、排序错误、截图缺失或损坏、来源失败、仅文档验证、SPA hash、exit0错误/空值/异常JSON、官方数据缺失、未知候选编号、未填方案模板、栈识别、规则冒充实测、越界报告路径、跨栈差异与无发现审计。

Covered: component/variant duplicates, 19-result failure, ordering, missing/corrupt screenshots, source failure, docs-only evidence, SPA hashes, exit0 errors and empty/unexpected JSON, missing upstream data, unknown selections, unfilled proposals, stack detection, rule/browser evidence distinctions, output boundaries, cross-stack adaptation, and clean audits.

## 实测边界 / Evidence boundaries

实际浏览与控件动作逐条记录。截图用于外观；不能仅凭截图断言完整动画、性能、键盘或手机通过。来源上传没有选择文件/拖放；Click Spark未捕获完整火花；部分hover和键盘未测试。

Actions are documented per candidate. Screenshots establish appearance, not comprehensive motion, performance, keyboard, or mobile behavior. File selection/drop and some hover/keyboard behaviors remain untested; the full Click Spark effect was not captured.

尚未修改目标网站。实施后的桌面1440×900、手机390×844、键盘、减动效和性能实测等待用户选择、确认方案并实施后执行。Vue前两次规则查询无匹配按失败处理，聚焦Composition API/router后有实际结果；空结果没有判为成功。

The target website was not modified. Post-implementation desktop, mobile, keyboard, reduced-motion, and performance checks remain pending user selection, confirmation, and implementation. Initial empty Vue queries failed correctly; a focused Composition API/router query returned actual rules.

## 安装与发现 / Installation and discovery

插件详情与管理页显示已安装、三个技能开关均启用，Codex自动同步完整副本。账号搜索与CLI常规市场列表未列出新私有插件；未把这个列表差异当作安装失败，也未安装无关插件。随后宿主技能目录已显示三个带插件前缀的入口。

The plugin detail/settings pages confirmed installation and all three enabled switches. Codex synchronized the complete runtime. General account search/CLI marketplaces did not list this new private plugin; those surfaces were not treated as installation proof. The host skill catalog subsequently exposed all three namespaced entries.

## 安装包 / Packaged archive

Portable ZIP: 113 files, 718227 bytes; one root directory; CRC passed. The hosted runtime adds a platform-generated Codex compatibility manifest, also retained in plugin/.codex-plugin/ in this repository.

```text
ec3c28dca11e9f7b29db2beddf2a91265528191971700ba778959c5d2e3a2433  frontend-inspiration-assistant-0.1.0.zip
```
