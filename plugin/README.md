# 前端灵感与审美实施助手

私有、跨项目复用的Codex技能插件，版本0.1.0。运行需要Codex桌面端的宿主浏览器；实施和视觉审查复用已安装的frontend-design与impeccable。Python3仅用于本地规则搜索、报告校验和打包，不增加业务HTTP API。

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
