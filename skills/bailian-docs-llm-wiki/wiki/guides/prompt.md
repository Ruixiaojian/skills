# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，支持通过模板化、样例增强、自动优化等多种方式构建结构清晰、效果可控的提示词。开发者可基于业务场景选择预置模板快速启动，或通过自定义模板、样例库、反馈优化等能力实现精细化控制，所有操作均需在华北2（北京）地域下使用 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 支持的模型/功能

- **模板类型**：分为[预置Prompt模板](../../raw/application-user-guide/prompt/prompt-template.md)（开箱即用，覆盖营销、办公、摘要等通用场景）和[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)（支持文本生成、图片生成两类，后者需分别配置正向/负向Prompt）。
- **样例增强**：`Prompt样例库`功能通过少样本学习注入高质量问答对，引导模型输出风格与结构一致性；但该功能**已停止维护**，官方明确建议迁移到 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **自动优化**：提供两种路径：
  - 基于单条原始 Prompt 的结构重写（角色设定、指令增强、安全边界注入）；
  - 基于输入-输出样例的反馈式优化（few-shot + 多轮评测反思），效果更贴近实际业务表现 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档3中 `Prompt样例库` 功能已废弃，而文档1和文档2仍将其作为可用功能描述，存在明显矛盾。请以文档3的停用声明为准，避免新项目依赖该能力。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspaceId` | 业务空间唯一标识，调用所有 Prompt 相关 API 的必需参数 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 等接口拉取内容 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的动态变量列表（如 `["platform", "topic"]`），用于运行时填充 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts=true` | 调用应用 API 时启用样例检索过程日志（仅限已停用的样例库功能） | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 样例库关联应用时可配置的召回样例数量（默认5，上限10） | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台
- **模板创建**：进入「组件管理 > 提示词」，选择「创建提示词」→ 指定类型（文本/图片生成）→ 选择输入模式（自定义创建 或 基于Prompt工程创建，后者支持 ICIO/CRISPE/RASCEF 等框架）→ 保存。
- **样例库（已停用）**：访问「组件管理 > 样例库」→ 创建并导入样例 → 在智能体应用配置中开启「样例库」开关并绑定 → 发布生效。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt → 单击「优化」→ 复制结果或「保存为模板」。

### API / SDK
- 必须先获取 `workspaceId`（参见[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)）。
- 核心接口：
  - `CreatePromptTemplate`：创建自定义模板；
  - `GetPromptTemplate`：获取模板内容及变量列表；
  - `OptimizePrompt`（非公开接口名，实际为控制台封装能力）：无直接 OpenAPI，需通过控制台或 SDK 封装调用。
- 所有 Prompt 相关接口均要求 `RegionId=cn-beijing`。

## 限制和注意事项

- **地域限制**：全部 Prompt 功能仅支持华北2（北京）地域，跨地域调用将失败 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **模板长度**：控制台编辑器最大支持 6144 字符；API 无显式长度限制，但受模型上下文窗口约束。
- **样例库限制（已停用）**：
  - 单库最多 300 条样例；
  - 单应用最多关联 5 个样例库；
  - 单次请求最多注入 10 条召回样例（增加 [Token](../concepts/token.md) 消耗）。
- **反馈优化数据要求**：
  - 样例数据集建议 5–10 条，覆盖全部类别；
  - 评测数据集建议 ≥20 条，越多效果越优 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **安全与隐私**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


