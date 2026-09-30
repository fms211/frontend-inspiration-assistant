# 工作流程与记录约定

## 项目上下文

以当前工作目录为项目根，先读取适用AGENTS.md、README/PRODUCT/DESIGN、package.json和目标路由/组件；只读确认工作树已有改动。CLI `inspect --project <绝对目录>` 列出上下文文件、实际依赖与识别栈，不能替代阅读文档。React、Next.js、Vue、Svelte、原生HTML等分别判定，React示例迁移到Vue不能标“直接兼容”。

检索目标包括受众、任务、页面性质、要改善的UI位置、已有主题/token、性能预算、禁止改动。未找到设计规范时记录未知并从当前页面和用户描述推导，标明推断。不要自动改项目说明。

## 浏览与计数

每轮四个入口都要保存访问状态、实际URL、时间和说明。优先免费内容，先探索分类，再从真实DOM链接进入详情。先看预览，再操作播放/重播/选项/滚动/上传等适用控件。上传演示仅用自建测试文件，不发项目素材。鼠标专有效果检查键盘、触屏替代；重动效逐页查看，用宿主支持的动作，不编造hover或性能测量。

候选的 `family` 使用 `react-bits`、`aceternity` 或 `hepengwei`；`component` 使用稳定组件名，`example` 是共享页面上的明确示例位置。canonical计数忽略语言与样式变体；React Bits GitHub只作为同组件辅助来源。`source_url` 保留hash路由，`source_links` 保存源码/授权链接。

`verification.status`：`browser-tested`为操作后实看；`browser-viewed`仅看外观；`docs-only`仅文档，不能算作完成浏览验收；`failed`访问失败。`interaction_observation`不能只写“正常”；写动作、前后变化及未确认项。每条保存时间、实际URL和证据文件。页面错误时记录，继续其他来源；不能绕开策略拦截。

实现成本用低/中/高并解释工时范围、CPU/GPU风险和新增依赖，不能给未测FPS。授权字段分别写免费/付费/未知、许可证及来源、可借鉴范围；付费效果只借鉴可见设计，不复制受限代码。

## 报告 CLI

把模板复制到一个新的报告目录，人工/代理依据真实证据填写，不让脚本生成候选。输出在同目录，保存输入、截图、浏览日志、审计建议。

```text
python <PLUGIN_ROOT>/scripts/inspiration.py inspect --project <PROJECT_ROOT>
python <PLUGIN_ROOT>/scripts/inspiration.py validate <REPORT_DIR>/candidates.json
python <PLUGIN_ROOT>/scripts/inspiration.py report <REPORT_DIR>/candidates.json --output <REPORT_DIR>/灵感汇总.md
python <PLUGIN_ROOT>/scripts/inspiration.py stack-fit <REPORT_DIR>/candidates.json --stack vue --output <REPORT_DIR>/栈兼容性建议.json
```

校验拒绝不足20、重复、排序错误、字段缺失、前五条截图缺失/损坏、虚构状态。来源失败且其他来源仍有20条时允许生成，但会在报告醒目标记失败和浏览限制。需要保留未达标结果用 `report --allow-incomplete`，仍返回非零退出码，输出明确“未达标”；不可将它报成成功。所有失败同时返回JSON `ok:false` 和非零状态。

报告必须有完整候选表、Top5截图、每条实际观察、Top3比较、组合方向、四源状态与未验证限制；聊天展示完整候选表，不能只发文件链接。报告时间用带时区ISO值。

## 选择与方案

用户回复编号/组合之后才填写 `templates/implementation.json`，`selection_origin:user`并保存原话。回归测试可以 `test-fixture`，但必须标明未获用户选择、禁止实施。CLI `brief <方案.json> --candidates <候选.json> --output <实施方案.md>` 验证ID衔接、参数齐备，输出始终为“待确认方案”。确认必须覆盖具体方案及页面修改范围。更换方向→新一轮报告；保留旧记录。
