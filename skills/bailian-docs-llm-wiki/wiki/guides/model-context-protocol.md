# model context protocol

Model Context Protocol（MCP）是阿里云百炼平台提供的标准化工具接入协议，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展的上下文交互通道。它屏蔽了工具接口差异，支持统一声明、自动发现与按需调用，无需为每个第三方服务单独开发适配逻辑。MCP 服务既可开箱即用，也可按需自定义部署或外部集成。

## 支持的模型/功能

- **适用场景**：仅限百炼平台内的**智能体应用**和**工作流应用**，不支持直接在千问 API 调用中接入（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **官方服务**：已预置 Amap Maps、Sequential Thinking、QuickChart、WebSearch 等 MCP 服务，覆盖地理信息、逻辑推理、图表生成、联网搜索等能力；其中 Amap Maps 试用版免 API Key，商业化定制支持传入 `AMAP_MAPS_API_KEY`（见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。
- **自定义服务**：支持三类部署方式：
  - **脚本部署**（npx/uvx）：适用于 Node.js/Python 开发的开源或自研 MCP 服务（如 `@modelcontextprotocol/server-memory`）；
  - **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
  - **OpenAPI 导入**：将阿里云产品（如 OSS、ECS）的 OpenAPI 快速发布为 MCP 服务（见 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）。

> **注意**：文档 5 中称“智能体和工作流应用已支持接入两种 MCP 服务”，但实际支持类型为官方服务与自定义服务两类，此处“两种”指服务来源维度，非协议版本或传输方式；而文档 3 明确指出协议已从旧版 SSE 升级为新版 Streamable HTTP，开发者需确认部署配置匹配（如 `type: "streamableHttp"` 对应 `/mcp` 端点），否则将触发错误码 `11200058`（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `service_name` | 服务标识名，仅用于控制台区分，不影响模型调用逻辑 | `"长期记忆"` |
| `type` | 传输协议类型，必须与后端端点严格匹配 | `"stdio"`（本地）、`"sse"`（`/sse`）、`"streamableHttp"`（`/mcp`） |
| `command` / `url` | 启动命令（npx/uvx）或远程服务地址（HTTP） | `npx -y @modelcontextprotocol/server-memory` 或 `https://your-server/mcp` |
| `env` | 敏感环境变量（如 API Key），**必须通过 KMS 凭据加密**，不可明文填写 | `{ "AMAP_MAPS_API_KEY": "kms://xxx" }` |
| `deployment_mode` | 仅脚本部署支持：`基础模式`（按调用计费）或`极速模式`（常驻+调用双计费） | 基础模式冷启动延迟高，极速模式成本更高 |

## 使用方式

1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务并点击“立即开通”。已开通用户需先“取消开通”再重新开通以升级至 Streamable HTTP 协议（见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。
2. **集成到智能体**：
   - 创建智能体 → 添加 MCP 服务（最多 5 个）→ 模型根据自然语言输入自动判断是否调用及使用哪个工具。
   - 示例提示词：“现在出发，从杭州萧山国际机场到杭州西湖景区。请你提供三种公共交通出行方案”（见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。
3. **集成到工作流**：
   - 拖入 MCP 节点 → 手动指定所用工具（如 `maps_weather`）→ 通过前置大模型节点提取结构化参数（如城市名）→ 后置大模型节点解析返回结果。
4. **外部调用**：
   - 通过 MCP SDK（如 `streamablehttp_client`）或兼容 OpenAI 的 `chat.completions.create` 接口调用；
   - 支持一键配置至 Cherry Studio/Cursor，或手动注入 `DASHSCOPE_API_KEY` 和服务 URL（见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

## 限制和注意事项

- **网络与资源限制**：自定义 MCP 服务运行于函数计算 FC，**无法访问本地数据库或硬件**；访问云数据库需配置 FC IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **协议兼容性**：必须严格匹配 `type` 与端点路径（如 `streamableHttp` → POST `/mcp`），否则报错 `11200058` 或 `11200059`（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **[Token](../concepts/token.md) 影响**：MCP 返回内容作为上下文注入模型，**显著增加输入 [Token](../concepts/token.md)**；模型响应可能因信息更丰富而间接增加输出 [Token](../concepts/token.md)（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **权限与安全**：敏感凭据（如 API Key）必须通过 KMS 加密；私有 npm 包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **版本更新**：`npx`/`uvx` 部署的服务**不会自动同步上游版本**，需手动重新部署（见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)


