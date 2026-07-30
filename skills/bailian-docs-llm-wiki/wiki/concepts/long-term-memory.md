# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户信息管理能力，用于突破大模型单次会话的上下文限制，实现跨对话、跨会话的用户偏好、待办事项、关键事件等信息的自动提取、语义存储与智能召回。它不是简单的文本缓存，而是基于专用抽取模型与语义向量引擎构建的可检索、可联动、可编程的记忆基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为核心上下文增强组件，长期记忆使 Agent 能“记住”用户历史指令（如“我过敏花生”）、习惯（如“默认用简体中文回复”）或承诺事项（如“下周三提醒我续保”），在后续交互中通过 `SearchMemory` 自动注入提示词，显著提升个性化与连贯性。注意：当前 LLM 应用层仅原生支持短期记忆（0–30 轮），长期记忆需显式调用 API 或通过 OpenClaw 插件启用 `autoRecall`。

- **用户画像构建**：通过指定 `profile_schema_id`，长期记忆可将非结构化对话（如“我今年35岁，在杭州做设计师”）自动映射为结构化字段（`age: 35`, `city: "杭州"`, `occupation: "设计师"`），支持多轮渐进填充，并与 `GetUserProfile` 联动输出完整画像。

- **记忆库（Memory Library）统一管理**：所有记忆片段均归属至逻辑隔离的记忆库（`memory_library_id`），支持多应用共享（按 `user_id` 隔离）、规则驱动（`project_id` 指定抽取/过期策略）和元数据分类（`meta_data` 自定义标签），是构建企业级用户认知中枢的基础单元。

- **插件化集成（OpenClaw）**：无需编码即可启用全自动捕获（`autoCapture`）与召回（`autoRecall`），插件在对话收尾时自动调用 `AddMemory` 和 `SearchMemory`，开发者只需配置规则与 Schema。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作以此隔离数据空间 | 业务系统用户 ID（如 `uid_12345`） |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`: 对话历史（最多 50 条）；`custom_content`: 直接文本（≤512 字符） | 优先用 `messages` 让模型自动理解上下文 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符）；不填则使用默认库 | 控制台创建后复制 ID，多租户场景建议显式指定 |
| `profile_schema_id` | string | 否 | 关联用户画像 Schema ID，触发结构化抽取 | 需先调用 `CreateProfileSchema` 创建 |
| `top_k`（SearchMemory） | integer | 否 | 检索返回条数（1–100） | 3–10（平衡精度与 token 开销） |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 [0.0, 1.0] | 0.5–0.7（避免噪声或漏召） |
| `enable_rerank` / `enable_judge` / `enable_rewrite`（SearchMemory） | boolean | 否 | 高级搜索开关，需显式启用 | `enable_rerank=True` 提升排序质量；`enable_judge=True` 过滤无关项 |

> ⚠️ 注意事项：
> - `project_id`（记忆片段规则 ID）非必需：未传时系统自动选用默认规则；规则中设置的“过期时间”仅影响新写入记忆的调度策略，**底层存储无自动物理删除机制**，业务侧需自行清理。
> - 所有接口限流为阿里云账号级别：`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM，总量 ≤3000 QPM。
> - `custom_content` 和单条 `messages.content` 均严格限制 ≤512 字符，超长内容将被截断，建议预处理摘要。

## 面向开发者，简洁实用

- **快速起步**：  
  ```python
  # 安装最新 SDK
  pip install agentscope-runtime>=1.1.5
  
  # 添加记忆（自动抽取）
  from agentscope.tools import AddMemory
  await AddMemory().arun(user_id="u123", messages=[{"role":"user","content":"帮我订明天下午3点的会议室"}])
  
  # 检索记忆（带语义重写+重排）
  from agentscope.tools import SearchMemory
  result = await SearchMemory().arun(
      user_id="u123",
      messages=[{"role":"user","content":"我最近有什么会议安排？"}],
      top_k=5,
      min_score=0.6,
      enable_rewrite=True,
      enable_rerank=True
  )
  ```

- **生产建议**：  
  - 写入前对 `messages` 做轻量清洗（移除系统提示、冗余确认语句），提升抽取准确率；  
  - 检索时优先用 `messages`（含角色上下文）而非裸 `query`，语义更鲁棒；  
  - 敏感信息（如身份证号）勿直接写入，应脱敏或走加密存储通道；  
  - 定期调用 `ListMemory` + `DeleteMemory` 清理过期/无效记忆，避免噪声累积。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)


