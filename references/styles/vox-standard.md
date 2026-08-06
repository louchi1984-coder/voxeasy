# 标准 Vox 4.0 视觉引擎

本文件只保留原始 VoxEasy 4.0 的视觉设计语言。工作流程、时间轴、比例、动作分段和 JSON 服从当前 `SKILL.md`。

## 视觉铁律

每个 Prompt 将以下内容有机写成一段自然英文，不使用模板标签：

1. **强对比纸质基底**：用暖珊瑚红 `#E8625C`、哑光青蓝 `#2B697A`、芥末琥珀黄 `#E5A93C`、奶油纸白 `#FAF9F5`、深炭灰 `#2D2D2D`、赤陶红 `#C05646` 的撕纸或拼接色块铺满画布。
2. **扁平实体表达**：把已确认的真实主体、故事场景或视觉隐喻转译成 `stylized minimal flat solid-color paper cutout sticker`。明确可见纸层厚度、切边和投影；禁止照片写实、光滑 3D、写实手部与说话人物。
3. **叙事演进**：使用主文件规定的时间戳完成一次“建立 → 转变”，并保持流体延时动画与纸质定格触感。
4. **原生质感**：保持锐利投影、明显纸层堆叠、高反差和干净矢量细节。

具体工作台、蓝图、卡片、云门或文件夹不是固定模板；只有当前内容和已确认的表达方式需要时才使用。

## 实体表达与映射

- 先服从 [`../expression-routing.md`](../expression-routing.md) 已确认的 `direct`、`story` 或 `metaphor`，标准 Vox 只负责视觉转译，不重新选择表达方式。
- `direct` 保留真实对象、过程、地图或数据的识别特征；`story` 保留人物、地点、道具与行动；只有 `metaphor` 才逐项说明“哪个实体代表哪个概念”。
- 隐喻模式优先使用可立即读懂的物体、机构、路径、门槛、比较装置和因果变化，不用抽象仪表盘代替内容。
- 一个中心主体，辅助元素最多三组。写清数量、形状、材质、颜色、Hex、方向、位置和状态。
- 标题 Shot 只显示用户确认的完整标题，`voiceover_text` 为空；用大号剪纸字、强对比背景和一个统一视觉钩子形成冲击构图，不承载第一句旁白。

## Vox 编辑与数据视觉

从 Shot 02 开始，每镜主动选择真正有信息作用的 1–2 种元素：

- 大号冲击数字：百分比、倍数、金额、年份或关键计数。
- 剪纸信息图：柱状图、饼图、折线图、进度条或对比尺度。
- 标注系统：红色圈选、箭头、虚线、括号或标签连接。
- 来源贴纸：已验证来源的简短名称和年份。
- 时间线标记：年份节点、里程碑或前后变化。

Shot 02 以后关闭大标题。只显示视觉确认阶段批准的短数据贴纸、来源和标签，不自动生成字幕全文。

## 构图与运镜

- 画面必须铺满全画幅并具有前、中、后景纸层，不做空白背景上的单张漂浮卡片。
- 相邻 Shot 不使用相同运镜方向。沿用原始 4.0 顺序：Shot 01 使用 `push_in`；Shot 02 使用 `tracking_pan_down` 或 `pan_right`；Shot 03 使用 `layer_dissection`；Shot 04 使用 `balance_tilt`；Shot 05 起轮换 `pull_out`、`parallax`、`static`，但静止只用于落幕点题。
- 运镜从头到尾连续执行，服务于主体、过程、故事行动或隐喻揭示，不作为额外动作。

## Prompt 规则

- 开头：`Vox style paper-cut collage art, [vertical 9:16 / horizontal 16:9]. [4/6/8/10]-second duration.`
- 每个主要元素都写具体颜色与 Hex，但 Hex 只能是不可见生成控制。
- 完整写出视觉基底、已确认的表达方式、场景锚点、元素、空间层次、文字白名单、时间轴和连续运镜；只有隐喻模式写概念映射。
- 结尾依据已确认运镜填写：

`Dynamic [confirmed camera motion and direction] camera motion, fluid time-lapse animation with stop-motion paper texture feel, sharp drop shadows, obvious paper layer stacking texture, high contrast, clean vector details. Use the specified Hex values only as invisible color-generation controls. Never render Hex codes or color-code notation as visible text inside the scene. Clean video canvas, no unapproved text, no debug text overlays, no watermarks, no voiceover, no human speech, no talking heads, silent video. --ar [actual ratio]`
