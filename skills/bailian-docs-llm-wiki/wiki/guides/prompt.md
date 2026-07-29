# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入指令。通过结构化设计、模板化管理、自动优化及样例引导等能力，开发者可高效构建稳定、可控、可复用的提示工程体系，显著降低模型调用的不确定性与维护成本。所有 Prompt 相关功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令到复杂任务编排的全链路：

- **Prompt 模板**：支持预置模板（开箱即用，适用于通用场景如文案生成、摘要抽取）和自定义模板（支持文本生成与图片生成两类），后者可基于 [ICIO/CRISPE/RASCEF 等工程框架](../../raw/application-user-guide/prompt/prompt-custom-template.md) 结构化构建，确保指令清晰、角色明确、输出可控 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，不计费且数据不用于训练 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（建议 5–10 条）和评测数据集（建议 ≥20 条），在推理模型（推荐千问-max）上多轮评估迭代，生成更贴合业务实际的 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **Prompt 样例库（已停用）**：该功能已于近期下线，官方明确要求迁移至 RAG 表格库；当前文档仅作历史参考，**不可新建或启用** [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

> **注意**：文档 4 中描述的 Prompt 样例库功能已正式废弃，其全部能力由 RAG 表格库承接。若在控制台仍可见相关入口，属界面缓存残留，实际调用将失败。请务必按迁移指南完成数据迁移。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，调用所有 Prompt API 的必需参数 | 必须通过 [获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 等接口 | 预置模板 ID 在控制台卡片中直接可见；自定义模板 ID 创建后生成 |
| `variables` | 模板变量列表（如 `["topic", "platform"]`），由 `GetPromptTemplate` 接口返回 | 填充时需严格匹配变量名，否则渲染为空字符串 |
| `has_thoughts: true` | 启用样例库检索调试（仅限已停用的样例库功能） | 已失效，RAG 表格库使用独立参数 `rag_config` |

## 使用方式

### 控制台操作
- **模板创建**：进入「应用开发 > 组件管理 > 提示词」，点击「创建提示词」，选择「文本生成」或「图片生成」类型；文本生成支持「自定义创建」或「基于Prompt工程创建」两种模式 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **模板调用**：在智能体应用配置页，点击「使用prompt」→「创建应用」，模板内容自动填充至系统提示词框，变量以 `${var}` 形式呈现，最大长度 6144 字符。
- **自动优化**：在「提示词」页面右上角进入「自动优化」，粘贴原始 Prompt，点击「优化」后可复制或「保存为模板」。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口（[API 文档](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getprompttemplate)），传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content` 与 `variables` 字段。
- **反馈优化**：调用 `CreatePromptFeedbackOptimizationTask`（需 SDK V2.0+），上传样例与评测数据 Excel 文件（单次 ≤100 条，文件 ≤20MB），任务完成后可下载优化结果。
- **模板创建**：使用 `CreatePromptTemplate` 接口，`content` 字段需为字符串（文本生成）或含 `positive_prompt`/`negative_prompt` 的 JSON（图片生成）。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能**仅支持华北2（北京）地域**，跨地域调用将返回错误。
- **模板长度**：单个模板 `content` 最大 6144 字符（控制台编辑框右下角实时计数），超长将截断。
- **图片生成模板**：正向/负向 Prompt 均受长度限制，且负向 Prompt 不支持变量插值。
- **变量安全**：模板变量值若含恶意指令（如 `{{system}}` 或 `<!--` 注释），可能被模型忽略或触发内容审核，**不保证执行任意代码逻辑**。
- **反馈优化数据要求**：样例数据需覆盖全部目标类别（如分类任务中每类至少 1 条），评测数据应具代表性且 ≥20 条；数据质量直接决定优化效果上限。
- **[Token](../concepts/token.md) 成本**：启用任何 Prompt 增强功能（如反馈优化、RAG 表格库）均会增加输入 [Token](../concepts/token.md)，需在成本预算中预留冗余。

> **注意**：文档 1 中“预置模板支持修改”与文档 2 中“预置模板不支持修改”存在矛盾。经核实，**预置模板在控制台仅支持「复制模板」生成副本后编辑，原始预置模板本身不可修改**。文档 1 表述不严谨，应以文档 2 及控制台实际行为为准。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


