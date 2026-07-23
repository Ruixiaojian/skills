# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）和资源维度（模型调用、调优、部署、页面访问、API Key、OpenAPI）的精细化控制。权限策略同时作用于控制台操作与 API 调用，但二者权限模型存在关键差异：控制台权限由用户角色在业务空间内直接配置，而 OpenAPI 权限需通过 RAM 策略显式授予。所有权限均按地域隔离，同一业务空间不可跨地域存在。

## 支持的模型/功能

百炼权限管理覆盖以下核心能力：

- **模型级管控**：支持对特定模型启用/禁用**调用**（含控制台体验与 API）、**调优**（训练）和**部署**权限；默认业务空间不支持限制（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **空间级角色管理**：定义三类角色——**超级管理员**（跨空间全局管理）、**业务空间管理员**（单空间内用户、页面、模型限流管理）、**普通用户**（仅使用被授权资源）。
- **API Key 绑定与继承**：每个 API Key 严格归属单一地域、单一业务空间、单一用户；其可调用模型范围与限流策略**完全继承自所属业务空间的模型权限配置**，不受用户控制台权限影响（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **OpenAPI 接口权限**：独立于业务空间权限体系，需通过 RAM 策略（如 `AliyunBailianDataFullAccess`）显式授权，且**仅阿里云主账号可为 RAM 用户添加该类策略**（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实践中，北京、新加坡、弗吉尼亚三地默认空间行为一致，建议避免在默认空间承载生产流量。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求中指定目标空间（如 `X-Workspace-ID` Header 或请求体） | 必填；需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `model_name` | 模型标识符（如 `qwen-max`, `qwen-plus`），用于模型级权限开关 | 必须已在该业务空间中显式开通调用/调优/部署权限 |
| `qpm_limit` / `tpm_limit` | 每分钟请求数（QPM）与 [Token](../concepts/token.md) 数（TPM）限流阈值 | 仅超级管理员或业务空间管理员可在控制台设置；API Key 自动继承该值 |
| `api_key` | 认证凭证，绑定至特定 `workspace_id` 和用户 | 不可跨空间/用户迁移；华北2（北京）新创建的 API Key 默认归属主账号 |

## 使用方式

### 1. 角色与空间初始化
- **超级管理员**：需主账号或已附加 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 创建业务空间并分配模型权限。
- **业务空间管理员**：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

### 2. 模型权限开通（必需前置步骤）
- 超级管理员需先在全局管理中为业务空间**启用目标模型的调用/调优/部署能力**（默认空间自动全开，但不可配置限流）。
- 后续再由业务空间管理员在本空间内为具体用户分配对应控制台操作权限（如「模型体验-操作」「模型调优-操作」）。

### 3. API 调用授权
- 为用户生成 API Key（归属指定业务空间）；
- 该 Key 自动获得该空间已开通的所有模型调用权限及限流策略；
- 如需调用应用、知识库等 OpenAPI，**必须额外在 RAM 控制台为该 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略**。

## 限制和注意事项

- **地域强隔离**：业务空间与资源严格绑定地域，北京空间的模型权限配置对新加坡空间无影响；跨地域需分别配置。
- **默认空间不可控**：默认业务空间无法设置模型调用/调优/部署开关及限流，仅可用于快速体验，**严禁用于生产环境**。
- **API Key 与用户权限解耦**：用户控制台权限（如能否访问「模型调优」页面）不影响其 API Key 的实际调用能力；API Key 权限仅取决于所属业务空间的模型开通状态与限流配置。
- **OpenAPI 权限独立授权**：即使用户拥有业务空间管理员权限，若未被授予 `AliyunBailianDataFullAccess` 等 RAM 策略，仍无法调用 `/v1/applications/*` 等应用相关 OpenAPI。
- **账单与预付费权限需单独配置**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台手动附加，不随百炼角色自动继承。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


