# 业务空间（Workspace）隔离

业务空间（Workspace）是阿里云百炼平台的**最小权限管理单元**，按地域划分，用于隔离用户、模型、API Key、数据资源与监控用量。开发者通过业务空间实现多环境（开发/测试/生产）、多业务线、多团队之间的资源边界与权限边界。

## 核心特性

- **地域绑定**：单个业务空间不能跨地域存在；北京、新加坡、弗吉尼亚等地域的业务空间相互独立。
- **资源隔离**：模型授权、API Key、数据连接（类目/文件/知识库）、限流配额、监控数据均在业务空间维度独立。
- **空间 ID 格式**：`llm-xxxxxxxxxxxx`，在控制台创建后获取，OpenAPI 调用时作为 `WorkspaceId` 路径参数传入。
- **默认空间限制**：默认业务空间无法配置模型调用、调优、部署的开关与限流，所有支持的模型默认全部开放。

## 在不同场景中的使用

### 1. 权限与角色管理

业务空间承载三类角色：

| 角色 | 跨空间管理 | 模型授权/限流 | 用户与页面管理 | API Key 管理 |
| --- | --- | --- | --- | --- |
| 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户） | 支持 | 支持 | 支持 | 支持 |
| 业务空间管理员（被授予某空间管理员权限的 RAM 用户） | 不支持 | 不支持 | 支持（限当前空间） | 支持（限当前空间） |
| 普通用户 | 不支持 | 不支持 | 不支持 | 仅使用被授权资源 |

业务空间管理员定义为：拥有某个业务空间「权限管理」页面访问权的 RAM 用户。

### 2. API Key 归属

- 一个 API Key 只能归属**一个地域 + 一个业务空间 + 一个用户**，**不可转移**。
- API Key 的可调用功能与限流，与所在业务空间的授权一致，**不受用户控制台权限影响**。
- 同一 API Key 适用于该空间下所有模型类型（文生文/文生图/语音等），无需为不同模型创建多个 Key。
- 自 **2026 年 3 月 25 日** 起，**华北 2（北京）** 地域新创建的 API Key 一律归属主账号。
- 华北 2（北京）地域支持为 API Key 设置 **IP 访问白名单**。

API Key 失效规则：

| 操作 | 主账号 API Key | RAM 账号 API Key |
| --- | --- | --- |
| 主动删除 | 失效，不可恢复 | 失效，不可恢复 |
| 账号移出业务空间 | — | 失效（重新加入后恢复） |
| RAM 控制台删除账号 | — | 失效，不可恢复 |

### 3. 模型调用与限流

业务空间维度可控制：

- **模型调用**：开关具体模型是否可在该空间被调用（控制台与 API），并设置请求数（QPM/RPM）与 Token（TPM）限流。
- **模型训练**：是否允许在该空间内进行模型调优及调优后部署。
- **模型部署**：是否允许直接部署模型。
- **控制台页面**：RAM 用户对该空间各功能页（模型体验/调优/部署/监控等）的访问权限。

### 4. 应用组件 OpenAPI（数据/知识库/Prompt/记忆）

`bailian/2023-12-29` 接口集合下的所有 API（类目、文件、表格、知识库、Prompt 工程、长期记忆等），请求路径都包含 `{WorkspaceId}` 路径参数。调用前提：

- RAM 用户需挂载 `AliyunBailianDataFullAccess`（全量）或 `AliyunBailianDataReadOnlyAccess`（只读）策略。
- RAM 用户必须已加入对应业务空间，否则鉴权失败。
- 资源配额按空间计算（如类目上限 500 个/空间）。

### 5. 监控与用量统计

- 模型监控、Token 用量、调用日志、告警等数据**按业务空间维度统计**，数据延迟约 1 小时，控制台仅保留最近 30 天。
- 高级监控通过 Prometheus HTTP API 暴露指标，`workspace_id` 是核心 Label，可用于 PromQL 过滤：
  ```
  model_usage{workspace_id="llm-xxx", model="qwen-plus"}
  ```
- 免费额度按业务空间独立计算，支持开启「免费额度用完即停」开关。

### 6. 子空间隔离调用

在 DashScope 模型调用接口中，可通过 `X-DashScope-WorkspaceId` Header 显式指定调用所归属的业务空间，用于在主账号下隔离多个子业务的用量与限流。

### 7. 安全合规

- 所有业务空间内的数据均以 **AES-256** 加密落盘，且不会被用于模型训练。
- 业务空间是合规隔离的载体：生产数据、测试数据、不同客户数据应放入不同空间，避免越权访问与误删。

## 关键参数与配置

| 配置项 | 说明 |
| --- | --- |
| `WorkspaceId` | 业务空间 ID，格式 `llm-xxxxxxxxxxxx`；OpenAPI 路径参数；DashScope 调用可通过 `X-DashScope-WorkspaceId` Header 指定 |
| `AliyunBailianFullAccess` | 授予 RAM 用户超级管理员权限（跨空间） |
| `AliyunBailianDataFullAccess` / `AliyunBailianDataReadOnlyAccess` | 调用应用组件 OpenAPI 必须的策略 |
| 限流（QPM/TPM） | 在业务空间内按模型配置请求数与 Token 数限流 |
| IP 白名单 | 华北 2（北京）地域可在业务空间内为 API Key 配置 |

## 生产环境最佳实践

- **按环境划分（推荐）**：为开发、测试、生产分别建空间，如 `project-dev-workspace` / `project-prod-workspace`，避免互相污染。
- **按业务线划分**：为不同部门或客户建独立空间，便于权限、成本、用量分摊。
- **限流分配**：将主账号总配额按业务优先级分配到各空间，建议预留约 10% 作为缓冲。例如总 1000 QPM：生产 600 / 测试 200 / 开发 100 / 缓冲 100。
- **凭证最小化**：每个空间只为业务方提供该空间内的 RAM 用户 API Key；不要在前端/移动端使用永久 Key，结合临时 API Key 接口（`POST /api/v1/tokens`）派发短 TTL（最长 1800 秒）的 `st-` 前缀临时 Key。
- **事件总线告警**：异步任务完成事件按地域转发，业务空间内的任务应配置与该空间同地域的事件规则。

## 常见限制

- 业务空间不能跨地域，跨地域使用需在每个地域分别创建并独立维护权限/Key/数据。
- 默认业务空间不支持模型授权与限流配置，生产场景应避免直接使用默认空间。
- RAM 用户 OpenAPI 默认无权限，必须由主账号在 RAM 控制台显式授予数据类策略，否则即便在空间内也无法调用应用 OpenAPI。
- 业务空间内的资源（类目/文件/Key/限流配额）不可在空间之间迁移，规划时应充分考虑后续治理成本。

## 关联主题页

- [application permission management](../guides/application-permission-management.md)
- [application component api reference](../api/application-component-api-reference.md)
- [more about models](../api/more-about-models.md)
- [model monitoring](../guides/model-monitoring.md)
- [security and compliance](../guides/security-and-compliance.md)


