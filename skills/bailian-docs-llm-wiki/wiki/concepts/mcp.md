# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化、可扩展的工具集成协议，用于在大语言模型与外部服务（如地图、搜索、天气、数据库等）之间建立安全、统一、流式响应的信息通道。它不是模型能力本身，而是百炼平台内智能体（Agent）和工作流（Workflow）调用外部能力的**事实标准接口层**，使模型能基于自然语言意图自主或按编排调用真实世界服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent 2.0）**：MCP 是[工具调用](tool-use.md)的核心载体。模型根据用户输入自动规划是否调用、调用哪个 MCP 工具（如 `maps_route`）、传入哪些参数，并支持单次对话中最多 5 轮[工具调用](tool-use.md)链。开发者只需在应用配置中启用已开通的 MCP 服务（如 WebSearch），无需编写适配逻辑。
  
- **工作流应用（Workflow）**：MCP 以「MCP 节点」形式显式编排。需手动拖入节点、选择具体工具（如 `amap_weather`），并配置输入映射（如将前置节点输出的 `city` 字段绑定为 `location` 参数）。输出结果可直接传递给后续节点（如大模型总结、变量处理）。

- **高代码应用（Rich Code）**：通过 Python SDK 或 HTTP Client 直接调用 MCP Server 接口（`/mcp` 端点），适用于需要精细控制请求/响应、自定义错误重试或与内部系统深度集成的场景。

- **插件（Plug-in）与 Skill 的底层统一**：  
  - 所有官方/三方插件（如 `quark_search`, `code_interpreter`）及自定义插件，在百炼平台内均被自动封装为符合 MCP 协议的服务；  
  - Skill 虽独立建模，但其运行时环境与 MCP 共享同一套沙箱基础设施与网络策略，且未来能力扩展（如接入云产品 API）推荐优先通过 MCP OpenAPI 导入方式实现，而非重复开发 Skill。

> ⚠️ 注意：MCP **仅在百炼平台内生效**。它不支持直接注入千问原始 API（如 `dashscope.Generation.call`）调用链，也不可通过 `dashscope` SDK 的基础模型接口启用——必须构建于智能体、工作流或高代码应用之上。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | 是 | 协议类型，决定端点路径与传输格式。**必须与 URL 严格匹配**：<br>• `"streamableHttp"` → 使用 `/mcp` 端点（**当前唯一支持的正式协议**）<br>• `"sse"` → `/sse`（已废弃，配置将触发 HTTP 405 错误） | `"streamableHttp"` |
| `url` | string | 是 | MCP Server 地址，格式固定：<br>`https://dashscope.aliyuncs.com/api/v1/mcps/{service-id}/mcp`<br>其中 `{service-id}` 在 MCP 广场开通服务后自动生成 | `https://dashscope.aliyuncs.com/api/v1/mcps/svc_abc123/mcp` |
| `headers.Authorization` | string | 是 | 鉴权头，必须为 `Bearer <DASHSCOPE_API_KEY>` | `Bearer sk-xxxxxx` |
| `env` | object | 否 | 自定义环境变量（仅脚本部署有效），用于传递密钥、配置项等。敏感值**必须通过 KMS 加密后填写** | `{ "AMAP_MAPS_API_KEY": "${kms:xxx}" }` |

- **调用限制关键项（开发者须主动关注）**：
  - 单次会话最多调用 5 个不同 MCP 工具（智能体）；
  - 自定义 MCP 服务部署于函数计算（FC），**无法访问本地文件、数据库或 localhost 服务**；如需访问云数据库，请配置 FC 的 VPC 或 IP 白名单；
  - 所有 MCP 请求必须使用 `streamableHttp` 类型，旧版 SSE 将返回 `11200058`（HTTP 405）或 `11200059`（HTTP 404）错误码。

## 面向开发者，简洁实用

- ✅ **快速上手**：开通官方服务 → 控制台「应用配置」中勾选 → 发布即用（免密钥、免编码）；  
- ✅ **自定义发布**：用 `npx mcp-server-node` 或 `uvx mcp-server-python` 启动本地服务 → 一键部署至函数计算 → 自动生成 `/mcp` 端点；  
- ✅ **调试建议**：  
  - 使用 `curl -X POST {url} -H "Authorization: Bearer ${key}" -d '{"tool":"web_search","parameters":{"query":"杭州天气"}}'` 直接测试端点；  
  - 在智能体对话中添加 `system_prompt` 强约束：“你**必须**只在需要实时信息时调用 MCP 工具，禁止虚构结果”；  
- ❌ **避坑提醒**：  
  - 不要尝试在 `dashscope.Generation` 中硬编码 MCP 调用逻辑——平台不解析、不执行；  
  - 不要将 `env` 中的明文密钥写入脚本或配置文件——KMS 加密是强制要求；  
  - 不要期望 MCP 工具支持流式响应（如 `text_to_image` 返回图片流）——当前所有 MCP 工具均为同步 JSON 响应。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [skill](../guides/skill.md)


