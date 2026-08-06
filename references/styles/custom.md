# 用户自定义画风 `custom`

## 建立画风档案

从用户描述提炼并在视觉确认中展示：

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

用户只说“自定义”而没有描述时，只追问想要的参考方向、配色或质感。

## 画面设计

- 保留已确认的核心信息、表达方式和场景锚点；只有隐喻模式保留视觉隐喻与实体映射。使用画风档案重新设计构图、材质、动作和运镜。
- 不套用标准 Vox 或其他预设构图；不要把画风名称误当题材。
- 用户提供参考作品、品牌或艺术方向时，只提取可见的配色、轮廓、材质、光影、构图和运动特征，不复制角色、标志或现成场景。
- 若属于纸质媒介，可使用与该媒介匹配的纸层控制；非纸质媒介禁止硬塞剪纸词。

## Prompt 锁定

最终 Prompt 明确复述 `shape_language`、`surface_texture`、`lighting_and_shadow`、`motion_grammar`、`camera_grammar` 和 `forbidden_additions`，并完整满足公共输出合同。

根据画风档案生成独立开头和结尾；追加实际比例、明确时长、文字白名单、不可见 Hex 控制、纯净画面、无水印、无配音、无人声和静音视频。
