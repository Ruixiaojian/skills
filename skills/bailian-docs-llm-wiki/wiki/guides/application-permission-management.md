# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，支持基于 RAM 的策略授权与 API Key 级资源隔离。所有权限配置均需结合业务空间上下文生效，**默认业务空间不支持限流与模型能力开关**，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型调用控制**：可对指定模型开启/关闭调用权限，并设置 QPM（每分钟请求数）与 Token 限流（仅非默认业务空间支持）。
- **模型调优（训练）控制**：支持启用/禁用特定模型的调优、数据集管理、评测与快照发布能力。
- **模型部署控制**：支持控制模型是否允许在该业务空间内直接部署为服务。
- **控制台页面级权限**：按功能模块（如“模型体验”“批量推理”“模型观测”等）授予或限制 RAM 用户的 UI 操作权限。
- **API Key 绑定与生命周期管理**：每个 API Key 严格绑定单一地域、单一业务空间和单一用户，其可调用模型范围与限流策略继承自归属业务空间，不受用户控制台权限影响 —— 这一关键约束在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

> **注意**：文档中多次提及“默认业务空间无法设置模型调用/调优/部署限制”，但未说明其是否支持 OpenAPI 调用。实际开发中需注意：**默认业务空间虽不限制模型能力，但 RAM 用户仍需显式获得 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 权限才能调用应用相关 OpenAPI**，该要求独立于业务空间配置，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的 “OpenAPI 接口权限” 章节。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求路由与权限校验 | 必填；需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 |
| `model_name` | 模型名称（如 `qwen-max`, `qwen-vl-plus`），用于模型级权限开关 | 必须已在该业务空间中显式启用（超级管理员操作） |
| `qpm_limit` / `token_limit` | 每分钟请求上限、Token 消耗上限 | 非负整数；仅对非默认业务空间生效 |
| `api_key` | 认证凭证，隐式携带 `workspace_id` 和 `user_id` 上下文 | 单 key 仅归属一个 workspace；不可跨空间复用 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或持有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置业务空间与模型权限。
   - 业务空间管理员：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，仅能管理指定业务空间内的用户与模型策略。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在业务空间维度启用目标模型的调用、调优或部署能力（见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) “业务空间权限管理” 章节），否则下游用户即使拥有对应控制台权限也无法生效。

3. **用户权限分配**  
   - 控制台操作：在业务空间「权限管理」页签中，为 RAM 用户勾选具体功能模块权限（如“模型体验-操作”、“模型调优-操作”）。
   - API 调用：为用户创建 API Key（归属该业务空间），Key 自动继承空间级模型与限流策略。

4. **OpenAPI 显式授权**  
   若需调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI，必须由主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此步骤与业务空间配置无关，但不可或缺。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单地域，跨地域资源（如北京空间的模型）无法被新加坡空间直接调用或管理。
- **默认业务空间限制**：所有模型能力默认开放且不可限流，不支持精细化管控，生产环境应避免使用。
- **API Key 不可迁移**：Key 创建后即锁定所属 workspace 和 user，删除用户或移出空间将导致 Key 失效（重新加入可恢复）。
- **控制台权限 ≠ API 权限**：用户在控制台的页面可见性/操作权限不影响其 API Key 的调用能力；反之亦然。
- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，与百炼权限策略无耦合。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


