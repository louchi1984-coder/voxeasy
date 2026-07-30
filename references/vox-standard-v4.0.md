---
name: voxeasy
description: VoxEasy — Vox 风格文生视频导演技能。将任意主题或文案，转化为拥有地道 Vox 拼贴美学、数据驱动叙事、叙事弧词库、相邻镜头避同运镜、1-to-1实体映射的工业级视频 Prompt 与脚本包。支持多语言适配、无头调用模式及结构化 JSON 导出，适应多 Agent 协作工作流。
disable-model-invocation: false
---

# VoxEasy (Vox 剪纸拼贴文生视频导演技能 4.0)

本 Skill 旨在将任意输入的主题或完整文案，转化为符合 **Vox 经典剪纸拼贴美学 (Paper-cut Collage Style)** 的工业级视频 Prompt 序列与同频旁白脚本。本版本专为 **Multi-Agent 协作**与**自动化流**优化，支持前台交互与后台无头（Headless）调用。

---

## 🛠️ 阶段一：参数解析与调用模式 (Input & Invocation)

支持两种调用模式：**交互模式 (Interactive)** 与 **无头模式 (Headless)**。
若入参未提供完整配置，Agent 需主动询问；若调用方（如其他 Agent/代码脚本）以 JSON 等结构化形式提供了全量参数，**必须跳过询问，直接执行阶段二**。

### 核心参数 (Core Parameters)
1. **`target_language` (目标语言)**: 旁白与画面贴纸文字的语言（默认根据输入语言自动推断）。
2. **`aspect_ratio` (画幅比例)**: `9:16` (竖屏), `16:9` (横屏), `1:1` (方屏)。
3. **`color_palette` (配色方案)**: 
   - `vox-authentic`: 暖珊瑚红 (`#E8625C`) + 哑光青蓝 (`#2B697A`) + 芥末琥珀黄 (`#E5A93C`) + 奶油纸白 (`#FAF9F5`) + 深炭灰 (`#2D2D2D`) + 赤陶红 (`#C05646`)
   - `retro-editorial`: 奶油纸 (`#FAF9F5`) + 牛皮纸 (`#E6E2D3`) + 荧黄 (`#FFE800`)
   - `warm-vintage`: 暖棕 (`#8B6914`) + 奶油白 (`#FAF9F5`) + 暗酒红 (`#722F37`) + 老报纸灰 (`#D5D0C8`)
4. **`target_engine` (目标渲染引擎)**: 决定 Prompt 倾向。
   - `sora_or_flow`: 强调物理动作与显式时长参数 (如 `6.5-second duration`)。
   - `midjourney_luma`: 强调静态构图，运镜通过后缀控制。

---

## ✍️ 阶段二：旁白文案撰写与第一次确认 (Scriptwriting & Voiceover Checkpoint)

* **文案优先 (Script-First Workflow)**: AI 必须先根据用户提供的主题或原始资料，撰写完整的分镜头旁白大纲（Voiceover Script）。
* **标题独立成镜 (Dedicated Title Shot)**: 成片必须以独立的 **Shot 01 标题镜头**开场。该镜头只展示标题，`voiceover_text` 必须为空，不得承载第一句旁白或其他叙事信息。若用户提供标题，必须 100% 原样保留；若用户未提供标题，AI 应先拟定标题并在第一次确认时一并交由用户确认。所有旁白分镜从 **Shot 02** 开始。
* **数据驱动写作 (Data-Driven Scripting)**: Vox 的灵魂是用数据说话。文案中**必须主动挖掘并嵌入具体的数字、百分比、倍数、对比数据**，而非空洞叙述。例如：
  - ❌ "使用门槛极高" → ✅ "配置流程超过 23 步，劝退了 90% 的创作者"
  - ❌ "全网爆火" → ✅ "单月播放量突破 2000 万"
  - ❌ "大幅提升效率" → ✅ "将制作时间从 4 小时压缩到 15 分钟"
  如果用户提供的原始素材中缺少数据，AI 应主动建议用户补充，或根据合理推断标注为近似值（如 "约 XX%"）。
* **强制搜索验证 (Mandatory Research)**: AI **严禁仅凭自身训练数据编造数字**。在撰写文案前，必须先使用搜索工具（如 `search_web`）查找与主题相关的真实数据、统计、用户量、时间节点等。搜索到的数据应标注来源（如 "据 GitHub 统计"），搜索不到的数据必须如实告知用户并请求补充，绝不可杜撰。
* **强制确认 (Mandatory Checkpoint 1)**: 输出初步的旁白文案后，**必须停止执行并询问用户**：“这是为您准备的旁白文案，请确认是否需要修改？确认无误后我将为您进行视觉隐喻设计。”
* **等待指令**：只有在用户明确回复确认或同意后，才能进入下一阶段。

---

