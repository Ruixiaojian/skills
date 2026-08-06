# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具接入机制，用于在大模型推理过程中动态调用外部能力（如地图、天气、知识图谱等），无需为每个工具单独开发适配层。MCP 服务可原生集成于智能体与工作流应用，并支持通过 Streamable HTTP 协议对外暴露，供第三方客户端（如 Cherry Studio、Cursor）或自研项目调用。

## 支持的模型/功能

MCP 本身不绑定特定大模型，但其调用效果高度依赖所配置的推理模型能力：
- **智能体应用**：支持最多同时配置 5 个 MCP 服务，由大模型根据对话上下文自动判断是否调用、调用哪个服务及传入参数（如 `Amap Maps` 规划路径、`Sequential Thinking` 辅助逻辑推理）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点仅能绑定一个具体工具（如 `maps_weather`），需通过前置大模型节点（如信息提取）显式解析参数并传递 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部调用**：支持通过 MCP SDK（如 `mcp.client.streamable_http`）或一键配置至 Cherry Studio/Cursor 等客户端，使用标准 Streamable HTTP 协议通信 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 3 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅限百炼平台内智能体/工作流或通过外部 MCP 客户端调用，**不支持**在直接调用 `qwen-*` 系列 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)时嵌入 MCP 工具调用。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **服务配置** | `type`（`stdio`/`sse`/`streamableHttp`） | 必须与服务端接入路径严格匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp`；配置错误将导致 11200058 错误码 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。 |
| **认证** | `DASHSCOPE_API_KEY` | 外部调用必需，需配置为请求 Header `Authorization: Bearer <key>`；API Key 无效或过期将触发 `MCP_SERVER_HTTP_UNAUTHORIZED`（11200049）错误 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。 |
| **环境变量** | `AMAP_MAPS_API_KEY` 等 | 官方服务（如 Amap Maps）试用版免填，商业化定制需手动注入；敏感密钥必须通过 KMS 凭据加密管理 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。 |

## 使用方式

1. **开通服务**  
   - 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 `Amap Maps`）→ 点击「立即开通」→ 确认。  
   - 自定义服务：支持三种方式：① **脚本部署**（npx/uvx 托管至函数计算 FC）；② **AI 网关导入**（封装现有 RESTful API）；③ **OpenAPI 导入**（对接阿里云产品）[原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

2. **集成到应用**  
   - **智能体**：创建后，在「MCP 服务」配置页添加已开通服务，无需指定工具，由模型自主调度。  
   - **工作流**：拖入「MCP 节点」→ 选择服务及具体工具 → 通过「引用」绑定上游节点输出（如 `信息提取/result`）作为输入参数。

3. **外部调用**  
   - 使用 `mcp.client.streamable_http` SDK 初始化客户端，传入 `mcp_url`（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）和 `headers`（含 `DASHSCOPE_API_KEY`）；  
   - 调用 `session.list_tools()` 获取工具列表，再通过 `session.call_tool()` 执行具体操作（详见文档 5 的 Python 示例）。

## 限制和注意事项

- **网络与资源限制**：  
  - MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
  - **不支持访问本地资源**（如本地文件、硬件设备），此类服务需本地部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：  
  - 百炼已全面升级至 **Streamable HTTP 协议**（非旧版 SSE），已开通用户需先「取消开通」再「重新开通」以完成升级 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。  
  - 自定义服务若使用 `npx`/`uvx` 部署，版本更新后**不会自动同步**，必须手动重新部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **计费与性能**：  
  - 官方服务调用费用由第三方收取（如高德 API），百炼不额外收费；自定义服务按「基础模式」（按调用时长计费）或「极速模式」（按部署+调用时长计费）计费 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。  
  - MCP 调用会增加模型 [Token](../concepts/token.md) 消耗：返回结果作为上下文计入输入 [Token](../concepts/token.md)；更丰富的上下文可能导致输出更详细，间接增加输出 [Token](../concepts/token.md) [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


