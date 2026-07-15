# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，用于突破大模型单次会话的上下文窗口限制，实现跨会话、跨请求的用户偏好、关键事件与结构化属性的自动提取、语义检索与全生命周期管理。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是被动存储，而是主动参与智能体决策闭环的核心组件，其使用方式因应用范式而异：

- **智能体（Agent 2.0）应用**：作为“有状态智能体”的基石，通过 `memory_search` 等运行时工具在 `before_agent_start` 钩子中自动注入相关记忆，或由 Agent 主动调用 `AddMemory` / `SearchMemory` 实现个性化响应（如“您上周提到要学习 Python，需要我推荐课程吗？”）。OpenClaw [插件](plugin.md)可实现零代码接入，自动捕获对话中的事实并召回历史上下文。

- **工作流（Workflow）应用**：在节点编排中显式调用 `memory_store` 或 `memory_search` 工具，将流程中间结果写入长期记忆，或在条件分支前检索用户画像字段（如 `profile_schema="health_habits"`），驱动差异化路径执行。

- **高代码应用**：通过 `agentscope-runtime` SDK（≥1.1.5）直接集成，以编程方式控制记忆生命周期。例如，在 Python 函数中解析用户上传的体检报告后，调用 `AddMemory(user_id=uid, custom_content=summary, meta_data={"category": "health"})`；后续查询时传入 `meta_data={"category": "health"}` 进行精准过滤。

- **RAG 增强场景**：与知识库检索正交协同——知识库提供通用领域知识，长期记忆提供专属用户事实（如“张三对青霉素过敏”），二者可在提示词中融合注入，显著提升回答准确性与个性化程度。

- **Managed Agents 沙箱环境**：虽沙箱本身无状态，但可通过 `SearchMemory` 在会话启动时拉取用户历史配置（如“默认导出格式为 CSV”），再写入沙箱文件系统，实现“有状态行为”的模拟。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识符（≤64 字符），所有操作均以此为隔离边界，**不可为空或重复复用** | `"u_abc123"` |
| `messages` / `custom_content` | array / string | 互斥 | `messages`：自动提取（最多 50 条，一问一答计 2 条）；`custom_content`：直接写入文本（≤512 字符） | 优先用 `messages` 提升提取质量 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符），未传则使用默认库；可在控制台“记忆库”页获取 | 生产环境建议显式指定 |
| `project_id` | string | 否 | 记忆片段规则 ID，控制提取逻辑（如仅提取提醒类内容）；未传则使用默认规则 | 规则需在控制台预先配置 |
| `profile_schema` | string | 否 | 用户画像模板 ID，触发结构化字段抽取（如 `{"name":"string","age":"integer"}`） | 模板需先调用 `CreateProfileSchema` 创建 |
| `top_k` | integer | 否 | `SearchMemory` 返回最大条数（1–100），影响召回精度与延迟 | 3–10（默认 10） |
| `min_score` | double | 否 | 相似度阈值（0.0–1.0），低于此值的结果被过滤；**统一使用浮点值，非整数** | 0.5–0.7（默认 0.3） |
| `meta_data` | object | 否 | 自定义元数据（≤1 KB），支持后续按字段过滤（如 `{"source": "wechat", "priority": "high"}`） | 用于分类、权限或业务路由 |

> ⚠️ 注意：`profile_schema` 参数实际为**可选**，传入无效 ID 将静默忽略，不报错；`expire_at` 字段或控制台规则配置决定记忆有效期（支持 7/30/180 天或永不过期），**平台不提供自动过期清理，需开发者主动调用 `DeleteMemory` 管理生命周期**。

## 面向开发者，简洁实用

- **认证**：所有 API 请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **SDK 优先**：安装 `agentscope-runtime>=1.1.5`，直接使用封装类（如 `AddMemory`, `SearchMemory`），避免手写 HTTP 请求。
- **输入优化**：确保 `messages` 中 `role` 明确为 `"user"`/`"assistant"`，内容语义清晰（避免模糊指代），可显著提升自动提取准确率。
- **检索技巧**：搜索时优先使用自然语言查询（`query` 字段），而非 `messages` 数组；若需高精度匹配，结合 `meta_data` 过滤 + `min_score=0.65`。
- **限流应对**：账号级总 QPM ≤3000（`AddMemory` ≤120，`SearchMemory` ≤300），突发流量建议加本地缓存或队列削峰。
- **调试建议**：首次集成时，先用 `ListMemory` 查看已写入内容，确认 `user_id` 和 `meta_data` 是否符合预期；再测试 `SearchMemory` 的召回效果。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)


