# model context protocol

Model Context Protocol（MCP）是阿里云百炼平台提供的标准化工具接入协议，用于在大模型应用（如智能体、工作流）与外部能力（如地图、天气、知识图谱、联网搜索等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独开发适配逻辑，即可统一管理、调用和编排多源工具能力。该协议已全面升级为 Streamable HTTP 协议，兼容主流 MCP 客户端生态 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用效果高度依赖所配置的推理模型能力：
- **智能体应用**：支持自动识别用户意图并动态选择、调用多个 MCP 服务（最多 5 个），适用于需多步协同的复杂任务（如“规划路线 + 查询天气 + 绘制图表”）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点仅支持绑定一个具体工具（如 `maps_weather`），需通过前置大模型节点（如信息提取）解析自然语言输入为结构化参数，并通过后置节点（如信息总结）将工具返回结果转为自然语言输出。
- **外部调用场景**：支持集成至 Cherry Studio、Cursor 等第三方客户端，或通过 MCP SDK 在自有项目中编程调用，此时需显式传入工具列表并实现工具调用循环逻辑 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 5 中称“MCP 服务需集成在智能体或工作流应用中使用”，而文档 3 明确说明可通过 SDK 在任意 Python 项目中调用（如示例中的 `WebSearch`）。实际支持范围以 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档为准，即 MCP 服务既可用于平台内应用，也可作为独立能力被外部系统调用。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **服务配置** | `type`（`stdio` / `sse` / `streamableHttp`） | 必须与接入路径严格匹配：`sse` 对应 `/sse` 端点（GET），`streamableHttp` 对应 `/mcp` 端点（POST）；配置错误将导致 `11200058` 错误码 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。 |
| **部署模式** | 基础模式 vs 极速模式 | 基础模式按调用时长计费（0.000156 元/秒），有冷启动延迟；极速模式额外收取部署时长费（0.000036 元/秒），适合高频调用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。 |
| **安全凭证** | KMS 加密凭据 | 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过阿里云 KMS 创建凭据并引用，不可明文写入配置 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。 |
| **外部调用** | `DASHSCOPE_API_KEY` + `mcp_url` | 外部 SDK 调用必需：`mcp_url` 格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-id}/mcp`，需配合有效的百炼 API Key 使用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。 |

## 使用方式

1. **开通服务**  
   - 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击目标服务（如 Amap Maps）卡片 → “立即开通”。试用版无需填 API Key；商业化定制需配置 KMS 凭据 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。  
   - 自定义服务：支持三种方式：① **脚本部署**（npx/uvx 托管开源包）；② **AI 网关导入**（封装现有 RESTful API）；③ **OpenAPI 导入**（对接阿里云产品）[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

2. **平台内集成**  
   - **智能体**：创建后，在“MCP 服务”配置页添加已开通服务，模型将自动决策调用时机与参数。  
   - **工作流**：拖入 MCP 节点，手动指定工具（如 `maps_weather`），并通过变量引用（如 `信息提取/result`）传递输入参数。

3. **外部调用**  
   - **第三方客户端**：在 MCP 服务详情页选择 Cherry Studio/Cursor，一键配置或手动导入 JSON 配置。  
   - **SDK 编程**：安装 `mcp` 和 `openai` 包，使用 `streamablehttp_client` 连接 MCP Server，通过 `ClientSession` 获取工具列表并参与 OpenAI 兼容的 `tool_calls` 循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务运行于函数计算 FC，无固定出口 IP，访问云数据库等资源需配置 IP 白名单或 VPC 打通；不支持访问用户本地资源（如本地文件、硬件）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **协议兼容性**：所有 MCP 服务必须遵循 Streamable HTTP 协议（旧版 SSE 已淘汰），部署时需确认 `type` 与端点路径（`/mcp`）匹配，否则触发 `11200058` 或 `11200059` 错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **[Token](../concepts/token.md) 开销**：MCP 返回内容会作为上下文注入模型输入，直接增加输入 [Token](../concepts/token.md)；同时可能因信息更丰富导致输出更详尽，间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **版本更新**：通过 npx/uvx 部署的服务，上游包版本更新后，必须手动重新部署才能生效；私有 npm 仓库包暂不支持直接部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **调用限制**：部分服务（如 WebSearch）有月度免费额度（2000 次）和 QPS 限流（15 QPS），超限后返回 `11200051` 错误，需降频或申请扩容 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)


