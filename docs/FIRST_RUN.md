# 首轮真实检索案例 / First research round

2026-09-30 · Next.js16.2.4 / React19.2.4 / Tailwind4 · 创作操作工作台

实际访问四个入口，查看22条不同候选。官网与GitHub、语言与样式版本合并计数；高7、中8、低7。所有UI目标为路由/下的操作区域或欢迎区域。

Four entrances were visited; 22 unique candidates were inspected. Website/source and language/style variants were merged. Seven high, eight medium, and seven low relevance candidates were ranked for an operational creation workspace.

browser-tested表示记录的动作已执行；browser-viewed表示外观已查看。它们不代表全面交互、键盘、移动或性能通过。原效果控件/文档值不等于计时实测。

The verification labels cover the documented actions or appearance only. They do not establish complete keyboard, mobile, performance, or animation support.

## 完整候选 / All candidates

| 编号 ID | 名称与来源 Name/source | 方向 Direction | 相关度 Relevance | 适用UI Target | 理由 Fit | 调整 Adaptation | 成本 Cost | 依赖与授权 Dependencies/license | 浏览 Verification |
|---|---|---|---|---|---|---|---|---|---|
| 01 | [Stateful Button](https://ui.aceternity.com/components/stateful-button) | 组件交互、动画 | 高 | / · 对话输入框右下发送按钮 | 直观解释发送中的等待状态 | 琥珀主题；接真实请求状态，补失败/重试 | 低，0.5–1天；局部动画 | React + Motion；沿用lucide，避免新增图标库；公开免费演示及源码；免费组件具体许可证未确认，仅取交互设计。Pro另有购买许可，不套用为MIT。 | browser-tested |
| 02 | [Animated List](https://reactbits.dev/components/animated-list) | 布局、组件交互、动画 | 高 | / · 左侧历史会话/任务列表 | 列表选中与渐隐适合快速找任务 | 保留分组和滚动位置，减动效直接显示 | 中，1–2天；长列表需限制动画项数 | React + Motion（当前未安装）；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 03 | [Multi Step Loader](https://ui.aceternity.com/components/multi-step-loader) | 组件交互、动画 | 高 | / · 视频生成任务阶段反馈 | 把等待解释为可理解的多个阶段 | 改为侧栏内联阶段；接真实进度，禁止假循环 | 中，1–2天；避免全屏blur常驻 | React + Motion；真实任务状态需现有数据支持；公开免费演示及源码；免费组件具体许可证未确认，仅取交互设计。Pro另有购买许可，不套用为MIT。 | browser-tested |
| 04 | [File Upload](https://ui.aceternity.com/components/file-upload) | 布局、组件交互 | 高 | / · 参考素材上传入口 | 拖放入口和文件反馈更易发现 | 中文标签；原生button、类型/大小限制和失败反馈 | 中，1–2天；大图避免同步解码 | 示例Motion/clsx/tailwind-merge/Tabler/react-dropzone；可复用原生文件输入和lucide；公开免费演示及源码；免费组件具体许可证未确认，仅取交互设计。Pro另有购买许可，不套用为MIT。 | browser-viewed |
| 05 | [Animated Tabs](https://ui.aceternity.com/components/tabs) | 布局、组件交互、动画 | 高 | / · 左侧历史/文件标签 | 选中指示器与内容切换说明当前位置 | 借用选中指示器，取消紫色堆叠大卡片 | 中，0.5–1.5天；不同时渲染全部重面板 | React + Motion；需tablist/tabpanel与焦点管理；公开免费演示及源码；免费组件具体许可证未确认，仅取交互设计。Pro另有购买许可，不套用为MIT。 | browser-tested |
| 06 | [Fade Content](https://reactbits.dev/animations/fade-content) | 动画 | 高 | / · 新增消息/结果卡片 | 不改变结构即可柔和呈现新内容 | 拟180ms透明度渐入；无blur、无自动消失 | 低，0.5天；仅opacity | GSAP（已有）；可简化为CSS；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 07 | [Sidebar](https://ui.aceternity.com/components/sidebar) | 布局、组件交互 | 高 | / · 历史会话侧栏 | 展开/收起结构适合当前左侧信息区 | 保留文字与显式开关；移动端抽屉，勿仅hover | 中，1–2天；保留现有结构 | React + Motion；沿用lucide；公开免费演示及源码；免费组件具体许可证未确认，仅取交互设计。Pro另有购买许可，不套用为MIT。 | browser-viewed |
| 08 | [Spotlight Card](https://reactbits.dev/components/spotlight-card) | 组件交互、背景 | 中 | / · 模型/风格选择卡片 | 深色局部光晕接近现有太空主题 | 改琥珀低强度；选中/焦点状态也能看见 | 低，0.5–1天；限制卡片数量 | React + CSS；无额外包标注；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 09 | [长文本省略与 More 入口](https://hepengwei.cn/#/html/visualDesign) | 文字排版、组件交互 | 中 | / · 历史标题/长提示词预览 | 多行省略有助于稳定信息密度 | 中文断行；可访问展开按钮，不隐藏全文入口 | 低，0.5天；无需动画 | 原生HTML/CSS；具体源码未核实；免费可见演示；源码授权未知，仅借鉴布局/交互，自行实现。 | browser-viewed |
| 10 | [Masonry](https://reactbits.dev/components/masonry) | 布局、动画 | 中 | / · 创作画廊的素材预览 | 不同纵横比素材可自然排列 | 图片预留比例和懒加载；任务列表仍用固定行 | 中，1–2天；大量图片需虚拟化 | GSAP（已有）+ React；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 11 | [Count Up](https://reactbits.dev/text-animations/count-up) | 文字排版、动画 | 中 | / · 工作统计总生成次数 | 总数变化有轻量可见反馈 | 数字等宽；仅真实数值变化触发，减动效直达终值 | 低，0.5天；避免高频重播 | React + Motion；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 12 | [Pill Nav](https://reactbits.dev/components/pill-nav) | 布局、组件交互、动画 | 中 | / · 顶部工作区导航 | 胶囊标签与现有导航语言相近 | 保留五项中文标签与显式滚动，不用纯图标替代 | 中，1天；控制导航宽度 | GSAP（已有）+ React；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 13 | [Animated Content](https://reactbits.dev/animations/animated-content) | 动画、滚动动效 | 中 | / · 结果卡片进入可视区 | 短距离入场可表明内容新增 | 位移100px改8px，取消反复播放和长等待 | 低，0.5–1天；避免遮挡输入 | GSAP（已有）；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 14 | [Border Glow](https://reactbits.dev/components/border-glow) | 组件交互、背景 | 中 | / · 选中的模型卡片边缘 | 与现有edge-glow可保持同一语言 | 只给选中/焦点卡片，缩小28px圆角与40px外光 | 中，1天；蒙版/渐变需采样性能 | React + CSS；无额外包标注；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 15 | [纸飞机发送按钮](https://hepengwei.cn/#/css/dynamicButtons) | 组件交互、动画 | 中 | / · 聊天发送按钮图标 | 纸飞机图形能清楚表达发送 | 复用lucide；按压反馈简化，补加载/失败状态 | 低，0.5天；不依赖整套示例库 | HTML/CSS示例；源码与授权未确认；免费可见演示；源码授权未知，仅借鉴布局/交互，自行实现。 | browser-tested |
| 16 | [Dock](https://reactbits.dev/components/dock) | 组件交互、动画 | 低 | / · 次要快捷工具区 | 可借鉴快捷入口，但弱化现有文字导航 | 只用于次要动作，显示文字；触屏取消放大 | 中，1天；弹簧缩放需防抖 | React + Motion；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 17 | [Star Border](https://reactbits.dev/animations/star-border) | 动画、背景 | 低 | / · 欢迎页单个重点CTA | 仅局部点缀，与操作区任务状态关联弱 | 改琥珀1px，取消无意义常驻循环 | 低，0.5天；持续绘制需停用条件 | React + CSS；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 18 | [Blur Text](https://reactbits.dev/text-animations/blur-text) | 文字排版、动画 | 低 | / · 欢迎页短标题 | 展示标题可用，但正文不应等待逐字显现 | 中文整句同时显示；缩短到180ms，减动效无blur | 中，1天；filter有额外绘制代价 | React + Motion；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 19 | [Logo Loop](https://reactbits.dev/animations/logo-loop) | 滚动动效、动画 | 低 | / · 产品介绍的模型生态展示 | 品牌展示用途强，工作区帮助小 | 保留静态文字选择；提供暂停，减动效静态排列 | 低，0.5–1天；避免常驻无意义滚动 | React；无额外运行包标注；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 20 | [Click Spark](https://reactbits.dev/animations/click-spark) | 组件交互、动画 | 低 | / · 欢迎页装饰反馈 | 额外点击火花对操作状态解释帮助小 | 仅装饰层且不阻挡事件；减动效禁用 | 低，0.5天；频繁点击需限流 | React + Canvas；无额外包标注；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-tested |
| 21 | [Tilted Card](https://reactbits.dev/components/tilted-card) | 3D、组件交互 | 低 | / · 单件作品展示封面 | 可用作展示，操作卡片倾斜会降低稳定感 | 手机/键盘静态；限3deg/1.01，不倾斜重要正文 | 中，1天；transform开销待测 | React + Motion；CSS3D，非WebGL；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |
| 22 | [Aurora](https://reactbits.dev/backgrounds/aurora) | 背景、动画 | 低 | / · 欢迎页顶部短区域 | 太空主题能借鉴色带，但工作区已有背景 | 使用冷暖token且低透明度；移动/减动效静态渐变 | 高，1–2天；WebGL/GPU与显存需实测 | React + OGL（新增）；优先已有背景能力；免费；MIT + Commons Clause；应用可用，组件不可单独/打包再分发；保留声明。见本轮LICENSE证据。 | browser-viewed |

## 前五条截图 / Top5 screenshots

### 01 · Stateful Button

![Stateful Button](./assets/previews/stateful-button-loading.jpg)

### 02 · Animated List

![Animated List](./assets/previews/animated-list.jpg)

### 03 · Multi Step Loader

![Multi Step Loader](./assets/previews/multi-step-loader.jpg)

### 04 · File Upload

![File Upload](./assets/previews/file-upload.jpg)

### 05 · Animated Tabs

![Animated Tabs](./assets/previews/tabs.jpg)

## 实际观察 / Recorded observations

- **01 Stateful Button**：点击Send message后截图出现旋转加载标记，随后回到可发送状态；成功状态由说明描述，未捕获成功瞬间。无实际消息发送测试。 Checked: 2026-09-30T11:55:52.184949+00:00.

- **02 Animated List**：点击Item 3，查看15项列表、边缘渐隐和滚动条；Keyboard Navigation开关已启用，但未实际完成方向键验收。 Checked: 2026-09-30T11:44:11.059313+00:00.

- **03 Multi Step Loader**：点击Click to load后出现步骤覆盖层；两张截图分别显示首项与第二项高亮推进。文档默认2000ms、loop=true；这是演示计时，不是真实任务完成。 Checked: 2026-09-30T11:56:09.439827+00:00.

- **04 File Upload**：实看网格上传卡片和文案，打开Manual核实依赖与源码；未选择文件、拖放或测试系统文件对话框。源码点击容器需补键盘语义。 Checked: 2026-09-30T11:57:10.839752+00:00.

- **05 Animated Tabs**：点击Services后选中背景移到Services，内容成为Services tab；原演示同时保留多张堆叠卡片，不能照搬到窄侧栏。 Checked: 2026-09-30T11:56:56.957894+00:00.

- **06 Fade Content**：点击Refresh animation后捕获由暗到可见的早期帧；面板显示Duration=1s、power2.out、blur关闭。1s是控件值，未测实际完成耗时。 Checked: 2026-09-30T11:50:22.179823+00:00.

- **07 Sidebar**：实看折叠图标栏、Dashboard/Profile/Settings/Logout和右侧内容骨架。hover展开、移动和键盘行为由说明提供，本轮未实测。 Checked: 2026-09-30T11:57:36.729382+00:00.

- **08 Spotlight Card**：点击Boost Your Experience文本后截图可见卡片局部聚光。默认rgba(255,255,255,0.25)来自Props；未连续采样指针轨迹。 Checked: 2026-09-30T11:52:17.553666+00:00.

- **09 长文本省略与 More 入口**：在Visual Design的长文本示例块点击More；截图可见两行省略和More入口，未观察到可确认的展开变化。只借鉴截断排版，实施时须真正展开并验证。 Checked: 2026-09-30T11:58:20.725082+00:00.

- **10 Masonry**：实看四列不同高度图片网格。面板duration=0.6s、stagger=0.05s；hover/重排和手机断点未实测。 Checked: 2026-09-30T11:54:04.084285+00:00.

- **11 Count Up**：最初读取预览为0，后续截图显示100。面板To=100、From=0、Duration=1；Props默认2是另一默认说明，不能混用或称实际1秒。 Checked: 2026-09-30T11:51:33.709476+00:00.

- **12 Pill Nav**：点击Mobile·375px后预览面板缩为375px，HOME/ABOUT/CONTACT仍可见；这只是来源预览宽度，不是当前项目手机验收。 Checked: 2026-09-30T11:51:12.080199+00:00.

- **13 Animated Content**：切换Reverse Direction后开关变为checked；控件显示100px、0.8s、power3.out。方向开关状态已确认，实际轨迹与帧率未采样。 Checked: 2026-09-30T11:51:46.579381+00:00.

- **14 Border Glow**：实看卡片外观及参数：edgeSensitivity=30、radius=28、glowRadius=40。指针跟随效果来自说明，未观察连续轨迹，不能当作性能通过。 Checked: 2026-09-30T11:52:35.221760+00:00.

- **15 纸飞机发送按钮**：在四列按钮画廊第一行第三列点击纸飞机Button；焦点落在该按钮，未出现持久状态变化。仅借鉴图标/形状，hover轨迹未测。 Checked: 2026-09-30T11:59:23.216594+00:00.

- **16 Dock**：实看四个图标按钮的Dock外观，baseItemSize=50、magnification=70来自控件。未实际完成指针放大或键盘导航测试。 Checked: 2026-09-30T11:52:46.597818+00:00.

- **17 Star Border**：实看黑色Star Border按钮，控件显示Magenta/1px/5s；Props默认speed=6s，区别于演示配置。截图未捕获完整边光运动。 Checked: 2026-09-30T11:53:49.557802+00:00.

- **18 Blur Text**：打开Animate By并选择Letters，面板变为逐字文本，截图捕获模糊起始字形。200ms是逐字延迟，stepDuration=0.35s来自Props，不能误认为整句总时长。 Checked: 2026-09-30T11:53:23.034363+00:00.

- **19 Logo Loop**：切换Fade Out后Reset出现，截图显示多枚技术Logo连续排列。100px/s和hoverSpeed=0是控件值；移动速度与暂停响应未实际测量。 Checked: 2026-09-30T11:54:41.595385+00:00.

- **20 Click Spark**：点击Click Around后保存截图，反馈在截图时未明显呈现；Duration=400ms、8条火花是控件说明。完整火花动画没有验证。 Checked: 2026-09-30T11:53:33.474259+00:00.

- **21 Tilted Card**：实看300px图片卡片与标题覆盖层。rotateAmplitude=12和scale=1.05是控件值，Props默认14/1.1另有区别；实际倾斜轨迹未实测。 Checked: 2026-09-30T11:54:20.869921+00:00.

- **22 Aurora**：逐页单独打开，截图可见绿紫色极光背景与标题。speed=1、blend=0.5来自控件；未测FPS、低端设备和WebGL回退。 Checked: 2026-09-30T11:59:52.463570+00:00.

## 比较与组合 / Comparison and combinations

01适合最局部的发送等待反馈，成本最低。02改善历史和任务定位，须保留搜索、分组和滚动。03适合较长的视频生成阶段，须改成内联并接真实任务事件。

01 is the most localized feedback change; 02 improves history/task finding; 03 suits longer generation workflows and must use real events rather than a demo timer.

- 操作反馈 / Operational feedback: **01 + 03 + 06**.
- 历史与素材 / History and assets: **02 + 04 + 05**.
- 局部视觉 / Local emphasis: **08 or 14**, avoiding duplicate glow effects.

## 实施边界 / Implementation boundary

这是插件浏览与报告验收，用户未选择或确认具体实施方案，目标网站没有修改。选择编号后先生成逐元素方案；确认后实施，随后做桌面、移动、键盘和减动效实测。

This round validates research/reporting. The target website was not modified. User selection leads to an element-level proposal; confirmation precedes implementation and post-implementation browser checks.
