# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的信息交互通道。它屏蔽了不同工具的底层实现差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中统一调用。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了深度集成与优化。

## 支持的模型/功能

MCP 本身不绑定特定模型，而是作为**工具调用协议层**运行于百炼应用架构中，当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动决策是否调用、调用哪个 MCP 工具及参数（如 `maps_route`、`web_search`），支持单次对话中多次调用多个工具（最多同时配置 5 个 MCP 服务）[原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式配置 MCP 节点并手动指定所用工具（如 `maps_weather`），输入参数须由上游节点（如大模型节点）结构化提取，输出结果再传递至下游节点进行后处理 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**。文档 5 明确指出：“MCP 服务能否在调用千问 API 时接入？不可以。阿里云百炼 MCP 服务需集成在**智能体**或**工作流**应用中使用，不能直接在调用千问 API 时接入。” 因此，若需工具调用能力，必须通过百炼平台的应用构建界面配置，而非 SDK 直接调用 Qwen 模型接口。

官方已提供多种预置 MCP 服务（如 Amap Maps、Firecrawl、WebSearch），亦支持自定义部署三类服务：  
① 使用脚本部署（npx/uvx 托管本地 MCP Server）；  
② 从 AI 网关导入现有 RESTful API；  
③ 从阿里云 OpenAPI 导入云产品操作能力 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **服务配置** | `type`（`stdio` / `sse` / `streamableHttp`） | 必须与接入端点路径严格匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp`；配置错误将导致 `11200058` 或 `11200059` 错误 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| | `command` & `args`（脚本部署） | 如 `npx -y @modelcontextprotocol/server-memory`，版本更新后需手动重新部署 |
| | `url`（远程 HTTP） | 必须可公网访问，且函数计算 FC 出口 IP 需加入目标服务白名单（如云数据库） |
| **调用控制** | `DASHSCOPE_API_KEY` | 外部调用必需，用于鉴权；错误或失效将触发 `11200049`（HTTP 401）错误 |
| | `KMS 凭据` | 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 加密存储，避免明文泄露 |

## 使用方式

### 1. 开通与部署
- **云部署服务**：在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 选择服务（如 Amap Maps），点击“立即开通”即可使用（试用版免填 API Key）。
- **自定义服务**：
  - 脚本部署：在 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) 中选择“使用脚本部署”，粘贴 JSON 配置（含 `mcpServers` 字段）；
  - AI 网关/OpenAPI 导入：需预先在对应平台托管服务，再通过百炼控制台导入。

### 2. 应用内集成
- **智能体**：创建应用 → 添加 MCP 服务（最多 5 个）→ 测试对话（如“从杭州萧山机场到西湖景区”自动触发路径规划）。
- **工作流**：拖入 MCP 节点 → 选择具体工具（如 `maps_weather`）→ 配置输入参数引用（如 `信息提取/result`）→ 连接上下游节点。

### 3. 外部调用
- **第三方 IDE 集成**：支持 Cherry Studio、Cursor，可通过“一键配置”自动注入 MCP Server 配置（含 `AliyunBailianMCP_amap-maps` 名称与 URL）。
- **SDK 编程集成**：使用 `mcp` Python SDK + `openai` 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点，调用 `list_tools()` 获取工具列表并转换为 OpenAI `tools` 格式 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地资源（如本地数据库、文件）**；  
  - 访问远程云服务（如 RDS）需配置 FC 出口 IP 白名单或 VPC 打通；  
  - 私有 npm/PyPI 仓库暂不支持直接部署，需发布至公共仓库或改用 SSE 连接。

- **协议与兼容性**：  
  - 百炼已全面升级至 **Streamable HTTP 协议（`/mcp`）**，旧版 SSE（`/sse`）需手动取消再开通以完成升级；  
  - `type` 字段必须与端点路径一致，否则触发 `11200058`（HTTP 405）或 `11200059`（HTTP 404）错误。

- **计费与限流**：  
  - 云部署服务：联网搜索免费额度 2000 次/月，超量后 29 元/千次；Amap Maps 限时免费；  
  - 自定义服务：基础模式按调用时长计费（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒）；  
  - 全局限流：同一主账号及其 RAM 子账号共享 15 QPS 限流阈值。

- **调试建议**：  
  - 遇 `MCP_CONNECTION_REFUSED`（11200044）等错误，优先执行 `curl <服务URL>` 测试连通性；  
  - 工具调用失败时，检查提示词是否明确指令（如“调用 Amap Maps 规划路线”），必要时升级至 Qwen-Max 等更强模型。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


