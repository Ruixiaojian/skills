# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格遵循阿里云 RAM 体系，需结合控制台操作与 RAM 策略协同配置。详细设计原则和角色能力边界见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型在指定业务空间内独立设置：
  - 调用权限（含控制台 & API）、QPM/TPM 限流；
  - 调优（训练）权限及调优后部署权限；
  - 部署权限（仅限支持部署的模型）。
- **空间级隔离**：业务空间按地域物理隔离，不可跨地域共享；默认业务空间**不支持**任何模型级权限限制（所有模型默认可调用、调优、部署）。
- **用户角色分层**：
  - **超级管理员**：拥有 `AliyunBailianFullAccess` 策略，可跨地域、跨空间统一管理模型、用户、API Key 及空间配置；
  - **业务空间管理员**：仅管理所属空间内的用户权限、页面可见性、模型开关及 API Key；
  - **普通用户**：仅能使用被显式授权的资源与页面，无管理能力。
- **OpenAPI 细粒度授权**：RAM 用户默认**无权调用**应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI；需主账号在 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求路由及权限校验；需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户，其可用模型与限流策略**完全继承归属空间的模型级配置**，不受用户控制台权限影响 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `region_id` | 百炼服务地域标识（如 `cn-beijing`），决定业务空间物理位置及 API Endpoint；API Key 与 workspace_id 均绑定此参数 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

> **注意**：华北2（北京）地域自 2026年3月25日起，新创建的 API Key 默认归属主账号，且不支持转移至 RAM 用户 —— 该变更未在旧版文档中同步说明，实际配置时请以控制台最新提示为准。

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已授 `AliyunBailianFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 为其他 RAM 用户添加该策略。
   - 业务空间管理员：由超级管理员或现有空间管理员，在百炼控制台 **权限管理 > 用户管理** 中为 RAM 用户勾选「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   - 超级管理员需先在全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)）为业务空间启用目标模型的「调用」「调优」「部署」开关。

3. **用户权限分配**  
   - 控制台权限：在业务空间内 **权限管理 > 页面权限** 中，为用户勾选对应功能模块（如「模型体验-操作」「批量推理-操作」）；
   - API 权限：为用户创建 API Key（需空间管理员及以上权限），Key 的模型能力自动继承空间级开关状态。

4. **OpenAPI 授权（独立步骤）**  
   - 必须由阿里云主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，**不能通过百炼控制台配置**。

## 限制和注意事项

- **默认业务空间不可限权**：所有模型默认开放调用、调优、部署，且无法设置限流 —— 如需精细化管控，必须新建非默认业务空间。
- **API Key 与用户权限解耦**：用户控制台权限（如禁用「模型体验」页面）**不影响**其 API Key 的调用能力；API Key 权限仅取决于归属业务空间的模型开关与限流配置。
- **地域强绑定**：业务空间、API Key、workspace_id 均严格绑定单一地域，跨地域调用需分别配置对应地域的资源。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，百炼控制台不提供集成入口。
- **OpenAPI 权限特殊性**：`AliyunBailianData*` 系列策略仅控制 OpenAPI 调用，与模型调用/调优的控制台权限无关联，必须显式配置。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


