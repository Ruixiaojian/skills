# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨任务的上下文感知与历史信息复用。它通过自动提取对话中的关键事实（记忆片段）或结构化属性（用户画像），以向量+规则融合方式存储，并支持语义检索与全生命周期管理。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为上下文增强的核心组件，长期记忆在每次会话开始前自动召回相关历史（如用户偏好、待办事项、会议约定），供大模型在规划与响应中引用；配合 `autoRecall`/`autoCapture` 机制，可实现“无感记忆注入”，无需开发者手动拼接上下文。
  
- **工作流（Workflow）应用**：通过显式调用 `SearchMemory` 或 `GetUserProfile` 工具节点，在流程中按需检索记忆（例如：“查询该用户最近3次订单地址”），将结构化结果注入后续节点变量，驱动条件分支或内容生成。

- **高代码应用（Rich Code）**：开发者可直接集成 `modelstudio-memory` SDK 或调用 REST API，在自定义 Python 服务中实现细粒度记忆控制——例如，在文件处理后自动提取合同主体信息并写入画像，在多轮审批流中动态更新任务状态记忆。

- **Managed Agents（托管智能体）**：虽其自身依赖沙箱环境维持短期执行状态，但长期记忆可作为外部状态中枢，为同一 `user_id` 下多次独立 Agent 会话提供一致的背景知识（如“该用户禁用短信通知”），弥补沙箱隔离导致的状态割裂问题。

> ✅ 提示：所有场景均以 `user_id` 为隔离边界，不同用户记忆完全独立；默认记忆库开箱即用，无需额外开通。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作的作用域锚点；建议使用业务系统 ID（如 `uid_12345`），避免使用临时 token。 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：对话数组（最多 50 条，一问一答计 2 条），用于自动提取；`custom_content`：纯文本（≤512 字符），绕过提取直接存为原始记忆。二者共存时优先使用 `custom_content`。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；不传则使用默认库；可在控制台「记忆库」页面创建并获取。 |
| `project_id` | string | 否 | 记忆片段提取规则 ID；用于指定不同业务场景的提取逻辑（如“客服规则” vs “销售线索规则”）；不传则使用默认规则。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需结构化抽取（如年龄、职业）时传入，需先调用 `CreateProfileSchema` 创建。 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"source": "app_ios", "priority": 2}`），用于分类、过滤与审计；在 `AddMemory`/`UpdateMemory` 中写入，`ListMemory` 返回时携带。 |
| `top_k`（SearchMemory） | integer | 否 | 检索返回最大条数，默认 `10`（API）或 `5`（部分 SDK），取值范围 `1–100`；生产环境建议设为 `3–8` 平衡精度与性能。 |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值，默认 `0.3`（API）或 `0`（部分文档），范围 `[0,1]`；设为 `0.5` 可显著减少噪声召回。 |

> ⚠️ 注意：  
> - `UpdateMemory` 接口暂未封装进 Python SDK，需直接调用 REST API（PATCH `/memory_nodes/{id}`）；  
> - 默认记忆片段有效期为 180 天，可在控制台「记忆库 → 规则详情」中修改为 `7`/`30`/`180` 天或 `永不过期`；  
> - 所有接口共享阿里云账号级限流：合计 ≤ 3000 QPM，其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。

## 面向开发者，简洁实用

- **快速上手三步走**：  
  1. 确保请求头含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`；  
  2. 调用 `AddMemory` 写入（推荐传 `messages`，让平台自动提取）；  
  3. 在下一次会话前，用 `SearchMemory` + 当前用户 query 检索，结果直接注入 [prompt](../guides/prompt.md) 或传给工具。

- **最佳实践建议**：  
  - ✅ 对敏感信息（如手机号、身份证号）启用 `meta_data` 标记 `{"sensitive": true}`，便于后续审计或脱敏处理；  
  - ✅ 检索时始终设置 `min_score ≥ 0.4`，避免低质量召回干扰模型推理；  
  - ✅ 避免高频写入：单 `user_id` 下 `AddMemory` 建议间隔 ≥ 1 秒，防止触发限流；  
  - ✅ 控制台是调试第一入口：在「记忆库 → 记忆检索」标签页实时验证召回效果，调整 `top_k` 和规则即可生效，无需改代码。

- **SDK 与 API 选择指南**：  
  - 日常开发优先使用 `agentscope_runtime.tools.modelstudio_memory` 中的封装类（如 `SearchMemory`, `AddMemory`）；  
  - 需要 `UpdateMemory` 或精细控制字段时，直接调用 REST API（Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`）；  
  - OpenClaw 用户可一键安装插件 `@modelstudio/modelstudio-memory-for-openclaw`，自动启用记忆捕获与召回。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


