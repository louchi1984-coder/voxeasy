# VoxEasy Independent Visual Style Presets

本文件只在用户选择非默认 `visual_style` 时读取。扩展风格拥有各自的画面设计逻辑，不必先生成或保留标准 4.0 的工作台、卡片、虚线路径、标注圆与中心组装结构。

## 目录

- 共同边界
- `american-comic` — 美漫纸质拼贴
- `monument-pastel` — 柔和几何画风
- `vintage-newspaper` — 复古报纸与模拟印刷
- `custom` — 用户自定义画风

## 共同边界

所有扩展风格只共用以下内容：

1. 使用已经确认的逐 Shot 字幕，不改变含义、事实和文字。
2. 使用已经确认的 `4 / 6 / 8 / 10` 秒时长。
3. 动作分段统一服从 `SKILL.md` 阶段五：4/6/8 秒使用两段，10 秒最多三段。
4. 每个 Shot 只表达一个核心视觉意思。
5. 视觉阶段确认构图、元素、可见文字、动作、视角和运镜后，才能生成 Prompt。
6. Prompt 仍以 `Vox style paper-cut collage art, [aspect ratio].` 开头，并保留纯净画面与静音约束。

扩展风格可以重新设计背景、构图、主体形态、辅助元素、位置关系、动作、视角和运镜。不得为了保留 4.0 外形而牺牲所选风格的视觉辨识度。

---

## `american-comic` — 美漫纸质拼贴

### 核心画风

- 对背景和前景统一使用粗手绘炭笔轮廓、Ben-Day 网点、角形排线、丝网印刷色块、轻微套色偏移与不均匀油墨密度。
- 保持纸质剪贴画媒介：扁平纸层、可见切边和真实投影。
- 默认配色：暖珊瑚红 `#E8625C`、哑光青蓝 `#2B697A`、芥末黄 `#E5A93C`、奶油白 `#FAF9F5`、深炭灰 `#2D2D2D`。

### 内容镜头设计

根据字幕选择一种最合适的美漫画面结构，不要每个 Shot 都使用同一模板：

- **单幅冲击画面**：一个夸张的中心隐喻，配合速度线、冲击线或锯齿框，适合结论、冲突和产品揭示。
- **顺序分格**：使用 2–3 个不对称纸质分格表现原因、过程和结果，适合步骤、比较和时间演进。
- **漫画编辑图解**：使用旁白框、箭头、放大框和局部特写解释复杂概念，适合机制与数据。

只选择内容真正需要的漫画元素，不必同时加入分格、对话框、拟声词和爆炸框。字幕不是对话时优先使用旁白框而非对话气泡。普通物体可以有略微夸张的漫画比例，但不得自动添加人脸。

### 动作与镜头

- 分格镜头可以依次翻开、滑入或被墨线划分。
- 单幅画面可以让主体突破边框、沿速度线冲入或在冲击框中落版。
- 图解镜头可以使用局部放大、墨线追踪和连续揭示。
- 根据结构选择横移、快速推近、漫画页拉远或局部特写，不按 Shot 编号固定。

### 禁止项

- 禁止可识别的版权角色、英雄制服、出版商标志和现有漫画页面复刻。
- 禁止把所有 Shot 都做成同一种放射爆炸背景。
- 禁止只有前景美漫化而背景仍是普通 Vox 画风。

### 英文风格锚点

`classic American comic-book print art direction, bold hand-inked charcoal contours, expressive cartoon proportions, Ben-Day halftone dots, angular black hatching, screen-printed color fills, slight registration offset, rough ink texture`

---

## `monument-pastel` — 柔和几何画风

### 核心画风

- 对背景和前景统一使用柔和粉彩、简化几何轮廓、干净建筑性色块、精确边缘、哑光纸面、柔和定向光与优雅长阴影。
- 推荐配色：灰粉珊瑚 `#E69A91`、柔和青绿 `#78A9A4`、粉雾薰衣草 `#A99BC4`、浅芥末 `#D9BB68`、暖奶油 `#F4E8D0`、克制炭灰 `#3C3A40`。
- 气质保持安静、梦幻、克制、有秩序。

### 内容镜头设计

根据字幕选择一种几何空间：

