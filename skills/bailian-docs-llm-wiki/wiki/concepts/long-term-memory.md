# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户信息管理能力，用于突破大模型上下文窗口限制，实现跨会话、跨请求的语义化信息存储与智能召回。它不依赖大模型实时推理，而是通过专用记忆服务自动提取、索引和检索关键事件（记忆片段）与结构化属性（用户画像），为智能体、RAG 应用及高代码服务提供可编程的“外部大脑”。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）**：通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件启用全自动捕获（`autoCapture`）与注入（`autoRecall`）——对话结束时自动提炼记忆，新对话开始前自动检索并注入相关记忆到系统提示词或消息上下文，显著提升个性化与连贯性。也可在工具调用链中主动使用 `memory_search` / `memory_store` 等标准工具进行精准控制。

- **RAG 应用与工作流**：作为知识增强的补充维度，长期记忆可与知识库（RAG）协同：RAG 提供领域静态知识，长期记忆提供用户动态偏好（如“用户讨厌咖啡因”“常出差至深圳”），二者联合注入 Prompt，实现更精准的意图理解与响应生成。

- **高代码应用（Python/Serverless）**：直接调用统一 REST API（`https://dashscope.aliyuncs.com/api/v2/apps/memory/`）或 `agentscope-runtime` SDK，实现细粒度记忆生命周期管理（增删改查、分页列表、语义搜索），适用于需自定义记忆策略、多租户隔离或与业务数据库联动的场景。

- **OpenClaw 等 Agent 框架集成**：以插件形式嵌入，仅需配置 `apiKey` 和 `userId` 即可启用，无需修改核心逻辑；支持 `top_k` 和 `similarity_threshold` 参数调节召回精度，适配不同敏感度场景（如医疗咨询需高阈值，闲聊推荐可放宽）。

- **记忆库统一管理**：所有能力基于“记忆库”（Memory Library）抽象，支持多应用共享同一记忆库，或为不同业务线配置独立记忆库（通过 `memory_library_id` 隔离），实现资源复用与权限管控。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 场景 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），**所有接口必需**，用于严格隔离记忆空间。建议使用业务系统中的稳定 ID（如 `uid_123456`），避免使用临时 token。 | 全场景 |
| `memory_library_id` | string | 否 | 目标记忆库 ID（≤32 字符）。未传则使用默认记忆库；生产环境强烈建议显式指定，便于监控、限流与迁移。可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 | 全场景 |
| `profile_schema` | string | 否 | 用户画像 Schema ID。配合 `CreateProfileSchema` 使用，用于触发结构化字段（如 `age`, `preference`）的自动抽取与存储。 | 用户画像场景 |
| `messages` / `custom_content` | array / string | 互斥必填（AddMemory） | `messages`：最多 50 条对话记录（`[{role:"user",content:"..."},{role:"assistant",content:"..."}]`），系统自动提取事件；`custom_content`：≤512 字符纯文本，优先级更高，适合精确写入（如“生日：2025-03-15”）。 | 写入记忆 |
| `top_k` | integer | 否（SearchMemory） | 检索返回条数，默认 10（API）或 5（OpenClaw 插件），取值范围 1–100。建议根据下游处理能力设置（如注入 Prompt 建议 ≤5）。 | 检索记忆 |
| `min_score` / `similarity_threshold` | double (0.0–1.0) | 否（SearchMemory） | 语义相似度阈值，默认 0.3（API）或 0.5（OpenClaw 插件）。值越高召回越严格，推荐从 0.4 起调优；注意 OpenClaw 插件文档中单位为 0–100（即 `0.4` = `40`）。 | 检索记忆 |
| `expiration_time` | integer (seconds) | 否 | 记忆片段有效期（秒）。**重要**：默认规则为 180 天（非“永不过期”），建议显式设置（如 `2592000` = 30 天）以符合数据合规要求。可通过控制台修改记忆库规则或 API 中指定 `project_id` 绑定规则。 | 写入记忆（推荐显式配置） |
| `meta_data` | object | 否 | 自定义元数据（如 `{"source": "chat", "priority": "high"}`），支持 JSON 对象，用于后续条件过滤或审计追踪。 | 高级管理 |

> ⚠️ 注意：`project_id`（记忆片段规则 ID）为可选参数，不传时自动选用记忆库默认规则；`UpdateMemory` 当前无 SDK 封装，需直接调用 PATCH REST API。

## 面向开发者，简洁实用

- **快速上手**：只需 `user_id` + `messages` 或 `custom_content`，一行代码调用 `AddMemory` 即可开启记忆；`SearchMemory` 传入当前用户问题（`query`）或对话上下文（`messages`），立即获得语义匹配结果。
- **零模型依赖**：所有提取、索引、检索均由平台后端专用服务完成，无需调用 `qwen-*` 模型，无额外 token 成本与延迟。
- **强一致性保障**：记忆写入后立即可搜，无最终一致性延迟；删除操作（`DeleteMemory`）即时生效。
- **生产就绪**：
  - 限流明确：全局 3000 QPM，`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM；
  - 数据持久：记忆长期保留（按 `expiration_time` 自动清理），无隐式过期风险；
  - 安全合规：`user_id` 隔离 + 可配置有效期 + 元数据支持审计，满足 GDPR/等保基础要求。
- **调试建议**：
  - 初期用 `ListMemory?user_id=xxx` 查看已存内容；
  - 检索不准时，先检查 `min_score` 是否过高，再尝试用 `custom_content` 替代 `messages` 测试提取质量；
  - 集成 OpenClaw 时，优先使用插件而非裸 API，大幅降低接入成本。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application support](../guides/application-support.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