## 🎨 阶段三：视觉设计与第二次确认 (Visual Design & Metaphor Checkpoint)

* **实体映射草案 (Metaphor Mapping)**: 基于已确认的旁白，为每个 Shot 设计核心的视觉元素（剪纸道具、隐喻载体）。必须严格遵守字面 1:1 实体化规则。Shot 01 只设计标题及其纸质背景，不添加旁白实体映射；从 Shot 02 开始，必须参照阶段四第 5 条「Vox 标志性数据可视化元素」，为每个 Shot 主动匹配大号冲击数字、信息图表、标注箭头等数据可视化元素（至少选用 1~2 种）。
* **强制确认 (Mandatory Checkpoint 2)**: 输出每个镜头对应的【核心画面设计简述】后，**必须再次停止执行并询问用户**：“这是为您准备的视觉分镜设计，请确认是否满意？确认后我将生成最终的完整提示词与 JSON 脚本。”
* **等待指令**：只有在用户明确回复确认视觉设计后，才能进入下一阶段。

---

## 🎬 阶段四：AI 导演控制核心 (Director Engine)

### 0. 绝对铁律：四段式流体延时美学框架 (Organic Integration)
所有的 Visual Prompt 必须将以下四段式美学**有机地融合**到一段流畅的英文描述中，绝不能像填表一样生硬，也**绝对禁止删除 Hex 颜色代码、运镜或负面词**：
1. **背景与视觉基底 (Base)**: 强制采用强对比纸质纹理拼接色块（如 vox-authentic 配色中的 `matte teal blue #2B697A` 与 `mustard amber yellow #E5A93C`）。所有元素必须是带有明显厚度感的“手绘纸质贴纸/剪纸插图风格 (Paper-cut Collage Style)”。
2. **扁平隐喻贴纸 (Flat Metaphors)**: 必须保留巧妙的实体隐喻（如金库大门代表 API），但**严禁 3D 化**。必须明确描述为“极简风格化的扁平纯色纸质贴纸 (stylized minimal paper cutout sticker)”，严禁写实手部或人类。
3. **叙事演进 (Evolution)**: 结合时间戳 `[0-3s]`, `[3-6s]`，动作必须体现“建立 -> 沿路径扩散/演变 -> 高潮”的流体延时动画 (Fluid time-lapse animation)。
4. **强行锁定原生质感**: 所有的 Prompt 结尾必须完整保留经典的相机运镜与负面约束（见阶段五）。

### 1. 动态时长、节奏律动与显式参数 (Duration, Pacing & Flow Specs)
单 Shot 时长必须基于旁白字数精准计算，确保旁白读完前画面不提前切帧：
* **标题镜头例外**：Shot 01 固定使用 `4-second duration`，JSON 中 `duration_seconds` 固定为 `4.0`，且 `voiceover_text` 为空。旁白时长计算只适用于 Shot 02 及后续镜头。
* **语速计算**：**中文**按 220~240 字/分钟计算；**英文**按 130~150 词/分钟计算。
* **引擎多档位吸附 (4s/6s/8s/10s Omni Flash 满载适配)**：Google Omni Flash 等主流引擎原生支持 **4秒、6秒、8秒、10秒** 四个固定档位输出，我们必须避免算力浪费与动态崩坏，实施“**智能向上吸附**”策略：
  - 如果语音计算时长 ≤ 3.8s ➔ Visual Prompt 强制使用 `4-second duration`，并写满 4 秒的动态描述。
  - 如果语音计算时长 3.8s ~ 5.8s ➔ Visual Prompt 强制使用 `6-second duration`，并写满 6 秒的动态描述。
  - 如果语音计算时长 5.8s ~ 7.8s ➔ Visual Prompt 强制使用 `8-second duration`，并写满 8 秒的动态描述。
  - 如果语音计算时长 > 7.8s ➔ Visual Prompt 强制使用 `10-second duration`，并写满 10 秒的动态描述。
* **后期裁切闭环**：Visual Prompt 负责生成完美的对应档位（4/6/8/10）素材，而 JSON 的 `duration_seconds` 字段负责记录配音所需的真实精准时长（如 `3.5` 或 `6.5`），用于后期精准剪辑裁切。

### 2. 相邻镜头运镜避同法则 (Camera Motion Diversification)
**连续两个 Shot 绝对不使用相同的运镜方向**：
* Shot 01 (独立标题镜头): `push_in` (2.5D 视差微推)
* Shot 02 (第一段旁白): `tracking_pan_down` 或 `pan_right`
* Shot 03: `layer_dissection` (图层抽离/特写)
* Shot 04: `balance_tilt` (天平/倾斜视角)
* Shot 05+: 轮换 `pull_out` / `parallax` / `static` (仅限落幕点题)。

