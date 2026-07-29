# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的行为均继承其归属业务空间的模型权限策略，与用户账号的控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制特定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（Fine-tuning），以及调优后是否允许部署；默认业务空间对所有支持调优的模型开放该能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：控制是否允许直接部署基础模型（如 Qwen 系列）至业务空间；默认业务空间无限制。
- **控制台页面权限**：按菜单粒度（如“模型体验”“批量推理”“模型观测”等）授予 RAM 用户访问和操作权限；该设置**不影响 API Key 行为**。
- **API Key 管理**：支持为 RAM 用户授权创建、删除、查看某业务空间下全部 API Key 的能力；单个 API Key 绑定唯一地域+业务空间+用户，不可迁移 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。实践中指用户首次开通百炼服务时自动创建的初始空间（通常命名含 `default` 或无显式名称），其权限策略不可编辑，需新建业务空间实现精细化管控。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求中的 `X-Workspace-ID` Header 或请求体；获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | — |
| `qpm_limit` / `token_limit` | 模型级限流阈值，由超级管理员在全局管理菜单中为业务空间配置；单位分别为 QPM 和 tokens/minute | — |
| `api_key` | 绑定至单一业务空间与用户的认证凭证；其可调用模型范围、限流值完全继承所属业务空间的模型权限配置 | — |
| `role_policy` | RAM 策略名，如 `AliyunBailianFullAccess`（超级管理员）、`AliyunBailianDataFullAccess`（OpenAPI 数据权限）等，需通过 RAM 控制台显式附加 | — |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已附加 `AliyunBailianFullAccess` 策略的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 管理所有空间。
   - 业务空间管理员：由超级管理员或同空间管理员在控制台 **权限管理 → 用户管理** 中授予“管理员”角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理中为指定业务空间启用目标模型的“调用”“调优”或“部署”开关；未开通则下游用户即使有操作权限也无法生效。

3. **控制台权限分配**  
   在业务空间内进入 **权限管理 → 用户管理 → 编辑用户权限**，勾选对应功能模块（如“模型体验-操作”“模型调优-操作”等）。

4. **API Key 分配与使用**  
   - 业务空间管理员可在 **权限管理 → API Key 管理** 中为用户创建 Key；
   - 调用时需在请求 Header 中携带 `Authorization: Bearer <api_key>` 及 `X-Workspace-ID: <workspace_id>`；
   - Key 的模型访问范围与限流策略**完全由其归属业务空间决定**，与用户账号的控制台权限无关。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域资源不可共享；同一业务空间名称在不同地域视为独立实体。
- **默认空间不可配置**：所有限流与模型开关功能仅对**非默认业务空间**生效；生产环境务必新建独立空间 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **OpenAPI 权限独立**：RAM 用户默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI；必须由主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **API Key 生命周期**：当 RAM 用户被移出业务空间时，其 API Key **临时失效**（重新加入后恢复）；若在 RAM 控制台彻底删除该用户，则 Key **永久失效且不可恢复**。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`；二者均需主账号在 RAM 控制台显式授权，不随百炼角色自动继承。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


