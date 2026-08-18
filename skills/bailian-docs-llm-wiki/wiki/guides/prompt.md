# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心控制机制。它既可作为静态指令直接调用，也可通过模板化、样例增强、自动优化等方式实现结构化、可复用、可迭代的工程化管理。合理设计和使用 Prompt，是保障模型输出质量、一致性与业务适配性的关键实践。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力，覆盖从基础指令到高阶工程优化的全链路需求：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），适用于华北2（北京）地域。文本生成模板支持两种创建模式：[自定义创建](../../raw/application-user-guide/prompt/prompt-custom-template.md)（适合已有 Prompt 的快速模板化）和[基于Prompt工程创建](../../raw/application-user-guide/prompt/prompt-custom-template.md)（如 ICIO、CRISPE、RASCEF 等框架，适用于复杂任务）。图片生成模板则需分别配置正向与负向 Prompt。
  
- **Prompt 样例库（Few-shot）**：通过注入高质量输入-输出对（user input / model output）引导模型风格与逻辑。但需注意：> **注意**：该功能[已不再维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐将数据迁移到 RAG 表格库中。

- **Prompt 自动优化与反馈优化**：
  - *自动优化*：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强等重写，不计费且数据不用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - *反馈优化*：基于用户提供的**样例数据**（5–10 条）和**评测数据**（≥20 条）进行多轮评估与迭代，生成更贴合实际场景的 Prompt，效果优于纯自动优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值/限制 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 必填；在控制台模板卡片上获取 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作均需指定 | 必填；通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| `variables` | 模板中定义的占位符列表（如 `${platform}`、`${topic}`） | 由 `GetPromptTemplate` 接口返回，用于运行时填充 |
| `has_thoughts` (API) | 控制是否在响应中返回样例检索过程（仅限已弃用的样例库功能） | `true`/`false`；默认 `false` |
| 召回片段数（样例库） | 注入上下文的样例数量 | 默认 5，最多 10（[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)） |
| 样例库容量 | 单个样例库最大条目数 | 300 条（同上） |

## 使用方式

### 控制台操作
- **创建模板**：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → “创建提示词”，选择类型（文本/图片）与输入模式（自定义 or [Prompt 工程](../concepts/prompt-engineering.md)）。
- **使用模板**：在智能体应用配置中点击“使用prompt” → “创建应用”，模板变量自动填充至提示词编辑框（最大 6144 字符）。
- **自动优化**：在[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)页面粘贴原始 Prompt，点击“优化”后可复制或“保存为模板”。
- **反馈优化**：进入[提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → “新增优化任务”，上传样例与评测数据集，启动优化。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 与 `variables`，动态填充后发送至目标模型。
- **模板创建**：使用 `CreatePromptTemplate` 接口（需提前获取 `workspaceId`）。
- **效果验证**：通过 `has_thoughts=true` 参数调试样例库召回逻辑（仅限历史兼容场景）。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）仅支持华北2（北京）地域，详见[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)与[Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **功能弃用**：> **注意**：Prompt 样例库功能已正式下线，[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)文档明确指出“已不再维护”，迁移至 RAG 表格库为强制要求。
- **Token 成本**：启用样例库（历史遗留）或反馈优化会显著增加输入 Token（样例/评测数据本身 + 注入上下文），直接影响调用费用；自动优化本身不计费，但生成的 Prompt 若更长，也会间接增加后续推理成本。
- **数据安全**：自动优化过程中提交的 Prompt 不会被存储或用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **模型依赖**：反馈优化推荐使用 `qwen-max` 作为推理模型；预置模板调用需在控制台或 API 中显式指定目标模型（如 `qwen-plus-latest-128k`）。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


