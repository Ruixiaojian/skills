# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断续接。相比无状态的智能体应用，Managed Agents 更适合需要有状态上下文、文件系统语义和可控执行环境的场景。

## 支持的模型与功能

- **支持模型**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需通过 `model.id` 字段显式指定，不支持别名或自动降级。
- **核心功能**：
  - 命令执行（`bash`）、文件操作（`read`/`write`/`edit`/`glob`/`grep`）、URL 文件下载（`download_file`）
  - MCP 服务接入与 Skill 挂载（可选扩展）
  - 沙箱内 pip/apt 包安装（通过 Environment 配置）
  - 文件挂载：上传文件自动挂载至 `/mnt/session/uploads/` 下，支持会话间隔离副本（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 表格中列出的是 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [模型服务目录](https://help.aliyun.com/zh/model-studio/model-service-catalog) 为准，旧文档中模型名可能已更新。

## 关键参数

| 参数 | 位置 | 说明 |
|------|------|------|
| `agent.id` | Session 创建时必填 | 智能体唯一标识，由 `agents.create()` 返回，不可复用名称 |
| `environment_id` | Session 创建时必填 | 运行环境 ID，沙箱配置独立于智能体（详见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)） |
| `resources` | Session 创建时可选字段 | 指定挂载的资源 ID 列表及目标路径，用于注入初始文件（见文档 6） |
| `tools` | Agent 创建时指定 | 支持 `"builtin_toolkit"`（启用全部内置工具）或显式工具列表；禁用某工具需显式排除，非默认关闭 |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，传入 `name`、`model.id`、`system` 和 `tools`；返回 `agent.id` 供后续复用（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 提供多语言 SDK 示例）。
2. **创建环境**：调用 `POST /api/v1/agentstudio/environments`，指定 `config.type = "cloud"` 及 `packages`（如 `{"pip": ["pandas"]}`），支持网络策略配置（`"unrestricted"` 或 `"restricted"`）。
3. **发起会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` 和 `environment_id`，可选传入 `resources` 挂载文件。
4. **交互与流式消费**：
   - 发送用户消息：`POST /sessions/{id}/events`，`input` 为标准消息数组（role=`user`）；
   - 接收事件流：`GET /sessions/{id}/events/stream`，使用 SSE 协议，事件类型包括 `message`、`tool_call`、`tool_output`、`session_status` 等。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/xxx`，不可自定义根路径。
- **沙箱隔离性**：同一资源被多个会话挂载时，各会话获得独立副本，修改互不影响；卸载后副本自动清理。
- **超时控制**：SSE 流默认无服务端超时，但客户端需设置合理 `timeout`（如 Python 示例中 `timeout=120.0`），避免长连接僵死。
- **状态持久化粒度**：事件历史在服务端完整持久化，但沙箱内存与进程状态**不跨会话保留**；重启会话即新建容器。
- **权限边界**：沙箱内禁止访问宿主机、其他会话沙箱或平台内部服务；网络访问受 `networking.type` 控制，`restricted` 模式下仅允许白名单域名。

> **注意**：文档 5 称“会话承载智能体的一次运行实例”，但文档 1 明确指出“支持中断与续接”——实际指会话本身可被暂停（`status=paused`）并恢复，而非终止后重建；若会话 `terminated`，则状态不可恢复，需新建会话。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


