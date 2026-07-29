# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为静态文本直接调用模型，也可通过模板化、样例增强、自动优化等机制实现结构化管理与效果提升。合理设计 Prompt 是保障模型输出准确性、一致性与业务适配性的关键环节，适用于文本生成、图片生成、智能体应用构建等多种场景。

## 支持的模型/功能

百炼平台提供多种 Prompt 相关能力，覆盖从基础指令构造到高级工程化优化的全链路：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（含文本生成与图片生成两类），通过变量插值（如 `${topic}`）实现动态内容填充。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**（已下线）：曾支持通过少样本问答对（user input / model output）引导模型风格与格式，但该功能[已不再维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移至 RAG 表格库。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验。该功能不计费，且用户数据不会用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入输出样例（few-shot）及评测数据集，通过多轮自动化评估与反思生成更贴合实际业务效果的 Prompt，尤其适用于分类、结构化输出等任务。

> **注意**：文档 2 中描述的 Prompt 样例库功能已正式停用，所有新项目应避免依赖该能力；现有应用需按指引迁移至 RAG 表格库。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 字符串，由平台生成 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，必需参数，用于鉴权与资源隔离 | 字符串，需通过控制台或 API 获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的变量名列表（如 `["platform", "topic"]`），用于运行时填充 | JSON 数组，最大支持 64 个变量 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | API 调用时启用样例检索调试信息（仅限历史兼容场景） | `true` / `false`，仅在样例库功能有效期内适用 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 关联样例库时注入上下文的样例数量（已下线） | 默认 5，上限 10 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作
- **模板创建与管理**：进入「组件管理 > 提示词」页面，支持自定义创建、基于 [Prompt 工程](../concepts/prompt-engineering.md)框架（ICIO/CRISPE/RASCEF）创建，或复制预置模板进行二次开发。
- **自动优化**：在「提示词 > 自动优化」页面粘贴原始 Prompt，点击「优化」获取增强版本，支持一键「保存为模板」。
- **反馈优化**：在「提示词 > 反馈优化」页面配置初始 Prompt、上传样例数据（建议 5–10 条，覆盖全部类别）与评测数据（建议 ≥20 条），启动多轮优化任务。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content`（模板字符串）与 `variables`（变量列表）。
- **渲染模板**：将业务数据按 `variables` 键名填入模板字符串（如 `content.replace('${topic}', 'AI芯片')`），生成最终 Prompt。
- **调用模型**：将渲染后的 Prompt 作为 `messages` 或 `system` 字段传入模型推理 API（如 `ChatCompletion`）。

### SDK 示例
SDK 示例代码（Java/Python 等）可在 `GetPromptTemplate` 接口文档的「SDK 示例」页签中自动生成，自动注入 `workspaceId` 和 `promptTemplateId`，开发者仅需配置 `accessKeyId` 和 `accessKeySecret` 即可运行。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（包括创建、获取、使用）当前**仅支持华北2（北京）地域**，跨地域调用将失败。
- **字符长度**：控制台编辑器中 Prompt 内容最大支持 **6144 字符**；API 层面受模型最大上下文限制（如 Qwen-Max 为 32K tokens），需自行校验总 token 数。
- **模板变量**：变量语法为 `${variableName}`，不支持嵌套或表达式（如 `${a.b}` 或 `${x + y}`）。
- **图片生成模板**：仅支持文本生成与图片生成两类，图片模板需分别配置正向 Prompt（期望内容）与负向 Prompt（排除内容）。
- **数据安全**：Prompt 自动优化与反馈优化过程中，用户提交的原始 Prompt 和样例数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策。
- **成本影响**：启用样例库（已下线）或反馈优化会显著增加输入 token 消耗；反馈优化本身不计费，但其产出的 Prompt 若导致更长输入或更高频调用，将间接影响模型调用费用。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


