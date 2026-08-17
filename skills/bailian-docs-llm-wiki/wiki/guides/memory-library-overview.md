# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于解决大模型上下文窗口限制导致的跨会话信息丢失问题。它通过自动从对话中提取关键事件（记忆片段）和结构化用户属性（用户画像），并持久化存储与语义检索，使智能体具备持续理解用户偏好与历史上下文的能力。该能力以开放 API 形式提供，支持任意应用接入及多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话消息中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、元数据标注、智能去重与动态更新。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（Profile Schema）**：基于预定义模板从对话中抽取结构化属性（如年龄、职业、爱好），字段可配置描述与初始值，支持多轮渐进式填充。适用于需固定属性建模的场景。  
- **双模式策略支持**：所有写入（`AddMemory`）与检索（`SearchMemory`）操作均支持 `pro`（开启 Rerank，质量更高）和 `lite`（关闭 Rerank，成本更低）两个策略版本，详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **自动捕获与召回**：在 OpenClaw 等框架中可通过插件实现对话结束自动写入、对话开始前自动检索注入，无需手动干预 —— 具体集成方式见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 1 称“记忆片段默认有效期 180 天”，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。该矛盾源于文档 1 描述的是**默认规则的过期配置项**（可编辑），而文档 3 指的是**未显式设置过期时间时的实际行为**。实际有效期由创建记忆片段规则时指定的 `expired_in_days` 决定；若未设置，则永不过期。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中的运行时行为为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 下记忆共享，不同 `user_id` 完全隔离。 |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库（每个账号自带一个，不可删除）。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则或记忆库中首个启用的规则。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需提取画像时传入，否则忽略。 |
| `meta_data` | object | 否 | 自定义键值对，用于分类管理（如 `"category": "reminder"`），支持后续按条件过滤。 |
| `plan_version` | string | 否（Search 必填推荐） | 取值 `pro` 或 `lite`，控制检索是否启用 Rerank（Search）或写入策略（Add，由关联规则决定）；大小写不敏感。 |

## 使用方式

1. **准备环境**：获取 DashScope API Key 并配置环境变量 `DASHSCOPE_API_KEY`（参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：每轮对话结束后调用 `AddMemory`，传入 `messages`（对话数组）或 `custom_content`（直接写入文本）及 `user_id`。示例见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
3. **检索记忆**：在新会话开始前或用户提问时调用 `SearchMemory`，传入 `user_id` 和自然语言查询（如 `"我需要做什么？"`），返回相关记忆片段列表。  
4. **注入上下文**：将 `SearchMemory` 返回的 `memory_nodes[].content` 拼接至 Prompt 的系统提示或历史消息中，供大模型参考。  
5. **高级操作**：支持 `ListMemory`（分页查看）、`UpdateMemory`（PATCH 更新内容）、`DeleteMemory`（按 ID 删除）及 `GetUserProfile`（获取完整画像）等管理接口，详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **速率限制**（阿里云账号级别）：  
  - `AddMemory`：120 次/分钟  
  - `SearchMemory`：300 次/分钟  
  - 所有记忆 API 合计：3000 次/分钟  
  （来源：[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 与 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）  
- **延迟预期**：`SearchMemory` 端到端延迟 200–500ms；`AddMemory` 延迟 500–1000ms；自动捕获为异步执行，不影响主流程响应速度。  
- **策略版本独立性**：`SearchMemory` 的 `plan_version` 参数优先级高于关联 `MemoryProject` 的 `plan_version`，两者互不影响计费与行为（例如 project 为 `lite`，但 Search 请求传 `plan_version: "pro"`，仍按 Pro 计费并启用 Rerank）。  
- **用户画像字段设计**：避免语义重复字段（如同时定义“姓名”“名字”“名称”），单次对话可能无法提取全部属性，建议通过多轮交互渐进收集。  
- **默认记忆库限制**：不可删除，但可编辑名称、描述及规则；其预置的“默认项目”规则可修改但不可删除。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


