# 会话记忆与长期记忆对比

在百炼平台上构建具备记忆能力的智能体时,需要区分"会话记忆"与"长期记忆"两类机制:前者负责单轮对话内或一次会话内的上下文维护,后者负责跨会话持久化用户偏好、历史事件与画像。本页面对二者的概念定位、API 形态和适用场景进行对比,帮助开发者做技术选型。

## 概念定位

- **会话记忆(短期记忆)**:对应 API 调用中传入的 `messages` 数组,记录当前会话内的对话历史。只在一次请求或一段会话生命周期内有效,过期即丢失,是大模型理解上下文的最基本输入,由调用方在客户端或应用进程内自行维护。
- **长期记忆**:对应记忆库(Memory Library)产生的"记忆片段(memory_node)"与"用户画像(profile)",从对话中自动提取关键信息并持久化存储,使智能体能够跨会话持续引用用户偏好和历史事件。由百炼后端托管,通过专用 REST API 写入与检索。

## 关键维度对比

| 维度 | 会话记忆 | 长期记忆 |
|------|---------|---------|
| 存储位置 | 客户端/应用进程,随请求体传递 | 百炼后端持久化(记忆库) |
| 生命周期 | 单次会话(请求结束即释放) | 跨会话长期保留(可配置 7 天 / 30 天 / 180 天 / 永不过期) |
| 输入形式 | `messages: [{role, content}, ...]` 数组 | 自动从 `messages` 中提取,或通过 `custom_content`(≤512 字符)直接写入 |
| 数据结构 | 原始对话消息 | 结构化的"记忆片段"与可选的"用户画像"属性 |
| 写入方式 | 调用方自行拼接每轮上下文 | 调用 `AddMemory`,平台自动抽取、去重、可选更新历史片段(`event: ADD/UPDATE/DELETE`) |
| 读取方式 | 直接拼入下一次请求的 [prompt](../guides/prompt.md) | 调用 `SearchMemory` 做语义检索,Top-K 召回后注入 [prompt](../guides/prompt.md) |
| 检索能力 | 无,按时间顺序拼接 | 语义检索 + 可选 `enable_rerank` / `enable_rewrite` / `enable_judge` |
| 主要 API 端点 | 各模型/应用调用接口的 `messages` 字段 | 基址 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`,含 `AddMemory` / `SearchMemory` / `ListMemory` / `UpdateMemory` / `DeleteMemory` 等 11 个接口 |
| 用户隔离 | 由调用方自己管理上下文 | 强制要求 `user_id`(≤64 字符),按用户聚合记忆 |
| 用户画像 | 不支持 | 支持自定义 `profile_schema`,通过 `CreateProfileSchema` / `GetUserProfile` 管理 |
| 跨应用共享 | 不支持(限于当前应用上下文) | 支持多应用共享同一 `memory_library_id` |
| 典型时延 | 取决于上游模型 | SearchMemory 200–500ms;AddMemory 500–1000ms |
| 速率上限 | 取决于调用的模型/应用配额 | AddMemory 120 次/分,SearchMemory 300 次/分,合计 3000 次/分 |
| 计费 | 随模型调用计费 | 限时免费 |
| 调用方式 | 任意 HTTP 客户端拼装请求 | REST(cURL)、Python SDK(`agentscope-runtime ≥ 1.1.5`),或通过插件(如 OpenClaw 的 `autoCapture` / `autoRecall` 钩子)集成 |
| 鉴权 | 同所调模型/应用 | Header `Authorization: Bearer $DASHSCOPE_API_KEY` |

## 工作流配合

会话记忆与长期记忆并非互斥,而是协同工作的两层:

1. 在一次会话内,业务侧维护 `messages` 数组作为会话记忆,直接喂给大模型。
2. 每轮或会话结束时,将 `messages` 透传给 `AddMemory`,由记忆库自动提取关键信息生成记忆片段,可选触发用户画像更新。
3. 下一次会话开始或话题切换时,使用当前用户输入作为 query 调用 `SearchMemory`,返回 Top-K(建议 3~10)的相关历史记忆。
4. 将检索到的长期记忆拼入新会话的 system [prompt](../guides/prompt.md) 或上下文,与本次会话记忆共同输入模型,实现"既记得过去、又理解当前"。

可总结为:**会话记忆 = 短期工作内存,长期记忆 = 持久化知识沉淀**。

## 选型建议

| 场景 | 推荐方案 |
|------|---------|
| 单轮问答、不需要历史的工具型应用 | 仅使用会话记忆,无需引入记忆库 |
| 短时多轮对话(客服、单次任务) | 以会话记忆为主;若需跨工单回看,可附加长期记忆 |
| 个人助理、角色扮演、教育辅导等"记住用户" | 会话记忆 + 长期记忆片段,按 `user_id` 隔离 |
| 需要持久化结构化属性(年龄、职业、偏好等) | 启用长期记忆中的用户画像(`profile_schema`),配合 `messages` 自动提取 |
| 多应用共享同一份用户记忆 | 显式创建记忆库,在各应用中传同一 `memory_library_id` |
| 已有第三方 Agent 框架(如 OpenClaw) | 通过插件接入,利用 `autoCapture` / `autoRecall` 免去手动调用 |
| 离线批量灌入背景知识 | 使用 `AddMemory` 的 `custom_content`,而非塞入 `messages` |

## 注意事项

- 记忆库为账号级别资源,默认提供一个不可删除的默认记忆库;`memory_library_id` 不填时使用默认库。
- `top_k` 建议 3~10,相似度阈值 `min_score` 建议 0.5~0.7,以平衡召回率与精度。
- 排序模型目前仅支持 `gte-rerank-v2`,通过 `enable_rerank=true` 开启。
- `SearchMemory` 在记忆库文档与长期记忆 API 文档中端点存在差异(`/api/v2/apps/memory/search` vs `/api/v2/apps/memory/memory_nodes/search`),实际以 API 参考为准。
- 长期记忆的过期时间在控制台规则中配置,长期记忆 API 文档另有"暂无失效日期"的描述,实际行为以控制台配置为准。
- 不要将完整会话记忆塞入 `custom_content`(上限 512 字符);需要保留原始对话请走 `messages` 通道,由平台自动抽取关键信息。
- 用户画像字段命名应保证语义唯一(如"姓名"与"名字"不应并存),并避免期望单轮对话就能提取完整画像。

## 被对比主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)


