# Prompt 工程

Prompt 工程是百炼平台上系统化设计、管理与优化大语言模型输入指令（Prompt）的方法论与工程实践，核心目标是将业务意图精准、稳定、可复用地转化为高质量模型输出。它不是单次提示词编写，而是涵盖模板化、变量注入、自动增强、数据驱动反馈优化等全生命周期能力的结构化工作流。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过「系统提示词」配置强化角色设定与行为约束（如“你是一名金融风控专家，仅基于提供的报告摘要作判断”），并结合知识库检索结果动态拼接上下文；Prompt 模板可作为 Agent 的默认推理入口，实现提示逻辑与工具调度解耦。  
- **工作流（Workflow）应用**：在「大模型节点」中直接引用已创建的 Prompt 模板，运行时自动填充 `query`、`historyList` 等会话变量；支持多版本模板灰度切换，无需修改工作流拓扑即可迭代提示策略。  
- **高代码应用开发**：通过 SDK 调用 `GetPromptTemplate` 接口拉取模板内容，解析 `variables` 字段后注入业务数据（如用户画像、订单状态），再构造完整 Prompt 发送给目标模型（如 `qwen3.7-plus`）；模板更新后，应用无需重新部署即可生效。  
- **RAG 增强场景**：Prompt 工程与 RAG 协同——RAG 负责召回相关知识片段，Prompt 工程负责设计“如何整合这些片段”的指令（例如：“请严格依据以下 3 条检索结果回答，禁止编造未提及的信息”），确保生成结果忠实、可控。  
- **图片/视频生成任务**：使用「图片生成类 Prompt 模板」，分别定义正向提示（`positive_prompt`）与负向提示（`negative_prompt`），支持变量占位（如 `${style}`、`${subject}`），便于批量生成风格统一的视觉内容。

> ⚠️ 注意：Prompt 样例库功能已正式下线，所有新项目应避免依赖该能力；历史项目请迁移至 RAG 表格库或使用反馈优化替代。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用（如 `GetPromptTemplate`） | 从控制台模板卡片复制，或通过 `ListPromptTemplates` 接口批量获取；建议在代码中常量化管理。 |
| `workspaceId` | 业务空间 ID，用于资源隔离与权限校验 | 必填，需提前通过控制台或 OpenAPI 获取；不同环境（测试/生产）应使用独立 workspace。 |
| `variables` | 模板中声明的变量列表（如 `${topic}`、`${num1}`），运行时需全部填充 | 使用 `GetPromptTemplate` 接口返回的 `variables` 字段做校验，缺失变量将导致渲染失败；建议封装 `renderPrompt(template, data)` 工具函数。 |
| `temperature` / `max_tokens` | 控制生成随机性与输出长度 | 属于模型调用参数，非 Prompt 模板本身属性；应在最终请求中显式设置（如 `temperature=0.3` 保证稳定性）。 |
| `enable_thinking` | 启用模型推理链路展示（仅对 `qwen-max` 等支持思考模式的模型生效） | 调试阶段开启便于分析 Prompt 效果；生产环境可关闭以降低延迟。 |

- **地域强制约束**：所有 Prompt 相关 API（模板管理、自动优化、反馈优化）**仅支持华北2（北京）地域**（`RegionId=cn-beijing`），跨地域调用将返回 `InvalidRegionId` 错误。  
- **容量限制**：单个文本 Prompt 模板最大 6144 字符；图片生成模板需分别填写正向与负向 Prompt，各自独立计长。  
- **反馈优化数据要求**：训练样例建议 5–10 条（覆盖典型 case），评测样例 ≥20 条（含边界 case）；数据不足将显著降低优化效果。

## 面向开发者，简洁实用

- ✅ **推荐做法**：  
  - 所有业务级 Prompt 必须通过「自定义 Prompt 模板」管理，禁用硬编码；  
  - 使用控制台「自动优化」快速提升初始 Prompt 质量（免费、不计费、不存数据）；  
  - 对关键业务流（如客服回复、合同审核），启用「反馈优化」并定期用线上真实样本迭代；  
  - 在 SDK 中封装模板渲染与错误处理逻辑，统一处理变量缺失、超长截断、地域校验失败等异常。

- ❌ **禁止做法**：  
  - 在代码中拼接字符串构造 Prompt（无法复用、不可审计、难调试）；  
  - 跨地域调用 Prompt 接口（必须显式指定 `cn-beijing` endpoint）；  
  - 继续使用已下线的 Prompt 样例库功能（包括 `recall_k`、`has_thoughts` 等参数）；  
  - 将敏感信息（如用户身份证号、密钥）直接写入 Prompt 模板（应通过变量注入，并确保传输加密）。

- 🛠️ **调试技巧**：  
  - 控制台右侧「测试区」支持实时变量填充与一键调试，优先用于验证模板逻辑；  
  - 查看 API 返回的 `RequestId`，配合日志追踪 Prompt 渲染与模型调用全过程；  
  - 对比「原始 Prompt」与「自动优化后 Prompt」，学习角色注入、约束强化等工程技巧。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)


