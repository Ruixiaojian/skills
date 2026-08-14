# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入，用于定义任务目标、约束输出格式、注入领域知识或引导推理路径。通过结构化模板、自动优化、样例增强等机制，开发者可系统性地提升模型响应的准确性、一致性与可控性，降低人工调优成本。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

- **模板化支持**：提供预置 Prompt 模板（如营销文案生成、摘要抽取）和自定义 Prompt 模板两类，分别适用于通用场景与高定制需求（如金融风控、JSON 格式强约束）。预置模板效果稳定、开箱即用；自定义模板支持编辑、复制与删除，且可基于 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 中描述的流程全生命周期管理。
- **多模态模板类型**：自定义模板支持「文本生成」与「图片生成」两种基础类型。图片生成模板需分别配置正向 Prompt（期望内容）与负向 Prompt（需排除元素），详见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **优化能力**：
  - **Prompt 自动优化**：对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，不计费，但输入内容需符合 [Token](../concepts/token.md) 限制与内容策略要求（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)）。
  - **Prompt 反馈优化**：基于用户提供的输入输出样例（5–10 条）与评测数据（≥20 条）进行多轮自动化评估与迭代，生成更贴合实际业务效果的 Prompt，推荐使用 `qwen-max` 作为推理模型。
- **样例增强（已下线）**：Prompt 样例库功能**已不再维护**，官方明确要求迁移至 RAG 表格库。> **注意**：文档 4 中描述的样例库创建、关联与调试流程已失效，不可用于新项目开发；当前仅支持通过 RAG 实现类似少样本引导效果。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`） | 必填；从控制台模板卡片获取 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作均需指定该上下文 | 必填；通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `variables` | 模板中声明的变量名列表（如 `["platform", "topic"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，不可手动修改变量语法（仅支持 `${var}`） |
| `max_retrieved_samples` | （历史参数，已弃用）样例库召回片段数，默认 5，上限 10 | > **注意**：该参数属于已下线的 Prompt 样例库功能，当前 RAG 表格库使用独立配置项，此处仅作兼容说明 |

## 使用方式

### 控制台操作
- **创建模板**：进入「应用开发 > 组件管理 > 提示词」，单击「创建提示词」，选择「文本生成」或「图片生成」，按需填写内容或使用 Prompt 工程框架（ICIO/CRISPE/RASCEF）构建结构化 Prompt。
- **优化 Prompt**：在「提示词」页面右上角进入「自动优化」，粘贴原始 Prompt 后点击「优化」，可直接复制结果或「保存为模板」。
- **使用模板**：在预置或自定义模板卡片上点击「使用prompt > 创建应用」，模板内容将自动填充至智能体应用的提示词编辑框，变量以 `${name}` 形式呈现（最大字符数 6144）。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 与 `promptTemplateId`，响应中包含 `content`（模板字符串）与 `variables`（变量列表）。
- **生成最终 Prompt**：将业务数据代入模板变量（如 `content.replace("${topic}", "AI伦理")`），再将生成的完整 Prompt 作为 `system` 或 `user` 消息发送至模型推理接口。
- **反馈优化任务**：调用 `CreatePromptFeedbackOptimizationTask`（需参考 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 文档），上传样例与评测数据集，异步获取优化后 Prompt。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板变量语法**：仅支持 `${variable}` 格式，不支持 `$variable`、`{{variable}}` 等变体；变量名须为合法标识符（字母/数字/下划线，不能以数字开头）。
- **[Token](../concepts/token.md) 开销**：启用任何样例增强类功能（如历史样例库或当前 RAG）均会增加输入 [Token](../concepts/token.md)，需在成本与效果间权衡；反馈优化本身不产生推理费用，但优化后的 Prompt 在实际调用中可能因长度增加而提高 Token 消耗。
- **安全与隐私**：通过自动优化或反馈优化提交的 Prompt 内容**不会被用于模型训练**，阿里云承诺严格遵守数据隐私政策（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)）。
- **版本一致性**：强烈建议通过 `GetPromptTemplate` 接口动态拉取模板，而非硬编码字符串——此举可实现逻辑与内容分离，避免因控制台更新模板导致应用行为不一致（参见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 常见问题）。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


