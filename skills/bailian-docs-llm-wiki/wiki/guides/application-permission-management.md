# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的调用权限均继承自其归属业务空间的配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台与 OpenAPI 层面对指定模型的调用许可、QPM 限流与 Token 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **模型调优（训练）**：允许在业务空间内进行模型微调、数据集管理、评测与快照发布；
- **模型部署**：支持将调优后的模型部署为可调用服务；
- **控制台页面权限**：按菜单项（如“模型体验”“批量推理”“模型观测”等）授予 RAM 用户对特定功能的访问与操作权限；
- **API Key 管理**：支持创建、删除、查看本空间内所有 API Key，且每个 API Key 严格绑定单一地域、单一业务空间与单一用户（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台最新 UI 为准，北京地域默认空间确为只读模式，而新加坡、弗吉尼亚地域部分新创建的默认空间已支持基础限流配置（需验证）。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用时指定作用域；必须与 API Key 所属空间一致 | 必须通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 |
| `qpm_limit` / `token_limit` | 模型级每分钟请求数与 Token 总量限流阈值，由超级管理员在全局管理菜单中设置 | 仅对非默认业务空间生效；默认空间不支持配置 |
| `api_key` | 绑定至单一 workspace + user + region，其调用能力完全继承该 workspace 的模型权限与限流策略 | 不可跨空间/跨用户迁移；华北2（北京）新创建的 API Key 默认归属主账号（2026-03-25起） |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 进行跨空间配置；  
   - 业务空间管理员：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色；  
   - 普通用户：由管理员分配具体功能权限（如「模型体验-操作」「数据管理-操作」等）。

2. **模型权限开通流程**  
   - 超级管理员在全局管理中为业务空间启用目标模型的「调用」「调优」或「部署」开关；  
   - 业务空间管理员在本空间「权限管理」中为用户分配对应控制台功能权限；  
   - 若需 API 调用，需为该用户在本空间生成 API Key（无需额外策略）。

3. **OpenAPI 权限开通**  
   - 必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略；  
   - 该操作独立于百炼控制台权限配置，不继承 workspace 设置。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，北京、新加坡、弗吉尼亚的同名空间互不互通，权限不可复用；
- **默认空间限制**：所有地域的默认业务空间均**不支持**模型调用/调优/部署的显式开关控制与限流配置，建议生产环境使用显式创建的业务空间；
- **API Key 生效逻辑**：其权限仅取决于归属 workspace 的模型授权状态，与用户账号的控制台权限（如是否拥有「模型体验-操作」）**完全无关**；
- **账号移出影响**：RAM 用户被移出业务空间后，其名下 API Key 将**立即失效**（重新加入后自动恢复），但主账号 API Key 不受此影响；
- **账单与预付费权限**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，百炼控制台不提供集成入口；
- **细粒度页面权限 ≠ API 权限**：控制台菜单权限（如「模型观测-操作」）仅控制前端可见性与交互能力，不影响 API 调用资格。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


