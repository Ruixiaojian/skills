# Prompt 工程

Prompt 工程是指系统性设计、验证、优化和管理提示词（Prompt）的方法论与实践体系，旨在通过结构化指令、角色设定、上下文注入、样例引导和边界约束等技术手段，精准控制大语言模型的行为与输出，提升结果的准确性、稳定性、可控性与业务适配性。它既是模型调用的基础能力，也是百炼平台实现高质量 AI 应用落地的核心工程范式。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，Prompt 工程并非仅限于手动编写文本指令，而是被深度产品化为可配置、可复用、可迭代的工程能力，覆盖以下关键场景：

- **模板化构建**：通过「Prompt 模板」功能，开发者可基于 ICIO、CRISPE、RASCEF 等成熟框架结构化定义提示词逻辑（如角色 `Role`、任务 `Instruction`、输入 `Context`、输出格式 `Output`），支持文本生成与图片生成两类任务（后者需分别配置正向/负向 Prompt）。模板支持变量占位（如 `{{topic}}`），便于运行时动态填充，实现“一次设计、多处复用”。

- **样例驱动优化（已迁移）**：原「Prompt 样例库」功能通过少样本（Few-shot）注入高质量问答对来引导模型风格与格式，但该能力**已停止维护**。官方明确要求新项目迁移至 RAG 表格库——即通过结构化知识库替代静态样例，使模型在真实业务上下文中自主检索并学习模式，更符合生产环境的可扩展性与安全性要求。

- **自动化增强**：「Prompt 自动优化」服务无需开发者具备 Prompt 工程经验，即可对原始提示词进行智能重构：自动补全角色设定、强化指令清晰度、注入安全边界（如拒绝越界请求）、优化句式结构，显著降低人工试错成本。

- **反馈闭环迭代**：「Prompt 反馈优化」面向高确定性任务（如分类、JSON 结构化输出），允许开发者提交带标注的 query-answer 样例集，平台基于大模型（推荐 `qwen-max`）进行多轮评估与重写，输出含 few-shot 示例、格式约束说明和边界提示的高精度 Prompt，支持效果可量化验证。

- **智能体系统集成**：在 LLM 应用（尤其是 Agent 2.0）中，系统提示词（System Prompt）本身就是 Prompt 工程的直接体现。开发者可通过控制台配置嵌入变量（如 `/user_profile`）、启用 `enable_thinking` 展示推理链，并与知识库、MCP 工具协同，形成“提示词 + 工具 + 记忆”的复合控制平面。

## 关键参数和配置

| 参数 | 说明 | 使用场景 | 注意事项 |
|------|------|----------|----------|
| `promptTemplateId` | Prompt 模板唯一标识符 | API 调用 `GetPromptTemplate` 获取模板内容后，用于渲染与模型请求 | 必须与 `workspaceId` 配对使用；模板内容最大 6144 字符 |
| `workspaceId` | 业务空间 ID | 所有 Prompt 相关 API（创建、获取、优化）及应用配置的必需路径参数 | 仅华北2（北京）地域有效；跨地域调用将失败 |
| `variables` | 模板中声明的变量名数组（如 `["topic", "tone"]`） | 运行时传入 `RenderPromptTemplate` 或 SDK 渲染接口 | 变量名由模板定义，不可在调用时动态增删 |
| `has_thoughts` | 请求头或参数，设为 `true` 时返回 `thoughts` 字段 | 调试已关联样例库（旧版）或 RAG 增强的智能体应用召回过程 | 仅对启用样例/RAG 的应用生效；非通用参数 |
| `temperature` | 控制输出随机性（0.0–2.0） | 在智能体或模型 API 调用中设置，影响 Prompt 执行结果的确定性 | 问答/结构化任务建议 0.1–0.6；创意生成可适度提高 |

> ⚠️ 重要限制：  
> - 所有 Prompt 功能（模板、优化、历史样例库）**仅支持华北2（北京）地域**；  
> - 文生图 Prompt 模板暂不支持通过 Application Component API 创建（仅控制台支持）；  
> - Prompt 自动优化与反馈优化过程中提交的数据**不会被存储或用于模型训练**，符合数据隐私规范。

## 面向开发者，简洁实用

- ✅ **起步建议**：新项目优先使用「Prompt 模板」+「RAG 表格库」组合，避免依赖已下线的样例库；从预置模板（如“营销文案生成”）开始快速验证，再逐步自定义。  
- ✅ **调试技巧**：在智能体调试窗口开启 `enable_thinking`，观察模型如何解析你的 Prompt；结合 `has_thoughts=true` 查看 RAG 召回片段，定位提示词与知识匹配偏差。  
- ✅ **API 最佳实践**：  
  - 创建模板 → `CreatePromptTemplate`（需 `workspaceId`）；  
  - 渲染变量 → `RenderPromptTemplate`（传入 `promptTemplateId` + `variables` 对象）；  
  - 发送请求 → 将渲染后的 `content` 作为 `input.prompt` 提交至目标模型 API。  
- ✅ **避坑提醒**：  
  - 不要尝试在 API 请求中动态修改模板变量结构；  
  - 图片生成类 Prompt 需严格区分正向（`positive_prompt`）与负向（`negative_prompt`）字段；  
  - 所有 Prompt 内容需 UTF-8 编码，避免不可见字符导致渲染异常。  

Prompt 工程不是“魔法咒语”，而是可测量、可版本化、可协作的软件工程实践。在百炼平台，它已被封装为开箱即用的能力模块——你只需聚焦业务逻辑，让平台处理结构、优化与部署。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)