### 3. 本地化标题与图形门控 (Localized Title & Label Gate)
* **Shot 01** (`title: true`): 必须是独立的纯标题镜头，显示大号剪纸标题，`voiceover_text` 为空，不得合并第一句旁白、数据标签或其他叙事信息。**警告：如果用户在请求中明确指定了视频标题，绝对不允许擅自缩写、提炼或修改，必须 100% 保留用户提供的原标题字眼！**
* **Shot 02~N** (`title: false`): 关闭大号标题。画面中的数据与注释标签必须使用硬核短数据贴纸（Data Tags），且语言必须符合 `target_language`。

### 4. 纯净画面负向约束 (Clean Canvas & Silent Video)
所有 Prompt 必须强制包含无杂质与无声指令：
`Clean video canvas, no hex color codes, no debug text overlays, no watermarks, no voiceover, no human speech, no talking heads, silent video.`

### 5. Vox 标志性数据可视化元素 (Signature Data Visualization)
Vox 纪录片的核心视觉语言是**数据即画面**。在阶段三设计视觉隐喻时，必须为每个 Shot 主动考虑以下元素（至少选用 1~2 种）：
* **大号冲击数字 (Hero Numbers)**: 画面中必须出现巨大的、具有视觉冲击力的数据贴纸（如 `"23 步"`, `"90%"`, `"×10"`, `"$4.2B"`），作为扁平纸质剪贴画渲染。
* **信息图表 (Infographics)**: 剪纸风格的柱状图、饼图、折线图、进度条等，用于可视化对比或趋势。
* **标注箭头与连线 (Annotation System)**: 红色圆圈圈出重点、箭头指向关键元素、虚线从标签连接到物体，增强信息层次。
* **来源引用小字 (Source Citation)**: 画面角落放置小号的 `"Source: xxx, 2024"` 风格的引用标注贴纸，增加权威感和纪录片质感。
* **时间线标记 (Timeline Markers)**: 年份节点标注（如 `"2019" → "2024"`）或里程碑标记，用于体现时间跨度和演进过程。

---

## 🎯 阶段五：结构化双端输出 (Structured Outputs)

必须在用户完成**两次确认（文案确认+视觉确认）**后，同时输出以下三种格式的内容：

### 1. 结构大纲：声画对照表 (Markdown Table)
列表展示每个 Shot 的精确秒数、字/词数、实体映射与对应旁白。

### 2. 人类可读：纯文本提示词包 (Continuous Prompts)
必须将四段式框架有机地融入自然连贯的段落，**绝不允许使用 `[背景与视觉基底]:` 等生硬模板标签**。
**强制规范，缺一不可：**
1. **开头定调**：`Vox style paper-cut collage art, [根据 aspect_ratio 参数填入: vertical 9:16 / horizontal 16:9 / square 1:1].`
2. **极简贴纸与 Hex 色值**：画面中的每个元素必须挂载具体的颜色和 Hex 值（例如 `mustard yellow (#E5A93C) paper cutout sticker`）。
3. **中文大标题/贴纸**：Shot 01 必须只包含用户确认的巨大中文标题，不得承载旁白内容；Shot 02 及后续镜头必须包含中文数据贴纸。
4. **时间戳流体演进**：将 `[0-3s]` 无缝嵌入句子，描述符号贴纸在背景上的流体延时扩散。
5. **神圣不可侵犯的结尾后缀**：在段落最后，**必须且只能**一字不差地加上这段经典后缀，用以控制运镜和约束画面：
`Dynamic [运镜方式如 tracking pan right] camera motion, fluid time-lapse animation with stop-motion paper texture feel, sharp drop shadows, obvious paper layer stacking texture, high contrast, clean vector details. Clean video canvas, no hex color codes (#FF0000), no debug text overlays, no watermarks, no voiceover, no human speech, no talking heads, silent video. --ar [根据 aspect_ratio 填入 9:16 / 16:9 / 1:1]`
（注：`fluid time-lapse animation` 控制整体运动流畅性，`stop-motion paper texture feel` 控制材质质感，两者互补而非矛盾。）

### 3. 机器可读：标准化 JSON 渲染指令 (JSON Artifact)
必须在代码块中输出一段标准的 JSON 数组，供下游 Render Agent 或自动化脚本解析。JSON 中的 `visual_prompt` 字段必须是完全符合上述规范的一整段连续文本。字段规范如下：
```json
[
  {
    "shot_id": "01",
    "duration_seconds": 4.0,
    "voiceover_text": "",
    "visual_prompt": "Vox style paper-cut collage art, vertical 9:16... a dedicated title-only paper collage shot displaying the exact confirmed title... Dynamic push-in camera motion, fluid time-lapse animation with stop-motion paper texture feel...",
    "ui_overlay": {
      "show_title": true,
      "text_labels": ["用户确认的完整标题"]
    },
    "data_viz": {
      "hero_numbers": [],
      "infographics": "none",
      "source_citation": ""
    }
  }
]
```
