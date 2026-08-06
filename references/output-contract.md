# 最终输出合同

只有字幕 Shot、生成参数和视觉设计全部确认后才输出。

## 交付物

1. 声画对照表。
2. 每个 Shot 一段 Google Flow 可直接复制的连续英文 Prompt。
3. 结构化 JSON。

## Prompt 强制项

每段 Prompt 必须依次写全：

1. 所选风格、实际比例和明确吸附时长；前两句形如 `Vox style paper-cut collage art, vertical 9:16. 6-second duration.`
2. 铺满画布的视觉基底，而非漂浮容器。
3. 已确认的表达方式和场景锚点；只有 `metaphor` 模式写视觉隐喻及其可见实体映射。
4. 中心主体和最多三组辅助元素的造型、材质、颜色、位置与状态。
5. 前景、中景、背景和上下左右关系。
6. 获准文字的逐字白名单；无文字时写 `Display no text.`。
7. 与生成时长完全一致的两段或三段动作时间戳。
8. 一种连续贯穿全 Shot 的运镜、方向和强度。
9. 所选风格的材质、轮廓、光影、动画稳定性和禁止项。
10. 实际 `--ar`、无水印、无配音、无人声和静音视频。

Hex 只用于控制颜色。Prompt 必须写：

`Use the specified Hex values only as invisible color-generation controls. Never render Hex codes or color-code notation as visible text inside the scene.`

Prompt 使用自然连续英文，不得输出“背景：”“主体：”等模板标签。时间戳不能代替明确的 `4/6/8/10-second duration`。

## JSON

```json
{
  "shot_id": "02",
  "source_start": "00:00.000",
  "source_end": "00:06.700",
  "subtitle_text": "确认后的字幕",
  "voiceover_text": "确认后的旁白",
  "included_blank_seconds": 1.3,
  "actual_duration_seconds": 6.7,
  "duration_seconds": 8,
  "model": "Google Flow / Omni Flash",
  "aspect_ratio": "9:16",
  "crop_target_ratio": null,
  "visual_style": "vox-standard",
  "core_message": "本镜核心信息",
  "expression_mode": "direct | story | metaphor",
  "scene_anchor": "真实主体、故事场景或隐喻场景",
  "continuity_anchor": null,
  "visual_metaphor": null,
  "entity_mapping": [],
  "visual_summary": "确认后的画面",
  "camera": "确认后的运镜",
  "visible_text": ["确认后的短标签"],
  "visual_prompt": "完整英文 Prompt"
}
```

`actual_duration_seconds` 记录连续真实区间；`duration_seconds` 必须是吸附后的 `4/6/8/10`，并与 Prompt 和生成工具调用参数完全一致。

`direct` 与 `story` 的 `visual_metaphor` 必须为 `null`，`entity_mapping` 通常为空；`metaphor` 必须填写两者。只有存在连续演变或跨 Shot 重复主体时才填写 `continuity_anchor`，否则为 `null`。

## 交付前检查

- 时间轴空白是否完整，真实时长与吸附档位是否正确？
- 模型、实际比例、裁切目标和风格是否已确认？
- 每个内容 Shot 是否有一个核心信息和一种表达方式，并满足该模式的场景锚点、隐喻或连续性要求？
- 是否只读取并使用所选风格，且达到完整 Prompt 合同？
- 可见文字是否完全来自白名单，Hex 是否明确禁止可见？
- 动作段数、动作时间戳和连续运镜是否与时长一致？

任一项为否时不得交付。

## 无持久化权限时的学习回退

正常情况下，学习状态写入外部 JSON，不改变上述交付物。只有发生真实失败、用户明确纠正或五次成功复盘到期，并且状态文件不可写时，才在全部正常交付物之后追加一个结构化对象：

```json
{
  "learning_observation": {
    "event_type": "failure | user_correction | success_batch_review",
    "observed_at": "ISO-8601 UTC",
    "summary": "不含原始文案、路径、账号、密钥或隐私信息的抽象说明",
    "candidate_improvement": {
      "trigger": "清楚触发条件",
      "action": "可执行规则",
      "boundary": "适用边界",
      "validation_plan": "测试、dry-run、validator、示例任务或人工检查"
    },
    "persistence_status": "unavailable"
  }
}
```

没有学习事件时不输出该对象。单次偶然失败或未通过学习门槛时，`candidate_improvement` 使用 `null`。不得把 Learning Observation 写入 `visual_prompt`。
