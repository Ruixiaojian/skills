# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化记忆持久化与智能召回。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），并基于向量检索技术在后续交互中动态注入相关上下文，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，支持直接集成、SDK 调用及 OpenClaw 等框架插件化接入。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：支持从多轮对话消息中自动提取事件性、意图性内容（如“每天上午9点提醒我喝水”），也支持直接写入自定义文本（`custom_content` 字段）。默认启用自动去重与语义索引构建。  
- **用户画像（User Profile）**：基于预定义 Schema（字段名 + 描述）从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与异步更新。Schema 创建后需在 `AddMemory` 中显式传入 `profile_schema` ID 才触发抽取。  
- **全生命周期管理**：除基础的 `AddMemory` 和 `SearchMemory` 外，支持 `ListMemory`、`UpdateMemory`、`DeleteMemory` 及 `GetUserProfile` 等完整 CRUD 操作，详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **插件化集成**：为 OpenClaw 提供开箱即用的 `modelstudio-memory-for-openclaw` 插件，内置 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索）机制，并注册 `memory_search`、`memory_store` 等工具供 Agent 主动调用 —— 具体配置方式见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 2 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且控制台支持配置 7/30/180 天或永不过期。实际行为以控制台配置及 `AddMemory` 请求中 `expire_time` 参数为准，文档 2 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 记忆隔离的主键，不同 `user_id` 数据完全隔离；OpenClaw 插件中为必填项，SDK/API 中亦为必需字段。 |
| `messages` | array | 否（与 `custom_content` 二选一） | 对话消息数组，用于自动提取记忆片段；格式为 `[{role: "user"/"assistant", content: "..."}]`。 |
| `custom_content` | string | 否（与 `messages` 二选一） | 直接写入的原始文本内容，绕过自动提取逻辑。 |
| `memory_library_id` | string | 否 | 指定目标记忆库 ID；不填则使用默认记忆库（每个账号自带一个，不可删除）。 |
| `project_id` | string | 否 | 指定记忆片段规则 ID；不填则使用该记忆库下默认规则。 |
| `profile_schema` | string | 否 | 用户画像 Schema ID；仅当需触发画像抽取时必填。 |
| `meta_data` | object | 否 | 自定义元数据键值对，用于分类、过滤或业务标记（如 `"location_name": "北京"`）。 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数；OpenClaw 插件中默认为 5，建议设为 3–10 平衡效果与性能。 |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（默认 0.0 / 0.5） | 检索相似度阈值；文档 1 控制台推荐 0.5–0.7，文档 3 CLI 默认为 0（即无阈值），实际应按业务精度要求调整。 |

## 使用方式

1. **API 直接调用**：配置 `DASHSCOPE_API_KEY` 环境变量后，通过 HTTP 请求调用标准 REST API（如 `POST /api/v2/apps/memory/add`）。所有接口均支持 cURL 与 Python SDK（`agentscope-runtime`）两种方式，示例详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
2. **SDK 集成**：安装 `pip install agentscope-runtime`，使用封装好的工具类（如 `AddMemory`, `SearchMemory`, `CreateProfileSchema`）进行异步调用，避免手动构造请求体与处理认证头。  
3. **OpenClaw 插件**：通过 `openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw` 安装，并在 `~/.openclaw/openclaw.json` 中配置 `apiKey` 和 `userId` 即可启用全自动捕获与召回；也可通过 CLI（如 `openclaw modelstudio-memory search "用户偏好"`）或 Agent 工具调用进行手动干预。

## 限制和注意事项

- **速率限制（阿里云账号级别）**：  
  - 所有 API 总计 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  超限将返回 `429 Too Many Requests`，需自行实现重试退避逻辑。  
- **延迟特性**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；OpenClaw 插件中 `autoCapture` 为异步执行，不影响主响应流。  
- **默认记忆库约束**：每个账号自带一个默认记忆库，不可删除，但可编辑名称、描述及规则；新建记忆库最多支持 50 条记忆片段规则 + 50 条用户画像规则。  
- **画像提取时效性**：调用 `AddMemory` 写入含画像信息的对话后，需等待约 3 秒再调用 `GetUserProfile` 获取结果，因系统需异步完成抽取与存储。  
- **兼容性说明**：OpenClaw 插件不支持阿里云百炼 Coding Plan 的 API Key，仅接受标准 DashScope API Key —— 此限制在 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 中明确标注。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)


