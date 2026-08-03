# 工具调用

工具调用是百炼平台中大模型与外部能力协同执行任务的核心机制，指模型在推理过程中主动识别用户需求、规划执行步骤，并安全、可控地调用预注册的外部工具（如代码解释器、搜索服务、图像生成器等）以补充自身能力边界的过程。

## 在百炼平台的不同场景中，这个概念如何使用

工具调用并非单一接口行为，而是贯穿多种运行时形态的统一抽象，具体体现为以下三类模式：

- **智能体（Agent）自主调用**：模型基于用户输入和系统提示，自动判断是否需要调用工具、选择哪个工具、构造参数并处理返回结果。适用于问答、数据分析、多步任务等场景。支持插件（Plugin）、Skill、MCP 服务及 Managed Agents 内置工具（如 `bash`、`read_file`）。
  
- **工作流（Workflow）显式编排**：开发者在可视化画布中将工具作为独立节点拖入流程，手动配置输入/输出映射关系。此时调用由流程引擎驱动，模型仅负责语义解析（如从用户消息中提取城市名传给天气工具），不参与决策。

- **API 层声明式启用**：通过 `tools` 参数在请求中声明可用工具列表（如 DashScope 原生接口或 Assistant API），SDK 自动处理「模型输出 → 工具调用 → 结果注入 → 下一轮推理」的完整循环，开发者无需实现代理逻辑。

> ✅ 关键区别：  
> - 插件（Plugin）和 MCP 服务面向业务能力扩展，强调标准化接入与跨应用复用；  
> - Skill 面向文件与结构化数据处理，以 ZIP 包形式封装逻辑，触发依赖 `description` 语义匹配；  
> - Managed Agents 内置工具（如 `download_file`, `edit`）运行于沙箱环境，专为长时、多步、带状态的任务设计；  
> - 所有工具调用均受平台统一调度、鉴权、审计与计费，不暴露原始网络或系统权限。

## 关键参数和配置

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `tool_id` 或 `function.name` | `tools` 数组中每个工具定义 | 是 | 工具唯一标识符（如 `"calculator"`、`"text_to_image"`），用于模型识别与路由。官方工具 ID 可在控制台复制，自定义工具需与注册时一致。 |
| `input` / `parameters` | 工具调用请求体 | 按工具要求 | 输入参数对象。若为 `大模型识别` 类型，由模型从上下文抽取；若为 `业务透传` 类型，需通过 `biz_params`（插件）或 `user_defined_params`（MCP）显式传入。建议为 Object 类型参数提供 `Value` 示例（如 `{"query": "杭州天气"}`）提升准确率。 |
| `type` | MCP 工具配置 | 是（MCP 场景） | 协议类型，必须为 `"streamableHttp"`（对应 `/mcp` 端点），旧版 `"sse"` 已弃用。 |
| `url` + `headers.Authorization` | MCP 工具配置 | 是（MCP 场景） | MCP Server 地址及有效 `DASHSCOPE_API_KEY`（格式：`Bearer <key>`）。 |
| `resources` | Managed Agents Session 创建 | 否（按需） | 挂载文件资源列表，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/data.csv"}]`，供内置工具读取。 |

> ⚠️ 注意事项：
> - 单次对话最多触发 **5 次工具调用**（MCP/插件），且同一智能体最多绑定 **10 个工具**；
> - `code_interpreter` 等沙箱工具禁止网络访问与本地文件上传，安全策略不可绕过；
> - RAM 子账号使用前必须获得 `ram:CreateServiceLinkedRole` 权限，否则无法完成插件/MCP 授权；
> - [OpenAI 兼容接口](openai-compatible-interface.md)默认**不启用工具调用**，需改用 DashScope 原生接口或 OpenAI兼容-Responses。

## 面向开发者，简洁实用

- **快速验证**：在智能体调试面板发送 `计算 sqrt(144) + 2^10`，观察是否自动调用 `calculator` 并返回 `1164.0`；
- **参数调试技巧**：对复杂工具，先在控制台“测试工具”功能中手动传参验证，再配置 `Value` 示例提升模型泛化能力；
- **错误排查优先级**：  
  ① 检查工具是否已发布且状态为“已启用”；  
  ② 核对 `tool_id` 大小写与控制台完全一致；  
  ③ 查看 SSE 流中 `tool_call` 事件是否发出、`tool_output` 是否返回、是否有 `error` 字段；  
  ④ 若为自定义工具，确认鉴权 Header（如 `Authorization: Bearer xxx`）拼接正确、KMS 凭据已解密；
- **性能优化**：对高频调用工具，优先选用 MCP 脚本部署（FC 托管），避免网络延迟；对低频定制逻辑，用 Skill ZIP 包封装更轻量。

工具调用是百炼实现“模型即服务”到“能力即服务”的关键跃迁——它让开发者聚焦业务逻辑，而非基础设施编排。善用这一机制，即可快速构建具备真实世界行动力的智能应用。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [managed agents](../guides/managed-agents.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model context protocol](../guides/model-context-protocol.md)


