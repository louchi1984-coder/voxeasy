# Vox Video Director Narrative Arc Architectures

所有架构都必须先插入独立的 Shot 01 标题镜头：只显示用户确认的完整标题，`voiceover_text` 为空，`title: true`，运镜为 `push_in`。叙事与旁白从 Shot 02 开始。

## 1. `pas` Arc (Pain - Agitate - Solve 痛点-激化-解决弧)
- Target: 产品发布、技术突破、效率工具展示 (如 Google Antigravity)
- Structure:
  - Shot 01 (Title): Dedicated title-only shot, no voiceover (`title: true`, `push_in`)
  - Shot 02 (Hook): Pain Point & Friction (`title: false`, `tracking_pan_down`)
  - Shot 03 (Agitate): Agitating the Complexity & Waste (`title: false`, `layer_dissection`)
  - Shot 04 (Breakthrough): Product Reveal & Paradigm Shift (`title: false`, `balance_tilt`)
  - Shot 05 (Solve): Core Subagents / Features Workflow (`title: false`, `parallax`)
  - Shot 06 (Outro): Final Value Proposition & Hero Lock (`title: false`, `static`)

## 2. `how_it_works` Arc (机制拆解弧)
- Target: 硬核科技科普、算法原理、武器/机械剖析
- Structure:
  - Shot 01 (Title): Dedicated title-only shot, no voiceover (`title: true`, `push_in`)
  - Shot 02 (Hook): Mystery / Exterior Reveal (`title: false`, `tracking_pan_down`)
  - Shot 03 (Anatomy): Internal Dissection & Layer Peeling (`title: false`, `layer_dissection`)
  - Shot 04 (Asymmetry): Material & Cost / Spec Comparison (`title: false`, `balance_tilt`)
  - Shot 05 (Workflow): Dynamic Process Linkage (`title: false`, `pan_right`)
  - Shot 06 (Impact): Final Synthesis & Takeaway (`title: false`, `static`)

## 3. `timeline` Arc (历史与地缘演进弧)
- Target: 重大事件解说、地缘政治 (如 伊朗威胁乌克兰)、历史发展
- Structure:
  - Shot 01 (Title): Dedicated title-only shot, no voiceover (`title: true`, `push_in`)
  - Shot 02 (Hook): Breaking News / Shocking Fact (`title: false`, `tracking_pan_down`)
  - Shot 03 (Origin): Historical Origin & Supply Chain (`title: false`, `layer_dissection`)
  - Shot 04 (Mechanism): Weaponry / Strategy Dissection (`title: false`, `balance_tilt`)
  - Shot 05 (Asymmetry): Economic & Military Balance (`title: false`, `pan_right`)
  - Shot 06 (Escalation): Escalation & Regional Spread (`title: false`, `parallax`)
  - Shot 07 (Dual-Front): Geopolitical Network (`title: false`, `pull_out`)
  - Shot 08 (Response): International Sanctions & Reaction (`title: false`, `tilt_down`)
  - Shot 09 (Outro): Future Warning & Hero Lock (`title: false`, `static`)

## 4. `man_in_hole` Arc (困境-突围弧)
- Target: 商业战局、品牌翻盘、危机突围
- Structure:
  - Shot 01 (Title): Dedicated title-only shot, no voiceover (`title: true`, `push_in`)
  - Shot 02 (Hook): The Crisis / Fall (`title: false`, `tracking_pan_down`)
  - Shot 03 (The Hole): Deepening Dilemma (`title: false`, `layer_dissection`)
  - Shot 04 (Pivot): The Pivot Decision / Discovery (`title: false`, `balance_tilt`)
  - Shot 05 (Climb): Rapid Execution & Rebound (`title: false`, `pan_right`)
  - Shot 06 (Outro): Triumph & Lessons (`title: false`, `static`)
