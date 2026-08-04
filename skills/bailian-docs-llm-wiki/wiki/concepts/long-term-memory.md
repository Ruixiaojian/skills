# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好、关键事件与结构化画像的自动提取、语义检索与动态更新。它不依赖应用本地状态管理，而是通过统一托管的记忆库（Memory Library）提供高可用、免运维的长期状态服务。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在对话结束后，通过 `AddMemory` 自动提炼用户指令（如“每天9点提醒我吃药”）为记忆片段；在新会话开始前，调用 `SearchMemory` 检索相关历史，将结果注入 Prompt，实现个性化响应与上下文延续。OpenClaw 等框架可通过 `modelstudio-memory-for-openclaw` 插件启用全自动捕获（`autoCapture`）与召回（`autoRecall`），无需手动集成。

- **工作流（Workflow）应用**：在关键节点（如用户信息收集、任务确认后）显式调用 `AddMemory` 写入结构化事实；后续步骤中通过 `SearchMemory` 或 `GetUserProfile` 动态获取用户画像（如职业、健康习惯），驱动条件分支与定制化执行逻辑。

- **高代码应用（Python/Serverless）**：直接集成 `agentscope-runtime` SDK（推荐）或 REST API，灵活控制记忆生命周期。例如，在自定义工具执行完成后，将结果连同 `meta_data`（如 `{"source": "health_app", "priority": "high"}`）一并写入；支持 `UpdateMemory` 增量修正（如更新提醒时间），或 `DeleteMemory` 清理过期条目。

- **用户画像建模**：配合 `CreateProfileSchema` 定义字段模板（如 `{"age": "integer", "diet_preference": "string"}`），在多轮对话中渐进填充；调用 `GetUserProfile` 聚合生成完整画像，供下游业务系统复用。

> ⚠️ 注意：`llm application` 控制台当前**不内置长期记忆配置入口**，所有写入与检索需通过 API 或 SDK 显式调用；该能力独立于应用类型，适用于所有需长期状态保持的场景。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 典型值 |
|------|------|------|------|--------|
| `user_id` | string | ✅ | 用户唯一标识，用于严格隔离记忆空间；建议使用业务侧稳定 ID（如 `uid_12345`），≤64 字符 | `"user_abc"` |
| `memory_library_id` | string | ❌ | 记忆库 ID；不传则使用账号默认记忆库（不可删除，预置 180 天规则） | `"lib-prod-001"` |
| `project_id` / `project_ids` | string / list | ❌ | 记忆片段规则 ID；单 ID 限定提取策略，多 ID（`SearchMemory`）支持混合召回提升覆盖 | `["rule_health", "rule_schedule"]` |
| `messages` / `custom_content` | array / string | ✅（互斥） | `messages`: 对话数组（最多 50 条，含 role/content）；`custom_content`: 纯文本（≤512 字符）；优先级：`custom_content` > `messages` | `[{"role":"user","content":"帮我订下周三的会议室"}]` |
| `top_k`（`SearchMemory`） | integer | ❌ | 最大召回数量，默认 10，取值范围 1–100；建议设为 3–5 以平衡精度与成本 | `5` |
| `min_score`（`SearchMemory`） | double | ❌ | 相似度阈值（0.0–1.0），默认 0.3；低于此值的结果被过滤；调高可减少噪声 | `0.5` |
| `meta_data` | object | ❌ | 键值对形式的自定义元数据，随记忆持久化；支持 `UpdateMemory` 增量更新（仅覆盖指定字段） | `{"category": "schedule", "source_app": "web"}` |

- **记忆规则配置**：在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 中可编辑规则有效期（7/30/180 天或永不过期）、抽取模式（`Pro` 含 Rerank，精度高；`Lite` 成本低）及画像模板绑定。
- **速率限制（阿里云账号级）**：`AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM，全接口合计 ≤ 3000 QPM。

## 开发者提示

- ✅ **首选 SDK**：安装 `agentscope-runtime>=1.1.5`，使用 `AddMemory`、`SearchMemory` 等封装类，自动处理认证与重试；`UpdateMemory` 暂未封装，需 `requests.patch` 直接调用。
- ✅ **注入上下文**：`SearchMemory` 返回的记忆片段含 `content` 和 `score`，建议按 `score` 降序拼接至 Prompt，并添加明确指示（如“参考以下用户历史：{content}”）。
- ✅ **画像延迟**：写入带 `profile_schema` 的记忆后，需等待约 3 秒再调用 `GetUserProfile`，否则可能返回空。
- ❌ **避免滥用**：`custom_content` 优于 `messages` 的简单场景（如日志写入）；复杂对话请确保 `messages` 格式合规（role 为 `"user"`/`"assistant"`，content 为 string）。
- 📦 **多模态注意**：当前仅对 `messages.content` 中的文本部分进行语义提取，图像 URL 等非文本内容被忽略。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


