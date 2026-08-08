# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是百炼平台统一的、标准化的工具集成机制，用于在大模型应用（智能体、工作流）与外部服务之间建立安全、可扩展、协议一致的信息通道。它屏蔽底层接口差异，兼容 Anthropic 开源 MCP 标准，并基于 Streamable HTTP 协议（`/mcp` 端点），支持官方托管服务与开发者自定义服务的统一接入与协同调用。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：MCP 服务作为“可规划工具”参与自主决策链路。模型根据对话意图自动触发调用（无需显式指令），最多同时启用 5 个 MCP 工具；工具调用过程（思考→调用→结果解析）在对话面板中实时可视化，支持回溯调试。
  
- **工作流应用（Workflow）**：MCP 以独立节点形式存在，每个节点**严格绑定一个工具**（如 `maps_weather`）。开发者需手动配置输入参数（支持变量引用 `${node_x.output}`）和输出字段映射，实现确定性编排，适用于需强控制的业务流程（如“搜索→解析→绘图→发送”链路）。

- **高代码应用（Rich Code）**：可通过 `dashscope` SDK 或原生 HTTP 客户端直接集成 MCP 服务。推荐使用 `mcp` 官方 SDK + `streamablehttp_client` 连接 `/mcp` 端点，动态获取工具列表、生成合法参数并处理流式响应，适合需要细粒度控制或与自有系统深度耦合的场景。

> ⚠️ 注意：MCP **不支持**在千问 API 直接调用中接入，也不支持旧版智能体（Agent 1.0）；仅限百炼平台内创建的智能体应用和工作流应用使用。

## 关键参数和配置

| 参数名 | 说明 | 开发者须知 |
|--------|------|------------|
| `tool name` | 工具唯一标识符（如 `web_search`, `quickchart_generate`） | 必须与 MCP 服务注册名完全一致；工作流节点中需显式填写；大小写敏感。 |
| `inputSchema` | 工具输入参数的 JSON Schema（定义字段名、类型、是否必填等） | 模型依赖此 Schema 生成合法参数；缺失或格式错误将导致调用失败或参数为空；建议使用 [JSON Schema Validator](https://json-schema.org/) 验证。 |
| `DASHSCOPE_API_KEY` | 外部调用 MCP 服务时的身份凭证 | 必须通过环境变量或 SDK 显式传入；错误时返回 `11200049` 错误码；生产环境请使用 RAM 子账号最小权限 AK。 |
| `KMS 凭据` | （仅云部署服务）用于加密第三方 API Key 等敏感配置 | 自定义 MCP 服务需自行实现密钥管理；百炼不存储或透传明文密钥。 |

## 面向开发者的实用提示

- ✅ **快速起步**：优先选用官方 MCP 服务（如 `WebSearch`, `Amap Maps`），开通即用，无需部署；控制台「应用配置 → 工具接入」一键添加。
- ✅ **自定义服务部署**：推荐使用 `npx @mcp/server`（Node.js）或 `uvx mcp-server`（Python）启动本地服务，再通过「自定义 MCP」入口注册其公网地址（需 HTTPS + `/mcp` 端点）。
- ✅ **调试技巧**：在智能体测试窗口点击「查看卡片流」，检查 `Tool Call` 卡片中的 `tool_name` 和 `input` 是否符合预期；若调用失败，重点验证 `inputSchema` 与实际传参结构是否匹配。
- ❌ **避坑指南**：
  - 不支持访问本地文件、数据库或硬件设备；
  - 不支持私有 npm/PyPI 仓库或需 VPC 内网访问的服务（除非已打通百炼函数计算网络）；
  - 自定义服务必须暴露标准 `/mcp` 端点，且响应头需包含 `Content-Type: application/json`；
  - 工作流中 MCP 节点的输入参数**不可留空**——即使字段为可选，也需显式传入 `null` 或默认值。

> 💡 提示：MCP 是百炼平台工具能力的事实标准。当需长期维护多工具集成时，建议统一采用 MCP 协议封装，而非混合使用插件（Plugin）机制——二者定位不同：MCP 专注标准化服务接入，插件更侧重轻量级、单点功能快捷调用。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)


