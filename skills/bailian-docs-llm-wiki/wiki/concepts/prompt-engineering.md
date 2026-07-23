# Prompt 工程

Prompt 工程是百炼平台中系统化设计、管理与优化大语言模型输入指令（Prompt）的方法论与技术实践，旨在通过结构化模板、上下文增强、自动化调优和闭环反馈等手段，稳定提升模型输出的准确性、一致性、安全性与业务适配性。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：Prompt 是智能体行为的“操作系统”。通过配置 `system_prompt` 定义角色、任务边界与工具调用规范（如“你是一个电商导购助手，仅能调用商品查询和比价工具”），结合变量注入（如 `{{user_intent}}`）和可选的 RAG 检索片段，驱动模型完成多步推理与执行。  
- **工作流（Workflow）应用**：在“大模型节点”中直接填写或引用 Prompt 模板，支持将上游节点输出（如意图分类结果、用户画像字段）作为变量动态填充，实现流程级 Prompt 编排。  
- **高代码应用**：开发者可在 Python 服务中调用 `GetPromptTemplate` 接口获取模板内容，解析 `variables` 后安全填充业务数据，再构造标准 OpenAI 兼容请求体提交至百炼模型网关。  
- **零代码构建**：控制台创建智能体/工作流时，“系统提示词”字段即为 Prompt 工程入口；支持一键启用“自动优化”，或上传样例数据触发“反馈优化”，无需编写代码即可获得工程级 Prompt。  
- **多模态生成（文生图/文生视频）**：Prompt 工程体现为结构化公式（如图像：`主体 + 场景 + 风格 + 负向约束`），需分别配置正向 Prompt（期望内容）与负向 Prompt（需排除元素），并通过图片生成模板统一管理。

> ⚠️ 注意：Prompt 样例库（Few-shot）功能已停止维护，**所有新项目请迁移至 RAG 表格库或反馈优化方案**；历史依赖该功能的生产流程应尽快重构。

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 备注 |
|------|------|----------|------|
| `promptTemplateId` | Prompt 模板唯一标识符 | API（`GetPromptTemplate`）、智能体/工作流节点配置 | 必填，需与 `workspaceId` 配对使用 |
| `workspaceId` | 业务空间 ID，所有 Prompt 资源的归属容器 | 所有 Prompt 相关 API 及控制台操作 | 必填，控制台“设置 > 工作空间”中查看 |
| `variables` | 模板中声明的动态变量名列表（如 `["topic", "tone"]`） | `GetPromptTemplate` 响应体中返回 | 不可手动指定，由平台解析模板内容自动生成 |
| `system_prompt` | 智能体/工作流中定义模型角色与行为准则的顶层指令 | 智能体配置页、“大模型节点”参数面板 | 推荐使用自动优化后的版本，避免模糊表述 |
| `has_thoughts` | 启用样例检索调试信息的开关 | 智能体应用 API 请求体 | 设为 `true` 可在响应 `thoughts` 字段中查看召回的 RAG 片段详情 |
| `召回片段数` | 单次请求从知识库/RAG 表格库中注入的上下文数量 | 智能体配置页 > 文件问答 > 切片检索设置 | 默认 5，最大 10；影响 Token 成本与效果平衡 |

## 面向开发者，简洁实用

- ✅ **首选自动化**：新项目直接使用「Prompt 自动优化」（免费、不存数据、10 秒出结果），粘贴原始指令即可获得符合 ICIO/CRISPE 等框架的增强版 Prompt。  
- ✅ **强业务适配用反馈优化**：当任务有明确输出格式（如 JSON 分类、表格抽取）时，上传 5–10 条高质量样例 + ≥20 条评测数据，启动反馈优化任务，推荐使用 `qwen-max` 模型。  
- ✅ **模板即资产**：通过 `CreatePromptTemplate` API 创建模板，类型设为 `text_generation` 或 `image_generation`；后续所有应用均可复用同一 `promptTemplateId`，实现集中治理。  
- ⚠️ **地域强约束**：所有 Prompt 功能（模板、自动优化、反馈优化）**仅支持华北2（北京）地域**，API Endpoint 必须为 `bailian.cn-beijing.aliyuncs.com`。  
- ⚠️ **Token 成本敏感**：启用 RAG 注入或反馈优化会显著增加输入 Token（样例内容 + 用户 Query + 系统指令），建议在控制台调试面板中开启 `has_thoughts` 观察实际注入量，并权衡效果与成本。  
- 🔐 **安全第一**：反馈优化中上传的样例与评测数据仅用于本次计算，请务必脱敏处理 PII/敏感业务字段；自动优化过程不存储、不训练、不共享用户输入。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [use cases](../guides/use-cases.md)


