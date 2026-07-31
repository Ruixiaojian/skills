# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台支持的标准化[工具调用](../concepts/tool-use.md)协议，用于在大模型应用（如智能体、工作流）与外部能力（如地图、搜索、数据库接口）之间建立可互操作的信息通道。它基于 Anthropic 提出的开源标准 [MCP 官方协议](https://modelcontextprotocol.io/) 实现，屏蔽底层通信细节，使开发者无需为每个工具单独开发适配层即可接入海量第三方或自定义服务。协议当前以 Streamable HTTP 为主力传输方式，兼容 SSE，支持平台内集成与外部 SDK 调用两种使用范式。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，而是作为**能力接入层**服务于百炼平台上的两类核心应用：
- **智能体（Agent）应用**：支持在 Prompt 驱动下自动识别调用意图、生成工具参数并处理返回结果；
- **工作流（Workflow）应用**：支持在可视化编排节点中显式调用已配置的 MCP 服务。

目前官方已预置并托管多种 MCP 服务，包括 Amap Maps（地理信息）、Firecrawl（网页爬取）、WebSearch（联网搜索）等，详见 [官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp)。同时支持三类自定义部署方式：  
1. **脚本部署**（`npx`/`uvx` 托管 Node.js 或 Python MCP Server）；  
2. **AI 网关导入**（将现有 RESTful API 封装为 MCP 服务）；  
3. **阿里云 OpenAPI 导入**（将阿里云产品 OpenAPI 快速发布为 MCP 工具）[原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 3 明确指出“MCP 服务需集成在**智能体**或**工作流**应用中使用，不能直接在调用千问 API 时接入”，而文档 1 中“大模型应用：智能体应用”“大模型应用：工作流应用”的表述与此一致，但未覆盖 API 直接调用场景——该限制为关键约束，非疏漏。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `type` | 传输协议类型 | `"streamableHttp"`（推荐）、`"sse"` | [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |
| `url` | MCP Server 接入地址 | `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp` | 文档 2 SDK 示例 |
| `command` / `args` | 脚本部署启动命令 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` | [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| `env` | 环境变量（含密钥） | `{"AMAP_MAPS_API_KEY": "xxx"}`（需配合 KMS 凭据加密） | 文档 2 开通说明 |
| `DASHSCOPE_API_KEY` | 百炼平台鉴权凭证 | 通过环境变量或请求头 `Authorization: Bearer <key>` 传递 | 文档 2 SDK 示例 |

所有 HTTP 请求必须携带有效的 `DASHSCOPE_API_KEY`，且 `type` 与 `url` 路径必须严格匹配：`"sse"` 对应 `/sse` 端点（GET），`"streamableHttp"` 对应 `/mcp` 端点（POST）[原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 平台内集成（智能体/工作流）
1. 在 [MCP 广场](https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market) 开通官方服务，或在 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) 创建自定义服务；
2. 在智能体/工作流编辑器中，从可用工具列表选择目标 MCP 服务并启用；
3. 在 Prompt 中明确指令（如“调用 Amap Maps 规划杭州到上海路线”），模型将自动解析并调用。

### 外部调用
- **第三方 IDE 集成**：支持 Cherry Studio、Cursor 等工具，提供一键自动配置或手动 JSON 导入（含 `DASHSCOPE_API_KEY` 替换）；
- **SDK 编码集成**：使用 `mcp` 客户端库（如 `streamablehttp_client`）连接 MCP Server，获取工具列表后，结合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（如 `qwen-max`）实现多轮[工具调用](../concepts/tool-use.md)循环 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：  
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地资源**（如本地文件、硬件）；  
  - 访问远程资源（如云数据库）需配置 FC IP 白名单或 VPC 打通；  
  - 私有 npm 仓库不支持直接部署，须发布至公共仓库或改用 SSE 连接。

- **协议与部署约束**：  
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署；  
  - `type` 与端点路径不匹配将触发错误码 `11200058`（HTTP 405）或 `11200059`（HTTP 404）；  
  - 初始化超时（`11200057`）常见于基础模式冷启动延迟，可切换至极速模式缓解。

- **计费与额度**：  
  - 官方服务（如 WebSearch）有免费额度（2000 次/月），超限后按 29 元/千次计费；  
  - 自定义服务按调用时长（0.000156 元/秒）或部署时长（0.000036 元/秒）计费，详见 [计费说明](https://help.aliyun.com/zh/model-studio/mcp-introduction#fb482455a3u8c)。

- **安全要求**：  
  敏感参数（如 API Key）**必须通过 KMS 凭据加密**，禁止明文写入配置；私有 MCP Server 仅限主账号及授权 RAM 用户访问。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)


