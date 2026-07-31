# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入指令。通过结构化设计、模板化管理与数据驱动优化，开发者可显著提升模型输出的准确性、一致性与可控性。平台提供从基础 Prompt 编写、模板复用，到基于样例反馈的自动优化等全链路能力，覆盖文本生成、图片生成、智能体应用等多种场景。

## 支持的模型/功能

- **模型支持**：所有百炼托管的文本生成模型（如通义千问系列）均原生支持 Prompt 输入；图片生成模型（如万相）支持正向/负向 Prompt 分离配置。  
- **核心功能**：  
  - **Prompt 模板**：支持预置模板（开箱即用）和自定义模板（含文本生成与图片生成两类），实现逻辑与内容分离 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；  
  - **[Prompt 工程](../concepts/prompt-engineering.md)框架**：内置 ICIO、CRISPE、RASCEF 等结构化框架，辅助构建复杂任务 Prompt [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)；  
  - **自动优化**：提供两种路径：  
    - *Prompt 自动优化*：基于大模型对原始 Prompt 进行重写与增强，适用于通用质量提升；  
    - *Prompt 反馈优化*：基于用户提供的输入-输出样例（few-shot）和评测数据集，进行多轮评估与迭代优化，效果更贴合实际业务场景 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)；  
  - **样例库（已弃用）**：曾支持通过少样本检索引导模型输出，但该功能**已停止维护**，官方明确要求迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
> **注意**：文档 5 中描述的 Prompt 样例库功能已被正式下线，任何新项目均不应依赖该能力；现有用户需按指引完成迁移，否则将无法获得技术支持或服务保障。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`） | 必填；在控制台模板卡片或响应体中获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填；通过 [获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `variables` | 模板中声明的变量名列表（如 `["topic", "platform"]`），用于运行时填充 | 由 `GetPromptTemplate` 响应返回，不可手动指定 |
| `has_thoughts` | API 请求参数，启用后响应中返回样例检索详情（仅限历史样例库，现不推荐使用） | 已弃用，仅兼容旧应用 |
| 召回片段数 | 样例库关联应用时可配置的参数（默认 5，上限 10） | 仅影响已弃用的样例库功能 |

## 使用方式

- **控制台操作**：  
  - 模板管理：访问 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持创建、编辑、复制、删除模板；  
  - 自动优化：在“自动优化”子页粘贴原始 Prompt，一键生成优化版本；  
  - 反馈优化：在“反馈优化”子页上传初始 Prompt、样例数据（5–10 条）及评测数据（≥20 条），启动多轮优化任务。  
- **API 调用**：  
  - 模板获取：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`；  
  - 模板创建：调用 `CreatePromptTemplate` 接口（需先获取 `workspaceId`）；  
  - 应用集成：将渲染后的 Prompt 作为 `system` 或 `user` 消息字段，传入模型推理 API（如 `ChatCompletion`）。  
- **SDK 集成**：各语言 SDK（V2.0 推荐）均提供 `GetPromptTemplate` 等接口封装，参数自动注入，支持在线调试与工程下载 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 相关功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败；  
- **字符与 [Token](../concepts/token.md) 限制**：  
  - 控制台 Prompt 输入框最大支持 **6144 字符**；  
  - 模板内容本身无显式 [Token](../concepts/token.md) 上限，但最终注入模型的总上下文（含变量填充后 Prompt + 用户输入）受所选模型最大上下文窗口限制（如 Qwen-Max 为 128K）；  
- **安全与合规**：  
  - 所有提交至自动优化功能的 Prompt 数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策；  
  - 优化过程可能因输入过长、含敏感词或触发审核策略而失败，需检查错误码并重试；  
- **模板变量语法**：统一使用 `${variableName}` 格式，不支持嵌套或表达式（如 `${a+b}`）；  
- **弃用功能警示**：  
  > **注意**：Prompt 样例库（文档 5）功能已下线，其全部能力（包括创建、关联、召回）均不再维护。新项目请使用 RAG 表格库替代；存量应用须尽快迁移，避免服务中断。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)


