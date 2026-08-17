# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体。通过结构化设计、模板化管理、样例引导和自动优化等能力，开发者可系统性提升模型输出的准确性、一致性与可控性。本文档面向开发者，聚焦 Prompt 的工程化实践，涵盖支持能力、关键参数、使用方式及约束边界。

## 支持的模型/功能

百炼平台提供多层次 [Prompt 工程](../concepts/prompt-engineering.md)能力，覆盖从基础指令到复杂任务编排的全链路需求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），适用于华北2（北京）地域。模板支持变量插值（如 `${topic}`）、结构化框架（ICIO/CRISPE/RASCEF）及正负向提示词分离（图片生成场景）。详情见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致。但需注意：> **注意**：该功能[已停止维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移到 RAG 表格库，不再新增功能支持。

- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与边界注入，无需人工标注数据。不计费，且输入数据不会用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

- **Prompt 反馈优化**：结合用户提供的输入输出样例（5–10 条典型样例 + ≥20 条评测数据），在推理模型（推荐千问-max）上多轮评估、反思并生成带 few-shot 示例的优化 Prompt。该能力更贴合业务实际效果，优于通用自动优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取；仅华北2（北京）有效 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 在控制台模板卡片或 API 响应中获取；预置与自定义模板均适用 |
| `variables` | 模板中声明的变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，用于运行时填充 |
| `has_thoughts=true` | 应用 API 调用参数，启用后响应含 `thoughts` 字段，展示样例检索过程 | 仅适用于已关联样例库的智能体应用（Agent 1.0）；但因样例库已停用，此参数实际价值下降 |
| 召回片段数 | 样例库关联配置项，控制注入上下文的样例数量 | 默认 5，上限 10；直接影响 [Token](../concepts/token.md) 消耗与响应延迟 |

> **注意**：文档 3 中关于样例库“每个库最多 300 条样例”“单应用最多关联 5 个库”等限制虽技术上仍存在，但因功能已停用，**不应作为当前架构设计依据**。

## 使用方式

### 控制台流程
1. **创建**：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面，选择“创建提示词”，按需选用“自定义创建”或“基于Prompt工程创建”（文本生成），或分别填写正/负向 Prompt（图片生成）。
2. **管理**：模板卡片支持编辑、复制 prompt、调用 API 示例查看、复制模板（生成副本）及删除（仅自定义模板）。
3. **使用**：在智能体应用配置中，点击“使用prompt > 创建应用”，模板内容自动填充至提示词框；变量（如 `${name}`）可见，右下角显示字符计数（最大 6144 字符）。

### API/SDK 流程
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables`。
- **生成 Prompt**：将业务数据代入 `content` 中的变量（如 `content.replace("${topic}", "AI芯片")`）。
- **调用模型**：将生成的完整 Prompt 作为 `system` 或 `user` 消息发送至目标模型 API（如 `ChatCompletion`）。
- SDK 示例可直接在 OpenAPI 调试页生成（V2.0 推荐），需配置 `accessKeyId`/`accessKeySecret`。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（创建、获取、使用）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **字符限制**：控制台提示词编辑框最大支持 **6144 字符**；超出需精简或拆分逻辑。
- **模板修改权**：预置 Prompt 模板**不可修改**，仅可通过“复制模板”生成自定义副本后编辑。
- **安全与隐私**：Prompt 自动优化功能**不存储、不训练、不共享**用户输入数据，符合阿里云数据隐私政策。
- **功能演进**：Prompt 样例库已归档，新项目应避免依赖；RAG 表格库是其替代方案，具备更强的语义检索与知识融合能力。
- **[Token](../concepts/token.md) 成本**：启用样例库（历史项目）或反馈优化（含大量 few-shot）会显著增加输入 [Token](../concepts/token.md)，需在效果与成本间权衡。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


