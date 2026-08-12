# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心控制机制。它既可作为静态指令直接调用，也可通过模板化、样例增强、自动优化等方式实现结构化、可复用、可迭代的工程化管理。合理设计和使用 Prompt，是保障模型输出质量、一致性与业务适配性的关键实践。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力，覆盖从基础调用到高级工程优化的全链路：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成（如文案创作、摘要抽取、代码生成）和图片生成（需分别配置正向/负向 Prompt）场景。模板支持变量插值（如 `${topic}`），便于动态注入业务数据 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 样例库**：基于少样本学习（Few-shot）原理，在推理时动态检索并注入高质量输入-输出对，显著提升领域任务准确性与风格一致性。该功能已**停止维护**，官方明确建议迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：提供两种优化路径：
  - 基于单条原始 Prompt 的重写（结构重组、角色设定、指令增强等）；
  - 基于用户提供的输入-输出样例（feedback data）进行多轮评估与迭代优化，效果更贴合实际业务场景 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 2 明确声明“Prompt样例库功能已不再维护”，而文档 3 和文档 1 中仍将其列为可用功能并描述操作流程。开发者应以文档 2 的停用声明为准，避免在新项目中依赖该能力。

## 关键参数

| 参数 | 说明 | 取值/约束 | 来源依据 |
|------|------|-----------|----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 字符串，由平台生成 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中定义的占位符列表（如 `["platform", "topic"]`） | JSON 数组 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` (API) | 控制是否返回样例检索过程详情（仅限已停用的样例库功能） | `true` / `false` | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 样例库关联应用时可配置的注入样例数量 | 默认 5，上限 10 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 评测数据量（反馈优化） | 影响优化质量的关键输入 | 建议 ≥20 条，覆盖全部类别 | [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) |

## 使用方式

### 控制台操作
- **创建模板**：进入「组件管理 > 提示词」，选择「文本生成」或「图片生成」类型，按需选用「自定义创建」或「基于Prompt工程创建」（支持 ICIO/CRISPE/RASCEF 等框架）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」后可复制或「保存为模板」[Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **反馈优化**：在「提示词 > 反馈优化」页面上传初始 Prompt、样例数据（5–10 条）及评测数据（≥20 条），启动多轮自动化优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

### API/SDK 调用
- 通过 `GetPromptTemplate` 接口获取模板内容（含 `variables` 和 `content`），填充变量后构造最终 Prompt 发送给目标模型。
- 模板 ID 与业务空间 ID（`workspaceId`）为必传参数，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 的 API 调用示例。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）当前**仅支持华北2（北京）地域** [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)、[Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **容量与规模**：
  - 单个 Prompt 模板内容最大支持 **6144 字符**（控制台编辑器限制）；
  - 单个样例库最多容纳 **300 条样例**（但该功能已停用）；
  - 反馈优化任务中，样例数据建议 **5–10 条**，评测数据建议 **≥20 条**。
- **安全与隐私**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **计费影响**：
  - Prompt 模板本身不额外计费；
  - 启用样例库（已停用）或反馈优化会增加输入 [Token](../concepts/token.md) 消耗，直接影响模型调用费用；
  - 优化过程本身（如调用 `OptimizePrompt` 接口）**不计费** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


