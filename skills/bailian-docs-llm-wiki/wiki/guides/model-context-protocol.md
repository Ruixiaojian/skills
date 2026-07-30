# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、天气等服务）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于开源 MCP 标准实现，并针对百炼平台进行了生产级增强与托管支持。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其能力需通过百炼平台的**智能体应用**和**工作流应用**触发与执行。当前支持以下两类服务集成方式：

- **官方 MCP 服务**：由阿里云百炼预部署并托管的云服务，开箱即用，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等。其中 Amap Maps 服务限时免费，WebSearch 提供 2000 次/月免费额度 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 服务**：支持三种部署路径：
  - *使用脚本部署*：通过 `npx`（Node.js）或 `uvx`（Python）直接运行开源或自研 MCP 服务代码；
  - *从 AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *从阿里云 OpenAPI 导入*：将 ECS、OSS 等云产品能力一键发布为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 中提到“百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，但文档 2 和文档 3 的配置示例及截图仍大量使用 `sse` 类型（如 `type: "sse/streamableHttp"`、`/sse` 路径）。实际部署时，请严格按文档 5 错误码说明验证协议匹配性：`"sse"` 必须对应 GET `/sse`，`"streamableHttp"` 必须对应 POST `/mcp`；混用将导致 `11200058` 或 `11200059` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

MCP 服务配置的核心参数取决于部署方式，通用关键项如下：

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `type` | 通信协议类型，决定传输方式与端点路径 | `"stdio"`（本地）、`"sse"`、`"streamableHttp"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `command` / `url` | 启动命令（npx/uvx）或远程服务地址 | `"npx"`, `"https://your-mcp-server/mcp"` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `env` | 环境变量，用于传递密钥、配置等敏感信息 | `{"AMAP_MAPS_API_KEY": "xxx"}` | [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| 部署模式 | 决定计费与延迟特性 | `基础模式（按次计费）` / `极速模式（常驻+调用双计费）` | [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |

> **注意**：敏感环境变量（如 API Key）必须通过 KMS 凭据加密，不可明文写入配置；否则部署将失败或存在安全风险 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

## 使用方式

### 在平台内集成（推荐）
- **智能体应用**：最多可同时添加 5 个 MCP 服务。大模型根据用户输入自动判断是否调用及调用哪个服务，无需显式指定工具名（但提示词中明确工具能力可显著提升成功率）。
- **工作流应用**：每个 MCP 节点仅能绑定一个具体工具（如 `maps_weather`），需手动配置输入参数（常通过前置大模型节点提取）和输出参数映射。

### 外部调用
支持两种标准方式：
- **集成至第三方应用**：一键配置到 Cherry Studio、Cursor 等 IDE，自动注入 MCP Server 配置（含 `DASHSCOPE_API_KEY` 和 URL）。
- **通过 SDK 开发集成**：使用 `mcp` 官方 SDK（如 `streamablehttp_client`）连接百炼 MCP 服务端点，再结合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`qwen-max`）实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地数据库或硬件**；访问云数据库需配置 FC IP 白名单或 VPC 打通；无固定出口 IP，代理场景需额外配置 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：非标准 MCP 实现（如依赖浏览器环境、本地文件系统）无法在百炼云端部署；私有 npm/PyPI 包暂不支持，需发布至公共仓库 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，**直接增加输入 [Token](../concepts/token.md) 数量**；丰富上下文也可能间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **模型调用隔离**：MCP 服务**仅可在百炼智能体/工作流应用中使用，不可直接接入千问 API 调用链** [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **错误排查**：常见连接失败（`11200044`）、超时（`11200045/46`）、认证失败（`11200049`）、协议不匹配（`11200054/58/59`）等问题，均需结合 `curl` 测试、FC 日志及下游服务文档定位 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


