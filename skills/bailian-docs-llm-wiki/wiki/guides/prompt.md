# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化设计、模板化管理、样例引导和自动优化等能力，开发者可高效构建稳定、可控、可复用的[提示工程](../concepts/prompt-engineering.md)体系，显著提升模型输出质量与业务适配性。所有 Prompt 相关功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令到复杂任务编排的全链路需求：

- **Prompt 模板**：支持预置模板（开箱即用，适用于通用场景如文案生成、摘要抽取）和自定义模板（支持文本生成与图片生成两类），后者可基于 [ICIO、CRISPE、RASCEF 等 Prompt 工程框架](../../raw/application-user-guide/prompt/prompt-custom-template.md) 结构化构建，确保指令清晰、上下文完备、输出可控。  
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型遵循特定解释风格或格式规范。但需注意：> **注意**：[文档 3](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确指出该功能“已不再维护”，推荐迁移至 RAG 表格库，不可用于新项目开发。  
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，适用于快速提升模糊 Prompt 的稳定性与效果。  
- **Prompt 反馈优化**：基于用户提供的输入输出样例（query-answer pairs）进行多轮评估与迭代优化，尤其适合高精度分类、格式强约束等垂直场景，效果优于纯文本自动优化。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作（创建、获取、调用）均需指定。获取方式见 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。 | [文档 1](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一 ID，用于 API 获取模板内容或在应用中引用。预置与自定义模板均支持。 | [文档 1](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的动态变量列表（如 `["platform", "topic"]`），调用时需传入对应值完成填充。 | [文档 1](../../raw/application-user-guide/prompt/prompt-template.md) 中 API 响应示例 |
| `has_thoughts=true` | 调用智能体应用 API 时启用样例库检索调试模式，响应中返回 `thoughts` 字段含详细召回信息。 | [文档 3](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 样例库关联应用时可配置的单次召回样例数量，默认 5，上限 10。影响 [Token](../concepts/token.md) 消耗与效果平衡。 | [文档 3](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作
- **模板管理**：进入「应用开发 > 组件管理 > 提示词」，可创建/编辑/复制/删除模板；预置模板支持「复制模板」生成可编辑副本。  
- **样例库管理**：访问「样例库」页面，支持手动输入或 Excel 批量导入（≤100 条/次，文件 ≤20MB），每个库最多 300 条样例。  
- **反馈优化**：在「提示词 > 反馈优化」页面新建任务，上传初始 Prompt、样例数据（建议 5–10 条，覆盖全部类别）及评测数据（建议 ≥20 条）。  

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，返回含 `content` 与 `variables` 的完整模板结构。  
- **创建应用**：将模板内容填入智能体应用的系统提示词字段，变量占位符（如 `${topic}`）将在运行时由业务逻辑注入。  
- **启用样例库**：在应用配置中开启「样例库」开关并绑定库，发布后生效；API 调用时需设置 `has_thoughts=true` 查看检索过程。  

### SDK 集成
- 使用 OpenAPI SDK V2.0（推荐），各语言示例自动填充 `workspaceId` 和 `promptTemplateId`，仅需配置 `accessKeyId`/`accessKeySecret` 即可运行。详情参见 [文档 1](../../raw/application-user-guide/prompt/prompt-template.md) 中的 SDK 示例章节。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）**仅支持华北2（北京）地域**，跨地域调用将失败。  
- **容量限制**：  
  - 单个 Prompt 模板最大长度为 **6144 字符**（控制台编辑框右下角实时计数）；  
  - 单个样例库最多 **300 条样例**，单个智能体应用最多关联 **5 个样例库**，单次请求最多召回 **10 个样例片段**；  
  - 批量导入样例时，Excel 文件大小 ≤20MB，单次条数 ≤100。  
- **功能弃用**：> **注意**：[文档 3](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确声明 Prompt 样例库功能已停止维护，新项目请使用 RAG 表格库替代。  
- **数据安全**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。  
- **模型依赖**：Prompt 反馈优化效果高度依赖推理模型选择，官方推荐使用 `qwen-max`；样例与评测数据质量直接影响优化结果，需确保覆盖典型场景且标注准确。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


