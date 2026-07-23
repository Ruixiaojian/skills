# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，用于突破大模型单次会话的上下文窗口限制，实现跨会话、跨应用的用户偏好、习惯、意图与关键事件的自动沉淀、语义检索与动态更新。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为个性化基础能力，长期记忆可被 Agent 主动调用（如通过 `memory_search` 工具），或由 OpenClaw 等框架自动注入（启用 `autoRecall` 后，在会话开始前将匹配的记忆片段作为系统提示补充）。适用于需记住用户历史指令（如“我常点辣子鸡”）、待办事项（如“明天10点开会”）或设备偏好（如“默认用蓝牙耳机播放”）的对话型智能体。

- **工作流（Workflow）应用**：可通过「记忆检索」节点接入 `SearchMemory` 接口，在流程中按需召回用户画像或历史事件，驱动条件分支（例如：若 `GetUserProfile` 返回 `occupation == "医生"`，则启用医学术语优化提示词）。

- **高代码应用**：开发者可直接集成 `agentscope-runtime` SDK 或调用 REST API，在自定义服务逻辑中完成记忆的写入（`AddMemory`）、聚合（`GetUserProfile`）与清理（`DeleteMemory`），实现与业务系统深度耦合的记忆生命周期管理（如订单完成后自动归档用户服务诉求）。

- **RAG 增强场景**：长期记忆可与知识库协同使用——知识库承载通用/静态知识（如产品文档），长期记忆承载个性化/动态信息（如用户上次咨询的订单号），二者在推理时分层注入，提升响应精准度与亲和力。

- **Managed Agents 沙箱环境**：虽不直接内置记忆能力，但可通过调用外部长期记忆 API，在 Bash 工具脚本或 Python 代码中读写 `user_id` 关联的记忆，实现沙箱内任务与用户长期状态的联动（例如：分析完销售数据后，自动将结论存为用户记忆：“已为您生成2024Q3销售趋势报告”）。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 实用建议 |
|--------|------|------|------|----------|
| `user_id` | `string` | 是 | 用户唯一标识（≤64 字符），所有操作均以此隔离数据空间。同一用户不同设备/会话应复用相同 `user_id`。 | 建议使用业务侧用户主键（如 `uid_12345`），避免使用临时 token 或 session_id。 |
| `messages` / `custom_content` | `array` / `string` | 互斥必填 | `messages`：传入最多 50 条对话消息，由平台自动提取关键事件；`custom_content`：直接传入 ≤512 字符的纯文本（绕过解析，适合结构化摘要）。 | 对话类场景优先用 `messages`；已预处理的结构化数据（如 JSON 序列化后的偏好设置）用 `custom_content` 更高效。 |
| `memory_library_id` | `string` | 否 | 目标记忆库 ID（≤32 字符）。不填则使用默认记忆库。可在控制台「记忆库列表」获取。 | 多租户或多业务线场景建议显式指定，便于权限隔离与配额管理。 |
| `project_id` | `string` | 否 | 记忆片段提取规则 ID。不填则使用记忆库默认规则。规则决定如何从对话中提炼事件（如是否忽略问候语、如何识别时间表达式）。 | 新建业务时建议创建专属 `project_id` 并配置定制化规则，避免与默认规则冲突。 |
| `profile_schema` | `string` | 否 | 用户画像模板 ID。传入后触发结构化字段抽取（如 `age`, `preference`），结果可通过 `GetUserProfile` 获取。 | 需先调用 `CreateProfileSchema` 定义模板；适用于需要固定字段的 CRM、会员系统等场景。 |
| `top_k` | `integer` | 否（`SearchMemory`） | 检索返回的最大条数，默认 `10`，范围 `1–100`。 | 生产环境推荐设为 `3–5`：兼顾召回率与模型输入长度，避免噪声干扰。 |
| `min_score` / `similarity_threshold` | `double` | 否（默认 `0.0`） | 相似度阈值，范围 `[0.0, 1.0]`；低于此值的结果被过滤。 | 初期调试建议设 `0.5`，稳定后可升至 `0.6–0.7` 提升精度；设 `0.0` 可用于调试全量召回结果。 |
| `meta_data` | `object` | 否 | 自定义 JSON 对象，支持任意键值对（如 `{"channel": "wechat", "device": "ios"}`），用于后续过滤或分析。 | 建议统一约定 key 命名（如全部小写+下划线），避免嵌套过深（≤3 层）。 |

> ⚠️ 注意：`UpdateMemory` 当前**未被 `agentscope-runtime` SDK 封装**，需直接调用 REST API 的 `PATCH /api/v2/apps/memory/update`。其他 CRUD 操作均有 SDK 异步封装，推荐优先使用。

## 面向开发者，简洁实用

- **快速起步**：安装 `agentscope-runtime>=1.1.5`，设置 `DASHSCOPE_API_KEY` 环境变量，即可用 3 行代码添加记忆：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory
  await AddMemory(user_id="user_001", messages=[{"role":"user","content":"帮我订明早8点的咖啡"}])
  ```

- **检索即用**：搜索时无需构造复杂 query，直接传自然语言问题（如 `"我之前订过什么？"`），平台自动做语义理解与匹配。

- **无过期陷阱**：记忆本身**无内置有效期**，其生命周期完全由 `project_id` 关联的规则控制（如默认规则设为 180 天）。如需永久保存，创建规则时将过期时间设为 `0`。

- **性能预期**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；高并发场景注意配额限制（`SearchMemory` ≤ 300 QPM/账号）。

- **错误排查**：常见失败原因包括 `user_id` 超长、`messages` 格式错误、API Key 权限不足。所有接口均返回标准 HTTP 状态码与 `error_code`，建议捕获 `429`（限流）、`401`（鉴权失败）并重试。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)


