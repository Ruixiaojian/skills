# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它支持结构化模板、样例增强、自动优化等多种工程化手段，帮助开发者将业务逻辑与模型能力解耦，实现可复用、可迭代、可评估的提示词管理。所有功能均需在华北2（北京）地域使用。

## 支持的模型/功能

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），通过变量插值（如 `${topic}`）动态生成 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：基于少样本学习（Few-shot）注入用户提供的高质量问答对，引导模型输出风格与格式一致的结果；但该功能[已停止维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移到 RAG 表格库。
- **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色设定、指令增强等重构，提升清晰度与稳定性 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入输出样例（query-answer pairs）与评测数据集，通过多轮评估-反思-重写闭环，生成场景适配性更强的 Prompt，效果优于纯文本自动优化 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 明确声明“Prompt样例库功能已不再维护”，而文档 1 和 2 中仍存在相关操作描述（如“在智能体应用中使用样例库”）。实际开发中应以文档 3 的迁移指引为准，避免依赖已下线功能。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) 中 `GetPromptTemplate` 接口必需参数 |
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API 均需指定 | 文档 1 和 2 均强调需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `variables` | 模板中声明的变量列表（如 `["platform", "topic"]`），用于运行时填充 | 见文档 1 中 `GetPromptTemplate` 返回 Schema 示例 |
| `has_thoughts=true` | API 调用时启用样例检索调试模式，响应中返回 `thoughts` 字段 | 仅适用于已停用的样例库功能（文档 3），不建议新项目使用 |
| 召回片段数 | 样例库关联应用时可配置的注入样例数量，默认 5，上限 10 | 文档 3 明确限制，但因功能已弃用，该参数无实际意义 |

## 使用方式

### 控制台操作
- **模板创建**：进入「组件管理 > 提示词」页面，点击「创建提示词」，选择「文本生成」或「图片生成」类型；文本生成支持「自定义创建」或「基于Prompt工程创建」（ICIO/CRISPE/RASCEF 框架）[原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **样例库（已弃用）**：访问「组件管理 > 样例库」，手动输入或批量导入 Excel（≤100 条/次，≤20MB），再在智能体应用配置中开启并关联（最多 5 个库）——**请勿采用此路径**。
- **反馈优化**：在「提示词 > 反馈优化」页面新建任务，上传初始 Prompt、5–10 条样例（覆盖各分类）、≥20 条评测数据，选择推理模型（推荐 `qwen-max`）后启动优化。

### API/SDK 集成
- **模板调用**：调用 `GetPromptTemplate` 接口（`workspaceId` + `promptTemplateId`），解析返回 JSON 中的 `content` 并替换变量，再传入目标模型。
- **反馈优化结果**：优化完成后，可在控制台复制生成的 Prompt，或直接保存为模板后通过 `GetPromptTemplate` 复用。
- **自动优化**：无独立 API，仅控制台功能，优化结果可手动复制或“保存为模板”。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、自动优化、反馈优化）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板长度**：控制台编辑器右下角显示字符计数，最大支持 **6144 字符**（含变量占位符）。
- **样例库已停用**：文档 3 明确说明该功能“已不再维护”，且计费模型依赖 [Token](../concepts/token.md) 注入，易导致成本不可控；必须迁移至 RAG 表格库替代 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **反馈优化数据要求**：样例数据建议 5–10 条且覆盖全部类别；评测数据建议 ≥20 条，数据质量直接影响优化效果 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **安全与隐私**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


