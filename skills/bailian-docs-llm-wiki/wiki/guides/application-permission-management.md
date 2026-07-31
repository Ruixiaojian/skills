# application permission management

百炼平台的权限管理以“业务空间”为最小单元，支持基于角色（超级管理员、业务空间管理员、普通用户）和资源维度（模型调用、调优、部署、页面访问、API Key）的精细化控制。权限策略同时作用于控制台操作与 OpenAPI 调用，但二者权限体系独立：控制台权限由百炼内部角色配置决定，而 OpenAPI 接口权限需通过 RAM 策略显式授予。所有权限均绑定至特定地域内的业务空间，不跨地域生效。

## 支持的模型/功能

权限管理覆盖以下核心能力：

- **模型调用**：控制指定模型在业务空间内是否可通过控制台或 API 调用，并支持设置 QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流。默认业务空间无法配置此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（如 LoRA 训练）、数据集管理、评测及调优后模型快照发布。默认业务空间对所有支持调优的模型开放该能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **[模型部署](../concepts/model-deployment.md)**：控制是否允许将调优后的模型或第三方模型直接部署为服务端点。默认业务空间对所有支持部署的模型开放该能力。
- **控制台页面级权限**：为 RAM 用户分配具体菜单项（如“模型体验”“批量推理”“模型观测”等）的查看与操作权限，但**不影响其所属 API Key 的调用能力**。
- **API Key 管理**：支持为 RAM 用户授予创建、删除、查看某业务空间下全部 API Key 的权限；单个 API Key 仅归属一个地域+一个业务空间+一个用户，不可迁移 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台界面为准——若北京地域默认空间已提供限流开关，则该描述可能已过时。

## 关键参数

| 参数 | 说明 | 来源层级 | 备注 |
|------|------|----------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求路由与权限校验 | 请求级 | 必须与 API Key 所属空间一致；获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 [Token](../concepts/token.md)/s | 业务空间级 | 由超级管理员在全局管理菜单中配置，普通用户不可见 |
| `api_key` | 认证凭证，隐式继承其归属业务空间的模型权限与限流策略 | 凭证级 | 不受用户控制台权限影响；华北2（北京）新创建 API Key 默认归属主账号 |
| `role` | 用户角色（`super_admin` / `workspace_admin` / `user`） | 账号级 | 决定可访问的管理界面与操作范围，但不直接控制 API 调用能力 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或具备 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略；后续可通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）跨空间授权。
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色。

2. **模型权限开通（必需前置步骤）**  
   由超级管理员在全局管理菜单中为业务空间显式启用目标模型的“调用”“调优”或“部署”开关。未开通则任何用户（含管理员）均无法执行对应操作。

3. **用户控制台权限分配**  
   在业务空间内进入 **权限管理 → 用户管理 → 编辑用户权限**，勾选所需功能模块（如“模型体验-操作”“模型调优-操作”等）。此操作仅影响控制台交互，不影响 API 调用。

4. **API Key 分配与使用**  
   - 在 **权限管理 → API Key 管理** 中为用户创建或分配 Key；
   - 调用 API 时必须携带 `workspace_id` 与 `api_key`，服务端依据 `api_key` 所属空间的模型白名单及限流策略进行鉴权；
   - 若需调用应用、知识库等 OpenAPI，**必须额外在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略**——该权限与百炼控制台角色无关 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定地域，同一逻辑空间在不同地域（如北京 vs 新加坡）视为完全独立实体，权限不互通。
- **默认空间限制**：默认业务空间不支持模型级权限管控（调用/调优/部署均无开关），建议生产环境使用自建业务空间。
- **API Key 生效逻辑**：API Key 的模型权限与限流策略**完全继承自其归属业务空间**，与用户自身的控制台角色无关；用户被移出空间后，其 API Key 将失效（重新加入后恢复）。
- **OpenAPI 权限独立性**：百炼控制台角色（包括超级管理员）**默认无权调用任何 OpenAPI**；必须通过 RAM 显式授予 `AliyunBailianData*Access` 系统策略，否则返回 `403 Forbidden`。
- **账单与预付费权限**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不在百炼控制台内管理。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


