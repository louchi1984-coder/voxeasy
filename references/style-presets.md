# VoxEasy Global Visual Style Presets

仅在用户选择非默认 `visual_style` 时读取本文件。所有预设都叠加在 VoxEasy 的纸质剪贴画框架之上，不替代叙事、实体映射、动作、时间轴、运镜或固定负向后缀。

## 目录

- 通用执行顺序
- `american-comic` — 美漫纸质拼贴
- `monument-pastel` — 纪念碑谷式柔和几何画风
- `vintage-newspaper` — 复古报纸与模拟印刷
- `custom` — 用户自定义全局画风

## 通用执行顺序

1. 先完成标准 Vox 镜头的内容、构图、实体、文字、动作和运镜设计。
2. 再把所选预设作为整帧渲染层，覆盖背景与前景的颜色、轮廓、纸面纹理、印刷痕迹和阴影。
3. 普通内容镜头不得因画风改变而增加、删除或重排元素。
4. 只有用户明确要求“介绍/展示该风格”时，才使用各预设的风格介绍镜头规则。
5. Prompt 开头仍必须使用 `Vox style paper-cut collage art, [aspect ratio].`，结尾仍必须使用 SKILL.md 规定的完整固定后缀。

## `american-comic` — 美漫纸质拼贴

### 全局渲染语言

- 对背景和前景统一使用粗手绘炭笔轮廓、Ben-Day 网点、角形排线、丝网印刷色块、轻微套色偏移与不均匀油墨密度。
- 保持所有元素为有厚度、可见分层边缘和真实投影的扁平纸质剪贴画。
- 默认沿用 `vox-authentic`：暖珊瑚红 `#E8625C`、哑光青蓝 `#2B697A`、芥末黄 `#E5A93C`、奶油白 `#FAF9F5`、深炭灰 `#2D2D2D`。
- 普通内容镜头只做全局画风替换，不自动引入漫画分格、对话框、拟声词、超级英雄或爆炸构图。

### 风格介绍镜头

必须一眼呈现真正的漫画语言，不能只展示印刷工艺。使用一个完整漫画页式构图，至少包含以下四类元素中的三类：

- 不对称漫画分格与粗黑纸质 gutter。
- 纸质对话框或旁白框。
- 拟声词，如本地化的“砰！”、“嗖！”。
- 速度线、冲击线或锯齿爆炸框。

同时保留网点、排线和套色偏移。可使用非人类的原创纸质机器人、火箭或普通物体演示动作；禁止可识别的版权角色、英雄制服、出版商标志和现有漫画页面复刻。

### 英文风格锚点

`classic American comic-book print art direction, bold hand-inked charcoal contours, expressive cartoon proportions, Ben-Day halftone dots, angular black hatching, screen-printed color fills, slight registration offset, rough ink texture`

## `monument-pastel` — 纪念碑谷式柔和几何画风

### 全局渲染语言

- 对背景和前景统一使用柔和粉彩、简化几何轮廓、干净建筑性色块、精确边缘、哑光纸面、柔和定向光与优雅长阴影。
- 推荐配色：灰粉珊瑚 `#E69A91`、柔和青绿 `#78A9A4`、粉雾薰衣草 `#A99BC4`、浅芥末 `#D9BB68`、暖奶油 `#F4E8D0`、克制炭灰 `#3C3A40`。
- 气质保持安静、梦幻、克制和有秩序；背景也必须使用相同的几何色块与光影语言。
- 只借用视觉语言，不自动改成等距视角；原构图不是等距视角时必须保留原视角。
- 不自动加入不可能建筑、连续楼梯、悬浮关卡、旋转廊桥、迷宫、游戏界面或具体游戏角色。

### 风格介绍镜头

用正常 Vox 信息构图介绍三项画风特征：

- “柔和配色”：叠放的粉彩纸质色样。
- “纯净几何”：圆形、拱形、柱形、阶梯色块的平衡组合。
- “安静光影”：简单几何物体与一条优雅长阴影。

三项内容应处于同一完整画布中。不得为了展示该风格而强制制造连续不可能空间或复刻具体游戏关卡。

### 英文风格锚点

