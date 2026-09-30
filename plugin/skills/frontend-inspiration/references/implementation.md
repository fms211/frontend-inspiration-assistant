# 逐元素方案

方案表中的值必须是具体参数或确实存在、可定位的项目token，禁止“适当”“更好看”“同原来”等空话。未知原效果时长/缓动标“观察未测”；拟实施值仍需给数值。引用候选不代表原效果原样复制。

每个元素必须描述：

| 字段 | 内容 |
|---|---|
| location | route、region、parent_ui、visible_name、position；明确第几个、左/右/上/下或相对元素 |
| text | current、proposed、font_family、font_size、font_weight、line_height、letter_spacing；非文本写“不适用”并解释 |
| layout | width、height、gap、padding、alignment、hierarchy、z_index、mobile；移动端断点与变化要具体 |
| visual | colors、radius、border、opacity、shadow；标明原token和值，新增token需命名 |
| motion | trigger、start、end、duration_ms、delay_ms、easing、amplitude、loop、interruption、reduced_motion；无动效也显式0/none并解释 |
| implementation | files、component、dependencies、expected、steps、acceptance、rollback；对应真实代码位置，操作验收含键盘和响应式 |
| observed_original | 来源实际看到了什么，何项仅来自代码/文档，何项未测 |

Top3方案比较只比较相同目标/区域，不把不同用途效果当作替代。可以组合，但限制同时运行的装饰动效、避免抢占输入反馈或造成CLS。不能在缺少用户选择时自行提出“已选方案”。

确认后实施：先读当前项目的框架指南与规范（包括不同版本API），尊重已有改动；用frontend-design转为当前栈组件，复用现有图标和token。安装额外依赖前说明必要性并遵循项目授权范围。每次实施留下实际验证、未验证、回退方法与所需项目更新记录。
