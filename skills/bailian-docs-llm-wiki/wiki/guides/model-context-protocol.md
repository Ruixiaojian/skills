# model context protocol

Model Context Protocol（MCP）是阿里云百炼平台提供的标准化工具接入协议，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展的上下文交互通道。它屏蔽了底层接口差异，支持统一声明、自动发现和按需调用，无需为每个工具单独开发适配逻辑。MCP 服务既可开箱即用，也可自定义部署，并兼容主流外部客户端。

## 支持的模型/功能

MCP 本身是协议标准，不绑定特定模型；其功能由百炼平台的**智能体应用**和**工作流应用**承载：

- **智能体应用**：支持自动推理调用（最多同时配置 5 个 MCP 服务），大模型根据对话上下文自主判断是否及何时调用工具，适用于多步协同任务（如“从杭州萧山机场到西湖景区的三种公交方案”需多次调用 Amap Maps）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点并手动指定工具（如 `maps_weather`），输入参数须经前置大模型节点提取，输出需经后置节点处理，适用于确定性、单路径任务（如城市天气查询）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部客户端集成**：支持 Cherry Studio、Cursor 等第三方工具通过 Streamable HTTP 或 SSE 协议接入，需通过百炼 MCP 广场一键配置或手动导入 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 5 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即纯 API 调用（如 `dashscope.ChatCompletion.create`）不支持 MCP 工具调用能力，必须通过百炼平台的智能体或工作流应用容器使用。

## 关键参数

| 参数类别 | 名称 | 说明 | 示例/约束 |
|----------|------|------|-----------|
| **服务配置** | `type` | 协议传输类型，决定端点路径和请求方式 | `"sse"` → `/sse`（GET）；`"streamableHttp"` → `/mcp`（POST）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| | `command` / `url` | 启动命令（npx/uvx）或远程服务地址 | `npx -y @modelcontextprotocol/server-memory`；`https://your-mcp-server/sse` |
| | `env` | 环境变量，用于敏感配置（如 API Key） | `"AMAP_MAPS_API_KEY": "xxx"`（需配合 KMS 凭据加密）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| **调用控制** | `tool_name` | 工具唯一标识符，模型调用时必需 | `maps_weather`, `web_search` |
| | `inputSchema` | JSON Schema 定义输入参数结构 | `{ "type": "object", "properties": { "city": { "type": "string" } } }` |

## 使用方式

1. **开通服务**  
   - 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通”。试用服务无需填写 API Key；商业化定制需配置 KMS 加密的凭据 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。  
   - 自定义服务：支持三种方式：  
     - *脚本部署*：使用 npx/uvx 托管开源或自研 MCP Server（如 Knowledge Graph Memory）；  
     - *AI 网关导入*：将现有 RESTful API 封装为 MCP；  
     - *OpenAPI 导入*：将阿里云产品（OSS/ECS）操作发布为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

2. **集成到应用**  
   - *智能体*：创建智能体 → “添加 MCP 服务” → 从已开通列表选择 → 保存后即可自动触发调用。  
   - *工作流*：拖入 MCP 节点 → 选择工具 → 配置输入（如引用前置节点输出）→ 连接上下游节点 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。  
   - *外部调用*：获取 DASHSCOPE_API_KEY → 使用 MCP SDK（如 `streamablehttp_client`）连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp` → 调用 `list_tools()` 和 `call_tool()` [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（替代旧版 SSE），已开通用户需先“取消开通”再“重新开通”以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **网络与权限**：  
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
  - 不支持访问本地资源（文件、硬件、本地数据库）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **部署与更新**：  
  - npx/uvx 部署的服务版本**不会自动更新**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；  
  - 私有 npm/PyPI 包暂不支持直接部署，需发布至公共仓库或改用 SSE 远程连接 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **调用可靠性**：  
  - 模型调用 MCP 的成功率高度依赖提示词质量，需在 System Prompt 中明确工具名称、描述和输入格式 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；  
  - 遇到连接失败（如 `MCP_CONNECTION_REFUSED`）应优先执行 `curl <服务地址>` 测试连通性，并检查下游服务日志 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


