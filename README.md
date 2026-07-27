# VoxEasy

一句话或一篇完整文案，直接生成可用于 Google Flow 的 Vox 风格视频 Prompt。

VoxEasy 是一个面向 AI Agent 的 Vox 剪纸拼贴视频导演 Skill。它会先整理旁白与叙事结构，再设计视觉隐喻、数据图表、纸质动画和运镜，最终输出可直接复制到视频模型的英文 Prompt 与结构化 JSON。

## 核心能力

- 输入一句话、一个主题或完整文案
- 独立生成标题 Shot，标题不与正文混用
- 将抽象概念映射为可见的纸质剪贴画实体
- 主动设计大号数字、图表、箭头、时间线等 Vox 信息图元素
- 根据旁白长度自动匹配 4、6、8、10 秒视频档位
- 避免相邻 Shot 重复使用相同运镜
- 输出声画对照表、Google Flow Prompt 和结构化 JSON
- 不需要额外配置第三方视频生成 API

## 画风

VoxEasy 4.2 内置五种画风选择：

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
主题或完整文案
      ↓
旁白文案与独立标题确认
      ↓
逐 Shot 视觉隐喻与画风确认
      ↓
Google Flow Prompt + 结构化 JSON
```

VoxEasy 采用两次确认机制。用户确认旁白后才进入视觉设计，确认画面后才输出最终 Prompt，避免在构图没有确认时直接生成成片指令。

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
    └── style-presets.md
```

- `SKILL.md`：完整工作流、确认节点、Prompt 与 JSON 输出规范
- `beat-architectures.md`：叙事弧与 Shot 结构
- `palettes.md`：配色方案
- `style-presets.md`：预设与自定义画风规则

## 版本

当前版本：VoxEasy 4.2

项目地址：<https://github.com/louchi1984-coder/voxeasy>
