# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化设计、模板化管理、样例引导和自动优化等能力，开发者可高效构建稳定、可控、可复用的提示词逻辑，显著提升模型输出质量与业务适配性。所有 Prompt 相关功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令到复杂工程化场景：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板，后者可基于 [ICIO、CRISPE、RASCEF 等 Prompt 工程框架](../../raw/application-user-guide/prompt/prompt-custom-template.md) 结构化构建，适用于文本生成与图片生成两类任务（后者需分别配置正向/负向 Prompt）[原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致性。> **注意**：该功能已停止维护，[官方明确建议迁移至 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，不再新增或更新样例库能力。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验即可获得更清晰、稳定的版本[原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入输出样例（query-answer pairs）进行多轮评估与迭代，生成带 few-shot 示例和边界说明的高精度 Prompt，尤其适用于分类、结构化输出等确定性任务[原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 通过控制台模板卡片或 `CreatePromptTemplate` 接口返回获取 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必须指定有效 workspace | 需提前通过 [获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `variables` | 模板中声明的变量名数组（如 `["platform", "topic"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口响应返回，不可在调用时动态增删 |
| `has_thoughts` | API 请求参数，设为 `true` 时可在响应 `thoughts` 字段中查看样例检索详情 | 仅适用于已关联样例库的智能体应用调用（见 [Prompt样例库优化文档](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |
| 召回片段数 | 单次请求注入上下文的样例数量，默认 5，上限 10 | 在智能体应用配置中调整，影响 [Token](../concepts/token.md) 成本与效果平衡 |

## 使用方式

### 控制台操作
- **模板创建**：进入「组件管理 > 提示词」，选择「创建提示词」，按类型（文本/图片生成）与输入模式（自定义 / 基于 [Prompt 工程](../concepts/prompt-engineering.md)）配置并保存。
- **样例库关联**：在智能体应用「配置」页启用「样例库」开关，选择已创建的样例库（最多 5 个），发布后生效。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」，结果可直接复制或「保存为模板」。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口（需 `workspaceId` + `promptTemplateId`），响应含 `content` 与 `variables`，填入变量后即可发送至模型。
- **反馈优化任务**：调用 `CreatePromptFeedbackOptimizationTask`（需推理模型、初始 Prompt、样例数据集、评测数据集），任务完成后获取优化版 Prompt。
- **应用调用**：若已关联样例库，设置 `has_thoughts=true` 可调试召回过程；模板类应用需先渲染 Prompt 再调用模型 API。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、优化）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；
  - 单个样例库最多 300 条样例，单次批量导入 Excel ≤ 20MB 且 ≤ 100 条；
  - 单个智能体应用最多关联 5 个样例库，单次召回最多 10 个样例片段。
- **数据安全**：Prompt 自动优化与反馈优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策[原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **过时功能警示**：Prompt 样例库功能已下线，新项目请勿依赖；存量应用应尽快按 [迁移指南](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 迁移至 RAG 表格库。
- **模型兼容性**：反馈优化推荐使用 `qwen-max` 作为推理模型；图片生成模板仅适配通义万相等图像模型，不适用于文本模型。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)




