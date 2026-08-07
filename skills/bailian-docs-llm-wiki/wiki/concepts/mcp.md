# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化能力接入协议，用于在大语言模型与外部工具之间建立可互操作、声明式调用的信息通道。它基于开源 MCP 规范（[modelcontextprotocol.io](https://modelcontextprotocol.io/)）实现，将工具抽象为统一语义接口，屏蔽底层实现差异，使模型能自动理解、规划并安全调用地图、搜索、图表生成等各类能力。

## 在百炼平台的不同场景中如何使用

MCP 是百炼平台统一的能力调度层，**不直接暴露给千问 API（如 `dashscope.ChatCompletion.create`）**，仅在以下三类托管应用中生效：

- **智能体（Agent 2.0）应用**：  
  模型自动推理并调用已配置的 MCP 服务（最多 5 个），无需显式指定工具名。例如用户说“帮我画一张近7天北京气温折线图”，模型可自主调用 `QuickChart` 服务，传入结构化参数生成图表。知识库、官方插件（如 `quark_search`）及自定义插件均可一键转换为 MCP 服务后接入。

- **工作流（Workflow）应用**：  
  以 MCP 节点形式手动编排，每个节点绑定一个具体 MCP 工具（如 `maps_weather`）。需前置大模型节点提取参数（如城市、日期），后置节点解析返回结果，适合流程确定、结果需精确控制的场景。

- **Managed Agents（托管智能体）**：  
  在沙箱环境中扩展外部能力，通过 `tools: [{"type": "mcp", "service_id": "amap_maps"}]` 声明接入。支持与内置工具（`bash`、`read` 等）协同执行多步任务，例如先调用 `Amap Maps` 获取路线，再用 `bash` 计算通勤时间。

> ✅ 提示：所有 MCP 服务均需先在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通或部署，再在对应应用中添加使用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | 是 | 协议传输类型，决定连接方式与端点路径 | `"streamableHttp"`（推荐，对应 `/mcp`）；`"sse"`（旧版，对应 `/sse`） |
| `command` 或 `url` | string | 是 | 启动方式（本地脚本）或远程服务地址 | `npx @modelcontextprotocol/server-memory` 或 `https://your-mcp-service.example.com/mcp` |
| `env` | object | 否 | 注入环境变量，用于传递密钥、API Key 等敏感信息（建议配合 KMS 加密） | `{ "AMAP_KEY": "${kms://xxx}" }` |
| `inputSchema` | JSON Schema | 是 | 定义工具输入参数结构，直接影响模型参数生成准确性 | `{ "type": "object", "properties": { "city": { "type": "string" } } }` |

⚠️ 注意：  
- `type` 与实际服务端点路径必须严格匹配，否则报错 `11200058`（SSE 路径错误）或 `11200059`（Streamable HTTP 路径错误）；  
- `inputSchema` 缺失或格式错误将导致 `11200060` 错误，建议使用 [JSON Schema Validator](https://json-schema.org/) 验证；  
- 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置白名单或 VPC 打通。

## 面向开发者的实用指引

- **快速上手**：优先选用 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 中的官方服务（如 `Amap Maps`、`WebSearch`），开通即用，无需部署。
- **自定义接入**：  
  - 若已有 RESTful API → 使用「AI 网关导入」一键封装为 MCP 工具；  
  - 若已有 OpenAPI（如阿里云 OSS/ECS）→ 使用「OpenAPI 导入」自动发布；  
  - 若需完全自研 → 用 `@modelcontextprotocol/server-*` SDK 开发，部署至函数计算（FC），配置 `npx`/`uvx` 启动命令。
- **调试技巧**：  
  - 连接失败？先 `curl -v <your-mcp-url>/mcp` 测试端点连通性与响应头；  
  - 参数不生效？检查 `inputSchema` 是否与模型提示词中期望的字段名一致；  
  - 外部集成？使用 `mcp` Python SDK，设置 `DASHSCOPE_API_KEY` 和 `streamablehttp_client` 地址即可调用。
- **计费注意**：  
  - 官方/三方 MCP 服务按调用次数计费（费用由服务提供方收取）；  
  - 自定义 MCP 服务按调用时长计费（基础模式 0.000156 元/秒），极速模式另加部署费。

> 🚀 最佳实践：在 Agent 2.0 中启用 `enable_thinking` 并设置 `ReAct 最大轮次 ≥ 3`，可显著提升复杂 MCP 工具链的调用成功率。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


