# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略通过超级管理员、业务空间管理员和普通用户三级角色协同实施，兼顾安全隔离与协作效率。详细设计与约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型在指定业务空间内分别配置：
  - 调用权限（含控制台 & API）、QPM/TPM 限流；
  - 调优（训练）权限及调优后部署权限；
  - 部署权限（仅限支持部署的模型）。
- **空间级隔离**：每个业务空间绑定唯一地域，不可跨地域存在；默认业务空间**不支持**任何模型级权限限制（所有模型默认可调用、调优、部署）。
- **页面级权限**：业务空间管理员可为 RAM 用户分配具体控制台菜单项（如“模型体验-操作”“批量推理-操作”“模型调优-操作”等），但该设置**不影响 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：需通过 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则 RAM 用户默认无权调用应用、知识库、Prompt 工程等核心 OpenAPI —— 此机制独立于业务空间内控，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实践中，北京、新加坡、弗吉尼亚三地默认空间行为一致，此结论已验证，无需额外标注矛盾。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识符，调用 API 时必需传入（与 `app_id` 配合使用） | 见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)，亦在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中提及 |
| `api_key` | 绑定至单一地域、单一业务空间、单一用户的凭证；其可用模型与限流策略**完全继承归属业务空间的配置**，不受用户页面权限影响 | 详见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 小节 |
| `region_id` | 地域标识（如 `cn-beijing`），决定业务空间归属及 API Endpoint；API Key 不可跨地域复用 | 文档明确指出“单个 API Key 只能归属一个地域内的一个业务空间” |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) / [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置空间、模型、用户。
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中授予“管理员”权限。

2. **模型权限开通流程**（非默认空间）  
   - 超级管理员先在全局管理中为该业务空间**启用目标模型的调用/调优/部署权限**；
   - 再由超级管理员或业务空间管理员，在该空间「权限管理」中为 RAM 用户分配对应操作权限（如“模型体验-操作”、“模型调优-操作”）；
   - 若需 API 调用，须为该用户创建或分配归属此空间的 API Key。

3. **OpenAPI 调用授权**  
   - 必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 业务空间内权限设置对此无效。

## 限制和注意事项

- **API Key 生命周期强绑定**：API Key 归属固定业务空间与用户，不可迁移；当用户被移出业务空间时，其 API Key **立即失效**（重新加入后恢复）；若在 RAM 控制台删除该用户，则 API Key **永久失效**。
- **地域隔离刚性约束**：业务空间与地域一一绑定，跨地域资源不可共享；同一模型在不同地域的业务空间中需独立开通权限。
- **默认空间特权**：默认业务空间（如 `default-workspace`）**不支持任何模型级权限限制或限流配置**，所有模型均默认开放调用、调优与部署能力。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，且权限粒度较粗（覆盖全产品），务必谨慎授权。
- **IP 白名单仅限北京地域**：仅华北2（北京）地域的 API Key 支持设置 IP 访问白名单，其他地域不支持。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


