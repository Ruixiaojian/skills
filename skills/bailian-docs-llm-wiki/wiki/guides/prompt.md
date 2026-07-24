# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于明确任务目标、设定角色、约束输出格式及注入上下文。通过结构化设计（如模板、样例库、自动优化等机制），开发者可解耦逻辑与内容、实现跨场景复用、提升输出一致性与可控性，并降低 [Prompt 工程](../concepts/prompt-engineering.md)门槛。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同开发阶段和精度要求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成与图片生成场景。预置模板覆盖营销文案、摘要抽取、风格改写等通用场景；自定义模板支持基于 ICIO/CRISPE/RASCEF 等工程框架结构化构建，并可关联变量（如 `${topic}`）实现动态填充 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型遵循特定解释结构、术语边界或输出风格。该功能已**停止维护**，官方明确建议迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

- **Prompt 自动优化与反馈优化**：
  - *自动优化*：基于单条原始 Prompt，由大模型进行结构重组、角色注入与指令增强，不依赖用户数据，**免费使用** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
  - *反馈优化*：需用户提供至少 5–10 条样例（覆盖各类别）及 ≥20 条评测数据，系统在推理模型（推荐千问-max）上多轮评估并生成带 few-shot 示例的优化 Prompt，效果更贴合业务实际 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档2明确声明“Prompt样例库功能已不再维护”，而文档4和文档1中仍存在对其创建与配置的详细说明。开发者应以文档2的停用声明为准，避免在新项目中采用该能力。

## 关键参数

| 参数 | 说明 | 取值/限制 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，调用所有 Prompt API 的必需参数 | 需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `promptTemplateId` | 模板唯一ID，用于 `GetPromptTemplate` 等接口 | 在控制台模板卡片上直接复制 |
| `variables` | 模板中定义的占位符列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动修改 |
| `has_thoughts` | API 调用时启用样例检索调试的开关（仅限已停用的样例库） | `true` 时响应含 `thoughts` 字段，用于验证召回逻辑 |
| 召回片段数 | （样例库）单次请求注入上下文的样例数量 | 默认 5，最大 10，可在应用配置中调整 |

## 使用方式

### 控制台
- **模板管理**：在[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面创建、编辑、复制或删除自定义模板；在[提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt)查看和复用预置模板。
- **样例库（已停用）**：在[样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case)页面创建、导入及关联至智能体应用（最多 5 个/应用）。
- **优化入口**：在提示词管理页右上角进入[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)或[反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize)页面。

### API / SDK
- **模板获取**：调用 `GetPromptTemplate` 接口（需 `workspaceId` + `promptTemplateId`），返回含 `content` 与 `variables` 的结构化响应 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **模板创建**：调用 `CreatePromptTemplate` 接口，支持文本生成与图片生成两类模板，后者需分别传入 `positive_prompt` 与 `negative_prompt` 字段。
- **反馈优化任务**：通过 `CreatePromptFeedbackOptimizationTask` 提交初始 Prompt、样例数据与评测数据，异步生成优化结果。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，文档1与文档4均明确标注此限制。
- **模板容量**：单个模板 `content` 最大支持 6144 字符（控制台编辑框右下角实时计数）。
- **样例库限制（历史）**：单库最多 300 条样例；单应用最多关联 5 个库；单次召回最多 10 条样例——但该能力已停用，仅作兼容参考。
- **安全与隐私**：Prompt 自动优化过程不存储用户输入，**不会用于模型训练** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **成本影响**：启用样例库（虽已停用）或反馈优化会显著增加输入 [Token](../concepts/token.md) 消耗，费用随召回样例总长度线性增长；模板本身无额外费用。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


