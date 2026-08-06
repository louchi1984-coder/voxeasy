# VoxEasy

输入一句话、完整文案或 SRT，生成可用于 Google Flow 的 Vox 风格视频分镜、Prompt 与结构化 JSON。

VoxEasy 4.13 先锁定字幕时间轴，再逐 Shot 选择直接呈现、故事场景或视觉隐喻，最后完成模型、比例、画面与运镜确认。标准 Vox 与每种扩展风格使用独立的构图和镜头语言。

## 核心流程

```text
一句话／完整文案／SRT
      ↓
字幕、完整时间轴、Shot与4/6/8/10秒吸附确认
      ↓
模型、实际比例、视觉风格选择
      ↓
核心信息 → 表达方式 → 场景锚点／隐喻映射 → 风格转译
      ↓
逐Shot画面与运镜确认
      ↓
Google Flow Prompt + JSON
```

SRT 会保留开场、字幕内部、镜头之间和已知尾部的空白。`actual_duration_seconds`记录真实连续区间，`duration_seconds`记录向上吸附后的生成档位。

## 公开版画风

| 画风 | 设计与运镜方向 |
| --- | --- |
| `vox-standard` | 原始4.0剪纸拼贴、实体表达、数据标注与Vox运镜序列 |
| `american-comic` | 单幅冲击、顺序分格或漫画图解；推近、横移、页面拉远或特写 |
| `monument-pastel` | 柔和几何舞台、路径与平衡构图；缓慢推拉、横移、俯视或克制绕行 |
| `vintage-newspaper` | 头版、档案、栏目与印刷机制；版面横移、栏目移动、放大或整版拉远 |
| `pixel-theater` | 原创像素人物与微缩舞台；稳定正面机位或居中轻推 |
| `custom` | 根据用户描述建立独立的构图、材质、动作与镜头档案 |

Hex 色值只作为不可见颜色控制，不得显示在画面里。4/6/8秒最多两个主要动作阶段，10秒最多三个。

具体主体、过程、地图和数据优先直接呈现；具体人物、地点和事件使用故事场景；只有总结、抽象关系或缺少现实载体时才使用视觉隐喻。失败、用户纠正和每五次成功使用会进入轻量复盘，但候选规则通过备份和回归验证前不会改变 Skill。

## 版本体系

仓库根目录是唯一公共核心。`profiles/`只定义版本差异，`scripts/build_variants.py`从同一核心生成可安装版本。

| 版本 | 调用 | 用途 |
| --- | --- | --- |
| `voxeasy` | 自动或`$voxeasy` | Git公开稳定版 |
| `voxeasy-news` | `$voxeasy-news` | 新闻、历史、调查和地缘政治 |
| `voxeasy-product` | `$voxeasy-product` | 产品发布、AI工具和工作流介绍 |
| `voxeasy-data` | `$voxeasy-data` | 数字对比、报告和信息图 |
| `voxeasy-lab` | `$voxeasy-lab` | 新画风、自定义与混合风格实验 |

只有公开版允许自动触发；定制版必须手动调用，避免多个Skill抢任务。

## 安装公开版

### Codex

```bash
git clone https://github.com/louchi1984-coder/voxeasy.git ~/.codex/skills/voxeasy
```

### Antigravity / Gemini

```bash
git clone https://github.com/louchi1984-coder/voxeasy.git ~/.gemini/config/skills/voxeasy
```

如果目标目录已存在，先备份，再选择更新或替换。

## 构建定制版

生成全部版本：

```bash
python3 scripts/build_variants.py --all
```

结果位于`dist/`。安装需要的版本：

```bash
cp -R dist/voxeasy-news ~/.codex/skills/
cp -R dist/voxeasy-product ~/.codex/skills/
cp -R dist/voxeasy-data ~/.codex/skills/
cp -R dist/voxeasy-lab ~/.codex/skills/
```

只构建一个版本：

```bash
python3 scripts/build_variants.py --profile profiles/news.json
```

私人定制可新增`profiles/private-*.json`；这些文件已被Git忽略。

## 目录

```text
voxeasy/
├── SKILL.md
├── agents/
├── references/
│   ├── timeline-rules.md
│   ├── expression-routing.md
│   ├── output-contract.md
│   ├── self-learning.md
│   ├── variant-profile.md
│   └── styles/
├── scripts/
│   ├── validate_timeline.py
│   ├── self_learning.py
│   └── build_variants.py
├── profiles/
├── evals/
└── archive/
```

当前公开版本：`4.13-public.1`

项目地址：<https://github.com/louchi1984-coder/voxeasy>
