# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交互通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一接入和编排多种能力。该协议基于开源 MCP 标准实现，支持云部署与自定义部署两种模式 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为能力接入层服务于百炼平台上的**智能体应用**和**工作流应用**。当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数，支持最多同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式添加 MCP 节点，并手动指定所用工具（如 `maps_weather`）、输入参数来源（如上游节点输出）和输出参数传递路径，适用于确定性、多步骤的工具链编排。

官方已预置并维护多种 MCP 服务，包括：
- Amap Maps（地理信息、路径规划、天气查询）
- WebSearch（联网搜索，含免费额度与计费规则）
- Firecrawl（网页爬取）
- Sequential Thinking（逻辑推理辅助）
- QuickChart（图表生成）

此外，支持通过三种方式接入自定义 MCP 服务：脚本部署（npx/uvx）、AI 网关导入（封装 RESTful API）、阿里云 OpenAPI 导入（操作云资源） [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 3 提到 MCP 协议已从旧版 SSE 升级为新版 Streamable HTTP 协议，而文档 2 和文档 4 的示例截图及部分配置项仍显示 SSE 相关字段（如 Cherry Studio 配置中类型标注为 `服务器发送事件 (sse)`）。实际部署时应以控制台最新 UI 和 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档中明确的 `streamableHttp` 协议为准，避免因协议不匹配导致 `11200058` 或 `11200059` 错误。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | 服务名称、描述 | 仅用于控制台识别，不影响模型调用逻辑 | `"长期记忆"`, `"记录用户个性化信息"` |
| **连接配置** | `type` | 必填，指定通信协议类型，决定端点路径与请求方法 | `"stdio"`（本地）、`"sse"`（已逐步淘汰）、`"streamableHttp"`（推荐） |
| | `url` | 远程 MCP Server 地址（`type` 为 `streamableHttp` 时必填） | `"https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp"` |
| | `command` / `args` | `type` 为 `stdio` 时指定启动命令与参数 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` |
| **认证与安全** | `Authorization` header | 外部调用时必需，格式为 `Bearer <DASHSCOPE_API_KEY>` | — |
| | KMS 凭据 | 涉及敏感密钥（如 `AMAP_MAPS_API_KEY`）时，必须通过 KMS 加密存储 | — |
| **工具级参数** | `tool.name` | 工具唯一标识符，模型调用时必须精确匹配 | `"maps_weather"`, `"web_search"` |
| | `tool.inputSchema` | JSON Schema 定义输入参数结构，影响模型参数生成准确性 | `{"type": "object", "properties": {"query": {"type": "string"}}}` |

所有参数均需严格遵循 MCP 协议规范，否则将触发 `11200054`（协议解析错误）或 `11200060`（Bad Request）等错误码 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 1. 开通服务
- 访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择目标服务（如 Amap Maps），点击“立即开通”。
- 对于需密钥的服务（如商业化高德地图），在开通流程中通过 KMS 创建并关联加密凭据。

### 2. 在智能体中集成
- 创建智能体后，在「MCP 服务」配置页添加已开通的服务；
- 模型将依据提示词自动决策调用时机与参数，无需显式声明工具名（但提示词中明确工具能力可提升成功率）。

### 3. 在工作流中集成
- 添加 MCP 节点，选择具体工具（如 `maps_weather`）；
- 手动配置输入参数（支持引用上游节点输出，如 `"引用：信息提取/result"`）；
- 输出结果需通过变量引用传递至后续节点（如大模型总结节点）。

### 4. 外部调用（第三方应用或 SDK）
- **集成至 Cherry Studio/Cursor**：在 MCP 服务详情页选择对应客户端，执行“一键配置”或手动导入 JSON 配置；
- **SDK 编程调用**：使用 `mcp.client.streamable_http` 客户端连接，配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)完成多轮工具调用循环（详见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 中的 Python 示例）。

## 限制和注意事项

- **模型兼容性限制**：MCP 服务**仅支持在百炼平台的智能体或工作流应用中使用**，无法直接接入千问 API 的原始调用（如 `dashscope.ChatCompletion.create`）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **网络与权限限制**：
  - 自定义 MCP 服务运行于函数计算 FC 环境，**无固定出口公网 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通；
  - **不支持访问用户本地资源**（如本地文件、硬件设备），此类服务应在本地部署。
- **部署与更新限制**：
  - 通过 `npx`/`uvx` 部署的服务，版本更新后**必须手动重新部署**，不会自动同步；
  - 私有 npm/PyPI 仓库中的包暂不支持直接部署，需发布至公共仓库或改用 `streamableHttp` 连接远程服务。
- **计费与限流**：
  - 云部署服务（如 WebSearch）有明确 QPS 限制（如 15 QPS，主账号与 RAM 子账号共享）和调用费用（29 元/千次）；
  - 自定义服务按“基础模式”（按调用时长计费）或“极速模式”（按部署+调用时长计费）计费，费率均为 0.000156 元/秒 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **调试建议**：
  - 遇到连接失败（如 `11200044`）或超时（如 `11200045`），优先使用 `curl` 测试服务地址连通性；
  - 遇到协议错误（如 `11200054`），务必核对 `type` 与端点路径是否匹配（`streamableHttp` → `/mcp`，`sse` → `/sse`）；
  - 模型调用失败时，首先检查提示词是否清晰表达工具意图，其次确认所选模型是否具备足够推理能力（推荐使用 Qwen-Max 或 Qwen3 系列）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


