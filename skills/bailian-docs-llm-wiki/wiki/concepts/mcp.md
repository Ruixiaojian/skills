# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化能力接入协议，用于在大语言模型与外部工具服务之间建立安全、可扩展、语义驱动的交互通道。它将工具调用抽象为统一的函数接口，使模型能基于自然语言上下文自主规划、参数化调用，并结构化接收结果，无需开发者手动编写适配胶水代码。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是深度集成于百炼三大应用范式的能力调度层：

- **智能体（Agent）**：MCP 服务作为“可调度工具”直接挂载到智能体配置中（最多 5 个）。模型根据用户输入自动判断是否调用、调用哪个工具及传入参数，整个过程无需人工干预。例如，当用户问“杭州明天天气如何？”，模型可自主调用 `maps_weather` 工具并填充 `{"city": "杭州"}`。
  
- **工作流（Workflow）**：通过显式拖拽 **MCP 节点** 接入工具，输入参数需由上游节点（如大模型节点或变量处理器）结构化输出，输出结果可直接传递给下游节点（如文本生成或条件分支），实现确定性编排。

- **高代码应用**：在 Python 项目中，通过 SDK 的 `MCPTool` 类或 `mcp_client` 模块直接调用已注册的 MCP 服务，支持同步/异步方式，适用于需要精细控制调用逻辑或与业务系统深度耦合的场景。

> ⚠️ 注意：MCP 服务**不能**在直连 DashScope Qwen API（如 `/v1/services/aigc/text-generation`）时使用；必须经由百炼应用容器（智能体/工作流/高代码应用）统一调度，这是平台级的安全与治理边界。

## 关键参数和配置

MCP 的核心配置分为 **服务注册** 和 **工具调用** 两类，均在控制台或 API 中定义：

### 服务注册参数（`mcpServers` 配置项）
| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `service_name` | 服务唯一标识名（仅控制台显示用） | 是 | `"天气查询"` |
| `description` | 工具功能描述，供模型理解能力边界 | 是 | `"获取指定城市的实时天气与预报"` |
| `type` | 协议类型，决定连接方式与端点路径 | 是 | `"streamableHttp"`（对应 `/mcp`）、`"sse"`（对应 `/sse`）、`"stdio"`（本地进程） |
| `url` 或 `command`/`args` | 远程服务地址 或 本地启动命令 | 是（二选一） | `https://weather-api.example.com/mcp` 或 `["npx", "-y", "@my-mcp-server"]` |
| `env` | 敏感环境变量（如 API Key），**必须使用 KMS 凭据 URI** | 否（但推荐） | `{"AMAP_KEY": "kms://acs:kms:cn-beijing:1234567890123456:alias/your-key"}` |

### 工具调用参数（模型侧感知）
| 参数 | 说明 | 示例 |
|------|------|------|
| `tool_name` | 模型在 `tool_calls` 中指定的函数名 | `"maps_weather"` |
| `inputSchema` | JSON Schema 定义输入结构，影响模型参数提取准确性 | `{ "type": "object", "properties": { "city": { "type": "string" } }, "required": ["city"] }` |

> ✅ 实践提示：`type` 字段必须与服务端实际监听路径严格匹配（如 `type: "sse"` → 服务必须响应 `/sse` 端点），否则触发 `11200058` 错误；所有敏感凭证务必通过 KMS 加密，明文写入将导致配置失败。

## 面向开发者，简洁实用

- **快速上手**：访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通官方服务（如 WebSearch、QuickChart），无需开发即可在智能体中启用。
- **自定义服务**：推荐使用 `npx` 脚本部署开源 MCP Server（如 [`mcp-server-python`](https://github.com/modelcontextprotocol/server-python)），5 分钟完成本地调试与上线。
- **调试技巧**：在智能体测试页开启「工具调用详情」开关，可查看模型生成的 `tool_calls` 内容、实际请求 payload 及原始响应，快速定位参数提取或服务连通问题。
- **错误排查**：常见错误码 `11200058`（HTTP 方法不支持）→ 检查 `type` 与服务端路径是否匹配；`11200061`（服务不可达）→ 检查 `url` 可访问性及 `env` 中 KMS 凭据状态。
- **兼容性**：所有支持 MCP 的服务均可跨平台复用（如 Cherry Studio、Cursor），但**在百炼内必须通过智能体/工作流/高代码应用调用**——这是平台强制执行的隔离与审计要求。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [managed agents api](../api/managed-agents-api.md)
- [application support](../guides/application-support.md)


