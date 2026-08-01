# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入，其质量直接影响输出的准确性、一致性与可控性。平台提供模板化管理、自动优化、样例增强等多种能力，支持开发者在文本生成、图片生成、结构化输出等场景下高效构建和迭代高质量提示词。所有功能当前仅适用于华北2（北京）地域。

## 支持的模型/功能

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板两类，覆盖文本生成与图片生成两大类型。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持通过控制台或 API 创建，可基于 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中描述的流程进行全生命周期管理。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致的结果。但需注意：> **注意**：该功能[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 已明确声明“不再维护”，官方推荐迁移至 RAG 表格库。
- **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，提升效果稳定性。该功能不计费，且用户数据不会用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入输出样例（query-answer pairs）与评测数据集，通过多轮自动化评估与反思生成更贴合业务场景的 Prompt。相比基础自动优化，其效果更贴近实际任务需求 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间 ID，调用模板类 API（如 `GetPromptTemplate`）必需 | 需通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于拉取模板内容或填充应用 | 在控制台模板卡片上直接复制 |
| `variables` | 模板中定义的占位符列表（如 `["topic", "platform"]`），用于运行时填充 | 由模板创建时自动解析，不可手动修改 |
| `has_thoughts=true` | API 调用参数，启用后响应中返回 `thoughts` 字段，含样例检索详情（仅限已弃用的样例库功能） | 仅适用于旧版样例库关联的应用 |
| 召回片段数 | 样例库关联应用时可配置的参数，默认 5，最大 10 | 控制注入上下文的样例数量，影响 Token 消耗与效果 |

## 使用方式

- **控制台操作**：
  - 模板：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持创建、编辑、复制、删除及“创建应用”一键填充。
  - 自动优化：在提示词管理页右上角进入 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面，粘贴原始 Prompt 后点击优化，结果可复制或直接保存为模板。
  - 反馈优化：在提示词管理页选择 **反馈优化** > **新增优化任务**，依次配置推理模型、初始 Prompt、样例数据（5–10 条）、评测数据（≥20 条）后启动。
- **API 调用**：
  - 模板获取：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content` 与 `variables` 字段，供程序动态渲染。
  - 模板创建：使用 `CreatePromptTemplate` 接口，支持 JSON 格式提交模板名称、内容、类型（`text-generation` 或 `image-generation`）等。
- **SDK 集成**：各语言 SDK 示例（V2.0 推荐）可在 OpenAPI 调试页直接生成，自动注入 `workspaceId` 和 `promptTemplateId`，仅需补充 AccessKey 配置即可运行。

## 限制和注意事项

- **地域限制**：所有 Prompt 相关功能（模板、优化、样例库）当前仅支持华北2（北京）地域，跨地域调用将失败。
- **容量与配额**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；
  - 单个样例库最多 300 条样例（已弃用）；
  - 单个智能体应用最多关联 5 个样例库（已弃用）；
  - 反馈优化的样例数据建议 5–10 条，评测数据建议 ≥20 条，数据越丰富优化效果越优。
- **兼容性与演进**：
  > **注意**：文档间存在明确过时信息——[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确声明该功能“已不再维护”，而 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 仍将其列为可用功能之一。开发者应以弃用声明为准，避免新项目依赖。
- **Token 成本**：启用样例库（已弃用）或反馈优化会显著增加输入 Token（含样例/评测数据），需在成本与效果间权衡；自动优化本身不产生额外调用费用，但生成的 Prompt 若导致模型输出变长，可能间接增加下游调用成本。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


