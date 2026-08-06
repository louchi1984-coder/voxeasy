# 平台无关自学习循环

本机制只改进 VoxEasy 已有的 Shot 规划、确认、画面设计、Prompt 与 JSON 质量，不扩展其职责。候选观察与正式规则严格分离。

## 状态与命令

状态默认保存到 `~/.voxeasy/learning-state.json`。可用环境变量 `VOXEASY_LEARNING_STATE` 或全局参数 `--state <path>` 覆盖。脚本只依赖 Python 标准库，使用原子写入，不需要 hooks、数据库、后台进程或特定 Agent 平台。

每次运行先执行：

```text
python3 scripts/self_learning.py validate
python3 scripts/self_learning.py status
```

状态不存在时运行 `init`。状态包含：`usage_count`、`successful_uses_since_review`、`last_reviewed_at`、`observed_failures`、`user_corrections`、`candidate_improvements`、`applied_patches`、`rejected_learning_items`、`review_due` 和 `review_reasons`。

## 嵌入原流程的三个触发点

### 失败后立即复盘

真实使用或验证失败后、再次尝试前：

1. 运行 `record-failure --summary ... --evidence ...`。
2. 运行 `review` 查看当前证据。
3. 修复当前任务；单次偶然失败只保留为观察，不生成正式规则。
4. 只有重复出现且通过全部门槛时，才用 `propose-candidate` 建立候选。

用户输入本身无效、正常的确认等待或外部服务暂时排队，不自动视为 Skill 失败。

### 用户纠正立即记录候选

用户明确指出流程、画面、文字、风格、时间或 Prompt 错误时：

1. 先修正当前任务。
2. 运行 `record-correction`，写清 `trigger`、`action`、`boundary`、抽象证据和 `validation-plan`。
3. 该命令立即生成候选，但候选仍须通过门槛和验证，不能立刻成为正式规则。

### 每五次成功批量复盘

用户明确接受结果，或进入无关的新任务且没有对上一结果提出纠正时，运行 `record-success`。`successful_uses_since_review` 达到 5 后 `review_due` 变为真。在交付结束后运行 `review`；复盘完成后才运行 `review --complete` 重置成功计数。复盘可以得出“无需修改”。

## 学习门槛

候选只有全部满足才允许沉淀：

- 来自真实使用过程，而非假设。
- 能复用于新的 VoxEasy 请求，不是一次性上下文。
- `trigger` 清楚。
- `action` 可执行。
- `boundary` 明确说明何时不适用。
- 有测试、dry-run、validator、示例任务或人工检查的验证方案与通过证据。
- 不扩大 VoxEasy 的触发范围、输入输出或职责。

候选应保持原子化：一个触发条件对应一个行动规则。多项问题拆成多个候选。

## 禁止学习

- 临时目录、下载路径、机器名或只属于本次运行的环境细节。
- 账号、密钥、令牌、联系方式、私密原文或其他隐私信息。
- 单次偶然失败。
- 没有证据的审美偏好或用户未明确表达的偏好。
- 与 Vox 视频 Shot、风格、Prompt、时间轴或输出合同无关的经验。
- 只适用于当前用户环境的细节；私人定制 Skill 应在自己的状态中学习，不污染公共 VoxEasy。
- 增加明显复杂度但缺少可验证收益的抽象、框架或新文件。

状态只保存经过脱敏的简短摘要，不保存完整对话、原始 SRT、Prompt、URL 查询参数或生成素材。

## 应用补丁

1. 用 `review` 检查到期原因和候选。
2. 用相关测试或 dry-run 验证候选；未通过则运行 `reject`。
3. 修改前运行：

```text
python3 scripts/self_learning.py backup --skill-root <skill-root> --reason <reason> --file <relative-path> [--file <relative-path> ...]
```

4. 确认命令返回的 manifest 和每个 `.bak` 文件存在；不得覆盖既有备份。
5. 只修改候选直接要求的最少文件，不顺带重构。
6. 运行 Skill validator、原有回归用例和候选专属验证。
7. 全部通过后运行 `record-applied`，记录候选 ID、补丁摘要、文件、验证结果和 backup manifest。
8. 验证失败时从 manifest 恢复原文件，删除本次新建文件，并运行 `reject` 记录原因。

正式补丁不得自动改变：frontmatter 触发边界、两次确认、SRT 空白、`4/6/8/10` 时长、事实核验、文字白名单、风格隔离或 Google Flow Prompt/JSON 核心交付，除非用户明确要求修改对应边界。

## 无法持久化

状态目录不可写时不要尝试旁路写入。继续完成 VoxEasy 当前任务；仅在发生学习事件时，按 [`output-contract.md`](output-contract.md) 输出一个脱敏的 `Learning Observation`，供外部系统保存。没有学习事件时不输出。
