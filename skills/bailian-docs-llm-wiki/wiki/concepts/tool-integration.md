# 工具集成

工具集成是百炼平台中将外部能力（如计算、搜索、图像生成、文件处理、API 服务等）以标准化、可编排、可调度的方式接入大模型工作流的核心机制。它通过统一协议（如 MCP）、运行时抽象（如 Managed Agents 沙箱）和声明式配置，使大模型不仅能理解用户意图，还能自主或受控地调用真实世界的能力，从而突破纯语言推理的边界，构建具备行动力的智能体。

## 在百炼平台的不同场景中，这个概念如何使用

工具集成不是单一功能，而是贯穿多个平台能力层的横切能力，其具体形态和使用方式依场景而异：

- **智能体应用（Agent）**：以「插件（Plug-in）」或「MCP 服务」形式接入。大模型基于自然语言输入自主规划调用时机、工具选择与参数构造（如“画一只穿宇航服的猫” → 自动触发 `text_to_image`）。官方插件开箱即用；MCP 服务支持更丰富的第三方能力（如高德地图、网页爬取），需在控制台开通并添加至智能体。

- **工作流应用（Workflow）**：以「MCP 节点」或「自定义工具节点」显式编排。开发者拖拽工具节点，手动绑定输入变量（如从上一节点提取的 URL）与输出字段（如返回的天气数据），实现确定性、可调试的任务链，适用于业务逻辑强、步骤固定的场景（如“用户提交表单 → 调用风控 API → 写入数据库”）。

- **Managed Agents（托管智能体）**：以「内置工具 + MCP/Skill 挂载」方式深度集成。除 `bash`、`read`、`write` 等沙箱原生工具外，还可挂载 Skill（ZIP 封装的端到端流程）或通过 MCP 接入外部服务。所有工具在隔离沙箱中执行，支持跨轮次文件读写与状态保持，适用于需多步交互、代码执行或文件处理的复杂任务（如“分析上传的 Excel → 生成图表 → 输出 PDF 报告”）。

- **Assistant API / Application Call**：通过 `tools` 字段声明可用工具集合（支持 OpenAI 兼容格式），在 `messages` 中触发调用。工具定义需包含 `tool_id`（插件）或 `function.name`（MCP），参数由模型自动填充或由业务透传（`biz_params`）。这是面向开发者的编程接口，适用于嵌入自有系统或构建定制化前端。

- **Skill（技能包）**：作为轻量级工具集成方案，以 ZIP 包形式封装预置逻辑（如 PDF 解析、CSV 清洗）。无需 API 配置，仅靠 `description` 语义匹配触发，对用户完全透明。适合高频、标准化、无外部依赖的原子能力扩展。

- **自定义插件 / MCP 服务**：面向开发者对接任意 REST 或 MCP 协议服务。需定义输入/输出 Schema、鉴权方式（Header/Query/KMS 加密凭证）、请求方式（JSON/x-www-form-urlencoded），发布后即可被上述所有场景复用。

## 关键参数和配置

工具集成的通用配置要素如下，具体字段依接入方式略有差异：

| 类别 | 参数名 | 说明 | 必填 | 示例 |
|------|--------|------|------|------|
| **标识** | `tool_id` / `function.name` | 工具唯一 ID，调用时必需 | 是 | `"quark_search"`, `"maps_weather"` |
| **输入** | `input_parameters` | 定义参数名、类型（String/Number/Boolean/Object）、是否必填、描述 | 是（自定义工具） | `{ "query": { "type": "string", "description": "搜索关键词" } }` |
| **输出** | `output_parameters` | 定义 API 返回字段结构，影响模型解析质量 | 是（自定义工具） | `{ "results": { "type": "array", "items": { "title": { "type": "string" } } } }` |
| **鉴权** | `auth_type`, `auth_token` | 自定义插件/MCP 所需：`basic`/`bearer`/`appcode`/`kms` | 否（官方插件无需） | `kms://acs:kms:cn-beijing:1234567890:alias/mcp-key` |
| **调用控制** | `enable_search`, `biz_params` | 控制是否启用某类能力（如搜索开关），或透传业务参数 | 否 | `{"enable_search": true}`, `{"user_id": "u123"}` |
| **环境绑定** | `environment_id` | Managed Agents 中指定沙箱环境（含预装依赖、网络策略） | 是（Managed Agents） | `"env-cloud-prod"` |

> ⚠️ 注意：  
> - `Object` 类型参数在 `GET` 请求中不被支持；  
> - 自定义工具的 `output_parameters` 必须完整定义，否则模型无法正确解析返回值；  
> - KMS 凭据为强制要求，禁止明文填写敏感信息；  
> - 所有工具必须处于「已发布」且「调试成功」状态才可调用。

## 面向开发者，简洁实用

- **快速起步**：优先选用官方插件（如 `calculator`, `code_interpreter`）或 MCP 广场中的预置服务（如 `WebSearch`），无需配置即可在智能体中测试。
- **自定义接入**：  
  - 对 REST API：用「自定义插件」向导，填入 URL、参数 Schema、鉴权方式，5 分钟完成发布；  
  - 对 MCP 协议服务：选择 `npx`/`uvx` 一键部署，或配置 `http` 连接自有服务，注意端点路径与 `type`（`streamableHttp`）严格匹配。
- **调试技巧**：  
  - 在控制台对话窗输入明确指令（如“用计算器算 15×24”），观察是否触发工具调用及返回结果；  
  - 查看 `tool_call` 和 `tool_output` 事件日志，确认参数传递与响应解析是否符合预期；  
  - 使用 SDK 的流式事件监听（如 `client.sessions.events.stream()`）实时跟踪工具执行过程。
- **生产建议**：  
  - 工具调用失败时，检查错误码（如 `130040` = 参数描述缺失，`11200058` = MCP 协议类型不匹配）；  
  - 敏感凭证一律通过 KMS 加密；  
  - 多环境部署时，使用 `environment_id` 隔离沙箱配置，避免测试污染生产；  
  - 工作流中优先用 MCP 节点替代硬编码 HTTP 调用，提升可维护性与可观测性。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application call](../api/application-call.md)


