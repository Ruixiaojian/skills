# 业务空间隔离

业务空间隔离是百炼平台的核心安全与治理机制，指以 **业务空间（Workspace）** 为最小逻辑单元，对资源、权限、配额、API 调用上下文及数据可见性进行严格划分与边界管控。每个业务空间独立拥有模型授权、知识库、应用、Prompt 模板、连接器等资源，且其 API 调用必须显式绑定该空间 ID 与对应 API Key，跨空间访问一律拒绝（返回 `403 Forbidden`）。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识服务（Knowledge API）**：所有知识检索与问答请求均通过 `{workspaceId}.cn-beijing.maas.aliyuncs.com` 构造专属 Base URL，请求自动覆盖该 workspace 下所有已启用的知识库，不支持跨空间查询或指定其他 workspace 的知识库。
  
- **应用组件管理（Application Component API）**：几乎所有接口（如 `CreateIndex`、`AddFile`、`ListPromptTemplates`）均要求显式传入路径参数 `WorkspaceId`，资源创建、读取、更新、删除均限定在该空间内，不同 workspace 的资源完全不可见、不可互访。

- **模型调用（Model API）**：标准模型需在目标业务空间中单独授权；私有模型仅限其部署所在 workspace 的 API Key 调用；子业务空间模型调用必须使用该空间的 API Key，并匹配地域 Endpoint（如 `https://{workspaceId}.ap-southeast-1.maas.aliyuncs.com`）。

- **智能体/工作流调用（Application Call）**：当应用部署于子业务空间或非北京地域时，`app_id` 必须配合 `workspace_id` 使用；DashScope 兼容模式下，`workspace_id` 决定路由与鉴权上下文，缺失或错配将导致调用失败。

- **权限与配额管理**：模型 QPM/[Token](token.md) 限流、API Key 生效范围、OpenAPI 接口访问控制（如 `AliyunBailianDataFullAccess`）均按业务空间粒度配置；默认 workspace（`default-workspace`）不支持限流与细粒度开关，生产环境必须使用显式创建的非默认空间。

## 关键参数和配置

| 参数 | 类型 | 说明 | 获取方式 |
|------|------|------|----------|
| `workspace_id` | string | 业务空间唯一标识符，用于路由、鉴权与资源隔离 | 控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面查看；或通过 [获取 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 文档指引获取 |
| `Authorization: Bearer <API-Key>` | header | 绑定至单一 `workspace_id + region_id + user_id` 的认证凭证 | 在控制台 [API Key 管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建；**不可跨空间复用** |
| Base URL 模板 | — | `https://{workspaceId}.{region}.maas.aliyuncs.com`（如 `https:myws.cn-beijing.maas.aliyuncs.com`） | 地域固定（如北京为 `cn-beijing`），`{workspaceId}` 替换为实际值；OpenAI 兼容模式需使用 `dashscope.aliyuncs.com/compatible-mode/v1` 或对应地域 workspace endpoint |

> ⚠️ 注意：`workspace_id` 是路径参数（如 `/api/v1/indices/{indexId}` 中不显式出现，但 Base URL 已承载）、请求头 `Authorization` 的隐式绑定要素，以及部分接口（如 Application Component API）的显式路径参数（如 `/workspaces/{WorkspaceId}/indices`）。三者必须严格一致。

## 面向开发者，简洁实用

- ✅ **必做**：生产环境务必创建**非默认业务空间**（避免 `default-workspace`），并在其中完成模型授权、知识库配置、API Key 创建。
- ✅ **必验**：每次调用前确认三要素匹配——`workspace_id`（URL 或参数）、`API Key`（header）、`region`（Endpoint 域名）。
- ✅ **必守**：不要尝试复用其他 workspace 的 API Key 或拼接错误 workspace_id 的 URL，会直接返回 `403`。
- ❌ **禁用**：不要在代码中硬编码 `default-workspace`；不要跨地域混用 workspace_id（如北京空间 ID 用于新加坡 Endpoint）。
- 🛠️ **调试建议**：若遇 `403` 或 `404`，优先检查 `workspace_id` 是否正确、API Key 是否归属该空间、Endpoint 地域是否匹配。控制台右上角业务空间切换状态可辅助验证当前上下文。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [application component api reference](../api/application-component-api-reference.md)
- [more about models](../api/more-about-models.md)
- [application permission management](../guides/application-permission-management.md)
- [application call](../api/application-call.md)


