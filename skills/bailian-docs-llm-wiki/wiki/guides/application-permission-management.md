# application permission management

百炼平台的权限管理以“业务空间”为最小单元，支持基于角色（超级管理员、业务空间管理员、普通用户）的多维度控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略与地域强绑定，且默认业务空间不具备限流与模型级细粒度管控能力。详细设计与行为约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级操作权限**：支持对单个模型配置调用、调优（训练）、部署三类能力的开关，仅在**非默认业务空间**中生效；默认业务空间下所有模型均自动开放，不可关闭或限流。
- **角色能力矩阵**：
  - 超级管理员：跨空间管理用户、模型、限流、API Key，并可开通账单与预付费权限；
  - 业务空间管理员：仅限本空间内用户管理、页面权限分配、模型调用/调优/部署授权；
  - 普通用户：仅能使用被显式授予的页面与模型功能，无管理权限。
- **配套功能集成**：权限策略直接影响 AI 安全护栏、模型监控、应用观测等功能的可用性——这些服务需由阿里云主账号在控制台一次性开通，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的说明。

## 关键参数

- `workspace_id`：业务空间唯一标识，调用 API 时必须显式传入（与 `app_id` 配合使用），获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。
- `region_id`：业务空间所属地域（如 `cn-beijing`、`ap-southeast-1`），API Key 和模型权限均严格绑定该地域，**不支持跨地域复用**。
- `qpm_limit` / `tpm_limit`：每分钟请求数（QPM）与 [Token](../concepts/token.md) 数（TPM）限流值，由超级管理员在业务空间维度设置，对所有归属该空间的 API Key 生效。
- `api_key`：单 key 仅归属一个地域+一个业务空间+一个 RAM 用户，其调用能力完全继承业务空间的模型权限，**不受用户控制台页面权限影响**（参见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 使用方式

1. **角色初始化**：
   - 超级管理员：需主账号或具备 `AliyunBailianFullAccess` + `AliyunRAMFullAccess` 的 RAM 用户，在 RAM 控制台授予权限；
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台「权限管理」页签中为 RAM 用户勾选「管理员」角色。

2. **模型权限开通**（必需前置步骤）：
   - 超级管理员需先在全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) | [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)）为业务空间启用目标模型的「调用」「调优」或「部署」开关。

3. **用户级权限分配**：
   - 控制台使用：在「权限管理」页签中为用户分配具体页面权限（如「模型体验-操作」「批量推理-操作」）；
   - API 调用：为用户创建归属该业务空间的 API Key，无需额外策略——其能力由空间模型权限自动决定。

4. **OpenAPI 权限补充**：
   - RAM 用户默认**无权调用应用/知识库/Prompt 工程等 OpenAPI**；
   - 必须由主账号在 RAM 控制台为其附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则 SDK/API 请求将返回 `403 Forbidden`。

> **注意**：文档中提及“华北2（北京）地域新 API Key 默认归属主账号”，但实际策略取决于账号类型与创建上下文；若需 RAM 用户自主管理 API Key，务必确认其已获「API-Key 管理」页面权限（见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 图示）。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间与地域一一绑定，同一逻辑空间无法跨地域存在；不同地域的“默认业务空间”实质为独立实体，权限不互通。
- **默认空间能力缺失**：默认业务空间无法设置模型调用/调优/部署开关，也无法配置 QPM/TPM 限流——生产环境务必创建独立业务空间。
- **API Key 生命周期依赖用户状态**：RAM 用户被移出业务空间后，其 API Key **立即失效**（重新加入可恢复）；若该 RAM 用户在 RAM 控制台被删除，则 API Key **永久失效且不可恢复**。
- **账单与预付费权限独立**：`AliyunBSSReadOnlyAccess` / `AliyunBSSOrderAccess` 属于阿里云通用权限，需在 RAM 控制台单独授予，不随百炼角色自动继承。
- **细粒度页面权限 ≠ API 权限**：用户在控制台被禁止访问「模型调优」页面，不代表其 API Key 无法调用调优接口——后者仅受业务空间模型开关与 OpenAPI 策略控制。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


