# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流配置及账单管理等全链路场景。权限策略严格遵循阿里云 RAM 体系，需结合系统策略（如 `AliyunBailianFullAccess`）与百炼控制台内细粒度授权协同生效。详细设计原则和基础概念请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心能力维度：

- **模型调用**：控制特定模型在业务空间内是否允许通过控制台或 OpenAPI 调用，并支持独立设置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（Fine-tuning）、数据集管理、评测与快照保存。
- **模型部署**：控制是否允许将调优后的模型或原生模型直接部署为可调用服务。
- **应用与知识库**：OpenAPI 对应用、知识库、Prompt 工程、[长期记忆](../concepts/memory.md)等功能的访问需额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此类权限**不随业务空间默认继承**，必须由主账号在 RAM 控制台显式绑定，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的 “OpenAPI 接口权限” 小节。
- **控制台页面级权限**：支持按菜单（如“模型体验”“批量推理”“模型调优”）为 RAM 用户分配可见性与操作权，但**不影响其 API Key 的实际调用能力**。

> **注意**：默认业务空间（Default Workspace）**不支持任何模型级权限限制**（调用、调优、部署均全部开放且不可限流），生产环境应避免使用，默认空间仅适用于快速体验。该约束在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调，是强制性设计前提。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求头 `x-bailian-workspace-id` 及 SDK 初始化。不同地域的同名空间 ID 不同，**不可跨地域复用**。 | 必须通过控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取；参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 常见问题第1条。 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 [Token](../concepts/token.md)/s，作用于整个业务空间对该模型的所有调用（含控制台+API）。 | 仅对非默认业务空间生效；限流策略需超级管理员在全局管理菜单中配置。 |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的认证凭证。其权限范围**完全继承归属业务空间的模型与功能开关**，不受用户控制台权限影响。 | 创建后不可迁移；华北2（北京）自2026年3月25日起新 API Key 默认归属主账号。详情见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的 “API-Key 权限” 小节。 |

## 使用方式

### 1. 角色初始化
- **超级管理员**：需主账号或已授 `AliyunBailianFullAccess` + `AliyunRAMFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 完成策略绑定，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一纳管空间与用户。
- **业务空间管理员**：由超级管理员或同空间其他管理员，在百炼控制台 **权限管理 → 用户管理** 中为指定 RAM 用户勾选“管理员”角色。

### 2. 模型权限开通（必需前置步骤）
- 超级管理员需先在全局管理菜单中为**目标业务空间**启用所需模型的：
  - ✅ 调用权限（含限流配置）
  - ✅ 调优权限（含训练/评测/部署开关）
  - ✅ 部署权限（针对原生模型）
- 此步骤不可由业务空间管理员执行，且**默认空间无法配置**。

### 3. 用户/Key 权限分配
- **控制台操作权**：在业务空间内 **权限管理 → 用户管理 → 编辑用户 → 页面权限** 中勾选对应菜单项（如“模型体验-操作”）。
- **API 调用权**：
  - 为用户创建/分配 API Key（需具备“管理 API-Key”权限）；
  - 若需调用应用/知识库等高级 OpenAPI，**必须额外在 RAM 控制台为该 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略** —— 此为独立权限，不包含在 `AliyunBailianFullAccess` 内。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格绑定地域，跨地域资源（如模型、API Key、账单）完全隔离，无法共享或迁移。
- **默认空间无权限控制**：所有模型调用、调优、部署均自动开放，且不可配置限流。生产环境必须使用**显式创建的非默认业务空间**。
- **API Key 与用户权限解耦**：用户在控制台被禁用某功能（如“模型调优”），其 API Key 仍可调用对应模型（只要业务空间已开通该模型权限）。反之亦然。
- **OpenAPI 权限需主账号授权**：`AliyunBailianDataFullAccess` 等策略**仅能由阿里云主账号在 RAM 控制台添加**，超级管理员（RAM 用户）无权授予；此限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确标注。
- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，不随百炼策略自动继承。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


