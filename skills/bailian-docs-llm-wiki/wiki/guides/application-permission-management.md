# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。API Key 的权限继承自归属业务空间，与用户控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台与 OpenAPI 层面的模型启用/禁用、QPM 与 [Token](../concepts/token.md) 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **模型调优（训练）**：支持在业务空间内开通特定模型的调优权限，并管理数据集、快照、评测与部署流程；
- **模型部署**：允许将调优后的模型部署为可调用服务；
- **控制台页面级权限**：按菜单（如“模型体验”“批量推理”“模型观测”等）分配操作权限；
- **API Key 管理**：创建、删除、查看及 IP 白名单设置（仅华北2支持），其调用能力严格绑定归属业务空间的模型权限（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，**不随业务空间权限自动继承**（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间（Default Workspace）**无法配置任何模型级限制**（调用、调优、部署均全量开放），生产环境应避免直接使用，默认空间仅适用于快速试用。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，用于 API 调用时指定作用域；可通过控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 文档获取 |
| `model_name` | 模型标识符（如 `qwen-max`, `qwen-vl`），须与百炼控制台模型列表中名称完全一致 |
| `qpm_limit` / `token_limit` | 每分钟请求数与 [Token](../concepts/token.md) 数上限，单位为整数，设为 `0` 表示禁用该模型调用 |
| `api_key` | 绑定至单一业务空间与 RAM 用户，不可跨空间复用；其权限范围由归属空间的模型开关与限流策略决定 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置；
   - 业务空间管理员：由超级管理员或同空间管理员在「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（超级管理员操作）**  
   在全局管理菜单 → 选择目标业务空间 → 「模型管理」中启用所需模型，并设置 QPM/[Token](../concepts/token.md) 限流值。

3. **用户控制台权限分配（超级管理员或业务空间管理员操作）**  
   进入业务空间 → 左侧导航栏「权限管理」→ 选择 RAM 用户 → 勾选对应功能模块权限（如「模型体验-操作」「模型调优-操作」等）。

4. **API 调用准备**  
   - 为用户在目标业务空间生成 API Key（「权限管理」→ 「API Key 管理」）；
   - 请求头携带 `Authorization: Bearer <api_key>`，并在参数中显式传入 `workspace_id`；
   - 若需调用应用、知识库等 OpenAPI，**必须额外在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或只读策略**。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域需独立创建空间并分别授权（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；
- **API Key 绑定不可变**：一旦创建，其归属的业务空间与用户不可迁移；删除用户或将其移出空间将导致 API Key 失效（重新加入可恢复）；
- **默认空间无限制能力**：所有模型默认可用且不限流，不适用于生产环境；
- **OpenAPI 权限独立于空间权限**：即使用户拥有某业务空间全部控制台权限，若未在 RAM 控制台显式授予 `AliyunBailianData*Access` 策略，仍无法调用应用相关 OpenAPI；
- **账单与预付费权限需额外配置**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独添加；
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域新创建的 API Key 默认归属主账号，不再支持 RAM 用户自主创建。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


