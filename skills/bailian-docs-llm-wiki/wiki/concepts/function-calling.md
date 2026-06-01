# 函数调用

函数调用（Function Calling）是大模型与外部工具交互的核心机制。开发者预先向模型声明一组可用的函数（工具）定义，模型在对话过程中根据用户意图自主判断是否需要调用某个函数，并生成结构化的调用参数，由应用侧执行后将结果返回模型，最终生成融合了外部信息的回复。

## 基本工作流程

函数调用遵循以下流程：

1. **声明工具**：开发者在请求中通过 `tools` 参数描述可用函数的名称、功能说明和参数结构（JSON Schema）。
2. **模型决策**：模型根据用户输入内容、工具名称和工具描述判断是否需要调用工具。
3. **生成调用参数**：若需要调用，模型输出函数名和结构化参数（而非直接回答用户）。
4. **应用执行**：应用侧根据模型返回的函数名和参数调用实际的 API 或服务。
5. **结果回传**：将执行结果作为 tool 角色的消息传回模型。
6. **生成最终回复**：模型结合工具返回结果生成面向用户的自然语言回答。

若模型判断无需调用工具，则跳过步骤 3–5，直接生成回复。

## 在百炼平台的使用场景

### 模型推理 API

在直接调用模型 API 时，函数调用是最基础的工具集成方式。百炼平台所有通用文本生成模型（如 `qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash` 等）均支持函数调用，部分视觉理解模型和全模态模型也支持。

支持函数调用的 API 接口包括：

| 接口类型 | 说明 |
|---------|------|
| OpenAI 兼容 Chat Completions | 与 OpenAI 工具调用协议兼容，迁移成本最低 |
| OpenAI 兼容 Responses | 内置工具 + 自定义函数调用 |
| Anthropic 兼容 Messages | 兼容 Anthropic 工具调用协议 |
| DashScope 原生接口 | 百炼原生接口，功能覆盖最全 |

### 实时多模态交互（Omni Realtime API）

在基于 WebSocket 的实时语音对话场景中，函数调用同样可用。通过 `session.update` 事件配置可用工具，模型在对话过程中通过以下事件完成工具调用：

- **`response.function_call_arguments.delta`**：增量返回函数调用参数
- **`response.function_call_arguments.done`**：函数调用参数生成完成
- **`conversation.item.create`**：客户端回传工具执行结果

此能力由 `qwen3.5-omni-realtime` 系列模型支持。

### 智能体应用

智能体应用中的插件和 MCP 服务本质上都基于函数调用机制运作：

- **新版智能体（Agent 2.0）**：将知识库、MCP 服务统一抽象为工具，由智能体在"规划-执行-反思"链路中自主决策调用顺序。
- **旧版智能体（Agent 1.0）**：知识库检索先行，再根据需要调用插件工具。

智能体通过 ReAct 最大轮次参数（1–50）限制单次会话中工具调用的迭代次数。

### 插件

插件是函数调用在应用层面的封装。大模型根据工具名称和描述判断调用意愿，应用内部自动完成函数执行并将结果回传模型。百炼提供官方插件（如夸克搜索、Python 代码解释器）、三方插件和自定义插件。每个智能体应用最多支持添加 10 个工具。

### MCP 服务

MCP（模型上下文协议）是函数调用的标准化扩展。与传统插件相比，MCP 提供统一的协议规范，开发者无需为每个工具单独编写接口适配代码。MCP 服务只能在智能体或工作流应用中使用，不能在直接调用千问 API 时接入。

## 关键参数与配置

### 工具定义（tools 参数）

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "城市名称，如"北京""
            }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `name` | 函数名称，模型据此选择要调用的函数 |
| `description` | 函数功能描述，直接影响模型的调用判断准确度 |
| `parameters` | 参数的 JSON Schema 定义，模型据此生成结构化参数 |

### 内置工具（无需额外配置）

Qwen3.6 和 Qwen3.5 系列的 plus/flash 版本支持内置工具，包括联网搜索和代码解释器，无需通过 `tools` 参数手动声明。

### 关联参数

| 参

## 关联主题页

- [model inference](../guides/model-inference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model context protocol](../guides/model-context-protocol.md)

