# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户状态管理能力，用于突破大模型上下文窗口限制，实现跨会话、跨应用的用户偏好、习惯、任务、属性等关键信息的自动提取、语义存储与智能召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）**：作为核心上下文增强源，替代部分短期记忆容量；可通过 `autoRecall` 插件在对话开始前自动检索并注入相关记忆片段（如“用户忌口花生”），或由 Agent 主动调用 `memory_search` 工具进行按需查询。  
- **工作流（Workflow）**：在「大模型」节点配置中启用「长期记忆」开关，指定 `user_id` 后，系统自动执行 `SearchMemory` 并将结果注入提示词上下文，支持基于历史行为的流程分支决策（如“若用户曾投诉物流，则跳转客服工单节点”）。  
- **高代码应用 / 自定义服务**：通过 HTTP API 或 Python SDK 直接集成，实现精细化控制——例如在订单履约服务中，调用 `AddMemory` 记录用户特殊配送要求（`custom_content: "请放物业柜，短信通知"`），后续履约节点再通过 `SearchMemory` 实时获取。  
- **OpenClaw 框架**：通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件一键启用 `autoCapture`（对话结束自动提炼）与 `autoRecall`（对话启动前自动注入），无需修改业务逻辑即可获得长期记忆能力。  
- **用户画像构建**：配合预定义的 `profile_schema`（如“健康档案”Schema），从对话中结构化抽取年龄、过敏史、运动频率等字段，生成可复用、可查询、可更新的动态用户画像，供多应用共享。

> ⚠️ 注意：长期记忆与短期记忆（0–30 轮对话历史）完全独立——前者持久化存储于专用记忆库，后者仅保留在单次会话的请求上下文中，不落盘、不跨会话。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 常用值 |
|--------|------|------|------|--------|
| `user_id` | string | ✅ | 用户唯一标识符（≤64 字符），用于数据隔离与归属。同一 `user_id` 下所有记忆自动聚合。 | `"u_123456"` |
| `memory_library_id` | string | ❌ | 目标记忆库 ID（≤32 字符）。不传则使用账号默认记忆库。可在控制台「记忆库」列表页获取。 | `"mlib_default"` |
| `project_id` | string | ❌ | 记忆片段规则 ID。不传则使用记忆库的默认规则。决定内容提取逻辑（如是否启用去重、时效策略）。 | `"rule_daily_reminder"` |
| `profile_schema` | string | ❌（仅画像场景） | 用户画像 Schema ID。传入后触发结构化属性抽取（需提前通过 `CreateProfileSchema` 创建）。 | `"schema_health_profile"` |
| `custom_content` | string | ✅（与 `messages` 互斥） | 纯文本自定义内容（≤512 字符），优先级高于 `messages`，适用于已明确语义的输入。 | `"用户每周三晚 8 点线上健身"` |
| `messages` | array | ✅（与 `custom_content` 互斥） | 最多 50 条对话记录（role/content 格式），由平台自动提炼关键事件。推荐用于自然对话流。 | `[{"role":"user","content":"帮我订明早 9 点的会议室"}]` |
| `meta_data` | object | ❌ | 用户自定义元数据（键值对），用于业务标签、分类、来源追踪等，写入后在 `ListMemory` 中透出。 | `{"category": "reminder", "source": "agent_v2"}` |
| `top_k` | integer | ❌（默认 10） | `SearchMemory` 返回的最大条数（1–100）。建议设为 3–10，兼顾召回率与性能。 | `5` |
| `min_score` | double | ❌（默认 0.3） | `SearchMemory` 相似度阈值 [0.0, 1.0]。低于此值的结果被过滤。生产环境建议设为 `0.5–0.7` 提升精度。 | `0.6` |

> 💡 提示：`custom_content` 和 `messages` 严格互斥；若同时传入，`custom_content` 优先生效。`min_score` 单位为小数（0.0–1.0），非百分制（如文档中出现的 `minScore: 60` 是旧 CLI 示例，实际 API 使用 `min_score: 0.6`）。

## 面向开发者，简洁实用

- **快速上手**：只需配置 `DASHSCOPE_API_KEY` 环境变量，调用 `https://dashscope.aliyuncs.com/api/v2/apps/memory/add` 即可写入第一条记忆。
- **SDK 推荐**：生产环境使用 `agentscope-runtime>=1.1.5`，封装了 `AddMemory`/`SearchMemory`/`ListMemory`/`DeleteMemory`；`UpdateMemory` 需自行 `PATCH` 调用（参考 API 文档）。
- **性能预期**：`AddMemory` 延迟约 500–1000ms，`SearchMemory` 约 200–500ms；QPM 限流为账号级总和 ≤3000（`AddMemory` ≤120，`SearchMemory` ≤300）。
- **生命周期管理**：记忆**永不过期**，无自动清理机制。业务方需主动调用 `DeleteMemory` 或设计定时清理逻辑（如按 `meta_data.category` 批量删除过期提醒）。
- **调试技巧**：使用 `ListMemory?user_id=xxx&top_k=20` 快速查看某用户全部记忆；结合 `meta_data` 过滤 + `SearchMemory` 验证语义召回效果。
- **避坑指南**：
  - 不要硬编码 `model.id` 到记忆逻辑中（记忆本身模型无关）；
  - `UpdateMemory` 的 `timestamp` 参数单位为**秒级 Unix 时间戳**（非毫秒）；
  - OpenClaw 的 `autoRecall` 注入内容默认以 `<memory>` 标签包裹，提示词中需预留对应占位符。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


