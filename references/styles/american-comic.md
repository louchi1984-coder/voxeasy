# 美漫纸质拼贴 `american-comic`

## 画风

- 整个背景、主体和文字容器统一使用经典美漫印刷语言：粗手绘炭笔轮廓、Ben-Day 网点、角形排线、丝网印刷色块、轻微套色偏移和粗糙油墨。
- 保留扁平纸层、可见切边、纸张厚度和真实投影，不做普通数字漫画或光滑 3D。
- 默认色：暖珊瑚红 `#E8625C`、哑光青蓝 `#2B697A`、芥末黄 `#E5A93C`、奶油白 `#FAF9F5`、深炭灰 `#2D2D2D`。

## 画面设计

根据已确认的核心信息、表达方式和场景锚点只选一种结构：

- **单幅冲击**：一个夸张中心主体或隐喻配速度线、冲击线或锯齿框，用于冲突、结论和揭示。
- **顺序分格**：2–3 个不对称纸质分格表现直接过程、人物行动或原因与结果。
- **漫画编辑图解**：旁白框、箭头、放大框和局部特写解释真实机制、数据或抽象关系。

不同时堆入分格、对话框、拟声词和爆炸框。字幕不是对话时用旁白框而非对话气泡。普通物体可适当夸张比例，但不自动添加人脸。背景必须同样美漫画风，不能只漫画化中心主体。

## 动作与镜头

- 分格可翻开、滑入或被墨线划分；单幅主体可沿速度线进入或突破边框；图解可局部放大和墨线追踪。
- 按画面选择横移、快速推近、漫画页拉远或局部特写，不按 Shot 编号固定。
- 只执行主文件规定的一次主要转变。

## Prompt 锁定

英文锚点：

`classic American comic-book print art direction, bold hand-inked charcoal contours, expressive cartoon proportions, Ben-Day halftone dots, angular black hatching, screen-printed color fills, slight registration offset, rough ink texture`

明确写出所选结构、分格或主体的尺寸、位置、边框和层级。可见文字放入旁白框、冲击框或短标签；没有批准文字时禁止自动生成拟声词。

结尾：

`Dynamic [confirmed camera direction] camera motion, fluid comic-panel animation with tactile paper-collage movement, bold hand-inked charcoal contours, Ben-Day halftone dots, angular black hatching, screen-printed color fills, slight registration offset, sharp paper-layer shadows, high contrast, clean illustrated details. Use the specified Hex values only as invisible color-generation controls. Never render Hex codes or color-code notation as visible text inside the scene. Clean video canvas, no unapproved text, no debug text overlays, no watermarks, no voiceover, no human speech, no talking heads, silent video. --ar [actual ratio]`

禁止版权角色、英雄制服、出版商标志、现有漫画页面复刻，以及每个 Shot 重复同一种放射爆炸背景。
