# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化工具调用协议，用于在大语言模型与外部服务之间建立安全、声明式、可扩展的信息通道。它不绑定特定模型，而是作为统一抽象层，使模型能基于上下文自主决策调用时机与参数，或由工作流显式编排执行。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用**：MCP 服务以“能力”形式挂载。模型根据用户输入和对话历史自动判断是否调用、调用哪个工具、传入哪些参数（如将“查上海今天空气质量”解析为 `air_quality` 工具调用）。单个智能体最多配置 5 个 MCP 服务。
- **工作流应用**：MCP 以独立节点形式存在，需手动拖入画布、选择具体工具（如 `WebSearch`）、并显式绑定上游输出（如 `引用：信息提取/result`）作为输入参数。每个 MCP 节点仅封装一个工具调用。
- **Managed Agents（托管智能体）**：MCP 服务可作为扩展能力挂载到 Agent 的 `tools` 列表中，与内置 `bash`、`read` 等沙箱工具协同使用，支持长时多步任务中的混合工具调用（如先爬网页再分析文件）。
- **Skill 和插件场景**：MCP 与 Skill、插件属并列能力扩展机制，但定位不同——MCP 专注**标准 HTTP 工具集成**（尤其适合已有 API 或云服务），而 Skill 侧重**无代码 ZIP 包封装的语义化任务**，插件则更通用（支持 Header/Query 鉴权等灵活配置）。三者可共存于同一智能体，由模型按需路由。

## 关键参数和配置

### 服务元数据（创建 MCP 服务时必填）
- `服务名称`：控制台内标识名，不影响调用逻辑；
- `描述`：简要说明用途，便于团队管理；
- `安装方式`：决定启动方式，取值为 `npx`（Node.js）、`uvx`（Python）或 `http`（远程服务）；
- `部署方式`：影响计费与延迟，选 `基础模式`（按次计费）或 `极速模式`（常驻实例 + 按次调用双计费）；
- `部署地域`：建议与主业务同地域（如北京），降低网络延迟。

### 运行时参数（按需配置）
- `env`：环境变量对象，**必须通过 KMS 加密注入敏感凭据**（如 `AMAP_MAPS_API_KEY`），禁止明文填写；
- `mcpServers`：定义服务端点，关键字段包括：
  - `type`: 必须为 `"streamableHttp"`（当前唯一支持类型，已替代旧版 SSE）；
  - `endpoint`: 必须为 `/mcp`（如 `https://your-service.com/mcp`）；
- 工作流中 MCP 节点的 `输入参数`：必须显式绑定上游变量（如 `引用：信息提取/result`），不可留空或依赖模型自动填充。

## 面向开发者，简洁实用

- ✅ **首选协议**：始终使用 `streamableHttp` 类型和 `/mcp` 端点，避免 `SSE` 相关错误（如错误码 `11200058`）；
- ✅ **快速接入官方服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通即用（试用服务免配 Key）；
- ✅ **自定义服务三路径**：
  - 脚本部署：`npx mcp-server-http --port 3000` 启动开源服务后，填入 `http` 安装方式；
  - AI 网关封装：将任意 RESTful API 封装为 MCP 工具，自动处理鉴权与参数映射；
  - OpenAPI 导入：一键将 ECS、OSS 等阿里云产品操作发布为 MCP 工具；
- ✅ **调试技巧**：在工作流中启用「节点日志」查看 MCP 请求/响应原始内容；智能体调试时关注 `tool_calls` 字段确认模型是否生成了正确工具调用；
- ⚠️ **注意限制**：MCP 服务运行于函数计算 FC，不支持长连接、WebSocket 或后台持久化任务；所有工具调用均为同步 HTTP 请求，超时默认 30 秒（不可配置）。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


