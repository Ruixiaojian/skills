# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API 服务）安全、标准化地集成到 AI 应用中，弥补大模型在实时检索、精确计算、代码执行、图像生成等场景下的固有局限。每个插件以“工具”为最小可调用单元，由模型基于语义理解自主决策调用时机与参数。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在智能体配置页的“插件”区块中添加官方、三方或自定义插件；最多支持同时启用 10 个工具。模型在对话中自动识别用户意图并调用合适插件，结果返回后继续推理生成最终响应。
- **工作流（Workflow）应用**：将插件作为独立节点拖入画布，手动编排执行顺序与数据流向（如“搜索 → 解析 → 生成图表”），支持条件分支与参数传递。
- **Assistant API 调用**：在请求体 `tools` 字段中声明工具列表（含 `type` 和 `function` Schema），模型根据输入自主选择是否调用及传参；无需显式指令，完全由 LLM 驱动。
- **Managed Agents 环境**：不直接使用传统插件，而是通过挂载 MCP（Model Context Protocol）服务接入外部 API，实现与插件能力对等的外部工具调用，适用于需沙箱隔离、多步状态保持的复杂任务。

> ⚠️ 注意：插件能力仅在指定模型上可用，当前支持 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-plus`、`qwen-vl-max`；`qwen3` 系列模型暂不支持传统插件，但可通过 Managed Agents 的 MCP 方式等效扩展。

## 关键参数和配置（面向开发者）

| 参数 | 说明 | 必填 | 示例/约束 |
|------|------|------|-----------|
| **工具 ID** | 插件内唯一标识符，API 调用时必需字段 | 是 | `"calculator"`、`"text_to_image"` |
| **插件 URL + 工具路径**（仅自定义插件） | 构成完整调用地址：`URL + 工具路径` | 是 | `https://api.example.com` + `/v1/search` → `https://api.example.com/v1/search` |
| **传参方式** | 决定参数来源：`大模型识别`（从用户输入提取）或 `业务透传`（由外部系统注入） | 是 | 配置为 `biz_params` 或 `user_defined_params` 字段传入 |
| **参数类型与校验** | 支持 `String`/`Number`/`Object`；`Object` 类型子属性**不可为空**，需显式定义默认值或必填项 | 是 | `{"query": {"type": "string", "description": "搜索关键词"}}` |
| **鉴权配置** | 支持 `Header`（`basic`/`bearer`/`appcode`）或 `Query` 方式；仅允许透传 `Authorization` Header，其他 Header 不支持 | 是 | `Bearer <token>`、`appcode <appcode>`、`?appcode=xxx` |
| **HTTP 方法** | 推荐使用 `POST`；若用 `GET`，**禁止输入参数为 `Object` 类型**（否则返回错误码 `130022`） | 建议 | `POST` 更安全、更灵活 |

## 开发者须知（简洁实用）

- ✅ **快速起步**：优先选用官方插件（如 `code_interpreter`、`quark_search`），开箱即用，无需配置。
- ✅ **自定义接入**：必须提供符合 OpenAPI 3.0 规范的 JSON Schema 描述，模型据此解析参数结构；发布前务必点击“测试工具”验证连通性，并完成“发布”操作。
- ✅ **权限准备**：首次使用需主账号授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限。
- ❌ **限制规避**：
  - `code_interpreter` 沙箱**无网络访问权限**，且依赖库版本固定（如 `pandas==2.2.2`, `requests~=2.31.0`）；
  - `quark_search` 和 `github_search` 仅返回标题、关键词与摘要，**不支持获取网页/仓库原始内容**；
  - 删除插件或工具将导致所有已上线应用立即失效，操作不可逆；
  - 修改插件 URL 或鉴权配置后，必须重新测试并发布全部下属工具。
- 🛡️ **安全要求**：所有自定义插件的稳定性、安全性、计费归属均由开发者自行承担；百炼平台仅保障调用链路的协议兼容性与基础转发可靠性。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)


