# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API 访问及控制台页面级权限。权限体系严格区分超级管理员、业务空间管理员与普通用户职责，确保资源隔离与安全合规。所有权限策略均需结合 RAM 系统策略与百炼控制台配置协同生效，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等模型的控制台与 API 调用权限控制，并可设置 QPM（每分钟请求数）和 Token 限流。
- **模型调优（训练）**：支持在指定业务空间内开通/禁用模型调优权限，包括数据集管理、训练任务提交、评测与快照管理。
- **模型部署**：支持控制是否允许将调优后的模型或基础模型直接部署为服务。
- **应用与数据功能**：包括知识库、[Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)等 OpenAPI 接口调用权限，需额外授予 RAM 策略（如 `AliyunBailianDataFullAccess`），该能力独立于业务空间模型权限，详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **细粒度控制台页面权限**：支持按菜单项（如“模型体验”“批量推理”“模型观测”）为 RAM 用户授权，但**不约束其 API Key 的实际调用行为**。

> **注意**：默认业务空间（Default Workspace）无法配置任何模型级权限限制（调用、调优、部署均全量开放），所有限制策略仅对**非默认业务空间**生效。此设计已在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确说明。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，API 调用必需，可通过控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `model_name` | 模型标识（如 `qwen-max`, `wanx-v1`），用于在业务空间中开启/关闭特定模型的调用、调优或部署权限 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `qpm_limit` / `token_limit` | 每分钟请求上限与 Token 消耗上限，作用于整个业务空间内该模型的所有 API Key 调用 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的凭证；其权限继承自归属业务空间的模型配置，**不受用户控制台页面权限影响** | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一管理空间与权限。  
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通流程**（以非默认空间为例）  
   - 步骤1（超级管理员）：在全局管理菜单 → 「模型管理」中为该业务空间启用目标模型的「调用」「调优」「部署」开关。  
   - 步骤2（空间管理员）：在业务空间内「权限管理」→ 「用户权限」中，为 RAM 用户分配对应功能模块权限（如「模型体验-操作」「模型调优-操作」）。  
   - 步骤3（空间管理员）：在「API-Key 管理」中为该用户创建或分配 API Key —— 此 Key 自动继承步骤1中配置的模型权限与限流值。

3. **OpenAPI 权限补充**  
   若需调用应用、知识库等 OpenAPI，必须由**阿里云主账号**在 RAM 控制台为对应 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。该操作与业务空间模型权限配置无依赖关系，但二者需同时满足方可完整使用。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一名称的业务空间在不同地域（如北京 vs 新加坡）是完全独立的实体。
- **API Key 绑定不可变**：单个 API Key 仅归属一个地域 + 一个业务空间 + 一个 RAM 用户，创建后不可迁移或解绑。
- **默认空间无权限控制**：默认业务空间不支持任何模型级权限开关或限流设置，所有模型默认全开，建议生产环境**禁用默认空间**，改用显式命名的业务空间。
- **控制台权限 ≠ API 权限**：用户在控制台被禁止访问「模型调优」页面，不代表其 API Key 无法调用调优接口；反之亦然。API 行为始终由业务空间模型配置 + RAM OpenAPI 策略共同决定。
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域新创建的 API Key 默认归属主账号，且不支持转移给 RAM 用户（旧 Key 不受影响）。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，不包含在百炼内置策略中。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


