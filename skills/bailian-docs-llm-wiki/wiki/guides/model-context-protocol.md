# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一接入和调用各类能力。MCP 基于开源标准 [MCP 官方规范](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了生产级增强与托管支持。

## 支持的模型与功能

MCP 本身是协议层，不绑定特定模型，但其能力需通过百炼平台的**智能体应用**或**工作流应用**触发。当前支持以下两类核心使用场景：

- **智能体应用**：大模型根据自然语言输入自动判断是否调用、调用哪个 MCP 工具及传入参数（如 `maps_route` 或 `web_search`），适用于对话式交互。
- **工作流应用**：开发者显式编排 MCP 节点，每个节点绑定一个具体工具（如 `maps_weather`），并手动配置输入/输出参数传递路径，适用于确定性任务链。

官方已预置多种 MCP 服务，包括 [Amap Maps](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)（地理信息）、[WebSearch](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)（联网搜索）、[Firecrawl](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)（网页爬取）等；同时支持自定义部署任意符合 MCP 协议的服务。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅集成于百炼平台内的智能体/工作流应用，**不可用于直连 DashScope Qwen API 的独立调用**。

## 关键参数

MCP 服务配置与调用涉及以下关键参数，需在控制台或 SDK 中正确设置：

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **服务元信息** | `服务名称`、`描述` | 仅用于控制台识别，不影响模型调用逻辑 | `"高德天气"`、`"查询实时城市天气"` |
| **连接方式** | `type` | 必须与端点协议严格匹配：<br>- `"sse"` → 对应 `/sse` 端点（旧版）<br>- `"streamableHttp"` → 对应 `/mcp` 端点（新版） | `"streamableHttp"` |
| **部署配置** | `安装方式` | 决定运行环境：<br>- `npx`（Node.js）、`uvx`（Python）→ 托管至函数计算<br>- `http` → 连接远程 SSE 服务 | `"npx"` |
| **计费模式** | `部署方式` | 影响成本与延迟：<br>- **基础模式**：按调用时长计费（0.000156 元/秒），有冷启动延迟<br>- **极速模式**：额外收取部署时长费（0.000036 元/秒），常驻内存降低延迟 | `"基础模式"` |
| **安全凭证** | `KMS 凭据` | 敏感配置（如 API Key）必须通过 KMS 加密，**禁止明文填写** | `kms://acs:kms:cn-beijing:1234567890:alias/mcp-amap-key` |

## 使用方式

### 1. 接入平台内应用（智能体/工作流）
- **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务并点击“立即开通”（如 [Amap Maps](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。
- **添加到智能体**：在智能体编辑页 > “工具” > “添加 MCP 服务”，最多可选 5 个；模型将基于提示词自动调度。
- **编排工作流**：拖入“MCP 节点”，选择具体工具（如 `maps_weather`），手动绑定输入变量（如 `信息提取/result`）与输出变量。

### 2. 外部调用（第三方应用/自研项目）
- **一键集成**：支持 Cherry Studio、Cursor 等 IDE，通过控制台“外部调用”页点击“一键配置”完成自动注册。
- **SDK 编程集成**：
  - 安装：`pip install openai mcp`
  - 使用 `streamablehttp_client` 连接百炼 MCP endpoint（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）
  - 通过 `ClientSession.list_tools()` 获取工具列表，转换为 OpenAI 兼容格式后传入 `chat.completions.create(..., tools=...)`
  - 完整示例见 [外部调用文档](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)

## 限制和注意事项

- **网络与权限限制**：  
  自定义 MCP 服务托管于函数计算 FC，**无固定公网出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**无法访问用户本地资源**（如本地文件、硬件设备）[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议兼容性**：  
  百炼已全面升级至 **Streamable HTTP 协议**（对应 `/mcp` 端点），旧版 SSE（`/sse`）已逐步淘汰。配置时务必确保 `type` 与端点路径一致，否则将触发错误码 `11200058`（HTTP 方法不被允许）或 `11200059`（404 Not Found）。

- **版本与更新**：  
  通过 `npx`/`uvx` 部署的服务**不会自动更新**。当上游包（如 `@modelcontextprotocol/server-memory`）发布新版本时，必须手动重新部署 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **调试与排错**：  
  遇到连接失败（如 `11200044`）、超时（`11200045`/`11200046`）或协议错误（`11200054`），应优先执行 `curl <MCP_URL>` 测试连通性，并检查函数计算 FC 日志（需提前开启日志服务）[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **Token 开销**：  
  MCP 调用返回的内容会作为上下文注入模型输入，**直接增加输入 Token 数量**；同时可能因信息更丰富而间接增加输出 Token [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)


