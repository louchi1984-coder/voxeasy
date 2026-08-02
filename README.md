# VoxEasy

输入一句话、完整文案或 SRT，生成可用于 Google Flow 的 Vox 风格视频 Prompt。

VoxEasy 是一个面向 AI Agent 的 Vox 剪纸拼贴视频导演 Skill。它先按语义和完整时间轴拆分字幕 Shot，再让用户选择模型、比例和风格；画面确认后，才输出可直接复制到视频模型的英文 Prompt 与结构化 JSON。

## 核心能力

- 输入一句话、完整文案或 SRT 字幕
- SRT 保留开场、句间、镜头间和尾部空白时间
- 按完整时间向上吸附为 4、6、8、10 秒素材
- 交互模式先选择模型、画面比例和视觉风格
- Google Flow / Omni 只提供原生支持的 `9:16`、`16:9`
- 方形成片使用中央 `1:1` 安全区，并在后期裁切
- 非 SRT 模式独立生成标题 Shot；SRT 模式服从原时间轴
- 将抽象概念映射为可见的纸质剪贴画实体
- 主动设计大号数字、图表、箭头、时间线等 Vox 信息图元素
- 4、6、8 秒使用两段动作，10 秒最多三段，避免模型执行过载
- 所有扩展画风继承标准 4.0 的 Prompt 信息完整度，显式锁定时长、构图、文字、动作和运镜
- 避免相邻 Shot 重复使用相同运镜
- 输出声画对照表、Google Flow Prompt 和结构化 JSON
- 不需要额外配置第三方视频生成 API

## 画风

VoxEasy 4.9 内置五种画风选择：

| 画风 | 说明 |
| --- | --- |
| `vox-standard` | 经典 Vox 剪纸拼贴，默认风格 |
| `american-comic` | 美漫分格、网点、对话框、速度线与冲击框 |
| `monument-pastel` | 柔和粉彩、纯净几何与安静长阴影 |
| `vintage-newspaper` | 旧新闻纸、粗网点、油墨颗粒与轻微错版 |
| `custom` | 用户用一句自然语言描述自己的画风 |

自定义画风示例：

```text
使用 VoxEasy，把这段文案做成低饱和蜡笔杂志风。
```

VoxEasy 会自动提炼配色、造型、材质、光影、背景处理和禁用元素，并在确认后应用到整个画面。

## 工作流程

```text
一句话、完整文案或 SRT
      ↓
字幕文案、时间轴与 Shot 确认
      ↓
模型、比例与风格选择
      ↓
逐 Shot 视觉设计确认
      ↓
Google Flow Prompt + 结构化 JSON
```

VoxEasy 在交互模式中设置三个停止节点：字幕分镜确认、生成参数选择、视觉分镜确认。任何一个节点未完成，都不会提前输出最终 Prompt。

Google Flow / Omni 不原生支持 `1:1`。用户需要方形成片时，VoxEasy 会先让用户选择 `9:16` 或 `16:9` 作为实际生成比例，再将人物、动作和文字限制在中央方形安全区，最终从中央裁切为 `1:1`。

## 安装

### Codex

```bash
git clone https://github.com/louchi1984-coder/voxeasy.git ~/.codex/skills/voxeasy
```

### Antigravity / Gemini

```bash
git clone https://github.com/louchi1984-coder/voxeasy.git ~/.gemini/config/skills/voxeasy
```

如果目标目录已经存在，请先备份现有版本，再选择更新或替换。

## 使用

在支持 Skill 的 Agent 中直接调用：

```text
使用 VoxEasy：

标题：最简单的 Vox 风视频 Skill 来了
画幅：9:16
画风：标准 Vox

最近，Vox 拼贴视频正在全球短视频平台爆火……
```

也可以只输入一句话：

```text
使用 VoxEasy，做一条介绍 AI Agent 工作流的 9:16 视频。
```

选择自定义画风：

```text
使用 VoxEasy，画风选择自定义：蓝白陶瓷纹样与粗糙手工纸结合。
```

## 目录

```text
voxeasy/
├── SKILL.md
└── references/
    ├── beat-architectures.md
    ├── palettes.md
    ├── style-presets.md
    └── vox-standard-v4.0.md
```

- `SKILL.md`：完整工作流、确认节点、Prompt 与 JSON 输出规范
- `beat-architectures.md`：叙事弧与 Shot 结构
- `palettes.md`：配色方案
- `style-presets.md`：预设与自定义画风规则
- `vox-standard-v4.0.md`：保存的原始 VoxEasy 4.0 标准视觉规则

## 版本

当前版本：VoxEasy 4.9

项目地址：<https://github.com/louchi1984-coder/voxeasy>
