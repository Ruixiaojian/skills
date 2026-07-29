# 业务空间隔离

业务空间隔离是百炼平台的核心安全与治理机制，指以 `Workspace`（业务空间）为最小逻辑单元，对计算资源、数据资产、模型权限、API 调用、监控数据及安全策略实施严格边界划分，确保不同业务主体（如部门、项目、客户）之间资源不可见、权限不越界、数据不交叉、行为可审计。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用层**：所有 OpenAPI（应用组件、托管智能体等）均强制要求传入 `workspace_id`（路径参数或 Header），服务端据此路由请求、校验权限、隔离资源。例如 `AddFile` 创建的文件仅在指定 Workspace 内可见，跨 Workspace 的 `Retrieve` 请求将直接拒绝。
  
- **权限管理层**：RAM 用户的 API Key 绑定且仅属于单一 Workspace；模型调用开关、QPM/[Token](token.md) 限流、页面菜单权限均按 Workspace 独立配置。一个用户在 Workspace A 有 `qwen-max` 调用权，在 Workspace B 无该权限，二者完全独立。

- **运行时环境层**：托管智能体（Managed Agents）的 `Agent`、`Environment`、`Session` 均归属特定 Workspace；沙箱执行、文件挂载、Skill 加载均受 Workspace 边界约束，无法跨空间访问或共享。

- **可观测性层**：应用监控（Application Monitoring）仅展示当前 Workspace 内已发布应用的 Trace 数据；Trace ID 和 Span 数据天然绑定 Workspace，不同 Workspace 的调用链互不可见、不可关联。

- **安全合规层**：私网访问（PrivateLink）、AI 安全护栏启用、加密推理密钥管理等能力均需在 Workspace 级别开通与配置；安全策略（如 `X-DashScope-DataInspection` 生效范围）也以 Workspace 为作用域。

## 关键参数和配置

- `workspace_id`：业务空间唯一标识符，**所有 API 必填参数**。常见传递方式：
  - ROA 接口：作为路径参数（如 `/workspaces/{workspace_id}/apps`）
  - REST 接口：通过 `X-Workspace-ID` HTTP Header 传递
  - SDK：初始化客户端时显式指定（如 Python SDK 的 `workspace_id="ws-xxx"`）

- `region`：地域标识（如 `cn-beijing`），与 `workspace_id` 组合构成资源全局定位。**同一逻辑 Workspace 在不同 region 视为完全独立实体**，权限、数据、配额均不互通。

- `api_key`：绑定至**单一 region + 单一 workspace_id + 单一 RAM 用户**，不可复用、不可迁移。创建后即锁定其作用域。

> ⚠️ 注意：默认业务空间（系统自动创建）无完整权限控制能力，开发者应主动创建自定义 Workspace 以获得模型限流、细粒度授权等能力。

## 面向开发者，简洁实用

- ✅ **必须做**：每次调用百炼 API 前，确认 `workspace_id` 正确且与你的 API Key 所属空间一致；检查 `region` 是否匹配 Endpoint（如北京地域用 `cn-beijing`）。
- ✅ **推荐实践**：为不同项目/客户分配独立 Workspace，避免权限混用与数据泄露风险；通过 RAM 策略精确授予 `AliyunBailianDataFullAccess` 等 Workspace 级权限。
- ❌ **禁止操作**：不要尝试复用 API Key 跨 Workspace 调用；不要在代码中硬编码 `workspace_id`，建议从环境变量或配置中心注入。
- 🔍 **排障提示**：若遇到 `403 Forbidden` 或 `ResourceNotFound`，优先检查 `X-Workspace-ID` 是否缺失、错误，或当前 API Key 是否未被授权该 Workspace。

## 关联主题页

- [application component api reference](../api/application-component-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [application permission management](../guides/application-permission-management.md)
- [application monitoring](../guides/application-monitoring.md)
- [security and compliance](../guides/security-and-compliance.md)


