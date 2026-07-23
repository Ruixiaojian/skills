# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为单次调用的直接输入，也可通过模板化、样例增强、自动优化等方式进行工程化管理，从而提升输出质量、一致性与可维护性。所有 Prompt 相关能力均需在华北2（北京）地域下使用。

## 支持的模型/功能

百炼平台提供多种 [Prompt 工程](../concepts/prompt-engineering.md)能力，覆盖从基础指令构造到闭环反馈优化的全链路：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），实现结构与变量分离，便于复用与集中管理。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致的结果。该功能已停止维护，**强烈建议迁移至 RAG 表格库**，参见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的迁移说明。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验即可获得更清晰、稳定的版本。该功能免费且不存储用户数据 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（query-answer pairs）和评测数据集，通过多轮自动化评估与反思生成高适配性的 Prompt，尤其适用于分类、结构化生成等任务。推荐使用 `qwen-max` 作为推理模型。

> **注意**：文档2明确指出“Prompt样例库功能已不再维护”，而文档1和文档3仍将其列为可用功能。开发者应以文档2为准，避免新建依赖该功能的生产流程。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填，需与 `workspaceId` 配对使用 |
| `workspaceId` | 业务空间 ID，是所有 Prompt 资源的归属容器 | 必填，获取方式见 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `variables` | 模板中声明的动态变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 |
| `has_thoughts` | API 调用时启用样例检索调试信息的开关 | 仅在调用智能体应用 API 时有效，设为 `true` 可在响应 `thoughts` 字段中查看召回详情 |
| 召回片段数 | 单次请求从样例库中注入上下文的样例数量 | 默认 5，最大 10，可在智能体应用配置中调整 |

## 使用方式

### 控制台操作
- **模板创建与管理**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持自定义创建、基于 [Prompt 工程](../concepts/prompt-engineering.md)框架（ICIO/CRISPE/RASCEF）构建，或复制预置模板快速迭代。
- **图片生成模板**：选择“图片生成”类型，分别填写正向 Prompt（期望内容）与负向 Prompt（需排除元素）。
- **自动优化**：在 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt，点击“优化”后可直接复制或“保存为模板”。
- **反馈优化**：在 [提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面上传样例数据（建议 5–10 条，覆盖全部类别）与评测数据（建议 ≥20 条），启动多轮优化任务。

### API 与 SDK
- **获取模板**：调用 `GetPromptTemplate` 接口（[文档](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getprompttemplate)），传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 后填充变量生成最终 Prompt。
- **调用智能体应用**：若已关联样例库，需在请求体中设置 `"has_thoughts": true` 以启用样例检索调试；若使用反馈优化生成的 Prompt，可直接作为 `system_prompt` 或 `user_input` 提交。
- **创建模板**：通过 `CreatePromptTemplate` 接口（[文档](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createprompttemplate)）提交模板名称、类型（`text_generation` / `image_generation`）、内容等字段。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、自动优化、反馈优化）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符；
  - 单个样例库最多 300 条样例（但该功能已停用）；
  - 反馈优化任务中，样例数据建议 5–10 条，评测数据建议 ≥20 条。
- **Token 成本**：启用样例库或反馈优化会显著增加输入 Token 消耗（样例内容 + 用户查询 + 系统指令），需在成本与效果间权衡。
- **安全与隐私**：Prompt 自动优化过程不存储用户输入，亦不用于模型训练；但反馈优化任务中上传的样例与评测数据将用于本次优化计算，建议脱敏处理敏感信息。
- **模型兼容性**：图片生成模板仅适配通义万相等图像模型；文本生成模板与反馈优化推荐使用 `qwen-max` 或 `qwen-plus-latest` 等长上下文模型以保障样例注入效果。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


