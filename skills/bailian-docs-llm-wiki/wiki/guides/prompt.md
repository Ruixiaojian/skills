# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，支持通过模板化、样例增强、自动优化等多种方式构建结构清晰、效果可控的提示词。开发者可基于业务场景选择预置模板快速启动，或通过自定义模板、样例库、反馈优化等能力实现精细化控制。所有 Prompt 相关功能均需在华北2（北京）地域使用。

## 支持的模型/功能

- **模板化支持**：提供[预置Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)与[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)两类，覆盖文本生成、图片生成等场景；其中预置模板开箱即用，自定义模板支持基于 ICIO/CRISPE/RASCEF 等 Prompt 工程框架创建。
- **样例增强**：曾提供 Prompt 样例库功能，用于通过少样本（few-shot）方式引导模型输出风格与格式一致性。> **注意**：该功能[已停止维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移至 RAG 表格库。
- **自动优化**：支持两种路径：
  - 基于单条原始 Prompt 的结构重写（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)）；
  - 基于输入输出样例的多轮评测反馈优化（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)），后者需提供至少 5 条样例（每类至少 1 条）和建议 ≥20 条的评测数据集，效果更贴近实际业务需求。

## 关键参数

| 参数 | 说明 | 取值/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `promptTemplateId` | 模板唯一标识符，用于拉取模板内容 | 在控制台模板卡片上直接复制；预置与自定义模板均适用 |
| `variables` | 模板中声明的动态变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，用于运行时填充 |
| `has_thoughts` | API 调用时启用样例检索调试信息的开关 | 仅适用于已配置样例库的智能体应用（但该功能已弃用） |
| 召回片段数 | 样例库关联应用时可配置的注入样例数量 | 默认 5，上限 10（见 [Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |

## 使用方式

- **控制台操作**：
  - 创建模板：进入「应用开发 > 组件管理 > 提示词」，点击「创建提示词」，选择「文本生成」或「图片生成」类型，并指定输入模式（自定义创建 / 基于 Prompt 工程创建）；
  - 使用模板：在预置或自定义模板卡片上点击「使用prompt > 创建应用」，模板内容将自动填充至智能体应用的提示词编辑框，变量以 `${var}` 形式呈现；
  - 自动优化：在「提示词」页面右上角进入「自动优化」，粘贴原始 Prompt 后点击「优化」，结果可复制或直接「保存为模板」；
  - 反馈优化：在「提示词 > 反馈优化」页面新建任务，依次配置推理模型、初始 Prompt、样例数据（5–10 条）、评测数据（≥20 条），启动优化流程。

- **API/SDK 调用**：
  - 获取模板：调用 `GetPromptTemplate` 接口（需传入 `workspaceId` 和 `promptTemplateId`），响应中包含 `content` 和 `variables` 字段；
  - 创建模板：使用 `CreatePromptTemplate` 接口（仅支持自定义模板）；
  - 应用调用：若启用样例库（已弃用），需设置 `has_thoughts=true` 查看 `thoughts` 字段；当前推荐方案是将样例数据预处理后作为 RAG 检索源集成到应用逻辑中。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板长度限制**：控制台提示词编辑框最大支持 **6144 字符**（含变量占位符），超长内容需精简或拆分逻辑。
- **样例库状态**：> **注意**：[Prompt样例库功能已正式下线](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，现有配置仍可运行但不再更新，新项目请使用 RAG 表格库替代。
- **安全与隐私**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。
- **计费影响**：启用样例库（历史功能）会显著增加输入 [Token](../concepts/token.md) 消耗；而 Prompt 自动优化本身**不计费**；反馈优化任务按实际调用的推理模型计费。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


