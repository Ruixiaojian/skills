# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息通道。通过 MCP，开发者无需为每个工具单独开发适配层，即可将官方或自定义工具统一接入智能体和工作流应用。该协议基于开源 MCP 标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部调用 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 支持的模型/功能

MCP 本身不绑定特定大模型，而是作为**[工具调用](../concepts/tool-use.md)中间件**，由百炼平台内的推理模型驱动调用。当前支持以下两类集成场景：

- **智能体应用**：模型根据自然语言对话自动判断是否及何时调用 MCP 工具（如 `maps_route`, `web_search`），支持单次对话中多次调用多个工具（最多 5 个）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点并手动指定所用工具（如 `maps_weather`），输入参数须经前置大模型节点解析，输出参数可传递至后续节点进行后处理。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**；仅限在百炼平台内构建的智能体或工作流应用中使用，不支持通过 `dashscope` SDK 直接调用时注入 MCP 工具 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `type` | string | 协议传输类型，必须与端点路径严格匹配：<br>`"sse"` → `/sse`（旧版，已逐步淘汰）<br>`"streamableHttp"` → `/mcp`（新版默认） | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `url` | string | MCP Server 地址，格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-id}/mcp` | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `headers.Authorization` | string | 必须携带有效的 `DASHSCOPE_API_KEY`，格式为 `Bearer <key>` | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `env` | object | 自定义环境变量（如 `AMAP_MAPS_API_KEY`），仅对脚本部署有效；敏感值需通过 KMS 凭据加密 | [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |

## 使用方式

### 1. 接入官方 MCP 服务
- 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 `Amap Maps` 或 `WebSearch`）→ 点击「立即开通」。
- 开通后，在智能体/工作流编辑器中添加该服务即可使用，无需额外配置密钥（试用版）。

### 2. 部署自定义 MCP 服务
支持三种方式：
- **脚本部署**（推荐）：适用于 Node.js/Python 开发的 MCP Server，通过 `npx` 或 `uvx` 启动，托管于函数计算 FC [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具，适用于内部业务接口。
- **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）的 OpenAPI 快速发布为 MCP 工具。

### 3. 外部调用（第三方集成）
- 支持 Cherry Studio、Cursor 等客户端一键配置；
- 或通过 MCP SDK 编程调用（需安装 `mcp` 和 `openai` 包），示例代码见 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问本地资源（如本地数据库、文件）**；  
  - 若需访问云数据库等远程资源，必须配置 FC 的 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议兼容性**：  
  - 所有服务必须使用新版 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）已停止维护；  
  - 配置中 `type` 与 URL 路径必须严格一致，否则触发错误码 `11200058`（HTTP 405）或 `11200059`（HTTP 404）。

- **计费与限流**：  
  - 官方服务如 `WebSearch` 免费额度为 2000 次/月，超限后 29 元/千次；  
  - 云部署服务限流为 **15 QPS**（主账号与 RAM 子账号共享）；  
  - 自定义服务按「基础模式」（按调用时长计费）或「极速模式」（按部署+调用时长计费）计费，费率均为 0.000156 元/秒 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试建议**：  
  - 遇到连接失败（如 `11200044`）、超时（`11200045/46`）或协议错误（`11200054`），优先执行 `curl <mcp-url>` 测试连通性，并检查 FC 日志；  
  - 模型未触发[工具调用](../concepts/tool-use.md)时，应优化提示词明确指令（如“调用 Amap Maps MCP 服务规划路线”），而非依赖隐含推理。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


