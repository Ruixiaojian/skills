# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API 访问及控制台页面级权限。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，且 API Key 权限与账号控制台权限解耦，需分别配置。所有权限策略均需结合阿里云 RAM 系统策略协同生效。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等模型的控制台与 API 调用权限控制，并可设置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。  
- **模型调优（训练）**：支持在业务空间内开通/关闭特定模型的调优权限，以及调优后模型快照管理、评测与部署权限。  
- **模型部署**：支持控制特定模型是否可在该业务空间直接部署为服务（含推理端点）。  
- **应用与数据功能**：包括 Prompt 工程、知识库、[长期记忆](../concepts/memory.md)、数据集管理等，其 OpenAPI 访问需额外授权（见 [OpenAPI 接口权限](#4adcb2854f9rv)），详见 [权限管理 (raw/application-user-guide/application-permission-management/application-permission-management-overview.md)](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。  
- **细粒度页面控制**：支持为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型评测-操作”等具体控制台菜单权限，但**不控制 API Key 行为**。

> **注意**：默认业务空间（如 `default-workspace`）无法配置任何模型级权限（调用/调优/部署限流均不可设），所有功能默认开放；如需精细化管控，必须创建非默认业务空间 —— 此限制在 [权限管理 (raw/application-user-guide/application-permission-management/application-permission-management-overview.md)](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调，是设计前提而非例外。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识，用于 API 请求头 `x-bailian-workspace-id` 或 SDK 配置，决定权限上下文 | 必须通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取；不同地域的同名空间 ID 不同 |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户，其可用模型与限流策略**完全继承归属业务空间的模型权限配置** | 创建后不可迁移；华北2（北京）新 API Key 默认归属主账号（见 [权限管理 (raw/application-user-guide/application-permission-management/application-permission-management-overview.md)](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)） |
| `qpm_limit` / `token_limit` | 模型级限流参数，由超级管理员在全局管理菜单中为业务空间设置，非 API Key 级别配置 | 仅对非默认业务空间生效；限流作用于该空间下所有 API Key 与控制台调用总和 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略（参考 [设置超级管理员](#h3-jp4-73a-2wi)）。  
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台「权限管理」页签中为 RAM 用户勾选「管理员」权限（见 [权限管理 (raw/application-user-guide/application-permission-management/application-permission-management-overview.md)](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)），为指定业务空间启用目标模型的「调用」「调优」「部署」开关。

3. **用户/Key 权限分配**  
   - **控制台权限**：在业务空间「权限管理」页签中，为 RAM 用户分配对应功能模块（如「模型体验-操作」）的「查看」或「操作」权限。  
   - **API 权限**：为该用户在所属业务空间创建 API Key；若需调用应用/知识库等 OpenAPI，**必须额外在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`**（此为硬性依赖，见 [OpenAPI 接口权限](#4adcb2854f9rv)）。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定地域，`cn-beijing` 的 `prod-workspace` 与 `ap-southeast-1` 的同名空间完全独立，权限、配额、API Key 均不互通。  
- **API Key 与账号权限解耦**：即使某 RAM 用户被禁用「模型体验-操作」权限，其 API Key 仍可调用已授权模型（只要业务空间允许该模型调用）；反之亦然。  
- **OpenAPI 权限独立授权**：所有涉及应用、知识库、Prompt、[长期记忆](../concepts/memory.md)的 OpenAPI（如 `CreateApp`, `CreateIndex`）**默认禁止调用**，必须由主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或只读策略 —— 此限制未在控制台 UI 中提示，易遗漏，务必检查。  
- **默认空间不可控**：默认业务空间（如 `default-workspace`）无法设置任何模型级权限，也不支持添加业务空间管理员；生产环境必须使用自定义业务空间。  
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，与百炼自身权限策略无关。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


