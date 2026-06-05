# 函数调用（工具调用）

函数调用（Function Calling），也称工具调用（Tool Calling），是百炼平台中大模型与外部工具协作的核心机制。开发者通过向模型描述可用工具的名称、功能和参数schema，模型在对话过程中自主判断是否需要调用工具，并生成结构化的调用参数，由应用侧执行后将结果返回模型以生成最终回复。

## 工作原理

函数调用的基本流程如下：

1. 开发者在请求中通过 `tools` 参数定义可用工具（名称、描述、参数 JSON Schema）
2. 模型根据**用户输入内容**、**工具名称**和**工具描述**判断是否需要调用工具
3. 若需要调用，模型输出工具名称和结构化参数（而非直接回答用户）
4. 应用侧执行对应函数，获取返回结果
5. 将工具返回结果与对话上下文合并，再次输入模型生成最终回复

若模型判断无需调用工具，则直接生成文本回复。

## 在百炼平台的使用场景

### 模型 API 直接调用

百炼平台的通用文本生成模型（如 `qwen3.6-plus`、`qwen3.7-max`、`qwen3.6-flash`）和部分视觉/全模态模型均支持 Function Calling。开发者可通过以下接口使用：

| 接口类型 | Function Calling 支持方式 |
|---------|--------------------------|
| OpenAI 兼容 Chat Completions | 通过 `tools` 参数定义工具，模型返回 `tool_calls` |
| OpenAI 兼容 Responses | 内置联网搜索、代码解释器等工具，自动管理调用流程 |
| Anthropic 兼容 Messages | 兼容 Anthropic 工具调用格式 |
| DashScope 原生接口 | 提供最完整的工具调用参数支持 |

### 智能体应用（Agent）

- **Agent 2.0（新版）**：将知识库、MCP 服务统一作为工具，由智能体自主规划调用顺序，支持完整的"规划-执行-反思"链路
- **Agent 1.0（旧版）**：通过插件机制调用工具，大模型根据工具描述决策是否调用
- 通过 ReAct 最大轮次参数（1-50）限制单次会话中工具调用的最大次数

### 工作流应用

在工作流中，工具（插件/MCP）作为节点按编排方式执行，每个节点手动指定一个工具并串联输入输出，由大模型节点负责自然语言与参数的转换。

### 实时多模态交互（Omni Realtime API）

`qwen3.5-omni-realtime` 系列模型在 WebSocket 实时交互中支持工具调用：

- 通过 `session.update` 事件配置可用工具
- 服务端通过 `response.function_call_arguments.delta` / `done` 事件返回工具调用参数
- 客户端通过 `conversation.item.create` 事件回传工具执行结果

## 工具接入方式

| 方式 | 说明 | 适用场景 |
|------|------|---------|
| 自定义 Function Calling | 在 API 请求中通过 `tools` 参数定义工具 | 直接调用模型 API 的开发者 |
| 插件（Plugin） | 平台预置或自定义的工具集合，包括官方插件、三方插件和自定义插件 | 智能体/工作流应用 |
| MCP 服务 | 通过模型上下文协议接入标准化外部工具 | 智能体/工作流应用 |
| 内置工具 | 联网搜索、代码解释器等无需额外配置的工具 | Qwen3.6/3.5 系列 plus/flash 模型 |

## 关键参数和配置

### tools 参数定义

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
              "description": "城市名称，如'北京'"
            }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

### 影响工具调用效果的要素

| 要素 | 说明 |
|------|------|
| 工具名称 | 应具有语义，帮助模型理解工具功能 |
| 工具描述 | 功能和使用场景的简要说明，直接影响模型的调用判断 |
| 参数描述 | 参数的含义和格式说明，影响模型提取参数的准确性 |
| 系统提示词 | 在智能体场景中，提示词中明确工具名称和能力描述可提升调用效果 |

###

## 关联主题页

- [model inference](../guides/model-inference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)

