# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨应用的语义化信息存储与智能召回。它通过大模型自动理解对话内容，将关键事件提炼为记忆片段（Memory Nodes），并支持从对话中抽取结构化用户画像（Profile），最终以低延迟、高相关性的方式注入 Prompt，显著提升智能体的个性化、连贯性与任务完成能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：作为核心上下文增强机制，替代传统“短期记忆”的有限轮次限制。开发者可在 Agent 配置中启用长期记忆[插件](plugin.md)（如 `@modelstudio/modelstudio-memory-for-openclaw`），实现 `autoRecall`（对话开始前自动检索相关记忆）与 `autoCapture`（对话结束后自动提取关键信息），无需手动拼接历史。
  
- **工作流（Workflow）与高代码应用**：通过直接调用长期记忆 API（如 `SearchMemory` + `AddMemory`），在节点逻辑或 Python 代码中按需读写记忆。例如：在订单处理工作流中，检索用户历史偏好以动态生成推荐话术；在高代码服务中，结合业务事件（如“用户完成注册”）主动写入结构化画像。

- **多应用共享场景**：同一记忆库可被多个智能体或工作流复用，通过统一 `user_id` 实现数据隔离，适用于 SaaS 多租户、客服系统多渠道（APP/小程序/网页）记忆同步等架构。

- **与知识库（RAG）协同**：长期记忆聚焦「用户专属状态」（如“张三过敏花生”“李四常订周二早餐”），知识库承载「通用领域知识」（如“花生过敏症状”“早餐营养标准”）。二者在 Prompt 中分层注入，避免语义混淆，提升推理准确性。

> ⚠️ 注意：当前长期记忆能力**仅对智能体应用（Agent 2.0）原生集成支持**；工作流与高代码需通过 API 主动调用；旧版 Agent 1.0 不支持。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 场景 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有接口强制要求，用于隔离记忆空间。不同 `user_id` 数据完全独立。 | 全场景 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）。不传则使用默认库；可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 | 全场景 |
| `profile_schema` | string | 否（仅 `AddMemory`） | 用户画像模板 ID。传入后触发自动结构化抽取（如从“我35岁，做设计师，喜欢爬山”中提取 `age=35`, `occupation="设计师"`, `hobby=["爬山"]`）。需先调用 `CreateProfileSchema` 创建模板。 | 用户画像场景 |
| `project_id` | string | 否（仅 `SearchMemory`/`AddMemory`） | 记忆片段规则 ID（即“提取策略”ID）。不传则使用默认规则；支持传入多个 ID（`["rule_a", "rule_b"]`）进行混合检索。 | 精准控制提取/召回范围 |
| `top_k` / `min_score` | integer / double | 否（仅 `SearchMemory`） | 检索结果数量上限（1–100，默认 10）；最小相似度阈值（[0,1]，默认 0.3）。建议生产环境设 `top_k=3~5` 平衡效果与 [Token](token.md) 成本。 | 检索精度控制 |
| `plan_version` | string | 否（仅 `SearchMemory`） | 检索策略版本：`pro`（启用 Rerank，精度高，¥0.001/次）或 `lite`（关闭 Rerank，成本低，¥0.00002/次）。默认 `pro`，优先级高于 `enable_rerank`。 | 成本与效果权衡 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"channel": "wechat", "priority": "high"}`），用于分类管理、过滤或业务标记。支持在 `SearchMemory` 中通过 `filter` 参数联合查询。 | 业务维度扩展 |

> ✅ 最佳实践：  
> - 单次 `AddMemory` 最多处理 **5 轮完整对话（10 条 message）** 或一段 ≤512 字符的 `custom_content`（二者互斥，`custom_content` 优先）；超长内容请分批调用。  
> - 记忆默认有效期为 **180 天**（非永不过期），可在控制台或创建规则时显式设置 `expired_in_days`（支持 7/30/180/0 表示永不过期）。  
> - 所有 API 均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 接入，Header 必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY`。

## 面向开发者，简洁实用

- **快速上手三步走**：  
  1️⃣ 控制台创建记忆库 → 定义画像模板（可选）→ 复制 `memory_library_id` 和 `profile_schema`；  
  2️⃣ 在智能体中启用记忆[插件](plugin.md)，或在代码中调用 `AddMemory(user_id="u123", messages=[...])` 写入；  
  3️⃣ 在后续请求前调用 `SearchMemory(user_id="u123", query="他上次要买什么？", top_k=3)` 获取上下文，并注入 Prompt。

- **SDK 推荐**：使用 `agentscope-runtime>=1.1.5`，自动处理鉴权、重试与错误码（如 `429` 限流、`400` 参数校验失败），比裸 HTTP 更稳定。

- **避坑提示**：  
  - ❌ 不要将长期记忆当作数据库使用：不支持 SQL 查询、事务、复杂关联；仅适合 KV+语义检索场景。  
  - ❌ 不要忽略 `user_id`：遗漏将导致写入/读取失败或数据错乱。  
  - ✅ 善用 `meta_data` + `filter`：例如 `SearchMemory(..., filter={"channel": "app"})` 可精准召回 APP 渠道专属记忆。  
  - ✅ 监控限流：账号级总 QPM ≤ 3000，其中 `SearchMemory` ≤ 300 QPM；高并发场景建议加本地缓存或降级策略。

- **计费提醒**：  
  - 存储免费，但检索（`SearchMemory`）按次计费（`pro`/`lite` 版本价格不同）；  
  - 记忆内容注入 Prompt **不额外收取 [Token](token.md) 费用**（该部分 [Token](token.md) 暂不计费）；  
  - 商业化计费起始时间：**2026 年 8 月 20 日 10:00（北京时间）**，此前为免费试用期。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)


