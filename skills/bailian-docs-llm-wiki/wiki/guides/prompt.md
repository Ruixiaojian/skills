# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为单次调用的直接输入，也可通过模板化、样例增强、自动优化等方式进行工程化管理，从而提升输出一致性、准确性与开发效率。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同精度与可控性需求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），通过变量插值（如 `${topic}`）实现结构复用与动态填充。预置模板效果稳定、开箱即用；自定义模板支持基于 ICIO、CRISPE、RASCEF 等 [Prompt 工程](../concepts/prompt-engineering.md)框架构建，适用于复杂任务 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
  
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型遵循特定解释结构、术语风格或格式规范。该功能已**停止维护**，官方明确建议迁移至 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验即可获得更清晰、稳定的版本 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

> **注意**：文档 3 中的 Prompt 样例库功能已废弃，其能力由 RAG 表格库承接；而文档 5 的“基于样例的 Prompt 反馈优化”为独立功能，仍有效且推荐用于高精度场景（如汽车文章分类），其依赖评测数据集驱动多轮自动化评估与迭代 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填，从控制台模板卡片或 API 响应中获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，参见[获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `variables` | 模板中声明的变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，用于校验填充完整性 |
| `has_thoughts` | API 调用时启用样例检索调试日志（仅限旧样例库） | 仅在样例库关联应用的 API 请求中生效，现已不推荐使用 |
| `recall_k` | 应用配置中可设的召回片段数（默认 5，上限 10） | 仅影响已弃用的样例库功能 |

## 使用方式

### 控制台操作
- **模板创建**：进入「组件管理 > 提示词」，选择「创建提示词」→ 指定类型（文本/图片生成）→ 选择模式（自定义创建 / 基于 [Prompt 工程](../concepts/prompt-engineering.md)创建）→ 输入内容 → 保存。
- **样例库（已弃用）**：进入「组件管理 > 样例库」→ 创建库 → 手动输入或批量导入 Excel（≤100 条/次，≤20MB）→ 在智能体应用配置中开启并关联。
- **自动优化**：进入「组件管理 > 提示词 > 自动优化」→ 粘贴原始 Prompt → 单击「优化」→ 复制结果或「保存为模板」。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口（`workspaceId` + `promptTemplateId`），响应含 `content` 与 `variables` 字段，供客户端变量替换 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **反馈优化**：调用 `/prompt/feedback-optimize`（需上传样例数据集与评测数据集），系统返回优化后 Prompt 文本，支持直接保存为模板或创建应用。

### SDK 集成
- 使用 V2.0 SDK（推荐），按 OpenAPI 文档生成代码，自动注入 `workspaceId` 和 `promptTemplateId`；访问令牌（AccessKey）需提前配置 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能仅支持华北2（北京）地域，跨地域调用将失败。
- **模板长度**：控制台编辑框最大支持 6144 字符；API 无显式长度限制，但受模型最大上下文窗口约束。
- **样例库容量**：单个样例库最多 300 条样例；单个智能体应用最多关联 5 个样例库（该功能已停用，仅作历史兼容参考）。
- **数据安全**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **计费影响**：启用样例库或反馈优化会显著增加输入 [Token](../concepts/token.md) 消耗（含样例文本），直接影响调用费用；模板本身不额外计费。
- **模型适配**：Prompt 反馈优化功能推荐使用 `qwen-max` 作为推理模型，以获得最佳优化效果 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


