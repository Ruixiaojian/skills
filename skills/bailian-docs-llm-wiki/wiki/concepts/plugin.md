# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 HTTP API）集成到推理链路中，弥补大模型在实时搜索、精确计算、代码执行、图像生成等场景的固有局限。它以“工具”为最小可调用单元，支持官方预置、三方市场及完全自定义三种来源，既可由大模型自主规划调用，也可在工作流中显式编排执行。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：在控制台「应用编排」→「MCP 区块」中添加已发布的插件（或其转换的 MCP 服务）。官方插件仅限与同业务空间内的智能体关联；自定义插件需先发布为 MCP 服务。大模型根据用户输入自动识别意图、选择工具并组织参数，完成“思考-执行-反思”闭环。
  
- **工作流应用（Workflow）**：将插件作为独立节点拖入画布，与其他节点（如大模型、条件判断）连接。执行顺序和输入参数由开发者显式编排，不依赖模型决策，适用于流程确定、结果可控的自动化任务（如订单状态查询+通知发送）。

- **Assistant API 调用**：在请求 payload 的 `tools` 字段中声明工具列表（含 `type: "function"`、`function.name`、`function.description` 和 `function.parameters`），并通过 `tool_choice` 控制策略（如 `"auto"` 或指定 `{"type": "function", "function": {"name": "calculator"}}`）。这是最轻量、最灵活的集成方式，适合已有 OpenAI 兼容架构的快速迁移。

- **Managed Agents（托管智能体）**：插件需以 MCP 协议服务形式接入，作为沙箱内可调用的外部能力。适用于需长时运行、多步交互、文件读写与命令执行的复杂任务（如数据分析报告生成），工具调用与沙箱环境深度协同。

- **高代码应用**：通过 SDK 或 MCP Client 直接调用已注册插件，支持在 Python 逻辑中混合模型推理与工具调用，实现高度定制化业务编排（如风控规则引擎 + 实时征信 API 调用）。

> ⚠️ 注意：所有插件调用均要求主账号或 RAM 子账号已授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户还需额外授予 `ram:CreateServiceLinkedRole` 权限。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| `tool_id` | 是 | 工具唯一标识符，用于模型识别与路由 | `"quark_search"`, `"text_to_image"` |
| `input.parameters` | 是（自定义插件） | 输入参数结构，需严格匹配 API 契约：<br>• 类型必须明确（`string`/`number`/`object`）<br>• `object` 类型子字段**不可为空**<br>• 鉴权参数若在 Header，需指定 `Type`（如 `"bearer"`）；若在 Query，需在插件配置中声明参数名 | `{ "query": "杭州天气", "region": "hangzhou" }` |
| `input.pass_mode` | 是 | 传参方式：<br>• `"llm_recognition"`：由大模型从用户 query 中抽取<br>• `"biz_pass_through"`：由上游系统通过 `biz_params` 主动注入 | `"llm_recognition"` |
| `output.parameters` | 是 | 输出字段定义，所有字段均为必填，描述需精简准确，便于模型提取关键信息 | `[{"name": "result", "description": "搜索摘要", "type": "string"}]` |
| `plugins`（API 请求） | 否（但启用插件时需） | Assistant API 中显式启用的插件 ID 列表 | `["calculator", "generate_qrcode"]` |

- **URL 与协议要求（自定义插件）**：  
  - 必须为 HTTPS 协议；  
  - 响应头需包含 `Access-Control-Allow-Origin: *` 或明确允许百炼域名；  
  - 工具路径必须以 `/` 开头（如 `/v1/search`），与插件基础 URL 拼接后构成合法完整地址。

- **模型兼容性**：仅以下模型支持插件调用：  
  `qwen-turbo`, `qwen-plus`, `qwen-max`, `qwen-vl-max`, `qwen-vl-plus`。  
  推荐优先选用 `qwen-plus` 或 `qwen-max` 进行开发验证。

## 面向开发者：简洁实用提示

- ✅ **快速起步**：直接使用官方插件（如 `calculator`、`text_to_image`），无需配置，控制台一键启用即可测试。
- ✅ **调试必做**：自定义插件发布前，务必使用控制台「在线调试」功能验证连通性、参数解析与响应格式。
- ✅ **参数安全**：`object` 类型输入中，所有子字段必须提供默认值或明确标记 `required`；空字段将触发错误码 `130022`。
- ✅ **鉴权简化**：仅支持透传 `Authorization` header；其他自定义 header 将被忽略，请勿依赖。
- ❌ **禁止行为**：`code_interpreter` 插件禁用网络访问（`requests` 不可用）和本地文件上传；`quark_search` / `github_search` 仅返回元信息，不抓取网页正文或源码。
- 📉 **调用限制**：单次对话最多调用 10 个工具（含重复调用），且受应用配额约束；删除插件将级联删除其下所有工具，已关联应用立即失效。

> 提示：插件本质是“可被语言模型理解并调度的标准化 API”。设计时请遵循 OpenAPI 3.0 规范，用清晰的 `description` 和最小必要参数降低模型幻觉风险。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


