# 工具调用

工具调用（Tool Calling）是百炼平台中大模型自主决策并执行外部能力的核心机制，指模型在推理过程中，根据用户意图与上下文，动态生成结构化调用指令（如 `tool_calls`），交由平台运行时解析、安全执行，并将结果回填至对话上下文，从而完成单次响应无法覆盖的复杂任务（如代码执行、文件处理、实时搜索、API 调用等）。

## 在百炼平台的不同场景中，这个概念如何使用

工具调用不是单一 API，而是贯穿多个能力层的统一抽象，具体实现方式依场景而异：

- **Managed Agents（托管智能体）**：工具调用由平台全自动闭环管理。模型输出 `tool_calls` 后，Agent 运行时自动匹配已挂载的工具（内置 `bash`/`read`/`download_file` 等、Skill 或 MCP 服务），在隔离沙箱中执行，并通过 `tool_result` 事件流式回传结果；开发者无需手动解析或调用，只需配置 `tools` 和 `skills` 即可启用。
  
- **插件（Plug-in）**：工具调用以“插件”为单元组织，支持官方、三方及自定义 HTTP 工具。模型识别触发后，平台按预设鉴权（Bearer/AppCode）、参数映射规则自动发起 HTTP 请求；业务系统也可通过 `biz_params` 透传结构化输入，实现人机协同控制。

- **Skill（技能包）**：工具调用基于语义触发，不依赖显式函数名。模型仅需理解用户请求与 Skill 的 `description`（如“解析 PDF 表格并导出 CSV”），即可自动匹配并调用对应 ZIP 包中的逻辑；调用过程对开发者完全透明，无需声明函数签名。

- **MCP（Model Context Protocol）**：工具调用遵循标准化协议，屏蔽底层通信差异。平台将 MCP 服务注册为统一工具源，模型调用时生成符合 MCP 规范的 `tool_call`，由 MCP Client（如 `streamableHttp`）转发至目标服务端点；支持跨平台互操作，适用于智能体与工作流双场景。

- **Assistant API（基础大模型 API）**：工具调用需开发者主动参与循环。模型返回 `tool_calls` 后，客户端必须解析、逐个执行外部工具，并将结果拼入下一轮 `messages` 中再次请求模型，形成“推理 → 调用 → 回填 → 再推理”的手动编排链路。

> ✅ 共同原则：所有场景均要求工具在调用前**已显式声明或挂载**（如 Agent 配置 `tools`、应用启用 Skill、MCP 服务已开通），未声明的工具不会被模型识别或执行。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 示例 |
|------|----------|------|------|
| `tools` | Managed Agents / Assistant API | 声明可用工具列表，支持 `"builtin_toolkit"` 简写或完整工具对象数组 | `[{"type": "builtin_toolkit"}]` |
| `skills` | Managed Agents | 挂载 Skill 版本列表，**必须指定 `id` 和 `version`**（不支持 `latest`） | `[{"id": "sk_abc123", "version": 2}]` |
| `tool_id` | 插件 / MCP | 工具唯一标识符，用于模型生成 `tool_calls` 及平台路由 | `"calculator"`, `"WebSearch"` |
| `input` / `parameters` | 插件 / MCP / Skill | 工具执行所需输入，由模型提取或业务透传；Object 类型子字段**不可为空** | `{"query": "杭州天气"}` |
| `biz_params` | 插件 | 业务系统透传的结构化参数，绕过模型提取，直接注入工具调用 | `{"user_id": "u123", "region": "cn-shanghai"}` |
| `type` + `url` | MCP | MCP 服务传输协议与接入地址，**必须严格匹配端点路径**（如 `type: "streamableHttp"` → `/mcp`） | `{"type": "streamableHttp", "url": "https://.../mcp"}` |

> ⚠️ 注意：所有工具调用均受平台安全沙箱约束——内置工具限于沙箱内文件系统；插件/MCP 默认禁止访问本地资源；Skill 执行路径固定为 `/mnt/session/uploads/`；超时、鉴权失败、参数校验错误会以标准错误码（如 `11200058`）返回，需在客户端处理。

## 面向开发者，简洁实用

- **选型建议**：  
  - 快速上线 → 用 Managed Agents（全自动）；  
  - 需精细控制调用时机 → 用插件（显式工具 ID）；  
  - 复用垂直领域流程 → 用 Skill（语义触发）；  
  - 接入大量外部服务 → 用 MCP（协议标准化）；  
  - 最小依赖轻量集成 → 用 Assistant API（手动循环）。

- **调试要点**：  
  - 检查工具是否已在当前 Agent/应用中**正确挂载并启用**（控制台或 API 返回 `active` 状态）；  
  - 查看模型输出 `tool_calls` 是否包含预期 `tool_id` 和非空 `parameters`；  
  - 通过 SSE 流监听 `tool_output` 事件确认执行结果，而非仅依赖最终 `message`；  
  - 自定义工具务必测试 `description`（Skill）或 `input schema`（插件）是否足够明确，避免误触发。

- **避坑提示**：  
  - 不要硬编码 `tool_id` 或模型 ID —— 从控制台下拉列表或 `GET /models` API 动态获取；  
  - Skill 版本变更后，**已创建的 Agent 不自动更新**，需重新挂载新版本；  
  - MCP 服务 URL 更新后，必须在平台重新配置，旧连接不会自动刷新；  
  - 文件类工具（如 `read`）路径必须为 `/mnt/session/uploads/xxx`，不可自定义根目录。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)


