# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话的用户信息持久化与语义化管理能力，通过专用记忆模型自动提取关键事实、构建用户画像，并支持高精度语义检索与全生命周期管理，突破大模型上下文窗口限制，实现对用户偏好、习惯、历史交互等信息的持续感知与复用。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：默认启用 `autoCapture`（自动捕获）和 `autoRecall`（自动召回），无需显式调用工具即可在对话中自动写入记忆片段（如“用户常订咖啡”）、并在后续轮次中将相关记忆注入 Prompt，增强个性化响应能力。  
- **OpenClaw 等插件集成场景**：通过安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件并配置 `apiKey` 和 `userId`，Agent 可直接使用 `memory_search`、`memory_store` 等内置工具完成记忆操作，实现开箱即用的记忆增强。  
- **自研高代码应用**：通过统一 HTTP API（`https://dashscope.aliyuncs.com/api/v2/apps/memory/`）或 Python SDK（`agentscope-runtime>=1.1.5`）调用 `AddMemory`、`SearchMemory` 等接口，灵活控制记忆写入时机、检索策略与数据结构。  
- **用户画像构建场景**：结合 `CreateProfileSchema` 定义结构化模板（如 `{age: number, occupation: string, interests: array}`），再调用 `AddMemory` 指定 `profile_schema` 参数，系统将按规则抽取并归一化属性，最终通过 `GetUserProfile` 获取标准化画像摘要。  
- **RAG 增强场景**：长期记忆作为独立于知识库的“用户专属知识层”，与 RAG 的文档知识正交互补——前者聚焦个体行为与偏好（如“张三过敏花生”），后者覆盖通用领域知识（如“花生过敏症状”），二者可协同注入模型输入。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `user_id` | string | 是 | — | 用户唯一标识（≤64 字符），用于严格隔离不同用户的记忆空间；建议使用业务侧稳定 ID（如 `uid_12345`），避免临时 token。 |
| `messages` | array | 否（与 `custom_content` 互斥） | — | 对话消息列表，每条含 `role`（`user`/`assistant`）和 `content`；最多 50 条（单轮问答计为 2 条）；内容将被记忆模型解析生成结构化记忆。 |
| `custom_content` | string | 否（与 `messages` 互斥） | — | 纯文本内容（≤512 字符），绕过对话解析逻辑，直接存为原始记忆片段，适用于已预处理的结构化信息（如日程提醒文本）。 |
| `memory_library_id` | string | 否 | 默认记忆库 | 记忆库存储位置 ID（≤32 字符）；可用于多租户隔离、A/B 测试或冷热数据分层；需在控制台创建后获取。 |
| `profile_schema` | string | 否 | — | 用户画像模板 ID；仅当需结构化抽取时填写，否则按通用记忆规则处理。 |
| `top_k` | integer | 否 | `10`（API） / `5`（插件） | `SearchMemory` 返回的最大结果数（范围 1–100）；建议根据下游 Prompt 容量合理设置（如 `top_k=3` 避免超长输入）。 |
| `min_score` | double | 否 | `0.3`（API） / `0`（插件，单位为 0–100） | 相似度阈值（[0,1] 区间）；低于此值的结果被过滤；调高可提升精度，调低可增加召回率。 |
| `expire_time` | string | 否 | `180d`（默认规则） | 记忆片段有效期，格式为 `Nd`（如 `7d`、`30d`、`180d`、`never`）；**强烈建议显式配置**，避免数据无限累积。 |

> ⚠️ 注意：`min_score` 在 API 中为 `[0,1]` 小数，在 OpenClaw 插件中为 `[0,100]` 整数，调用时需按实际接口规范转换。

## 面向开发者，简洁实用

- **快速起步**：优先使用 Python SDK（`agentscope-runtime`），避免手动构造 HTTP 请求；`AddMemory` 和 `SearchMemory` 已封装为异步工具，开箱即用。  
- **性能优化**：`SearchMemory` 平均延迟 200–500ms，建议在 Agent 规划阶段异步触发，避免阻塞主推理流；`AddMemory` 为异步写入，不影响当前响应。  
- **数据治理**：长期记忆存储免费，但其内容注入 Prompt 后产生的 [Token](token.md) 不额外计费；需自行管理生命周期——通过 `expire_time` 或定期调用 `DeleteMemory` 清理过期数据。  
- **调试技巧**：在百炼控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list) 页面可实时查看记忆片段、测试语义搜索效果、验证画像抽取结果，无需编码即可验证逻辑。  
- **错误排查**：常见失败原因包括 `user_id` 超长、`messages.content` 超 512 字符、`Authorization` Header 缺失或无效；所有接口返回标准 HTTP 状态码与 JSON 错误体，建议捕获 `400`（参数错误）、`401`（鉴权失败）、`429`（限流）并重试。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)


