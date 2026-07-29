# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好、关键事件与结构化属性的自动提取、存储与语义召回。它由平台统一托管的记忆专用模型驱动，无需开发者自行训练或部署 Embedding 模型。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）持续性增强**：通过 `AddMemory` 自动从对话中提炼关键信息（如“每天9点提醒我喝水”），再在后续交互中用 `SearchMemory` 语义检索召回，使 Agent 具备上下文延续能力；OpenClaw [插件](plugin.md)支持 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动注入），实现零代码集成。
- **用户画像构建**：配合 `ProfileSchema` 系统，定义结构化字段（如 `age`, `occupation`, `diet_preference`），在 `AddMemory` 中指定 `profile_schema` 参数，即可从自然对话中自动抽取并聚合为标准化用户画像，再通过 `GetUserProfile` 获取快照。
- **RAG 增强补充**：作为 RAG 的补充层，长期记忆聚焦于**用户个体状态**（而非通用知识库），适用于个性化推荐、习惯追踪、服务历史回溯等场景；可与知识库检索并行调用，共同注入 LLM 提示词。
- **应用级状态管理**：替代自建数据库存储轻量级用户状态（如设置项、偏好标签、任务进度），通过标准 CRUD 接口（`ListMemory`/`DeleteMemory`/`UpdateMemory`）实现生命周期控制，降低运维复杂度。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识，64 字符内；所有接口必须传入，用于严格隔离用户数据空间 | `"usr_abc123"` |
| `memory_library_id` | string | 否 | 目标记忆库 ID（32 字符）；不传则使用账号默认库（控制台可创建多个库） | 控制台「记忆库列表」获取 |
| `messages` / `custom_content` | array / string | 互斥必填（仅 `AddMemory`） | `messages`: 最多 50 条 role/content 对话；`custom_content`: ≤512 字符纯文本（绕过自动提取） | 优先用 `messages` 实现语义理解 |
| `profile_schema` | string | 否（仅需画像时） | 用户画像模板 ID；需先调用 `CreateProfileSchema` 创建，否则忽略抽取逻辑 | 控制台「画像模板」页获取 |
| `top_k` | integer | 否（`SearchMemory`） | 召回最大条数，默认 10；范围 1–100 | 3–10（平衡精度与性能） |
| `min_score` | double | 否（`SearchMemory`） | 相似度阈值，默认 0.3；范围 [0,1]，低于此值结果被过滤 | 0.5–0.7（高精度场景建议 ≥0.6） |
| `enable_rerank` | boolean | 否（`SearchMemory`） | 是否启用重排序（提升相关性），默认 `false` | `true`（对召回质量敏感时启用） |

> ⚠️ 注意：  
> - 所有记忆**默认永不过期**，无自动失效机制；业务需通过 `DeleteMemory` 或按规则主动清理。  
> - `UpdateMemory` 仅支持增量更新 `meta_data`（合并新键值对），且需直接调用 REST API（Python SDK 当前未封装）。  
> - `project_id`（记忆规则 ID）可选，用于绑定定制化提取/过滤策略；未指定则使用记忆库默认规则。

## 开发者提示

- **认证方式**：所有请求 Header 必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 从[控制台](https://help.aliyun.com/zh/model-studio/get-api-key)获取）。
- **SDK 推荐**：安装 `agentscope-runtime>=1.1.5`，直接调用 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 四个封装工具；`UpdateMemory` 需手动发起 PATCH 请求。
- **限流控制**：账号级总 QPM ≤3000；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM —— 生产环境请做好降级与重试。
- **调试建议**：控制台「记忆检索」页支持实时测试查询、开启改写/重排序/意图判别，验证效果后再上线。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application support](../guides/application-support.md)


