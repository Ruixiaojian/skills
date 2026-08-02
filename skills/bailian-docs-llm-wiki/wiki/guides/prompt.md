# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化设计、模板化管理、样例引导与自动优化等能力，开发者可系统性提升模型输出的准确性、一致性与可控性。本文档面向开发者，聚焦 Prompt 的工程化实践，涵盖模板管理、样例库、自动优化及反馈优化等核心能力，并明确其适用范围与约束条件。

## 支持的模型/功能

百炼平台提供四类 Prompt 相关能力，均基于通义系列大模型（如 `qwen-max`、`qwen-plus` 等）实现，**当前仅支持华北2（北京）地域**（见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 和 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)）：

- **Prompt 模板**：支持预置与自定义两类模板，用于分离固定结构与动态变量。预置模板覆盖营销文案、摘要抽取、风格改写等通用场景；自定义模板支持文本生成（含 ICIO/CRISPE/RASCEF 等工程框架）和图片生成（正向/负向 Prompt 分离）。
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型输出风格与结构一致的结果。适用于智能客服、术语解释、格式化生成等需强参考约束的场景。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验即可获得更清晰、稳定的版本。
- **Prompt 反馈优化**：基于用户提供的输入输出样例（query-answer pairs），在推理模型上多轮评估、反思并迭代生成 Prompt，效果优于纯文本优化，尤其适合垂直领域任务（如汽车文章分类）。

> **注意**：[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确声明该功能“已不再维护”，推荐迁移至 RAG 表格库。但文档中描述的样例库创建、关联应用、多路召回等操作流程仍可在控制台访问，属历史功能残留。实际生产环境应优先采用 RAG 方案替代。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需。通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取。 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等 API 调用。预置模板 ID 在控制台卡片中可见；自定义模板 ID 创建后生成。 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts: true` | API 调用时启用样例检索调试模式，响应中返回 `thoughts` 字段包含召回详情。 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 单次请求注入上下文的样例数量，默认 5，上限 10。可在智能体应用配置中调整。 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 样例库容量 | 每个样例库最多 300 条样例；每个智能体应用最多关联 5 个样例库。 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作
- **模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持创建、编辑、复制、删除自定义模板；预置模板可通过 [提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt) 浏览与“复制模板”转为自定义。
- **样例库**：访问 [样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case)，支持手动输入或 Excel 批量导入（≤20MB，单次≤100条），再在智能体应用配置中开启并关联。
- **自动优化**：在 [提示词 > 自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt，点击“优化”后可复制或“保存为模板”。
- **反馈优化**：在 [提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) 页面上传初始 Prompt、样例数据（5–10 条）与评测数据（≥20 条），启动多轮优化任务。

### API/SDK 调用
- **模板管理**：使用 `CreatePromptTemplate`、`GetPromptTemplate`、`DeletePromptTemplate` 等接口，需传入 `workspaceId` 和 `promptTemplateId`（参见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中的 SDK 示例）。
- **样例库集成**：在调用智能体应用 API 时，设置 `has_thoughts=true` 即可触发样例检索（见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)）。
- **反馈优化**：通过 `CreateFeedbackOptimizationTask` 等专属接口提交任务，需指定推理模型（推荐 `qwen-max`）、样例集与评测集（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)）。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）**仅限华北2（北京）地域**，跨地域调用将失败（见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 和 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 开头“重要”提示）。
- **Token 限制**：模板内容最大支持 6144 字符；样例库单次召回最多 10 条，总 Token 消耗随样例长度线性增长，直接影响计费（见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 计费说明）。
- **数据安全**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 常见问题）。
- **功能演进**：Prompt 样例库功能已标记为“不再维护”，新项目应避免依赖；RAG 表格库是其官方推荐替代方案（见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 说明）。
- **模型选择**：反馈优化任务中，**推理模型必须选择 `qwen-max`**（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 说明），其他模型不支持该流程。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


