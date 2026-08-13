# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入指令。通过结构化设计、模板化管理、自动优化与样例增强等能力，开发者可高效构建稳定、可控、可复用的提示词逻辑，显著提升模型输出质量与业务适配性。所有 Prompt 相关功能均需在华北2（北京）地域使用。

## 支持的模型/功能

- **模板化支持**：提供预置 Prompt 模板（覆盖营销文案、摘要抽取、风格改写等通用场景）和自定义 Prompt 模板（支持文本生成与图片生成两类），均通过控制台或 API 管理，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **自动优化**：支持基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，适用于快速提升 Prompt 质量，该功能不计费且数据不用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **反馈式优化**：支持基于用户提供的输入输出样例（few-shot 数据）与评测集，通过多轮评估-反思-生成机制自动产出高精度 Prompt，尤其适用于垂直领域分类、格式强约束等任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **样例库（已停用）**：原支持通过少样本问答对引导模型输出风格与结构，但该功能已下线，官方明确要求迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

> **注意**：文档 4 中描述的 Prompt 样例库功能已正式停止维护，所有新项目应使用 RAG 表格库替代；若现有应用仍在使用该功能，须按指引完成迁移，否则将无法长期保障服务可用性。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填，从控制台模板卡片或响应体中获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，参见[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `variables` | 模板中声明的变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，用于运行时填充 |
| `recall_count` | 样例库召回片段数（历史参数，仅影响已启用样例库的应用） | 默认 5，最大 10；**注意**：该参数已随样例库下线而失效 |
| `has_thoughts` | API 调用时启用样例检索过程日志输出（`thoughts` 字段） | 仅对仍启用样例库的应用有效，非推荐路径 |

## 使用方式

### 1. 模板创建与管理
- **预置模板**：直接在控制台 [提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt) 查看、复制或“复制模板”生成可编辑副本。
- **自定义模板**：
  - 文本生成：支持「自定义创建」（粘贴原始 Prompt 后一键优化）或「基于Prompt工程创建」（ICIO/CRISPE/RASCEF 框架引导）；
  - 图片生成：需分别配置正向 Prompt（期望内容）与负向 Prompt（排除内容）；
  - 所有模板均支持编辑、删除、批量复制，详情见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

### 2. 模板调用流程
1. 调用 `GetPromptTemplate` 接口（或 SDK）传入 `workspaceId` 与 `promptTemplateId`；
2. 解析响应中的 `content` 与 `variables`；
3. 将业务数据按 `variables` 键名填充至 `content` 的 `${var}` 占位符；
4. 将生成的完整 Prompt 作为 `system` 或 `user` 消息发送至目标模型（如 `qwen-plus`）。

### 3. 自动优化接入
- 控制台路径：**应用开发 > 组件管理 > 提示词 > 自动优化**；
- 输入原始 Prompt → 单击「优化」→ 复制结果或「保存为模板」；
- 支持直接集成至 CI/CD 流程：通过 `OptimizePrompt` API（需 workspaceId）实现自动化调用。

### 4. 反馈优化工作流
- 上传两类数据：**样例集**（5–10 条，覆盖全部类别）、**评测集**（≥20 条，用于效果验证）；
- 指定推理模型（推荐 `qwen-max`）；
- 启动任务后，平台生成含原始指令 + few-shot 示例 + 边界提示的增强版 Prompt；
- 优化结果可一键保存为模板或创建智能体应用。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **字符与 [Token](../concepts/token.md) 限制**：
  - 模板内容最大 6144 字符（控制台编辑框上限）；
  - 自动优化输入 Prompt 需符合模型 [Token](../concepts/token.md) 限制，超长将触发失败（见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 常见问题）；
  - 反馈优化中，评测集数据越多效果越好，但单次上传文件需 ≤20MB（Excel 格式）。
- **模板变量语法**：统一使用 `${variable_name}` 格式，不支持嵌套或表达式（如 `${a.b}` 或 `${x + y}`）。
- **安全与合规**：
  - 自动优化过程不存储用户数据，不用于模型训练；
  - 所有 Prompt 内容受百炼平台内容安全策略约束，触发审核将导致优化或调用失败。
- **版本与兼容性**：
  - 预置模板不可修改，但可通过「复制模板」创建自定义副本并迭代；
  - 自定义模板支持无限次编辑，但历史版本不保留，需自行备份关键变更。

> **注意**：文档 1 与文档 2 均强调“仅适用于华北2（北京）地域”，但文档 5 的案例实践截图及参数说明未显式重申该限制，实际部署时必须严格校验 `RegionId=cn-beijing`，否则 `CreatePromptTemplate`、`GetPromptTemplate` 等核心接口将返回 `InvalidRegionId` 错误。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


