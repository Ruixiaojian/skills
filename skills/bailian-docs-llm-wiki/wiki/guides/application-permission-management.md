# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格遵循阿里云 RAM 体系，需结合主账号与 RAM 用户角色协同配置。所有权限生效均依赖业务空间归属关系，且 API Key 权限继承自其所属空间而非用户控制台权限 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型设置调用（含控制台 & API）、调优（训练）和直接部署三类开关，仅在**非默认业务空间**中可配置；默认业务空间对所有模型开放全部能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **角色分级**：
  - **超级管理员**：拥有 `AliyunBailianFullAccess` 策略，可跨地域、跨空间管理模型限流、用户、API Key 及空间生命周期；
  - **业务空间管理员**：仅管理指定空间内的用户权限、页面可见性及模型可用性；
  - **普通用户**：仅能使用被显式授权的页面与资源，无管理能力。
- **细粒度页面权限**：通过控制台「权限管理」页签为 RAM 用户分配具体菜单项（如“模型体验-操作”“批量推理-操作”），但该设置**不影响 API Key 的调用能力** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI，需主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，API 调用必需参数 | 必须与 API Key 所属空间一致；获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `qpm_limit` / `token_limit` | 模型级请求/[Token](../concepts/token.md) 限流值（QPM、TPM） | 仅在非默认业务空间中可设置；全局配额按空间比例分配（如生产环境占 60%） |
| `api_key` | 绑定至单一地域+单一业务空间+单一用户的凭证 | 不可跨空间/跨用户迁移；华北2（北京）新创建的 API Key 默认归属主账号（自 2026-03-25 起） |
| `ip_whitelist` | API Key 的 IP 访问白名单 | 仅华北2（北京）地域支持 |

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台界面为准——若某地域默认空间页面中缺失限流开关，则视为不可配置。

## 使用方式

1. **初始化空间**：超级管理员通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）创建非默认业务空间，并为该空间开通目标模型的调用、调优或部署权限。
2. **分配角色**：
   - 超级管理员：在 RAM 控制台为 RAM 用户附加 `AliyunBailianFullAccess`；
   - 业务空间管理员：在百炼控制台「权限管理」页签中为用户勾选「管理员」角色。
3. **配置模型权限**：
   - 控制台调用：为目标用户分配「模型体验-操作」「批量推理-操作」等页面权限；
   - API 调用：为用户在对应空间创建 API Key（自动继承空间级模型权限）。
4. **启用 OpenAPI**：主账号在 RAM 控制台为 RAM 用户绑定 `AliyunBailianDataFullAccess` 或只读策略。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定单一地域，跨地域资源不可共享；即使同名空间（如 `project-prod-workspace`）在不同地域也互不关联。
- **API Key 绑定刚性**：一个 API Key 仅归属一个地域、一个业务空间、一个用户，删除用户或将其移出空间将导致其 API Key 失效（重新加入后恢复）。
- **权限继承逻辑**：API Key 的模型调用能力完全由其所属业务空间的模型开关与限流策略决定，**不受用户控制台页面权限影响**；例如用户无「模型体验」权限但仍可通过 API Key 调用已开通模型。
- **账单与预付费权限**：RAM 用户需单独授予 `AliyunBSSReadOnlyAccess`（查看账单）或 `AliyunBSSOrderAccess`（购买预付费）策略，且该授权作用于**全阿里云产品**，非百炼专属。
- **默认空间例外**：所有限流与模型开关功能在默认业务空间中不可用，建议生产环境务必使用自建非默认空间 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