- **几何舞台**：用平台、拱门、柱体和圆形承载主体，适合单一概念和产品展示。
- **空间路径**：用连续平台、门洞、桥面或色块路径表现流程与关系，适合步骤和迁移。
- **平衡构图**：用大小、重量、距离和长阴影表现比较、冲突与结论。
- **抽象信息地图**：用几何节点和空间层级表现网络、数据或系统。

原字幕不涉及空间悖论时，不强制制造不可能建筑、连续楼梯或迷宫。等距视角只是可选手段，不是默认要求。

### 动作与镜头

- 几何体可以平移、旋转、升降、对齐或改变尺度。
- 平台和门洞可以依次展开，长阴影随动作平滑变化。
- 运镜优先使用缓慢推拉、平稳横移、轻微俯视或空间绕行，保持安静节奏。

### 禁止项

- 禁止复刻具体游戏关卡、角色或标志。
- 禁止为了“像纪念碑谷”而加入与字幕无关的楼梯、乌鸦、迷宫或悬浮城堡。
- 禁止背景保留普通 Vox 撕纸工作台而只把主体改成粉彩几何。

### 英文风格锚点

`serene pastel geometric art direction, simplified geometric silhouettes, clean architectural color blocking, matte paper surfaces, precise edges, gentle directional lighting, elegant long shadows, balanced negative space, calm dreamlike atmosphere`

---

## `vintage-newspaper` — 复古报纸与模拟印刷

### 核心画风

- 对背景和前景统一使用纤维感旧新闻纸、粗黑油墨、可见网点、复印机高反差、褪色边缘、轻微折痕、不均匀着墨和克制套色偏移。
- 推荐配色：旧报纸灰 `#D5D0C8`、奶油纸 `#FAF9F5`、深黑 `#111111`、暗酒红 `#722F37`、芥末棕 `#B58A32`。
- 画布必须是完整的报纸编辑世界，而不是普通背景上的一张悬浮报纸。

### 内容镜头设计

根据字幕选择一种编辑结构：

- **头版冲击**：大标题、主图框、数据印章和次级栏线，适合新闻钩子与结论。
- **档案拼贴**：照片剪影、日期、地图碎片、引文框和档案编号，适合历史与调查。
- **栏目演进**：连续文本栏、图表与时间线逐列展开，适合过程和因果。
- **印刷机制**：滚筒、油墨层、裁切线和套印层揭示信息，适合机制与制作过程。

不得把字幕全文排成密集报纸正文。只显示视觉确认阶段批准的标题、短标签、日期和数字。

### 动作与镜头

- 报纸栏可以逐列揭开，档案碎片可以被裁切、盖章、圈选或钉入版面。
- 图像可以从粗网点逐渐显影，强调色可以通过套印层落下。
- 运镜可以使用版面横移、纵向栏目滚动、局部放大、印刷机跟随或整版拉远。

### 禁止项

- 禁止漫画分格、对话气泡和与报纸无关的爆炸构图。
- 禁止只给主体添加复印噪点而让背景保持普通纸张。
- 禁止生成大段未经确认的假新闻文字。

### 英文风格锚点

`vintage newspaper and analog photocopy editorial style, fibrous old newsprint, coarse black ink, visible halftone dots, uneven photocopy contrast, faded edges, subtle fold marks, imperfect ink coverage, restrained color misregistration`

---

## `custom` — 用户自定义画风

### 建立画风档案

接受用户的一句话画风描述，自动提炼：

- `name`
- `palette`
- `shape_language`
- `surface_texture`
- `lighting_and_shadow`
- `background_treatment`
- `composition_grammar`
- `motion_grammar`
- `camera_grammar`
- `forbidden_additions`
- `english_style_anchor`

用户只说“自定义”而没有描述时，只追问：“你想要什么画风？直接说参考方向、配色或质感即可。”

### 内容镜头设计

- 根据 `composition_grammar` 为每个字幕 Shot 重新设计画面，不套用标准 Vox 或其他预设的构图。
- 根据 `motion_grammar` 和 Shot 时长执行 `SKILL.md` 阶段五规定的 2–3 段连续动作弧。
- 根据 `camera_grammar` 选择视角和运镜。
- 在第二次确认中先展示画风档案摘要和逐 Shot 画面。

不得把画风名称当成题材指令。用户提供参考作品、品牌或艺术方向时，只提取可见的配色、轮廓、材质、光影、构图和运动特征，不加入其角色、标志或现成场景。
