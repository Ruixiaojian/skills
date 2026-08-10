# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格遵循阿里云 RAM 体系，需结合主账号与 RAM 用户协同配置。所有权限生效均依赖业务空间归属关系，且 API Key 权限与用户控制台权限相互独立。

## 支持的模型/功能

- **模型级操作控制**：支持对单个模型在指定业务空间内启用/禁用以下能力：
  - 模型调用（含控制台体验与 API 调用），并可分别设置 QPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流；
  - 模型调优（训练）及调优后部署；
  - 模型直接部署（无需调优）。
  
- **空间级角色管理**：基于三种角色实现分层管控：
  - **超级管理员**：拥有 `AliyunBailianFullAccess` 策略，可跨地域、跨空间管理模型、用户、API Key 及限流策略，但 [OpenAPI 接口权限](#4adcb2854f9rv) 仅主账号可开通；
  - **业务空间管理员**：仅管理所属空间内的用户权限、页面可见性、模型开关及 API Key；
  - **普通用户**：仅能使用被显式授权的资源与功能。

- **细粒度页面权限**：通过控制台「权限管理」页签为 RAM 用户分配具体菜单项操作权（如「模型体验-操作」「批量推理-操作」），但该设置**不影响其 API Key 的调用能力**。

> **注意**：默认业务空间（Default Workspace）不支持任何模型级权限限制（调用、调优、部署均默认开放），如需精细化管控，必须创建自定义业务空间 —— 这一约束在 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识，API 调用必需参数；可通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 | 必须与 API Key 所属空间一致 |
| `qpm_limit` / `tpm_limit` | 模型级限流阈值，单位分别为 QPM 和 TPM；仅对已开通调用权限的模型生效 | 由超级管理员在全局管理菜单中配置，见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户；其可用模型与限流策略**完全继承自归属业务空间**，不受用户控制台权限影响 | 创建后不可迁移，详见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

1. **创建与分配业务空间**  
   - 超级管理员通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）新建空间，并为各空间分配模型权限与限流值。

2. **配置用户角色**  
   - 超级管理员或业务空间管理员在控制台「权限管理」页签中为 RAM 用户授予角色（如「管理员」）或细粒度页面权限（如「模型调优-操作」）。

3. **开通 API 调用能力**  
   - 对于 OpenAPI（如知识库、Prompt 工程等），需主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此步骤独立于百炼控制台权限设置。

4. **生成与绑定 API Key**  
   - 在业务空间内为用户创建 API Key；该 Key 自动继承空间级模型权限与限流策略，无需额外配置模型白名单。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定地域，跨地域资源不可共享；即使同名空间（如 `project-prod-workspace`）在不同地域也互不关联。
- **默认空间限制**：默认业务空间无法配置模型调用/调优/部署开关及限流，生产环境务必使用自定义空间。
- **API Key 生命周期**：RAM 用户被移出业务空间时，其 API Key **立即失效**（重新加入后恢复）；若在 RAM 控制台删除该用户，则 Key **永久失效**。
- **账单与预付费权限**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，与百炼权限无关。
- **IP 白名单**：仅华北2（北京）地域的 API Key 支持设置 IP 访问白名单。
- **主账号特权**：OpenAPI 接口权限开通、AI 安全护栏服务开通、模型监控与应用观测功能启用，**必须使用阿里云主账号操作**，RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法完成。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


