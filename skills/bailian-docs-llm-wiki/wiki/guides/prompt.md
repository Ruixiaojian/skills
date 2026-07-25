# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入，用于明确任务目标、设定角色、约束输出格式并注入领域知识。通过模板化、自动优化和样例增强等机制，开发者可系统性地提升模型输出的准确性、一致性与可控性，降低人工调优成本。所有 Prompt 相关功能当前仅支持华北2（北京）地域。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，适用于不同开发阶段和精度要求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），实现结构与变量分离，便于复用与协作。模板类型详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入与指令增强，适用于快速提升模糊 Prompt 的清晰度与稳定性。该功能不计费，且用户数据不会被用于模型训练，详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（few-shot）和评测数据集，通过多轮评估与反思生成更贴合业务场景的 Prompt，尤其适合分类、格式化生成等高精度任务。推荐使用千问-max 作为推理模型，详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：Prompt 样例库功能已停止维护，官方明确建议迁移至 RAG 表格库。请勿在新项目中使用该功能，相关操作指南见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间唯一标识，调用 Prompt 相关 API（如 `GetPromptTemplate`）必需 | 需通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `promptTemplateId` | 模板唯一 ID，用于拉取模板内容或在智能体应用中引用 | 在控制台模板卡片上直接复制；预置模板 ID 不可修改，自定义模板 ID 可重命名但不可变更 |
| `variables` | 模板中声明的占位符列表（如 `["platform", "topic"]`），用于运行时填充 | 变量名需为合法字符串，不支持嵌套语法（如 `${user.profile.name}`） |
| `has_thoughts` | API 调用参数，设为 `true` 时返回样例检索详情（仅限已弃用的样例库功能） | 已不推荐使用；RAG 场景应使用 `retrieval_config` 替代 |

## 使用方式

### 控制台操作
- **创建模板**：进入「应用开发 > 组件管理 > 提示词」，选择「创建提示词」，按需选用「自定义创建」或「基于Prompt工程创建」（支持 ICIO/CRISPE/RASCEF 框架）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **优化 Prompt**：在「提示词」页面右上角点击「自动优化」，粘贴原始 Prompt 后执行优化，结果可直接复制或「保存为模板」。
- **关联样例（已弃用）**：在智能体应用配置中开启「样例库」开关并绑定——此路径不再适用，请改用 RAG 表格库。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content` 和 `variables` 字段。
- **创建应用**：在智能体应用配置中，将模板内容（含 `${var}` 占位符）填入系统提示词字段；运行时通过 SDK 或 API 请求体注入实际变量值。
- **反馈优化**：调用 `/prompt/feedback-optimize` 接口（或使用控制台「反馈优化」页），需上传初始 Prompt、样例数据（5–10 条）及评测数据（≥20 条）。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）均仅支持华北2（北京）地域，跨地域调用将失败。
- **[Token](../concepts/token.md) 限制**：单个 Prompt 模板内容最大支持 6144 字符；反馈优化中样例与评测数据总 [Token](../concepts/token.md) 数过高可能导致优化失败。
- **模板变量安全**：变量填充时需确保输入值已做 XSS/注入过滤，平台不自动转义 `${var}` 中的内容。
- **图片生成模板**：仅支持「图片生成」类型模板，需分别定义正向 Prompt（期望内容）与负向 Prompt（排除内容），不支持变量插值。
- **弃用功能提醒**：Prompt 样例库已下线，其关联的 `has_thoughts` 参数、多路召回策略及 Excel 导入流程均失效；迁移方案参见官方文档 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


