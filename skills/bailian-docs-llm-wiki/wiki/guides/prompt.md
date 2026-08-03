# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，支持通过模板化、样例增强、自动优化等多种机制实现结构化设计与工程化管理。开发者可基于业务场景选择预置模板快速启动，或通过自定义模板、反馈优化、样例库等能力构建高精度、强一致性的提示词体系。所有 Prompt 相关操作均需在华北2（北京）地域下使用。

## 支持的模型/功能

- **模板类型**：支持两类 Prompt 模板——[预置Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)（由阿里云提供，覆盖营销、办公等通用场景）和[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)（支持文本生成与图片生成双模态，含 ICIO/CRISPE/RASCEF 等 Prompt 工程框架）。
- **增强机制**：
  - **Prompt 样例库**：通过少样本问答对引导模型输出风格与结构一致性（如术语解释类任务），但该功能[已不再维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方推荐迁移至 RAG 表格库。
  - **Prompt 反馈优化**：基于用户提供的输入-输出样例（5–10 条）与评测数据（≥20 条）进行多轮自动化评估与重构，显著提升特定任务准确率。
  - **Prompt 自动优化**：对原始 Prompt 进行结构重组、角色注入、指令增强与边界约束，适用于通用质量提升场景。
- **模型适配**：所有 Prompt 功能均兼容百炼支持的主流模型（如通义千问系列），其中 Prompt 反馈优化明确推荐使用 `qwen-max` 作为推理模型。

> **注意**：文档 3 明确声明“Prompt样例库功能已不再维护”，而文档 1 和文档 2 中仍存在对其调用流程的详细描述。开发者应以文档 3 的迁移指引为准，避免在新项目中依赖该已弃用功能。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，调用 `GetPromptTemplate` 等 API 必填 | [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `promptTemplateId` | 模板唯一 ID，用于拉取模板内容及变量定义 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中“API 使用”章节 |
| `variables` | 模板中声明的动态占位符列表（如 `["platform", "topic"]`），需在填充时传入对应值 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 返回 Schema 示例 |
| `has_thoughts=true` | 调用智能体应用 API 时启用样例检索过程日志输出（仅限样例库功能，已弃用） | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 样例库关联应用中可配置的单次召回样例数量，默认 5，上限 10 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

- **控制台操作**：
  - 创建：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面，点击 **+ 创建提示词**，选择“文本生成”或“图片生成”，按向导完成配置。
  - 优化：在同页面右上角进入 **[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)**，粘贴原始 Prompt 后点击“优化”。
  - 关联应用：在智能体应用配置页开启“样例库”开关（不推荐新用）或直接引用模板 ID 填充系统提示词。
- **API 调用**：
  - 获取模板：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段。
  - 填充模板：将业务数据按 `variables` 键名映射为字符串，替换 `content` 中 `${variable}` 占位符。
  - 发送请求：将填充后的完整 Prompt 作为 `system` 或 `messages[0].content` 传入目标模型 API。
- **SDK 集成**：参考 [GetPromptTemplate SDK 示例](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getprompttemplate) 自动生成代码，确保正确设置 `accessKeyId` 和 `accessKeySecret`。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板容量**：
  - 单个 Prompt 模板内容最大支持 **6144 字符**（控制台编辑框右下角实时计数）。
  - 图片生成模板需分别填写正向/负向 Prompt，无单独字符限制，但总长度受模型上下文窗口约束。
- **样例库弃用**：[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 功能已停止维护，存量应用应尽快迁移至 RAG 表格库；新建项目禁止使用。
- **[Token](../concepts/token.md) 成本影响**：启用样例库或反馈优化会显著增加输入 [Token](../concepts/token.md)（样例内容 + 用户查询），直接影响调用费用，需在效果与成本间权衡。
- **数据安全**：Prompt 自动优化过程不存储用户输入，亦不用于模型训练，符合百炼数据隐私政策。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


