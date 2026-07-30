# 应用部署

应用部署是百炼平台上将已构建的智能体（Agent）、工作流（Workflow）或模型服务发布为可被业务系统稳定调用的在线服务的过程。它标志着开发成果从调试环境进入生产可用状态，是连接模型能力与实际业务的关键环节。

## 在百炼平台的不同场景中，这个概念如何使用

应用部署在百炼平台中并非单一操作，而是根据底层能力形态分为三类典型实践：

- **模型级部署**：面向基础大模型或微调后模型，通过 `model deployment 1` 或 `model production` 能力，将其封装为独占资源、性能可控的推理服务（如 PTU/MU/Lora 模式），提供独立 endpoint，供 SDK 或 HTTP 直接调用。适用于需高 SLA、低延迟或定制化推理参数（如 thinking mode、context length）的场景。

- **智能体/工作流级部署**：面向已配置完成的智能体应用或工作流应用，在控制台点击「发布」或调用 `application call` API 的发布接口，使其获得全局唯一 `app_id` 并进入 `RUNNING` 状态。发布后即可通过标准 `/apps/{app_id}/completion` 接口被外部系统调用，支持多轮对话、插件参数透传和[多模态](multi-modal.md)输入。

- **托管智能体运行时部署（Managed Agents）**：不暴露传统 endpoint，而是通过 `managed agents api` 创建 `Agent`、`Environment` 和 `Session` 资源，由平台统一托管执行生命周期。开发者无需管理服务扩缩容或沙箱环境，只需按需创建 Session 并推送事件流，适用于强调安全隔离、工具链管控与事件驱动交互的复杂智能体场景。

三者本质不同：模型部署输出的是“模型即服务（MaaS）”，应用部署输出的是“智能体即服务（AaaS）”，而托管智能体则提供“运行时即服务（RaaS）”。选择依据是业务对控制粒度、安全要求、集成方式（同步/异步/流式）及运维成本的权衡。

## 关键参数和配置

| 场景 | 核心参数 | 说明 | 注意事项 |
|------|----------|------|----------|
| **模型部署** | `plan`（`ptu`/`mu`/`lora`） | 计费与调度模式标识 | `lora` 仅用于 LoRA 微调模型，`capacity` 参数无效；PTU/MU 模式需显式配置吞吐或规格 |
| | `ptu_capacity.{input/output}_tpm` 或 `deploy_spec` + `capacity` | 性能规格 | PTU 模式按 token 吞吐预购；MU 模式按副本数（`capacity`）扩展并发能力 |
| | `max_context_length`, `enable_thinking` | 推理行为控制 | 仅 MU 模式支持；需模型原生支持且未超出上限 |
| **应用部署（智能体/工作流）** | `app_id` | 应用唯一标识符 | 控制台发布后自动生成，调用必需 |
| | `workspace_id` | 条件必填 | 华北2（北京）地域默认隐含；跨地域或子业务空间调用必须显式传入 |
| | `stream`, `background` | 调用模式开关 | `stream=true` 仅工作流应用在发布时启用才生效；`stream` 与 `background` 互斥 |
| | `biz_params.user_defined_params` | 插件参数透传 | 仅对已关联对应插件的应用生效，结构需严格匹配插件定义 |
| **托管智能体（Managed Agents）** | `agent_id` + `environment_id` + `session_id` | 运行实例三元组 | `Session` 是实际执行单元，`Environment` 可复用，`Agent` 支持版本快照 |
| | `Event` 类型（`user_message`/`tool_call_approved`/`function_result`） | 交互协议 | 必须通过 SSE 流式订阅事件，以 `session_status` 字段判断终态 |

## 面向开发者，简洁实用

- **先确认目标**：你要部署的是一个模型（如 Qwen3-8B）、一个智能体（如客服助手）、还是一个带沙箱的托管智能体？选错路径会导致无法调用或权限错误。
- **发布 ≠ 部署完毕**：模型部署后需等待状态变为 `RUNNING`；应用发布后需检查 `app_id` 是否生效；托管智能体需成功创建 `Session` 才可投递事件。
- **Endpoint 与地域强绑定**：
  - 模型部署：endpoint 自动分配，无需指定地域；
  - 应用调用：优先使用 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`（通用），但工作流应用务必确认在华北2（北京）；
  - 托管智能体：endpoint 固定为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，`region` 当前仅支持 `cn-beijing`。
- **安全第一**：所有调用均需 `Authorization: Bearer <API_KEY>`，API Key 必须归属对应 workspace 且拥有 `application:call` 或 `model:deploy` 权限；切勿硬编码。
- **调试建议**：首次调用失败时，优先检查 `request_id` 并查阅错误码文档；模型部署关注 `status` 字段；应用调用关注 `app_id` 和 `workspace_id` 是否匹配；托管智能体关注 `Session` 状态机流转是否正常。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [managed agents api](../api/managed-agents-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application call](../api/application-call.md)
- [model production](../api/model-production.md)


