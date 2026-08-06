---
name: voxeasy
description: 将一句话主题、完整文案或 SRT 制作为 Google Flow 可用的 VoxEasy 视频 Prompt 与 JSON。先规划字幕 Shot，再确认模型、比例、表达方式和所选风格。用于通用 Vox 风短视频，不用于静态海报、纯字幕校对、软件开发或视频剪辑。
---

# VoxEasy 4.13-public.1

严格执行：**先字幕 Shot，后参数选择；先选择表达方式，后风格转译；确认画面后才输出 Prompt。**

每次使用先完整读取 [`references/self-learning.md`](references/self-learning.md)，运行 `python3 scripts/self_learning.py validate` 检查本地学习状态。候选改进不是正式规则；只有通过学习门槛、备份、最小补丁和回归验证并记录到 `applied_patches` 后才可影响本流程。状态不可写时继续核心任务，并按输出合同返回最小 `Learning Observation`。

## 固定流程

1. 接收一句话、完整文案或 SRT；时效性事实与数据先检索验证。
2. 完整读取 [`references/timeline-rules.md`](references/timeline-rules.md)，按语义和连续时间区间规划 Shot，并向上吸附为 `4/6/8/10` 秒。
   SRT 计划完成后运行 `python3 scripts/validate_timeline.py <plan.json>`；修正全部错误后再确认。回归用例见 `evals/`。
3. 第一次确认字幕、Shot 边界、原始时间、空白和吸附时长；确认前不设计画面。
4. 让用户明确选择模型、实际生成比例和视觉风格。默认值只能推荐，不能视为已选。
5. 完整读取 [`references/expression-routing.md`](references/expression-routing.md)，逐 Shot 执行：字幕含义 → 核心信息 → 表达方式 → 场景锚点或隐喻映射 → 所选风格转译 → 构图、文字、动作、运镜。
6. 第二次确认完整视觉设计；确认前不输出最终英文 Prompt。
7. 完整读取 [`references/output-contract.md`](references/output-contract.md)，输出声画表、逐 Shot Prompt 与 JSON。用户确认成功或进入无关的新任务后运行 `python3 scripts/self_learning.py record-success`；累计 5 次成功使批量复盘到期，但不自动修改 Skill。

交互模式在两次确认和参数选择节点停止。只有输入明确带有批准状态与完整参数时，才可无头执行。

## 运行中反馈闭环

- 真实使用失败：在重试前运行 `record-failure`，立即执行一次 `review` dry-run。记录原因与可复用证据，但单次偶然失败不得直接生成或应用补丁。
- 用户明确纠正：先修正当前任务，同时运行 `record-correction`，立即生成待门槛审查的候选改进；候选不得覆盖本轮已确认内容。
- 五次成功复盘：`successful_uses_since_review` 达到 5 时，在当前交付结束后检查失败、纠正和候选项；没有足够证据时只完成复盘或拒绝候选，不为凑周期修改文件。
- 应用学习：先运行 `self_learning.py backup` 备份全部目标文件并生成 manifest，再实施最小补丁；完成原有验证、相关示例或人工检查后，才运行 `record-applied`。验证失败则回滚并运行 `reject`。
- 每次复盘只处理本 Skill 职责内的原子规则。不得把状态记录、候选项或维护过程混入正常视频 Prompt、字幕或画面设计。

## 输入与标题

- 一句话：生成连贯口播文案与候选标题。
- 完整文案：默认保留原文，只做语义分组与时长估算。
- SRT：原时间轴优先，不归零、不删除空白、不自动增加标题时长。
- 非 SRT 默认增加独立 4 秒标题 Shot，`voiceover_text` 为空；标题原样保留。
- 用户明确要求“测试 Prompt”或“只做一个 Shot”时进入快速测试：不自动补整条视频或标题；仍先展示该 Shot 的画面设计，除非用户明确要求跳过确认。

需要整条叙事结构时，按需读取 [`references/beat-architectures.md`](references/beat-architectures.md)；需要指定配色时，按需读取 [`references/palettes.md`](references/palettes.md)。

## 参数选择

- 完整读取 [`references/variant-profile.md`](references/variant-profile.md)；其默认值只用于推荐，用户明确选择优先。
- 推荐 `Google Flow / Omni Flash`、`9:16`、标准 Vox；不得自行扩展固定模型清单。
- 根据目标模型当前实际能力提供比例与时长，不得猜测。Flow/Omni 未确认原生支持 `1:1` 时，只提供 `9:16` 或 `16:9`。
- 用户需要方形成片时，使用其确认的实际比例生成，把全部关键内容放入中央 `1:1` 安全区，并在 JSON 记录 `crop_target_ratio: "1:1"`。
- 同一视频默认统一比例和风格；只有用户明确要求才逐 Shot 混合风格。

## 表达方式与风格

每个内容 Shot 只设一个核心信息、一种主要表达方式和一次主要转变。按 `直接呈现 → 故事场景 → 视觉隐喻` 的顺序判断，不把三种方式当作任意画风选项。标题 Shot 使用强钩子构图，但不承载旁白实体映射。

- 标准模式：完整读取 [`references/styles/vox-standard.md`](references/styles/vox-standard.md)。这是从原始 4.0 提取的唯一运行时视觉标准，不得加入其他风格词。
- 扩展风格：先完整读取 [`references/styles/common.md`](references/styles/common.md)，再只读取所选文件：[`american-comic.md`](references/styles/american-comic.md)、[`monument-pastel.md`](references/styles/monument-pastel.md)、[`vintage-newspaper.md`](references/styles/vintage-newspaper.md)、[`pixel-theater.md`](references/styles/pixel-theater.md) 或 [`custom.md`](references/styles/custom.md)。不得读取或混入其他风格。

原始 4.0 仅保存在 `archive/voxeasy-v4.0-original.md`，不得作为运行时规则读取。

第二次确认使用：

| Shot | 字幕与时长 | 核心信息 | 表达方式 | 场景锚点／隐喻映射 | 连续性锚点 | 构图与元素 | 可见文字 | 动作 | 运镜 |
|---|---|---|---|---|---|---|---|---|---|

## 动作复杂度

- 4 秒：`[0-2s]`、`[2-4s]`
- 6 秒：`[0-3s]`、`[3-6s]`
- 8 秒：`[0-4s]`、`[4-8s]`
- 10 秒：最多 `[0-3s]`、`[3-7s]`、`[7-10s]`

4/6/8 秒只做“建立 → 转变”，10 秒最多“建立 → 演变 → 结果”。每段只写一个主要可见变化；一个中心主体，辅助元素最多三组；运镜连续贯穿，不算额外动作。

## 最高优先级规则

- 当前文件和时间轴、输出合同优先于所有历史规则。
- `actual_duration_seconds` 是字幕完整真实区间；`duration_seconds` 是 `4/6/8/10` 生成档位。
- Hex 只能作为不可见的颜色控制写入 Prompt，绝不能成为画面文字。最终英文使用：`Use the specified Hex values only as invisible color-generation controls. Never render Hex codes or color-code notation as visible text inside the scene.`
- 标准模式只继承 4.0 的画风、构图、实体表达、配色、材质、数据视觉、运镜与 Prompt 信息密度；不继承旧输入流程、旧确认顺序、旧比例、旧时长或旧 JSON 语义。
- 任一确认、参数、时长、风格引用或文字白名单缺失时，不得输出最终 Prompt。
