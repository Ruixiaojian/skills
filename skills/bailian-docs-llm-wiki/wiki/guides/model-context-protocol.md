# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立可互操作的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入各类能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**能力接入层**，供百炼平台内的以下两类应用调用：
- **智能体应用**：支持自动推理并动态调用最多 5 个已配置的 MCP 服务（如 `Amap Maps` 的路径规划、`Sequential Thinking` 的逻辑推理），无需显式指定工具；  
- **工作流应用**：支持手动编排，每个 MCP 节点仅绑定一个具体工具（如 `maps_weather`），需通过前置大模型节点解析自然语言输入为结构化参数，再传递至 MCP 工具执行 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

当前官方已预置多种 MCP 服务，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，均支持一键开通使用；同时支持三类自定义部署方式：  
- 使用脚本部署（npx/uvx 托管本地 MCP Server）；  
- 从 AI 网关导入（将现有 RESTful API 封装为 MCP 工具）；  
- 从阿里云 OpenAPI 导入（将 OSS/ECS 等云产品能力暴露为 MCP 工具） [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出 MCP 服务“**不能直接在调用千问 API 时接入**”，即 MCP 仅限百炼平台内智能体/工作流场景，不支持通过 DashScope SDK 直接调用千问模型时注入 MCP 工具 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **服务配置** | `type`（`stdio`/`sse`/`streamableHttp`） | 必须与接入端点严格匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp`；配置错误会导致 `11200058` 错误码 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| **部署模式** | `基础模式` / `极速模式` | 基础模式按调用时长计费（0.000156 元/秒），无部署费；极速模式额外收取部署费（0.000036 元/秒），适合高频调用场景 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) |
| **安全凭证** | KMS 加密凭据 | 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 凭据加密，不可明文填写 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| **外部调用** | `DASHSCOPE_API_KEY` + `mcp_url` | 外部 SDK 集成时需提供百炼 API Key 和服务地址（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），且必须使用 `streamableHttp` 协议 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |

## 使用方式

### 平台内集成（智能体/工作流）
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片点击「立即开通」；  
2. **添加到应用**：  
   - 智能体：在应用编辑页「MCP 服务」区域添加，最多 5 个；  
   - 工作流：拖入「MCP 节点」，手动选择工具并绑定输入参数（如引用上游节点输出）；  
3. **提示词优化**：明确指令工具名称与能力（例：“调用 Amap Maps MCP 服务规划杭州到上海的路线”），避免模糊表述导致调用失败 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

### 外部 SDK 集成
1. 安装依赖：`pip install openai mcp`；  
2. 初始化 `streamablehttp_client`，传入 `mcp_url` 和 `Authorization` 头；  
3. 调用 `session.list_tools()` 获取工具列表，转换为 OpenAI `tools` 格式；  
4. 在 `chat.completions.create` 中启用 `tools`，处理 `tool_calls` 并通过 `session.call_tool()` 执行 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络限制**：自定义 MCP 服务托管于函数计算 FC，**无固定出口公网 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
- **本地资源不可达**：不支持访问用户本地文件、硬件或数据库，仅限云端可访问服务 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
- **版本同步**：通过 `npx/uvx` 部署的服务，上游包更新后**不会自动生效**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文输入模型，**直接增加输入 [Token](../concepts/token.md) 数量**；丰富上下文也可能间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
- **协议兼容性**：旧版 SSE 服务需手动升级为 Streamable HTTP 协议，否则外部调用可能失败 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


