# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为单次调用的直接输入，也可通过模板化、样例库、自动优化等机制进行结构化管理和持续迭代。合理设计 Prompt 是提升模型输出准确性、一致性与可控性的关键工程实践，尤其在面向业务场景的智能体应用开发中具有基础性作用。

## 支持的模型/功能

百炼平台支持多种 Prompt 相关能力，覆盖从基础指令输入到高级工程化管理的全链路：

- **Prompt 模板**：提供预置模板（如营销文案生成、摘要抽取）和自定义模板两类，支持变量插值（如 `${topic}`）、多类型（文本生成/图片生成）及结构化框架（ICIO/CRISPE/RASCEF）[原文标题](../../raw/application-user-guide/prompt/prompt-template.md)；
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致；但需注意，该功能[已不再维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移到 RAG 表格库；
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强等重写，不计费且不用于模型训练 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)；
- **Prompt 反馈优化**：结合用户提供的输入输出样例（query-answer pairs）与评测数据集，在推理模型（推荐千问-max）上进行多轮评估与迭代，生成更贴合实际业务效果的 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 明确指出 Prompt 样例库功能已下线，而文档 1 和 2 中仍存在相关操作描述，开发者应以文档 3 的迁移指引为准，避免依赖已废弃能力。

## 关键参数

使用 Prompt 相关功能时，以下参数需重点关注：

- `workspaceId`：业务空间 ID，所有 Prompt 模板、样例库、反馈优化任务均需绑定至指定 workspace，获取方式见[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)；
- `promptTemplateId`：模板唯一标识符，用于 `GetPromptTemplate` 等 API 调用；
- `variables`：模板变量列表（如 `["platform", "topic"]`），由 `GetPromptTemplate` 接口返回，用于运行时填充；
- `has_thoughts=true`：调用智能体应用 API 时启用样例检索调试（仅限样例库功能，当前已不推荐）；
- 召回片段数（`top_k`）：样例库关联配置中可设，默认 5，上限 10，直接影响上下文 [Token](../concepts/token.md) 消耗；
- 评测数据量：反馈优化要求评测数据集至少 20 条，样例数据集建议 5–10 条且覆盖全部类别 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 使用方式

### 控制台操作
- **模板创建/管理**：进入「组件管理 > 提示词」页面，支持基于预置模板复制、或从零创建（文本生成/图片生成），并可选择「自定义创建」或「基于Prompt工程创建」模式；
- **自动优化**：在提示词管理页右上角点击「自动优化」，粘贴原始 Prompt 后一键生成优化版本，支持直接复制或保存为模板；
- **反馈优化**：在「提示词 > 反馈优化」页面新建任务，依次配置推理模型、初始 Prompt、样例数据（上传或选库）、评测数据后启动优化流程。

### API/SDK 调用
- **模板获取**：调用 `GetPromptTemplate` 接口（需 `workspaceId` + `promptTemplateId`），响应包含 `content` 与 `variables` 字段，供客户端动态渲染；
- **模板创建**：使用 `CreatePromptTemplate` 接口，支持 JSON 格式提交模板名称、内容、类型等；
- **智能体调用**：若已关联样例库（不推荐），需在请求体中设置 `has_thoughts: true` 以获取检索详情；反馈优化生成的 Prompt 可直接用于标准应用调用。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）目前仅支持华北2（北京）地域，跨地域调用将失败；
- **字符限制**：控制台编辑 Prompt 模板时，内容最大支持 6144 字符；
- **样例库限制**：单库最多 300 条样例，单应用最多关联 5 个库，单次召回最多 10 条样例 —— 但该功能已废弃，仅作历史兼容参考；
- **[Token](../concepts/token.md) 成本**：启用样例库或反馈优化会显著增加输入 [Token](../concepts/token.md)（样例内容 + 评测数据注入），需在成本与效果间权衡；
- **安全边界**：自动优化过程不会存储用户数据，亦不用于模型训练，符合阿里云数据隐私政策；
- **图片生成模板**：需分别定义正向 Prompt（期望内容）与负向 Prompt（排除内容），二者共同约束图像生成结果；
- **框架选择**：ICIO 适用于简单任务，CRISPE 适合角色扮演类交互，RASCEF 适用于多步骤复杂流程，需按任务复杂度匹配 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


