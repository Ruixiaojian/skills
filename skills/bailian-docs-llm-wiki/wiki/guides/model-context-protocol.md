# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地理服务、网页爬取、天气查询等）之间建立安全、可扩展的信息通道。通过 MCP，开发者无需为每个工具单独开发适配层，即可在智能体或工作流中声明式接入官方或自定义工具服务。该协议基于开源 MCP 标准实现，当前百炼采用 Streamable HTTP 协议作为默认传输机制（替代旧版 SSE），并提供云部署、脚本托管、AI 网关封装和 OpenAPI 导入等多种集成路径。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用能力需由百炼平台内的**智能体应用**或**工作流应用**承载。目前支持以下两类核心使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用 MCP 工具，并动态生成参数（如“从杭州萧山国际机场到西湖景区”触发 Amap Maps 路径规划）。单个智能体最多可配置 5 个 MCP 服务 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式添加 MCP 节点，并手动指定所用工具（如 `maps_weather`）、输入参数来源（如引用前序节点输出）及输出传递逻辑。每个 MCP 节点仅支持一个工具 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

官方已预置多种 MCP 服务，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking（逻辑推理）和 QuickChart（图表生成）等；同时支持通过三种方式接入自定义服务：  
1. **使用脚本部署**（npx/uvx/http）：适用于开源或自研 MCP 服务代码包；  
2. **从 AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；  
3. **从阿里云 OpenAPI 导入**：将 ECS、OSS 等云产品操作发布为 MCP 工具 [原文标题](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 提到“百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议”，而文档 2 和文档 3 中部分截图和描述仍沿用 SSE 术语（如 Cherry Studio 配置显示类型为 `sse`）。实际部署时应以控制台最新配置项为准，优先选择 `streamableHttp` 类型及 `/mcp` 端点路径，避免因协议不匹配导致 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（错误码 11200058）或 `MCP_SERVER_HTTP_NOT_FOUND`（错误码 11200059）等连接失败问题。

## 关键参数

MCP 服务配置涉及两类关键参数：**服务元数据**与**运行时参数**。

- **服务元数据**（必填）：
  - `服务名称`：仅用于控制台识别，不影响模型调用逻辑；
  - `描述`：简要说明服务用途，供开发者管理参考；
  - `安装方式`：决定启动机制，支持 `npx`（Node.js）、`uvx`（Python）或 `http`（远程 SSE/Streamable HTTP）；
  - `部署方式`：影响计费与延迟，分为 `基础模式（按次计费）` 与 `极速模式（常驻+调用双计费）`；
  - `部署地域`：建议选择与主业务同地域（如北京），降低网络延迟。

- **运行时参数**（按需配置）：
  - `env`：环境变量对象，用于注入敏感凭据（如 `AMAP_MAPS_API_KEY`），**必须通过 KMS 凭据加密**，禁止明文填写 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)；
  - `mcpServers` 配置块：定义具体服务实例，需严格匹配 `type`（如 `"stdio"` 或 `"streamableHttp"`）与端点路径（如 `"/mcp"`）；
  - 工作流中 MCP 节点的 `输入参数`：必须显式绑定上游节点输出（如 `"引用：信息提取/result"`），不可依赖模型自动解析。

## 使用方式

### 1. 开通服务
- 官方服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击目标服务卡片（如 Amap Maps）→ **立即开通** → **确认开通**。试用服务无需填写 API Key，商业化定制需配置个人密钥并加密 [原文标题](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- 自定义服务：进入 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) → **创建 MCP 服务** → 选择部署方式（脚本/AI 网关/OpenAPI）→ 填写对应配置 → 提交部署。

### 2. 在应用中集成
- **智能体**：创建后，在「MCP 服务」配置页勾选已开通服务，保存即可。模型将根据提示词自主决策调用时机与参数。
- **工作流**：拖入「MCP 节点」→ 选择服务及具体工具 → 在「输入参数」中绑定上游变量（如 `引用：信息提取/result`）→ 连接至下游节点。

### 3. 外部调用
支持两种集成模式：
- **第三方应用**：一键配置至 Cherry Studio 或 Cursor，自动注入服务地址与认证信息；
- **自有项目**：使用 `mcp` SDK（如 `streamablehttp_client`）连接百炼 MCP endpoint（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)完成多轮工具调用循环 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：
  - MCP 服务托管于函数计算 FC，**无法访问用户本地资源（如本地数据库、文件系统）**；
  - 访问远程云资源（如 RDS、Redis）需配置 FC 的 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - 敏感凭据（API Key、[Token](../concepts/token.md)）必须通过 KMS 加密，明文配置将导致部署失败或安全风险。

- **协议与兼容性**：
  - 百炼默认使用 Streamable HTTP 协议（`/mcp` 端点），若使用旧版 SSE 配置（`/sse`），需重新开通或升级服务，否则触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 错误；
  - 自定义服务需严格遵循 MCP 协议规范，非标准实现（如返回非 JSON-RPC 格式）将导致 `MCP_PROTOCOL_ERROR`（11200054）。

- **计费与限流**：
  - 官方服务（如 WebSearch）有免费额度（2000 次/月），超量后按 29 元/千次计费；云部署服务无部署费，但第三方 API 调用费用由服务商收取；
  - 限流策略按主账号共享（如 WebSearch 为 15 QPS），子账号调用计入同一配额；
  - 自定义服务按部署模式计费：基础模式仅对调用时长计费（0.000156 元/秒），极速模式额外收取部署时长费（0.000036 元/秒）。

- **调试与排障**：
  - 首选排查链路：`curl <MCP_URL>` 测试连通性 → 查看 FC 日志（需提前开启）→ 核对 `type` 与端点路径是否匹配；
  - 常见错误码详见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)，如 `11200046`（请求超时）建议切换极速模式或优化下游服务响应时间。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


