# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。它分为官方预置 Skill 和用户自定义 ZIP 技能包两类，通过语义描述驱动调用，适用于对话式应用中的自动化工作流。详细背景请参见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv`、`.pdf` 解析与生成），开箱即用，无需配置；版本更新后已添加的应用将自动生效。
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业定制需求（如专有格式解析、业务规则校验等）；其行为完全由 `SKILL.md` 中的 `description` 字段定义，智能体据此判断是否触发调用。具体规范详见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：当前所有 Skill 均不依赖特定大模型底座，而是作为独立于 LLM 推理链之外的工具调度单元；但 Skill 的触发准确性高度依赖 LLM 对 `description` 的语义理解能力，因此 description 编写质量直接影响可用性——该关键约束在 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md) 中被反复强调。

## 关键参数

自定义 Skill 的核心元信息全部定义在 ZIP 包根目录下的 `SKILL.md` 文件中，采用 YAML 格式，仅含两个必填字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需全小写+连字符（如 `invoice-parser`），且在同一账号下不可重复。 |
| `description` | 是 | 决定 Skill 是否被调用的关键字段，必须明确包含：<br>• 输入类型（如 `.xlsx`, JSON 数据）<br>• 支持操作（如“清洗缺失值”“生成图表”）<br>• 触发关键词（如“导出为表格”“整理成 Excel”）<br>• **不适用场景**（如“不处理 Word 文档”“不输出 HTML”） |

该结构要求和示例完整定义见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加；  
   - 自定义 Skill：打包含合规 `SKILL.md` 的 ZIP（≤10 MB），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 `+` 号选取 Skill。

3. **测试验证**  
   在应用配置页右侧对话窗格中输入典型触发语句（如“把这份 CSV 按销售额排序并生成柱状图”），观察是否自动调用对应 Skill 并返回预期结果。

## 限制和注意事项

- ZIP 包大小上限为 **10 MB**，超限将导致上传失败；
- `name` 字段在账号维度全局唯一，重名上传会拒绝而非覆盖；
- 自定义 Skill 审查耗时约 2 分钟，失败时需根据提示修改 `SKILL.md` 后重传；
- 官方 Skill 版本更新全自动同步，但自定义 Skill **必须重新上传 ZIP 才能更新**，旧版本不会被自动停用；
- `description` 中若未明确排除不适用场景（如“不处理图片”），可能导致误触发——这是实际调试中最常见的问题，务必严格遵循 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写建议。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


