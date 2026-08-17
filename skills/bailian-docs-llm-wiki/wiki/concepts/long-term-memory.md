# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话用户状态持久化能力，通过自动从对话中提取关键事件（记忆片段）和结构化属性（用户画像），实现语义化存储与高精度检索，使智能体具备持续理解用户偏好、历史行为与上下文的能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在 Agent 2.0 中，长期记忆作为可规划的“工具”被统一调度。对话结束时自动调用 `AddMemory` 持久化关键信息；新会话开始前或用户提问时，通过 `SearchMemory` 检索相关记忆，并将结果注入系统提示或历史消息，显著增强上下文连贯性与个性化响应能力。OpenClaw 等框架支持插件式自动捕获与召回，无需手动编码。
  
- **工作流（Workflow）应用**：虽不内置自动记忆机制，但可通过「HTTP 调用」节点集成长期记忆 API，在关键节点（如用户确认偏好后、任务完成时）显式写入 `custom_content` 或触发画像更新，再于后续步骤中检索，实现流程驱动的记忆闭环。

- **高代码应用**：开发者可直接使用 `agentscope-runtime>=1.1.5` SDK 中的 `AddMemory`、`SearchMemory` 等异步工具类，在自定义 Python 逻辑中灵活控制记忆的写入时机、内容粒度与检索策略，适配复杂业务规则（如仅保存付费用户行为、按标签过滤记忆）。

- **Managed Agents（托管智能体）**：长期记忆独立于沙箱运行环境，为托管会话提供外部状态支撑。例如，在多步文件处理任务中，可将用户对某份 PDF 的标注偏好（如“重点关注财务数据”）存为记忆片段，后续会话中自动召回并指导模型聚焦解析。

- **API 直接调用（Application Call）**：当通过 DashScope API 调用已发布应用时，长期记忆不参与 `session_id` 管理（该机制仅维护短期对话轮次），但可在应用内部逻辑中主动调用记忆 API，实现“一次配置、全局生效”的用户状态复用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 实际建议 |
|------|------|------|------|----------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于严格隔离不同用户的记忆空间。同一用户所有操作必须保持一致。 | 使用业务侧稳定的用户 ID（如 `uid_123456`），避免使用临时会话 ID。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）。不传则使用账号默认库；多应用共享时建议显式指定统一库 ID。 | 生产环境推荐显式传入，便于权限管控与监控。 |
| `messages` / `custom_content` | array / string | 互斥 | `messages`：最多 50 条对话消息（一问一答计为 2 条），由平台自动提取关键信息；`custom_content`：≤512 字符纯文本，优先级更高，适合写入结构化摘要或明确指令。 | 对话质量高时用 `messages`；需强控内容或补充元信息时用 `custom_content`。 |
| `profile_schema` | string | 否 | 用户画像模板 ID，需预先通过 `CreateProfileSchema` 创建并发布。仅当需结构化抽取（如年龄、职业）时传入。 | 模板设计应精简（≤10 字段），避免语义重叠；首次调用前务必确认模板已启用。 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"category": "reminder", "source": "agent_v2"}`），支持后续按条件过滤与分析。 | 建议约定统一 key 名（如 `category`, `priority`, `source_app`），便于运营看板建设。 |
| `plan_version` | string | 否（`SearchMemory` 推荐必填） | 取值 `pro`（开启 Rerank，精度高）或 `lite`（关闭 Rerank，成本低），大小写不敏感。**该字段优先级最高，覆盖项目/规则级配置。** | 高价值场景（如客服决策）用 `pro`；高频轻量检索（如日程提醒）用 `lite`。 |
| `top_k` / `min_score` | integer / double | 否 | `SearchMemory` 专属：召回数量（1–100）、最小相似度（0.0–1.0）。建议 `top_k=5` + `min_score=0.3` 平衡覆盖率与噪声。 | 避免 `top_k > 20`，防止 Prompt 过长；`min_score < 0.2` 易引入无关噪声。 |
| `expired_in_days` | integer | 否 | 记忆片段有效期（天），不传则永不过期。支持动态设置（如 `30` 表示 30 天后自动失效）。 | 敏感信息（如验证码）设为 `1`；通用偏好设为 `180`；核心画像建议 `0`（永不过期）。 |

> ⚠️ 注意：`UpdateMemory` 的 `timestamp` 为秒级 Unix 时间戳（非毫秒）；`AddMemory` 无自动去重，重复内容需业务侧通过 `meta_data` 标记或 `ListMemory` + `DeleteMemory` 主动清理。

## 面向开发者，简洁实用

- **快速上手**：只需 `user_id` + `messages` 或 `custom_content` 即可调用 `AddMemory`；`SearchMemory` 传 `user_id` + 查询语句（如 `"我上次说要买什么？"`）即可返回相关片段。
- **SDK 优先**：强烈推荐使用 `agentscope-runtime`（≥1.1.5）封装的异步工具类，自动处理认证、重试与错误码映射，减少胶水代码。
- **注入 Prompt**：将 `SearchMemory` 返回的 `memory_nodes[].content` 拼接至系统提示词末尾（格式建议：`【过往记忆】${content}`），避免干扰原始指令。
- **成本可控**：`lite` 版本调用成本约为 `pro` 的 1/3；`SearchMemory` QPM 限流 300，若超限请增加本地缓存或降级为关键词匹配。
- **生命周期自主**：平台不提供自动过期，务必在业务逻辑中根据场景显式设置 `expired_in_days` 或定期调用 `DeleteMemory` 清理。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)


