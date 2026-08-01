# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，通过专用记忆模型自动从对话中提取关键信息生成语义化记忆片段，并支持增删改查、语义检索与用户画像建模，实现跨会话、跨请求的上下文延续与个性化服务。

## 在百炼平台的不同场景中如何使用

- **通用 API 集成**：直接调用 `/api/v2/apps/memory/` 下的 `AddMemory`、`SearchMemory` 等接口，适用于自研 Agent、工作流后端或第三方系统。支持传入对话历史（`messages`）或纯文本（`custom_content`），自动解析为结构化记忆；检索时以自然语言查询触发语义匹配，结果可注入 Prompt 提升回复连贯性。

- **OpenClaw 插件（智能体 2.0）**：启用 `autoCapture` 和 `autoRecall` 后，在 `agent_end` 和 `before_agent_start` 钩子中自动完成记忆写入与召回，无需手动编码。插件默认使用 `top_k=5`、`min_score=0.3`，支持通过配置项调整召回策略，适合快速构建具备“记忆感知”的对话型智能体。

- **用户画像建模**：通过 `CreateProfileSchema` 定义结构化字段（如 `age`, `preferred_language`, `fitness_goal`），在 `AddMemory` 中指定 `profile_schema` 参数，即可从对话中精准抽取并持久化固定属性，适用于需要强约束建模的客服、健康助手等场景。

- **工作流与高代码应用**：虽当前 LLM Application 层暂不原生集成长期记忆（仅支持短期记忆 0–30 轮），但可通过 SDK 或 HTTP 调用在节点逻辑中主动调用记忆 API，将 `SearchMemory` 结果作为变量输入下游节点，实现定制化记忆增强流程。

> ⚠️ 注意：Managed Agents 当前未内置长期记忆自动捕获机制，需开发者在会话事件流中自行判断时机调用记忆 API。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | `string` | 是 | 用户唯一标识，最大 64 字符；所有操作均以此隔离数据空间 | 使用业务侧用户 ID（如 `uid_12345`） |
| `memory_library_id` | `string` | 否 | 指定记忆库 ID；不传则使用默认库（控制台可创建/管理） | 生产环境建议显式指定，便于分库治理 |
| `project_id` | `string` | 否 | 记忆片段规则 ID（控制台配置）；影响提取逻辑与有效期 | 默认规则为 `default`，自定义规则需提前创建 |
| `profile_schema` | `string` | 否 | 用户画像模板 ID；仅当需结构化抽取时传入 | 需先调用 `CreateProfileSchema` 创建 |
| `top_k` | `integer` | 否（SearchMemory） | 检索返回最大条数 | 通用场景建议 `3–10`；OpenClaw 插件默认 `5` |
| `min_score` | `double` | 否（SearchMemory） | 相似度阈值，范围 `[0.0, 1.0]`；低于此值的结果被过滤 | 初始建议 `0.3–0.5`，可根据召回质量调优 |
| `meta_data` | `object` | 否 | 自定义 JSON 元数据，用于分类、标签或业务上下文透传 | 如 `{"source": "chat", "priority": "high"}` |

- **有效期配置**：记忆默认有效期为 180 天（控制台可设为 7/30/180 天或永不过期），无自动失效机制，业务侧需结合 `ListMemory` + `DeleteMemory` 主动清理过期数据。
- **内容限制**：
  - `custom_content` ≤ 512 字符；
  - `messages` 最多 50 条（role/content 对）；
  - 单次 `AddMemory` 请求仅生成一个记忆片段（非批量）。

## 开发者提示

- ✅ **首选 SDK**：使用 `agentscope-runtime>=1.1.5`，封装了 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory`，减少 HTTP 封装成本；`UpdateMemory` 需手动调用 PATCH 接口。
- ✅ **认证方式**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 请从 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取。
- ✅ **错误处理**：关注 `400`（参数超限/格式错误）、`404`（schema 或 memory_node_id 不存在）、`429`（限流）响应；`AddMemory` 单独限流 120 QPM，`SearchMemory` 300 QPM。
- ❌ **避免陷阱**：
  - 不要混用 `messages` 和 `custom_content`（互斥）；
  - `user_id` 为空或超长将直接失败；
  - `SearchMemory` 的稳定 endpoint 为 `/api/v2/apps/memory/memory_nodes/search`（非 `/search`）；
  - `profile_schema` 仅在 `AddMemory` 中生效，且必须已存在，否则报错。

> 提示：首次集成建议先用 `AddMemory` 写入测试数据，再用 `SearchMemory` 查询验证语义效果，最后结合 `meta_data` 和 `min_score` 迭代优化召回精度。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)


