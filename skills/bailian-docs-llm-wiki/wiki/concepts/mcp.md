# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化外部能力接入机制，用于在大模型推理过程中**按需、动态、可组合地调用外部工具服务**（如地图、天气、知识图谱、代码执行等），无需为每个工具定制适配逻辑。MCP 通过统一协议抽象工具语义与通信方式，使大模型能在上下文理解基础上自主决策是否调用、调用哪个工具及如何传参。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：  
  在「MCP 服务」配置页一次性添加最多 5 个已开通的 MCP 服务（如 `Amap Maps`、`WebSearch`）。模型根据用户输入和对话历史**自主判断调用时机、工具选择与参数生成**，全程无需人工编排。适用于开放域、多跳推理类任务（如“查上海明天天气并规划去外滩的地铁路线”）。

- **工作流应用（Workflow）**：  
  使用「MCP 节点」显式接入——每个节点绑定**唯一工具**（如 `maps_weather/get_current_weather`），并通过上游节点（如信息提取、意图识别）输出的结构化结果**显式传递参数**（如 `{"city": "上海"}`）。适用于确定性强、流程固定的业务编排场景。

- **外部客户端调用（如 Cherry Studio、Cursor 或自研系统）**：  
  通过标准 `Streamable HTTP` 协议直接调用 MCP 服务端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），使用 `mcp.client.streamable_http` SDK 初始化客户端，调用 `list_tools()` 获取可用工具列表，再以 `call_tool(tool_name, parameters)` 方式发起请求。**不支持在直接调用千问 OpenAI 兼容 API（如 `/v1/chat/completions`）时嵌入 MCP 工具调用。**

> ✅ 提示：旧版插件（Plugin）已统一纳入 MCP 协议体系；所有新开发的自定义插件必须发布为 MCP 服务方可被智能体或工作流调用。

## 关键参数和配置

| 类别 | 参数 | 说明 | 注意事项 |
|------|------|------|----------|
| **协议类型** | `type`（必填） | 指定服务接入协议：`streamableHttp`（推荐，百炼当前默认）、`sse`、`stdio` | 必须与服务端路径严格匹配：<br>• `streamableHttp` → `/mcp`<br>• `sse` → `/sse`<br>配置错误将返回 `11200058` 错误 |
| **认证凭证** | `DASHSCOPE_API_KEY`（Header: `Authorization: Bearer <key>`） | 外部调用必需，用于鉴权 | API Key 需具备 `MCPInvoke` 权限；无效或过期触发 `11200049` 错误 |
| **环境密钥** | 如 `AMAP_MAPS_API_KEY` 等 | 官方服务试用版免填；商业化定制或自定义服务需手动注入 | 敏感密钥**必须通过 KMS 凭据管理**，禁止明文写入配置 |
| **服务地址** | `mcp_url` | 格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service_id}/mcp` | 服务 ID 可在 MCP 广场或控制台服务详情页获取 |

## 面向开发者：快速上手要点

- ✅ **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通官方服务；或通过「脚本部署（npx/uvx）→ AI 网关封装 → OpenAPI 导入」三种方式发布自定义 MCP 服务。
- ✅ **集成验证**：  
  - 智能体：添加服务后，用测试会话发送含工具需求的指令（如“北京今天气温多少？”），观察是否自动触发 `weather_mcp`；  
  - 工作流：在 MCP 节点配置「工具路径」与「参数映射」，确保上游节点输出字段名与工具 schema 一致；  
  - 外部调用：用 SDK 执行 `session.list_tools()`，确认返回工具列表后再调用 `call_tool()`。
- ⚠️ **避坑提醒**：  
  - MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问 RDS/VPC 内资源需配置白名单或 VPC 对等连接；  
  - **不支持访问本地文件、硬件设备或 localhost 接口**；此类能力需本地部署 MCP 服务并反向代理至百炼；  
  - 自定义服务升级后**不会自动同步**，必须手动重新部署；  
  - 已开通的旧版 SSE 服务需先「取消开通」再「重新开通」，才能升级至 Streamable HTTP 协议。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [application component api reference](../api/application-component-api-reference.md)


