# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化能力接入协议，用于在大语言模型与外部工具服务之间建立安全、可互操作、声明式的信息通道。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)）实现，并升级为 Streamable HTTP 协议，屏蔽底层通信细节，使开发者无需为每个工具单独编写适配逻辑即可集成能力。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 是百炼平台中**工具能力的统一抽象层**，不直接绑定模型，而是作为智能体和工作流的“能力底座”被调用：

- **智能体应用（Agent）**：在智能体编辑页的「MCP 服务」区域一键添加最多 5 个已开通的 MCP 服务（如 `Amap Maps`、`WebSearch`）。大模型根据用户自然语言指令自动推理并动态调用，无需显式指定工具名或参数结构——提示词中建议明确提及服务名称（例如：“请调用 WebSearch MCP 获取最新 AI 会议信息”），以提升调用准确率。

- **工作流应用（Workflow）**：在画布中拖入「MCP 节点」，手动绑定一个具体 MCP 工具（如 `maps_weather`）。需前置一个大模型节点（如 `qwen-plus`）将用户输入解析为结构化参数（如 `{"city": "杭州"}`），再通过参数映射传递至 MCP 节点执行。适用于需精确控制调用时机、顺序与输入输出的编排场景。

- **Managed Agents（托管智能体）**：MCP 服务可作为 `tools` 显式注入到 Managed Agent 的运行环境中，与沙箱内 `bash`、`read` 等内置工具协同使用，支撑多步、有状态的复杂任务（如“先查天气，再规划路线，最后生成行程图”）。

> ⚠️ 注意：MCP **不支持**通过 DashScope SDK 直接调用千问 API（如 `dashscope.Generation.call`）时注入；也不支持在 Assistant API 的 `tools` 字段中以 OpenAI 格式传入 MCP 工具。它仅限百炼平台内原生智能体/工作流/Managed Agents 场景使用。

## 关键参数和配置

| 参数类别 | 字段/配置项 | 说明 | 开发者须知 |
|----------|-------------|------|-----------|
| **协议类型** | `type`（必填） | 取值为 `stdio` / `sse` / `streamableHttp`，必须与服务端点严格匹配：<br>• `sse` → 对应 `/sse` 端点<br>• `streamableHttp` → 对应 `/mcp` 端点<br>配置错误将返回 `11200058` 错误码 | 部署自定义 MCP Server 时，务必在服务配置中声明正确 `type`，并在百炼控制台选择对应协议 |
| **部署模式** | `基础模式` / `极速模式` | • 基础模式：按调用时长计费（0.000156 元/秒），无部署费<br>• 极速模式：额外收取部署费（0.000036 元/秒），适合高频、低延迟场景 | 高频调用推荐极速模式；首次调试建议用基础模式快速验证 |
| **安全凭证** | KMS 加密凭据 | 敏感参数（如 `AMAP_MAPS_API_KEY`、`FIRECRAWL_API_KEY`）**必须**通过百炼控制台的 KMS 凭据管理功能加密后引用，禁止明文填写 | 控制台配置 MCP 服务时，所有带锁图标（🔒）的字段均需关联 KMS 凭据 |
| **外部调用地址** | `mcp_url` | 格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service_name}/mcp`（如 `WebSearch`）<br>外部 SDK 集成时需配合 `DASHSCOPE_API_KEY` 使用 | 外部调用仅支持 `streamableHttp` 协议；`/mcp` 后缀不可省略 |

## 面向开发者，简洁实用

- ✅ **开通即用**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击「立即开通」→ 自动完成服务注册与权限授权。
- ✅ **自定义三路径**：
  - 快速本地试跑：`npx mcp-server-stdio` 或 `uvx mcp-server-sse` 启动标准 MCP Server；
  - 封装现有 API：通过「AI 网关」导入 RESTful 接口，自动转换为 MCP 工具；
  - 对接云产品：从阿里云 OpenAPI 导入（如 OSS 文件上传、ECS 实例管理），一键暴露为 MCP 工具。
- ✅ **调试技巧**：
  - 提示词中避免模糊指令（❌“帮我查一下” → ✅“调用 WebSearch MCP 搜索‘2024 Qwen 最新论文’”）；
  - 工作流中 MCP 节点的输入参数，优先使用上游节点的 `output.xxx` 引用，而非硬编码；
  - 自定义 MCP Server 日志需输出到 `stdout`，便于函数计算（FC）日志排查。
- ❌ **禁止事项**：
  - 不得访问本地文件、硬件设备或未打通网络的私有数据库；
  - 自定义服务托管于 FC，无固定出口 IP，访问云数据库等资源需配置白名单或 VPC；
  - 不支持在非百炼平台环境（如本地 Python 脚本直连千问 API）中启用 MCP。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


