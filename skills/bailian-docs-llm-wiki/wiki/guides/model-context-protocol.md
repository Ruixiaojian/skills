# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型应用（如智能体、工作流）与外部工具服务之间建立安全、可扩展的双向通信通道。它屏蔽了底层协议差异，支持统一接入官方服务、第三方服务及自定义服务，无需为每个工具单独开发适配逻辑。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，已在百炼平台深度集成。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，而是通过百炼平台的**智能体应用**和**工作流应用**间接赋能大模型能力。当前支持以下两类核心使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用 MCP 服务，并动态生成参数（如 `maps_route`、`maps_weather`）。单个智能体最多可同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式添加 MCP 节点并手动指定所用工具（如仅使用 `maps_weather`），输入参数须由上游节点（如大模型节点）结构化输出，输出结果再传递至下游节点处理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 调用链路**，仅限在百炼平台内构建的智能体或工作流应用中使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

MCP 服务配置与调用涉及以下关键参数，需在不同环节准确设置：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | `服务名称` / `描述` | 仅用于控制台识别，不影响模型调用逻辑 | `"长期记忆"` / `"记录并检索个性化信息"` |
| **连接方式** | `type` | 必须与端点路径严格匹配，否则触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 错误 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`） |
| **部署配置** | `command` / `args` | `npx` 或 `uvx` 部署时必需，指定启动命令与包名 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` |
| **远程服务** | `url` | HTTP/SSE 服务地址，必须可公网访问且 TLS 有效 | `"https://your-server.com/sse"` |
| **鉴权凭证** | 环境变量或 KMS 凭据 | 敏感字段（如 `AMAP_MAPS_API_KEY`）需通过 KMS 加密存储，禁止明文填写 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) | `YOUR_ENV_KEY: YOUR_ENV_VALUE` |

## 使用方式

### 1. 接入官方 MCP 服务  
开通后即可在智能体/工作流中直接选择使用。以 Amap Maps 为例：  
- 进入 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击卡片 → **立即开通**；  
- 在智能体配置页添加该服务，或在工作流中拖入 MCP 节点并选择 `maps_weather` 工具。

### 2. 外部调用（第三方集成）  
支持两种模式：  
- **一键配置**：对接 Cherry Studio、Cursor 等 IDE，自动注入 `DASHSCOPE_API_KEY` 和服务元数据；  
- **SDK 编码集成**：使用 `mcp` SDK + OpenAI 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点，实现工具发现与调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

### 3. 自定义部署  
提供三种路径：  
- **脚本部署**（`npx`/`uvx`）：适用于 Node.js/Python 开发的 MCP 服务包；  
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；  
- **OpenAPI 导入**：将阿里云产品 OpenAPI（如 OSS、ECS）发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问本地资源（文件、硬件）或用户私有数据库**；  
  - 若需访问云数据库等远程资源，必须配置 FC 的 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：  
  - 百炼已全面升级至 **Streamable HTTP 协议**（`/mcp`），旧版 SSE（`/sse`）仍支持但需确保 `type` 与路径匹配，否则报错 `11200058`；  
  - 自定义服务若使用私有 npm 仓库，**暂不支持直接部署**，需发布至公共仓库或改用 SSE 连接 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **计费与限流**：  
  - 官方服务（如联网搜索）有免费额度（2000 次/月）和 QPS 限制（15 QPS，主账号与 RAM 子账号共享）；  
  - 自定义服务按模式计费：基础模式按调用时长（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒） [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

- **调试建议**：  
  - 遇到连接失败（如 `MCP_CONNECTION_REFUSED`），优先执行 `curl <服务地址>` 测试连通性；  
  - 工具调用失败时，检查提示词是否明确声明工具名称与能力，避免模型因意图模糊而跳过调用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)


