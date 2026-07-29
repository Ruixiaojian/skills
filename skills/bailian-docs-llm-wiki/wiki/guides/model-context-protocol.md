# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、天气等服务）之间建立安全、可扩展的信息通道。通过 MCP，开发者无需为每个工具单独开发适配逻辑，即可在智能体或工作流中声明式接入官方或自定义工具。该协议基于开源 MCP 标准实现，当前采用 Streamable HTTP 协议（替代旧版 SSE），并深度集成于百炼应用架构中 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的模型/功能

MCP 本身不绑定特定大模型，而是作为**工具调用层**服务于百炼平台上的推理模型。目前所有支持工具调用能力的百炼内置模型均可使用 MCP，包括但不限于：
- 通义千问系列：`qwen-max`、`qwen-plus`、`qwen-turbo`
- 其他已启用 `tools` 参数的兼容模型（需在应用配置中显式开启工具调用开关）

MCP 支持两类核心使用场景：
- **智能体应用**：模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数（如路径规划、逐步思考）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：开发者手动编排 MCP 节点，每个节点绑定一个具体工具（如 `maps_weather`），并显式传递输入/输出参数，适用于确定性任务链 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：文档 5 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即纯 API 调用（如 `dashscope.ChatCompletion.create`）不支持 MCP；必须通过百炼平台的智能体或工作流应用容器使用。

## 关键参数

MCP 的关键配置分散在服务部署与应用集成两个层面：

### 服务侧（部署时配置）
- `type`：协议类型，必须与接入路径严格匹配 — `"sse"` 对应 `/sse` 端点，`"streamableHttp"` 对应 `/mcp` 端点（错误匹配将导致 `11200058` 错误）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- `command` / `args`：脚本部署方式（如 `npx` 或 `uvx`）及其启动参数，需与目标 MCP Server 的 CLI 规范一致。
- `env`：环境变量注入，用于传递敏感凭据（如 `AMAP_MAPS_API_KEY`），**禁止明文写入配置代码**，应通过 KMS 凭据加密管理 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

### 应用侧（调用时隐含）
- 工具名称（`tool.name`）与描述（`tool.description`）：由 MCP Server 在 `list_tools()` 响应中提供，智能体据此生成调用决策。
- 输入 Schema（`tool.inputSchema`）：JSON Schema 定义参数结构，工作流节点需据此校验输入值格式。
- 会话级超时控制：`MCP_INIT_TIMEOUT`（初始化超时）、`MCP_REQUEST_TIMEOUT`（请求超时）等错误码直接影响调用稳定性 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 使用方式

### 1. 接入官方 MCP 服务
- **开通**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 `Amap Maps`）→ 点击“立即开通” → 确认（试用版免填 API Key）。
- **配置到智能体**：创建智能体 → “添加 MCP 服务” → 最多选 5 个 → 保存后模型自动触发调用。
- **配置到工作流**：拖入 MCP 节点 → 选择工具（如 `maps_weather`）→ 手动绑定输入参数（如引用上游节点的 `city` 字段）→ 连接下游节点处理结果。

### 2. 部署自定义 MCP 服务
支持三种方式：
- **脚本部署**（推荐）：上传符合 MCP 协议的 `npx`/`uvx` 启动配置，托管至函数计算 FC [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 服务后，从 AI 网关一键导入。
- **OpenAPI 导入**：将阿里云产品 OpenAPI（如 OSS、ECS）发布为 MCP 工具。

### 3. 外部调用（第三方集成）
- **SDK 集成**：使用 `mcp` Python SDK 连接 `streamableHttp` 端点（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)实现工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **IDE 集成**：一键配置至 Cherry Studio 或 Cursor，自动注入 MCP Server 配置。

## 限制和注意事项

- **网络与资源限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - **不支持访问本地资源**（如本地文件、硬件设备），此类服务需本地部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**，旧版 SSE 客户端需升级；已开通用户需先“取消开通”再重新开通以完成协议升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
  - 私有 npm/PyPI 包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **运维与调试**：
  - 部署后仅允许编辑服务名称和描述；修改 `command`、`args` 或 `type` 必须**先停用再重新部署**。
  - 排查连接失败（如 `11200044`）优先执行 `curl <服务地址>` 测试连通性，并检查 FC 日志 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
  - 模型调用失败常见原因为提示词未明确工具能力，建议在 System Prompt 中清晰描述工具名称、用途及输入输出格式 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

- **计费说明**：
  - 官方服务（如联网搜索）按调用量计费（29 元/千次），免费额度 2000 次/月。
  - 自定义服务分“基础模式”（按调用时长计费，0.000156 元/秒）和“极速模式”（另加部署费 0.000036 元/秒），冷启动延迟敏感场景建议选极速模式 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


