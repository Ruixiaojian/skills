# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，通过专用记忆引擎自动从对话中提取关键事实与偏好，构建可检索、可更新的用户画像与记忆片段，突破大模型上下文窗口限制，实现跨会话、跨应用的连续性智能交互。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在 Agent 2.0 中，长期记忆作为独立能力模块接入，支持在会话开始前自动召回（`autoRecall`）相关记忆片段或用户画像，并注入系统提示词；也可在对话结束后触发 `autoCapture`，将 `messages` 自动提炼为结构化记忆。适用于个性化推荐、习惯追踪、多轮任务状态保持等场景。

- **工作流（Workflow）应用**：可通过“记忆检索”节点调用 `SearchMemory` 接口，在任意流程节点中以自然语言查询历史信息（如“用户上次预约的时间”），结果作为变量输入下游节点；也可通过“记忆写入”节点调用 `AddMemory`，将工作流中生成的关键结论（如订单确认、服务承诺）持久化存储。

- **Managed Agents（托管智能体）**：虽不内置自动记忆集成，但开发者可在 `input` 消息中显式注入 `SearchMemory` 返回的记忆内容，或将 `tool_output` 中的关键状态通过 `AddMemory` 主动写入；结合沙箱文件操作，可实现记忆与本地状态（如临时分析结果）的协同管理。

- **插件集成（OpenClaw）**：通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件一键启用全局记忆能力，所有 Agent 共享同一记忆空间，自动完成捕获与召回，无需修改业务逻辑代码，适合快速落地标准化客服、助手类应用。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `user_id` | string | 是 | — | 用户唯一标识（≤64 字符），决定记忆隔离边界；不同 `user_id` 数据完全不可见 |
| `memory_library_id` | string | 否 | 默认记忆库 ID | 记忆库 ID，用于多租户/多业务线隔离；需在控制台创建并获取 |
| `project_id` | string | 否 | 默认规则 ID | 记忆片段提取规则 ID，控制从 `messages` 中抽取哪些信息（如“提取健康目标”“识别旅行偏好”） |
| `profile_schema` | string | 否 | — | 用户画像 Schema ID，定义结构化字段（如 `age`, `diet_preference`），启用后自动填充 |
| `top_k` | integer | 否 | `10`（API） / `5`（SDK/插件） | `SearchMemory` 返回的最大条数，范围 1–100 |
| `min_score` | double | 否 | `0.3`（API） / `0`（插件） | 相似度阈值（0–1），低于此值的结果被过滤；建议生产环境设为 ≥0.4 提升精度 |
| `custom_content` | string | 互斥必填（与 `messages`） | — | 直接写入的结构化文本（≤512 字符），适用于预置知识、人工标注等场景 |
| `messages` | array | 互斥必填（与 `custom_content`） | — | 对话消息数组（最多 50 条），每轮 `user`+`assistant` 计为 2 条；内容总长度受协议层隐式约束 |

> ⚠️ 注意：  
> - `AddMemory` 的 `meta_data` 字段为**全量覆盖写入**，`UpdateMemory` 的 `meta_data` 为**增量更新**；  
> - 记忆默认有效期为 **180 天**（非永久），可在控制台规则配置中调整为 7 天、30 天或永不过期；  
> - `user_id` 与 `memory_library_id` 共同构成数据隔离域，跨库同 `user_id` 数据不可互通。

## 开发者提示

- **优先使用 SDK**：Python 推荐 `agentscope-runtime>=1.1.5`，已封装 `AddMemory`/`SearchMemory`/`ListMemory`/`DeleteMemory`；`UpdateMemory` 需手动 `PATCH` 调用。
- **认证统一**：所有接口均需 `Authorization: Bearer $DASHSCOPE_API_KEY`，Base URL 固定为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。
- **限流管控**：阿里云账号级配额——总 QPM ≤3000，`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM；高并发场景请做好客户端降级与重试。
- **避免常见错误**：勿混用 `messages` 与 `custom_content`；勿在 `user_id` 中使用特殊字符（建议仅用字母、数字、下划线）；`projectId` 错误会导致提取失败且无明确报错，建议先调用 `ListProjectRules` 确认可用 ID。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)


