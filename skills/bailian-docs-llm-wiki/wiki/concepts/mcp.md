# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具调用协议，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可发现、可扩展的双向通信通道。它基于开源 MCP 标准实现，统一抽象工具接入方式，使大模型能自动理解、发现并结构化调用各类服务（如地图、天气、[长期记忆](long-term-memory.md)等），无需为每个工具单独编写适配逻辑。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：MCP 作为“可规划工具”深度集成。大模型根据对话上下文自主判断是否调用、调用哪个工具（如 `maps_weather`）、传入哪些参数，全程自动完成工具发现、参数生成与结果解析。单个智能体最多配置 5 个 MCP 服务，支持动态决策与思考链可视化。

- **工作流应用**：需显式添加 **MCP 节点**，手动选择目标工具（如仅启用 `maps_route`），输入参数必须由上游节点（如大模型节点）以 JSON Schema 兼容格式输出。适用于需要确定性编排、多步骤协同或结果后处理的场景。

- **不支持的场景**：MCP 服务**不可直接接入千问 API 原生调用链路**（如通过 `dashscope.ChatCompletion.create()` 直接调用），也不支持在 Assistant API 或高代码 SDK 中透传使用——仅限百炼控制台构建的智能体/工作流应用内生效。

## 关键参数和配置

| 类别 | 参数名 | 说明 | 开发提示 |
|------|--------|------|----------|
| **服务标识** | `服务名称` / `描述` | 控制台显示用，不影响调用逻辑；建议命名体现功能（如 `"用户长期记忆"`） | 无需编码配置，仅控制台填写 |
| **协议类型** | `type` | 必须与服务端点路径严格匹配：<br>• `"sse"` → 对应 `/sse` 端点<br>• `"streamableHttp"` → 对应 `/mcp` 端点（推荐，百炼默认升级至此） | 错配将触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（错误码 `11200058`） |
| **远程地址** | `url` | HTTP/SSE 服务地址，要求：<br>• 可公网访问<br>• TLS 证书有效（HTTPS）<br>• 响应头含 `Access-Control-Allow-Origin: *`（若跨域调用） | 自建服务需确保防火墙、SLB 或网关放行对应路径 |
| **鉴权凭证** | 环境变量 / KMS 加密凭据 | 敏感字段（如 `AMAP_MAPS_API_KEY`）**禁止明文填写**，必须通过百炼控制台的 KMS 加密存储或环境变量注入 | 使用 `KMS_SECRET_NAME` 引用加密凭据，避免硬编码 |
| **部署命令**（自定义服务） | `command` / `args` | `npx` 或 `uvx` 启动时必需：<br>`"npx"` + `["-y", "@modelcontextprotocol/server-memory"]` | Python 服务请优先选用 `uvx`，Node.js 推荐 `npx` |

> ⚠️ 注意：自定义 MCP 服务运行于函数计算（FC），**无法访问本地文件、硬件设备或未授权的私有数据库**；如需连接云数据库，请配置 FC 的 VPC 网络或 IP 白名单。

## 面向开发者的实用建议

- **优先使用官方服务**：开通即用，免部署、免运维。访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 一键启用 Amap Maps、[长期记忆](long-term-memory.md)等服务。
- **调试技巧**：开启智能体「调试模式」可查看完整工具调用请求/响应日志，验证 `type` 与 `url` 是否匹配、参数是否被正确序列化。
- **自定义服务快速验证**：本地启动 `@modelcontextprotocol/server-memory` 后，用 `curl https://your-server.com/mcp/tools` 测试工具发现接口是否返回标准 JSON Schema。
- **计费提醒**：官方服务有免费额度（如联网搜索 2000 次/月），自定义服务按调用时长计费（基础模式 0.000156 元/秒），建议在工作流中设置超时与重试策略。
- **兼容性注意**：百炼已全面升级至 Streamable HTTP（`/mcp`），旧版 SSE（`/sse`）仍兼容但逐步淘汰；新项目请统一使用 `type: "streamableHttp"`。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [start using](../guides/start-using.md)
- [application support](../guides/application-support.md)


