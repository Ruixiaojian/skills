# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、图表生成等服务）之间建立安全、可扩展的上下文交互通道。它屏蔽了底层通信细节，使开发者无需为每个工具单独开发适配器，即可在智能体或工作流中声明式接入各类能力。MCP 基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了生产级增强与托管支持。

## 支持的模型与功能

MCP 协议本身不绑定特定模型，但其调用能力需由百炼平台内支持工具调用的模型驱动。当前**智能体应用**和**工作流应用**均原生支持 MCP 服务集成：

- **智能体应用**：自动根据对话意图识别并调用已配置的 MCP 工具（最多同时启用 5 个），适用于路径规划、逐步推理、多工具协同等场景（如[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)中所述的“气温趋势”案例）。
- **工作流应用**：需显式配置 MCP 节点并指定具体工具（如 `maps_weather`），适用于结构化、确定性任务编排（如[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)中天气查询工作流）。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**，仅限百炼平台内的智能体或工作流应用使用（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)第3条）。

支持的服务类型包括：
- **官方云部署服务**：如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，开箱即用；
- **自定义服务**：支持三种部署方式——脚本部署（npx/uvx 托管）、AI 网关导入（封装现有 RESTful API）、OpenAPI 导入（操作阿里云资源），详见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 关键参数

| 参数 | 说明 | 示例/取值 |
|------|------|-----------|
| `service_name` | 服务唯一标识名，仅用于控制台区分 | `"长期记忆"` |
| `type` | 通信协议类型，决定后端连接方式 | `"stdio"`（本地进程）、`"sse"`（Server-Sent Events）、`"streamableHttp"`（HTTP POST） |
| `command` / `url` | 启动命令或远程服务地址 | `"npx"` 或 `"https://your-server/sse"` |
| `env` | 环境变量（敏感信息需通过 KMS 凭据加密） | `{"AMAP_MAPS_API_KEY": "xxx"}` |
| `deployment_mode` | 部署模式，影响计费与延迟 | `"basic"`（按次计费，有冷启动）、`"ultra"`（常驻，额外部署费） |

> **注意**：`type` 必须与端点路径严格匹配——`"sse"` 对应 `/sse` 端点（GET），`"streamableHttp"` 对应 `/mcp` 端点（POST）。配置错误将导致 `11200058` 错误（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)错误码表）。

## 使用方式

### 1. 开通服务
- 访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务卡片 → **立即开通**；
- 敏感参数（如 API Key）需通过 KMS 凭据加密，不可明文填写（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)说明）。

### 2. 在智能体中配置
- 创建智能体 → **添加 MCP 服务** → 从已开通列表中勾选（最多 5 个）；
- 无需手动指定工具，模型根据 Prompt 自动决策调用（示例见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)“路程规划”测试）。

### 3. 在工作流中配置
- 拖入 **MCP 节点** → 选择已开通服务 → 指定具体工具（如 `maps_weather`）；
- 输入参数需通过上游节点（如大模型节点）提取并传递（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)“天气查询工作流”步骤）。

### 4. 外部调用
- 支持集成至 Cherry Studio、Cursor 等第三方客户端（一键自动配置或手动 JSON 导入）；
- 支持 SDK 编程调用：使用 `mcp.client.streamable_http` 连接，配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)实现多轮工具调用（代码示例见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

## 限制和注意事项

- **网络限制**：自定义 MCP 服务运行于函数计算 FC，**无固定公网出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)第6条）；
- **本地资源不可达**：不支持访问用户本地文件、硬件或数据库（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)第5、9条）；
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 数量**；输出 [Token](../concepts/token.md) 也可能因响应更详尽而增加（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)第2条）；
- **版本更新**：通过 `npx`/`uvx` 部署的服务**不会自动同步上游包更新**，需手动重新部署（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)第10条）；
- **协议升级**：已开通用户需主动取消再重开以升级至新版 Streamable HTTP 协议（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)“升级协议”说明）；
- **错误排查**：常见连接失败（如 `11200044`）、超时（`11200045`/`11200046`）、鉴权失败（`11200049`）等问题，需结合 `curl` 测试、FC 日志及下游服务文档定位（见[文档 4](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)错误码表）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)


