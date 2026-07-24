# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制能力。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间级管理和资源使用权限。所有 API Key 的权限继承自其归属业务空间，与用户控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对指定模型（如 Qwen 系列、通义万相等）开启/关闭控制台与 OpenAPI 调用，并可配置 QPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流。默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持在业务空间内启用/禁用特定模型的调优能力（含数据准备、训练、评测），并控制调优后模型的部署权限。默认业务空间默认开放全部调优能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持独立开关某模型在该空间内的直接部署权限（即无需调优即可部署的预置模型），部署后方可通过 API 或控制台调用。
- **控制台页面级权限**：支持按菜单项（如“模型体验”“批量推理”“模型调优”“我的模型”等）为 RAM 用户授予或收回操作权限，但**不影响其 API Key 的调用能力**。
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则 RAM 用户无法调用应用、知识库、Prompt 工程等核心 OpenAPI [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识符，API 调用必需 | 由百炼分配，可通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 查询 |
| `model_name` | 模型标识符（如 `qwen-max`, `wanx-v1`） | 必须已在该业务空间中显式启用调用/调优/部署权限 |
| `qpm_limit` / `tpm_limit` | 模型级限流阈值 | 整数，≥0；设为 0 表示禁用该模型调用 |
| `api_key` | 绑定至单个业务空间与用户的凭证 | 不可跨空间/跨用户迁移；华北2（北京）新创建的 API Key 默认归属主账号 |

## 使用方式

1. **角色配置**  
   - 超级管理员：需主账号或持有 `AliyunBailianFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予策略，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)）统一管理。  
   - 业务空间管理员：由超级管理员或同空间管理员在百炼控制台「权限管理」页签中为 RAM 用户分配「管理员」角色。

2. **模型权限开通**  
   - 超级管理员需先在全局管理中为业务空间启用目标模型的「调用」「调优」「部署」开关；  
   - 再由超级管理员或业务空间管理员在该空间「权限管理」中为具体 RAM 用户分配对应菜单操作权限（如「模型调优-操作」）。

3. **API 调用授权**  
   - 为 RAM 用户在目标业务空间创建 API Key（控制台「权限管理」→「API Key 管理」）；  
   - 该 API Key 自动继承业务空间级模型权限与限流策略，**无需额外配置模型白名单**；  
   - 若需调用 OpenAPI，必须另行在 RAM 控制台绑定 `AliyunBailianDataFullAccess` 或只读策略。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确其是否支持限流配置。实际行为以控制台界面为准——若默认空间无对应开关，则限流不可配。建议生产环境始终使用显式创建的业务空间。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域资源不可共享，亦不可跨地域授权 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **API Key 绑定刚性**：一个 API Key 仅归属一个地域、一个业务空间、一个用户，删除用户或将其移出空间将导致其 API Key 失效（重新加入可恢复）。
- **OpenAPI 权限独立**：控制台页面权限（如「模型调优-操作」）**完全不赋予 OpenAPI 调用能力**，必须通过 RAM 策略显式授权。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，与百炼权限无关。
- **主账号特权**：AI 安全护栏、模型监控、应用观测等功能的首次开通**必须使用阿里云主账号**操作，RAM 用户无权执行。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


