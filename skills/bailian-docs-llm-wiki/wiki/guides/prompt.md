# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令机制。它既可作为静态文本直接调用模型，也可通过模板化、样例增强、自动优化等方式实现工程化管理与持续迭代。开发者可通过控制台或 API 灵活构建、复用和优化 Prompt，适配从通用问答到专业领域任务的多样化需求。

## 支持的模型/功能

百炼平台提供多种 Prompt 相关能力，覆盖不同抽象层级和使用场景：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板，适用于华北2（北京）地域 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。模板分为文本生成与图片生成两类，后者支持正向/负向 Prompt 分离控制。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强等重构，不计费且不用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（few-shot）及评测数据集，通过多轮评估与反思生成更贴合业务场景的 Prompt；推荐推理模型为 `qwen-max` [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **Prompt 样例库（已停用）**：原支持少样本检索并注入上下文，但该功能**已不再维护**，官方明确建议迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

> **注意**：文档 1 中描述的 Prompt 样例库功能已废弃，所有新项目应避免依赖；其技术路径（如多路召回、样例库容量限制）不再适用当前架构。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 必填，需与 `workspaceId` 配合使用 |
| `workspaceId` | 业务空间 ID，用于定位模板归属环境 | 必填，需通过[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)获取 |
| 变量占位符 | 模板中动态插值字段，格式为 `${variableName}` | 支持任意合法变量名，无内置保留字限制 |
| 正向/负向 Prompt | 图片生成模板专用，分别定义期望与排除内容 | 负向 Prompt 非必填，但强烈建议设置以提升生成可控性 |
| 评测数据集大小 | Prompt 反馈优化中用于评估效果的数据量 | 建议 ≥20 条；样例数据集建议 5–10 条，且覆盖全部目标类别 |

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **创建提示词** → 选择类型（文本/图片）与输入模式（自定义 / Prompt 工程框架如 ICIO、CRISPE）→ 编辑并保存。
- **自动优化**：在 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt → 单击 **优化** → 复制结果或单击 **保存为模板**。
- **反馈优化**：在 [提示词 > 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 新增优化任务 → 选择推理模型、输入初始 Prompt、上传样例与评测数据 → 启动优化。

### API 调用
- 获取模板：调用 [`GetPromptTemplate`](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getprompttemplate) 接口，传入 `workspaceId` 和 `promptTemplateId`。
- 创建应用时注入：在智能体应用配置中，将渲染后的 Prompt 字符串（含变量替换结果）填入系统提示词字段；最大长度为 6144 字符。
- 图片生成：调用图像模型 API 时，分别传入 `positive_prompt` 和 `negative_prompt` 字段。

## 限制和注意事项

- **地域限制**：Prompt 模板功能（含预置与自定义）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **[Token](../concepts/token.md) 开销**：启用 Prompt 样例库（已停用）或反馈优化时，注入的样例内容会显著增加输入 [Token](../concepts/token.md)，直接影响计费；公式为：`总输入 Token ≈ 用户查询 Token + 召回/嵌入样例总 Token + 系统指令 Token`。
- **数据安全**：Prompt 自动优化过程中的输入数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。
- **模板变量校验**：变量名需为 ASCII 字母/数字/下划线组合，不支持中文或特殊符号；若变量未传值，渲染后将保留 `${xxx}` 原样，可能导致模型理解错误。
- **图片生成限制**：负向 Prompt 对部分开源图像模型（如 Stable Diffusion 系列）效果更显著，而百炼原生图像模型对负向提示的解析能力仍在持续增强中。

> **注意**：文档 3 中提到的“基于 Prompt 工程创建”模板虽支持 ICIO/CRISPE/RASCEF 等框架，但实际效果高度依赖所选推理模型的理解能力；建议在 `qwen-max` 或 `qwen-plus` 上验证框架适配性，避免在 `qwen-turbo` 等轻量模型上过度依赖复杂结构。

## 来源文档

- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


