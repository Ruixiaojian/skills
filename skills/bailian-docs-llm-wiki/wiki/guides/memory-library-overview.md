# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好与历史信息持久化存储与语义召回。它通过自动从对话中提取结构化记忆片段和用户画像，并提供标准化 API 接口，使智能体能在新会话中基于检索结果动态注入上下文，从而提供连贯、个性化的交互体验。该能力面向开发者开放，支持多应用共享同一记忆库，也支持细粒度规则配置与计费控制。

## 支持的模型/功能

- **记忆片段（Memory Node）**：从对话消息中自动提取关键事件与事实（如“每天上午9点提醒我喝水”），支持自定义内容直写（`custom_content`）、元数据标注（`meta_data`）及智能去重。适用于大多数[长期记忆](../concepts/memory.md)场景。  
- **用户画像（Profile Schema）**：基于预定义模板从对话中抽取结构化属性（如年龄、职业、爱好），字段支持描述引导与初始值设置。适用于需固定属性建模的业务场景。  
- **自动捕获与召回**：OpenClaw 等框架可通过插件实现 `autoCapture`（对话结束自动写入）与 `autoRecall`（对话开始前自动检索注入），详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **完整生命周期管理**：支持 `AddMemory`、`SearchMemory`、`ListMemory`、`UpdateMemory`、`DeleteMemory` 及 `GetUserProfile` 等全链路操作，覆盖写入、检索、浏览、更新与删除。

> **注意**：文档 1 称“记忆片段默认有效期 180 天”，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。实际行为以规则配置为准——记忆过期时间由记忆片段规则中的 `expired_in_days` 参数控制，未显式配置时按规则默认值（如默认项目为 180 天）生效；若规则设为“永不过期”，则无自动过期机制。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中 `CreateMemoryProject` 的 `expired_in_days` 字段为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 目标记忆库 ID；不传则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID；用于触发结构化属性抽取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `plan_version` | string | 否 | 取值 `"pro"` 或 `"lite"`，控制 Rerank 是否启用；`SearchMemory` 中独立生效，`AddMemory` 由关联规则决定 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否 | 检索返回最大条数，默认 `5`（OpenClaw 插件）或 `10`（API 最佳实践） | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |

## 使用方式

1. **准备环境**：获取 DashScope API Key 并配置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **选择接入方式**：
   - **直接调用 API**：使用 `AddMemory` 写入、`SearchMemory` 检索，支持 cURL/Python（需 `agentscope-runtime`）等语言；示例见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
   - **集成 OpenClaw 插件**：安装 `@modelstudio/modelstudio-memory-for-openclaw`，配置 `apiKey` 与 `userId`，启用 `autoCapture`/`autoRecall` 即可零代码接入；插件还暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用（[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
3. **高级控制**：
   - 创建自定义记忆库与规则（如设置 `expired_in_days`、`auto_refresh`、`plan_version`）；  
   - 通过 `meta_data` 对记忆分类管理，提升检索精度；  
   - 使用 `ListMemory`/`UpdateMemory` 进行人工干预与维护。

## 限制和注意事项

- **速率限制**（阿里云账号级别）：  
  - `AddMemory`：≤ 120 次/分钟  
  - `SearchMemory`：≤ 300 次/分钟  
  - 所有 API 合计：≤ 3000 次/分钟  
  （详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）  
- **计费说明**：  
  - `AddMemory`：Pro ¥0.03/次，Lite ¥0.018/次（由 MemoryProject `plan_version` 决定）；  
  - `SearchMemory`：Pro ¥0.001/次，Lite ¥0.00002/次（由请求参数 `plan_version` 决定，优先级高于 `enable_rerank`）；  
  - 商业化起始时间为 **2026 年 8 月 20 日 10:00（北京时间）**（[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 与 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 均明确提及）。  
- **兼容性**：  
  - 不支持阿里云百炼 Coding Plan 的 API Key；  
  - `plan_version` 大小写不敏感（`"PRO"` ≡ `"pro"`），非法值将报错；  
  - 修改 MemoryProject 的 `plan_version` 仅影响后续 `AddMemory` 调用，存量记忆不受影响。  
- **最佳实践**：  
  - `top_k` 建议设为 `3–10`，平衡效果与性能；  
  - 用户画像字段名应语义唯一（避免“姓名”/“名字”并存），描述需具体清晰；  
  - 自定义 `meta_data` 可用于业务维度分类（如 `"category": "health_reminder"`），便于精准过滤。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


