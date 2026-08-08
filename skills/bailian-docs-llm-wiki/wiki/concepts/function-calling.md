# 函数调用

函数调用（Function Calling）是百炼平台支持的一种关键模型能力，允许大语言模型在推理过程中主动识别用户意图、生成结构化工具调用请求（而非仅输出自然语言），并将结果交由外部系统执行后返回给模型继续推理。该能力是构建可靠智能体（Agent）和自动化工作流的基础机制。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）开发**：当模型具备 `function-calling` 能力（如 `qwen3.7-plus`、`qwen3.8-max`、`qwen3.5-omni-plus` 等），开发者可通过 `tools` 参数声明一组可调用函数（JSON Schema 描述），模型将根据对话上下文自动选择函数、填充参数并生成 `tool_calls` 字段；平台不执行函数本身，仅返回标准化的调用请求，由应用层解析、执行并回填结果。
  
- **[OpenAI 兼容接口](openai-compatible-interface.md)**：在 Chat Completions 或 Responses API 中启用函数调用，需在请求体中传入 `tools` 数组及可选的 `tool_choice`（如 `"auto"`、`"required"` 或指定工具名）。Responses API 还支持内置工具（如联网搜索、代码解释器），无需显式定义 `tools`，直接启用即可。

- **多模态与全模态场景**：`qwen3.5-omni-plus` 和 `qwen3.7-plus` 均支持跨模态的函数调用（例如图像理解后触发数据库查询、语音转写后调用日程服务），但需确保输入数据格式符合模型要求（如图片需为 `oss://` URL 或 base64 编码）。

- **异步任务链路**：函数调用本身为同步行为；若被调用的工具涉及长耗时操作（如视频生成、3D建模），建议在工具实现中封装为异步任务（返回 `task_id`），再通过轮询或事件回调获取最终结果，避免阻塞模型响应。

## 关键参数和配置

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `tools` | array of object | 是（启用函数调用时） | 每个对象包含 `type="function"`、`function.name`（字符串，唯一标识）、`function.description`（功能描述）、`function.parameters`（JSON Schema，严格校验输入） |
| `tool_choice` | string / object | 否 | 控制调用策略：`"auto"`（模型自主决定）、`"none"`（禁用）、`"required"`（必须调用）、或 `{ "type": "function", "function": { "name": "xxx" } }`（强制指定） |
| `enable_thinking` | boolean | 否（Qwen3+ 系列） | 设为 `true` 可启用结构化思维链输出，提升函数选择准确性（尤其适用于复杂多步骤任务） |
| `response_format` | object | 否 | 若需强制模型返回 JSON 结构（如工具参数校验），可设为 `{ "type": "json_object" }`，配合 `tools` 使用效果更佳 |

> ⚠️ 注意：函数调用能力依赖模型原生支持——调用前请通过 `/api/v1/models` 接口确认目标模型的 `capabilities` 字段是否包含 `"function-calling"`；不支持的模型将忽略 `tools` 参数，按普通文本生成处理。

## 面向开发者：实用建议

- **Schema 定义要精简**：避免嵌套过深或字段过多，推荐使用 `required` 明确必填项，减少模型幻觉；
- **错误处理需前置**：模型可能生成非法参数（如类型错误、缺失字段），务必在调用外部工具前做 JSON Schema 校验；
- **状态管理靠应用层**：百炼不维护函数调用上下文或会话状态，`previous_response_id`（Responses API）仅用于关联多轮响应 ID，工具执行结果需由你主动注入下一轮请求的 `tool_results`；
- **调试技巧**：设置 `stream=false` + `enable_thinking=true`，观察模型思考过程与工具选择逻辑；生产环境建议关闭 `enable_thinking` 以降低延迟。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


