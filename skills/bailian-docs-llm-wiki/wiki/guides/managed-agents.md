# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断续接与调试可观测性。其核心价值在于将代理循环、沙箱编排与工具调度等基础设施复杂度下沉，使开发者聚焦于 Agent 逻辑本身。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需在创建 Agent 时显式指定，不支持运行时动态切换。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在沙箱内受限执行，无跨会话文件访问能力。
- **扩展能力**：
  - **MCP 服务**：通过标准 MCP 协议接入外部工具服务；
  - **Skill**：复用预置的端到端工具组合（如数据清洗、PDF 解析等）；
  - **自定义工具**：暂未开放用户自定义工具注册接口，仅支持平台内置及 MCP/Skill 两类。

> **注意**：文档 1 中称“支持安装依赖”，但文档 2 的 API 示例中 `packages` 配置仅允许在 Environment 创建阶段声明（如 `pip: ["pandas"]`），**不支持运行时动态 `pip install`**；实际执行中若 Agent 尝试在 `bash` 工具中调用 `pip install`，将因沙箱权限限制失败。该行为以[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)为准。

## 关键参数

| 参数 | 位置 | 说明 | 是否必需 |
|------|------|------|----------|
| `model.id` | Agent 创建 | 指定底层大模型 ID，如 `"qwen3-max"` | 是 |
| `system` / `instructions` | Agent 创建 | 系统提示词，定义角色与行为边界；影响工具选择与输出格式 | 是 |
| `tools` | Agent 创建 | 工具列表，支持 `"builtin_toolkit"`（全量内置）或细粒度枚举（如 `[{"type": "bash"}]`） | 否（默认启用全部） |
| `config.type` | Environment 创建 | 沙箱类型，仅支持 `"cloud"`（百炼托管容器） | 是 |
| `config.packages` | Environment 创建 | 预装依赖，支持 `apt`（系统包）和 `pip`（Python 包）字段 | 否 |
| `resources` | Session 创建 | 挂载资源列表，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/data"}]` | 否 |

## 使用方式

1. **创建 Agent**：通过控制台向导或 API 定义名称、模型、系统提示词与工具集。Agent 创建后获得唯一 ID（如 `agent_xxx`），可被多个会话复用 —— 参见[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。
2. **创建 Environment**：独立配置沙箱环境，指定预装包与网络策略（如 `unrestricted`）。Environment 亦可被多个会话共享 —— 参见[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。
3. **创建 Session**：绑定 Agent ID 与 Environment ID，可选挂载资源（如上传的 CSV 文件）。Session 启动后即进入 `idle` 状态，等待事件输入 —— 参见[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。
4. **发送事件与接收流**：
   - 发送 `user` 消息触发执行（`POST /sessions/{id}/events`）；
   - 订阅 SSE 流（`GET /sessions/{id}/events/stream`）实时接收 `message`、`tool_call`、`tool_output`、`session_status` 等事件；
   - 事件历史在服务端完整持久化，支持断点续查。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；沙箱内文件操作受容器磁盘配额约束（默认 5 GB）。
- **会话生命周期**：空闲会话（无新事件）将在 30 分钟后自动终止；活跃会话最长运行 24 小时，超时强制终止。
- **资源挂载路径**：所有挂载文件统一出现在 `/mnt/session/uploads/` 下，不可自定义根路径；系统提示词中须使用该绝对路径引用（如 `/mnt/session/uploads/report.pdf`）。
- **工具执行隔离**：每个会话拥有独立沙箱实例，`bash` 命令、文件修改、`pip install`（即使环境预装）均无法跨会话生效。
- **错误处理**：工具执行失败（如命令返回非零码、文件不存在）将生成 `error` 类型事件，Agent 可据此自主重试或终止；平台不自动重试。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


