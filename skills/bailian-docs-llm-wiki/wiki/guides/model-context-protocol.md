# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交互通道。它屏蔽了底层工具的实现细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于开源 MCP 标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 支持的模型/功能

MCP 本身是协议层，不绑定特定模型，但其调用能力需由百炼平台内支持 MCP 的**应用类型**承载：

- **智能体应用**：支持自动推理调用（无需显式指定工具），最多同时接入 5 个 MCP 服务；适用于多步协同任务（如路径规划+天气查询+图表绘制）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动配置 MCP 节点并指定具体工具（如 `maps_weather`），适合确定性、单步调用场景；常配合大模型节点完成参数提取与结果摘要 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 调用链路**，仅限百炼平台内的智能体或工作流应用使用，此限制在文档 5 中明确说明 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 示例/取值 |
|------|------|-----------|
| `type` | MCP 服务连接方式，决定协议和端点匹配 | `"stdio"`（npx/uvx）、`"sse"`（旧版）、`"streamableHttp"`（新版，默认） |
| `url` | 远程 MCP Server 地址（仅 `streamableHttp`/`sse`） | `"https://your-server.com/mcp"` |
| `command` + `args` | 本地脚本启动命令（仅 `stdio`） | `"npx"` + `["-y", "@mcp/server-memory"]` |
| `env` | 环境变量（如 API Key），敏感信息需通过 KMS 凭据加密 | `{"AMAP_MAPS_API_KEY": "xxx"}` |
| 部署模式 | 影响计费与延迟 | `基础模式`（按调用时长计费，有冷启动）、`极速模式`（按部署+调用双计费，常驻） |

## 使用方式

1. **开通服务**  
   - 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击服务卡片 → “立即开通”（部分服务如 Amap Maps 试用免密钥）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。  
   - 自定义服务：支持三种方式：  
     - *脚本部署*：用 npx/uvx 启动开源或自研 MCP Server（需发布至 npm/PyPI）；  
     - *AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；  
     - *OpenAPI 导入*：将阿里云产品 OpenAPI 快速转为 MCP 工具 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

2. **集成到应用**  
   - 智能体：在应用配置页“添加 MCP 服务”，选择已开通服务即可；模型根据对话自动触发调用。  
   - 工作流：拖入 MCP 节点 → 选择工具 → 通过变量引用上游节点输出（如 `信息提取/result`）作为输入参数。

3. **外部调用**  
   - 支持 Cherry Studio、Cursor 等客户端一键配置；  
   - 开发者可通过 MCP SDK（如 `mcp.client.streamable_http`）结合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，详见 Python 示例代码 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务托管于函数计算 FC，无固定公网 IP，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**不支持访问用户本地资源（如本地文件、数据库）** [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：百炼已全面升级至 Streamable HTTP 协议（`/mcp` 端点），旧版 SSE（`/sse`）需手动升级；配置中 `type` 必须与端点路径严格匹配（如 `"streamableHttp"` 对应 POST `/mcp`），否则报错 `11200058` [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **调试与错误**：常见错误码（如 `11200044` 连接拒绝、`11200051` 限流）需结合 `curl` 测试、FC 日志及下游服务文档排查；自定义服务版本更新后需**手动重新部署**，不会自动同步 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回内容会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 数量**；复杂响应也可能间接提升输出 [Token](../concepts/token.md) [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


