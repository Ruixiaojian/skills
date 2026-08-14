# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化外部能力接入机制，用于在大模型推理过程中安全、高效地调用外部工具服务（如地图、天气、联网搜索、知识图谱等）。它通过统一协议抽象底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体、工作流或第三方应用中一致集成和管理工具。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent 2.0）**：MCP 服务作为“可调度工具”与知识库并列，由模型自主规划调用时机与参数。最多支持同时配置 5 个 MCP 服务；模型根据对话上下文自动判断是否需要调用、调用哪个工具，并生成合法参数。适用于路径规划、多步推理、跨工具协同绘图等动态任务。
  
- **工作流（Workflow）**：每个 MCP 节点绑定一个工具，需显式配置输入参数（如从前置节点提取的 `city_name`）和输出参数映射（如将 `weather_result` 传给总结节点）。适合确定性流程，例如“用户提问 → 提取地点 → 调用天气 MCP → 格式化回复”。

- **Managed Agents（托管式智能体）**：MCP 服务以 Skill 形式挂载到 Agent 配置中，与内置工具（`bash`、`read` 等）统一纳入沙箱执行环境。工具调用结果作为事件流（`tool_output`）实时返回，支持长时态、多轮交互下的状态保持与文件联动。

- **高代码应用与外部客户端**：可通过 `mcp` SDK（如 `streamablehttp_client`）或 [OpenAI 兼容接口](openai-compatible-api.md)直接调用；支持一键接入 Cherry Studio、Cursor 等标准 MCP 客户端，也可通过 `DASHSCOPE_API_KEY` 手动配置。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `type` | string | 是 | 协议类型，必须为 `"sse"` 或 `"streamableHttp"` | 必须与后端端点严格匹配：`"sse"` 对应 `/sse`（GET），`"streamableHttp"` 对应 `/mcp`（POST）；错配将触发 `11200058`/`11200059` 错误 |
| `url` | string | 是 | MCP 服务公网可访问地址 | 若服务部署在 VPC 内，需通过函数计算 FC 的 VPC 打通或配置 IP 白名单 |
| `env` | object | 否 | 非敏感环境变量注入，如 `{"BASE_URL": "https://api.example.com"}` | 用于传递配置项，**不得包含密钥** |
| 敏感凭证（如 `AMAP_MAPS_API_KEY`） | — | — | 必须通过 KMS 凭据加密管理 | **禁止明文填写**，否则存在安全风险 |
| `command` / `args` | string / array | 仅脚本部署时必填 | 如 `npx mcp-amap-server` 及其参数 | 包名需在 npm/PyPI 公开可访问，私有仓库暂不支持 |

> ⚠️ 所有 MCP 服务必须严格遵循 [MCP 官方协议规范](https://modelcontextprotocol.io/)，非标实现将导致 `11200054`（协议解析错误）等异常。

## 面向开发者的实用提示

- **选型建议**：优先使用官方 MCP 服务（如高德地图、WebSearch），开箱即用且免费额度明确；自定义服务推荐采用“AI 网关导入”方式封装已有 RESTful API，最快 5 分钟完成接入。
- **调试技巧**：在控制台测试时，开启 `enable_thinking: true` 并设置 `ReAct 最大轮次 ≥ 3`，可清晰观察模型是否识别工具、生成参数及处理响应。
- **[Token](token.md) 优化**：MCP 返回结果会注入模型上下文，显著增加输入 [Token](token.md)。若响应冗余，可在系统提示词中明确要求“仅返回 JSON 结构化结果，不含解释性文字”。
- **错误排查**：
  - `11200054` → 检查服务是否符合 MCP 协议（尤其 `capabilities` 响应格式）；
  - `11200058`/`11200059` → 核对 `type` 与 `url` 路径是否匹配；
  - 工具未被调用 → 检查模型是否支持工具调用（推荐 `qwen-max`、`qwen-3` 系列），并确认系统提示词中已声明可用工具。
- **计费注意**：MCP 本身不收取平台服务费，但调用产生的第三方 API 费用（如高德地图调用量）、函数计算资源费（自定义服务）及模型 [Token](token.md) 费仍需承担。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)


