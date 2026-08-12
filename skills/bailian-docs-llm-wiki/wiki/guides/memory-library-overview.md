# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/memory.md)能力核心组件，用于解决大模型上下文窗口限制导致的跨会话信息丢失问题。它通过自动从对话中提取关键事件（记忆片段）和结构化属性（用户画像），持久化存储并支持语义检索，使智能体能在后续交互中持续理解用户偏好与历史上下文。该能力以开放 API 形式提供，可集成至任意应用，并支持多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段**：从对话消息中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、动态更新与智能去重。适用于大多数[长期记忆](../concepts/memory.md)场景。  
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、爱好），支持字段级描述引导与初始值设置。适用于需固定属性建模的场景。  
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过[插件](../concepts/plugin.md)生命周期钩子（`agent_end`/`before_agent_start`）实现全自动记忆写入与检索，无需手动干预 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **工具化能力**：除自动流程外，还提供 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个可被 Agent 主动调用的工具，支持运行时按需操作 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明记忆片段规则支持配置过期时间（7天/30天/180天/永不过期），且默认规则有效期为 180 天。实际行为以控制台配置及 API 参数为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 共享命名空间 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传则使用默认记忆库（每个账号自带一个） |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则或记忆库中首个启用的规则 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需触发画像提取时传入 |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与高级检索 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数，推荐设为 3–10 平衡效果与性能 |
| `minScore` | number | 否（默认 0） | 相似度阈值（0–100），低于此值的记忆不返回 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：每轮对话结束后调用 `AddMemory`，传入 `messages` 数组（含 user/assistant 交替内容）或 `custom_content`（直接写入文本）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
3. **检索记忆**：在新会话开始前或用户提问时调用 `SearchMemory`，传入自然语言查询（如 `"我需要做什么？"`）或 `messages` 上下文，系统返回语义最相关记忆列表。  
4. **注入 Prompt**：将 `SearchMemory` 返回的 `memory_nodes[].content` 拼接至当前 Prompt 的 system 或 user 部分，实现个性化上下文增强。  
5. **管理记忆**：通过 `ListMemory` 分页查看、`UpdateMemory` 修改内容、`DeleteMemory` 删除指定记忆节点（需 `memory_node_id`）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **速率限制**（阿里云账号级别）：  
  - `AddMemory`：120 次/分钟  
  - `SearchMemory`：300 次/分钟  
  - 所有记忆 API 合计：3000 次/分钟  
  （详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）  
- **延迟指标**：`SearchMemory` 端到端延迟 200–500ms；`AddMemory` 延迟 500–1000ms；自动捕获为异步执行，不影响主响应流。  
- **默认记忆库**：不可删除，但可编辑名称/描述及添加自定义规则；预置一条“默认项目”规则（有效期 180 天，可编辑）。  
- **版本差异**：记忆抽取支持 `Pro`（开启 Rerank，¥0.03/次）与 `Lite`（关闭 Rerank，¥0.018/次）两种版本，默认为 `Pro`；用户画像 `Lite` 版本定价为 ¥0.025/次。  
- **兼容性**：不支持阿里云百炼 Coding Plan 的 API Key；OpenClaw [插件](../concepts/plugin.md)为统一配置，暂不支持按 Agent 独立配置记忆库。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