`serene pastel geometric art direction, simplified geometric silhouettes, clean architectural color blocking, matte paper surfaces, precise edges, gentle directional lighting, elegant long shadows, balanced negative space, calm dreamlike atmosphere`

## `vintage-newspaper` — 复古报纸与模拟印刷

### 全局渲染语言

- 对背景和前景统一使用纤维感旧新闻纸、粗黑油墨、可见网点、复印机高反差、褪色边缘、轻微折痕、不均匀着墨和克制套色偏移。
- 推荐配色：旧报纸灰 `#D5D0C8`、奶油纸 `#FAF9F5`、深黑 `#111111`、暗酒红 `#722F37`、芥末棕 `#B58A32`。
- 使用撕裂栏线、裁切档案纹理、印刷图表碎片、墨线箭头和小型印章增加编辑密度，但不得破坏信息层级。
- 背景必须同样报纸化并填满画布，不得把内容缩成一张孤立报纸悬浮在普通背景上。

### 风格介绍镜头

用一张铺满画布的连续报纸编辑构图介绍三项印刷痕迹：

- “粗网点”：放大的网点图像或剪影。
- “油墨颗粒”：不均匀黑墨与复印噪点。
- “轻微错版”：两层强调色与黑色轮廓的微小错位。

使用箭头、连线和纸质标签连接三项特征，不使用漫画分格、对话框或与报纸无关的装饰性爆炸构图。

### 英文风格锚点

`vintage newspaper and analog photocopy editorial style, fibrous old newsprint, coarse black ink, visible halftone dots, uneven photocopy contrast, faded edges, subtle fold marks, imperfect ink coverage, restrained color misregistration`

## `custom` — 用户自定义全局画风

### 输入与提炼

接受用户的一句话自然语言画风描述，不要求用户填写参数表。例如：“低饱和蜡笔杂志风”“蓝白陶瓷纹样风”“黑金雕版印刷风”。若用户只说“自定义”而没有描述，按 SKILL.md 的规定只追问一次。

收到描述后，自动提炼为 `custom_style_profile`：

- `name`：简短画风名称。
- `palette`：3～6 个主色及 HEX。
- `shape_language`：轮廓、比例、几何或手绘造型规则。
- `surface_texture`：纸张、颜料、印刷、笔触或材料质感。
- `lighting_and_shadow`：光线方向、阴影软硬和层次方式。
- `background_treatment`：背景如何使用同一画风并保持信息密度。
- `forbidden_additions`：用户未要求、但模型容易擅自加入的题材或结构。
- `english_style_anchor`：将以上特征压缩成一段可直接放入英文 Prompt 的全局画风锚点。

### 执行规则

- 先完成标准 Vox 内容和构图，再将 `custom_style_profile` 应用于整个画面。
- 同时处理背景和前景，不得只改变主体、标题或局部装饰。
- 保留原有物体、位置、文字、动作、时间轴、视角和运镜。
- 不得把画风名称当成题材指令；只使用用户描述中明确出现或可由其视觉特征直接推导的元素。
- 用户提供参考作品、品牌或艺术方向时，提取可见的配色、轮廓、材质、光影和排版特征，不加入其角色、标志、具体场景或现成构图。
- 在视觉确认阶段先展示 `custom_style_profile` 摘要，让用户确认后再生成最终 Prompt。

### 风格介绍镜头

当用户要求介绍自己的自定义画风时，从 `custom_style_profile` 中选择最有辨识度的三个可见特征，将它们实体化为同一完整画布中的三个示例，并使用本地化短标签。不得套用美漫、报纸或纪念碑谷预设的展示元素，除非用户的自定义描述明确包含这些特征。

### JSON 写法

每个使用自定义画风的 Shot 必须包含：

```json
{
  "visual_style": "custom",
  "custom_style_profile": {
    "name": "用户画风名称",
    "palette": ["#000000", "#FFFFFF"],
    "shape_language": "简短规则",
    "surface_texture": "简短规则",
    "lighting_and_shadow": "简短规则",
    "background_treatment": "简短规则",
    "forbidden_additions": ["禁用项"],
    "english_style_anchor": "English global style anchor"
  }
}
```
