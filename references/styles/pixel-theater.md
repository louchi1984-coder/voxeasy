# 像素小剧场 `pixel-theater`

## 画风

- 使用原创 16-bit 像素动画微缩剧场：严格低分辨率网格、nearest-neighbor 硬边、无抗锯齿、克制抖色。
- 默认色：哑光青蓝 `#2B697A`、暖珊瑚红 `#E8625C`、芥末黄 `#E5A93C`、奶油白 `#FAF9F5`、深炭灰 `#2D2D2D`。
- 场景必须有镜框式舞台、幕布、脚灯、侧幕和前／中／背景三层具体布景。
- 人物是视觉中心：默认 1–2 个原创全身像素角色，轮廓、表情、姿态、服装和视线清楚稳定。
- Vox 编辑图形只能成为舞台道具、招牌或布景，不得用抽象面板或信息图替代人物和场景。

## 画面设计

根据已确认的表达方式和场景锚点只选一种小剧场结构：

- **交接／救援**：人物交接项目、物件或工具。
- **故障／修复**：主角面对明确故障物件，另一人物协助解决。
- **揭示／演示**：主角揭开、展示或启动真实主体、过程或隐喻道具。
- **场景化流程**：人物操作可见装置，另一人物观察或完成下一步，适合直接呈现机制。

必须具体写出舞台占画面范围、幕布与脚灯颜色、字幕对应的三层布景、人物数量及服装／位置／表情，以及核心道具的位置和作用。隐喻模式才写概念映射。不得复用测试 Prompt 的固定角色、城市或胶片。

## 动作、镜头与文字

- 每段只安排一次清楚角色动作或互动；使用正常视频帧率中的 12fps 式阶梯动画、整数像素移动和轻微待机动作。
- 运镜使用稳定正面机位或一次轻柔居中推近，可带克制整数步缩放和分层视差；禁止混乱追踪或频繁切镜。
- 可见文字只放在大型像素灯牌或舞台标牌，最多三组并逐字批准；避免细小中文像素字。

## Prompt 锁定

开头：`Character-driven Vox editorial pixel-art miniature theater animation, [actual ratio]. [confirmed duration]-second duration.`

英文锚点：

`character-driven editorial pixel-art miniature theater animation, strict low-resolution pixel grid, crisp nearest-neighbor edges, expressive original full-body sprite characters, layered proscenium stage scenery, limited Vox-inspired color palette, deliberately stepped sprite motion, restrained dithering, stable pixel proportions, clear theatrical storytelling`

结尾：

`Use a stable [confirmed frontal camera or centered push-in] throughout the full shot. Deliberately stepped 12-fps-style sprite animation inside a normal video frame rate, integer-pixel movement, consistent character anatomy and clothing, stable facial features, layered stage parallax, crisp nearest-neighbor pixel edges, restrained dithering, high contrast, clean pixel details. Use the specified Hex values only as invisible color-generation controls. Never render Hex codes or color-code notation as visible text inside the scene. No paper-cut texture, no smooth vector curves, no anti-aliasing, no 3D voxels, no Minecraft aesthetic, no platform-game layout, no game HUD, no health bars, no neon cyberpunk, no CRT scanlines, no copyrighted characters, no photorealism, no extra text, no debug overlays, no watermarks, no lip movement, no voiceover, no human speech, silent video. --ar [actual ratio]`

不得使用 `Vox style paper-cut collage art` 开头，不得混入纸张定格材质。
