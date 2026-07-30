# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流策略及账单协同等全场景。权限体系严格区分超级管理员、业务空间管理员与普通用户职责，确保生产环境隔离性与安全合规性。详细设计原则与初始配置说明见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心模型能力与功能模块：

- **模型调用**：支持对文生文、文生图、语音合成等所有百炼托管模型的控制台/API 调用开关及限流（QPM/[Token](../concepts/token.md)）；
- **模型调优（训练）**：支持开启/关闭特定模型在业务空间内的调优（Fine-tuning）、数据集管理、评测与快照发布；
- **模型部署**：支持控制是否允许将调优后模型或第三方模型直接部署为服务；
- **应用与数据功能**：包括 [Prompt 工程](../concepts/prompt-engineering.md)、知识库、[长期记忆](../concepts/long-term-memory.md)、批量推理、应用观测等，但其 OpenAPI 访问需额外授权（见下文）；
- **页面级控制台权限**：可精确控制 RAM 用户在某业务空间内可见/可操作的菜单项（如是否显示“模型调优”、“我的模型”等页签）。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限限制（调用、调优、部署均默认全部开放），也不支持限流配置；如需精细化管控，必须创建并使用非默认业务空间。该限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调。

## 关键参数

| 参数 | 说明 | 权限主体 | 生效范围 |
|------|------|----------|----------|
| `model_call_enabled` | 控制模型是否可在该业务空间被调用（控制台 & API） | 超级管理员 | 业务空间级（全局开关） |
| `qpm_limit`, `token_limit` | 每分钟请求数与 [Token](../concepts/token.md) 总量上限，作用于该空间内所有已启用调用的模型 | 超级管理员 | 业务空间级（模型粒度可配） |
| `fine_tuning_enabled` | 控制模型是否可在该业务空间进行调优与部署 | 超级管理员 | 业务空间级 |
| `console_permission_mask` | 控制台菜单权限掩码（如 `model_experience:op`, `batch_inference:op`） | 超级管理员 / 业务空间管理员 | 用户级（绑定至 RAM 用户） |
| `api_key_scope` | API Key 绑定唯一业务空间 + 用户 + 地域，其模型访问能力与限流策略**完全继承自归属业务空间**，不受用户控制台权限影响 | 超级管理员 / 业务空间管理员 | API Key 级（不可转移） |

所有参数均通过百炼控制台「权限管理」页签或 OpenAPI（需对应权限）配置，具体字段定义与取值范围详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 使用方式

### 1. 角色初始化
- **超级管理员**：主账号或已授予 `AliyunBailianFullAccess` 策略的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 管理全地域业务空间；
- **业务空间管理员**：由超级管理员在目标业务空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色；
- **普通用户**：由管理员分配具体控制台菜单权限与 API Key。

### 2. 模型权限开通流程（必经步骤）
1. 超级管理员在全局管理中为业务空间**启用目标模型的调用/调优/部署权限**；
2. 管理员在该业务空间内为 RAM 用户分配对应控制台权限（如 `model_experience:op`, `model_finetune:op`）；
3. 若需 API 调用，须为该用户在**同一业务空间**创建 API Key —— 其能力自动继承空间级模型开关与限流策略。

> **注意**：API Key 的模型访问能力**仅取决于其归属业务空间的配置**，与用户是否拥有 `model_experience:op` 等控制台权限无关。此行为在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确说明，避免常见误配。

### 3. OpenAPI 特别授权
RAM 用户默认**无权调用**应用、知识库、Prompt、[长期记忆](../concepts/long-term-memory.md)等 OpenAPI。必须由阿里云主账号在 RAM 控制台为其附加以下任一策略：
- `AliyunBailianDataFullAccess`（全读写）  
- `AliyunBailianDataReadOnlyAccess`（只读）

该限制独立于业务空间权限，且仅主账号可配置，详情参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的「OpenAPI 接口权限」章节。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定单一地域（如 `cn-beijing`），无法跨地域复用；不同地域的同名默认空间实为独立实体。
- **默认空间限制**：默认业务空间不可配置模型开关与限流，亦不支持设置业务空间管理员角色。
- **API Key 绑定刚性**：一个 API Key 仅归属一个地域 + 一个业务空间 + 一个用户，创建后不可迁移或解绑；华北2（北京）地域新创建的 API Key 默认归属主账号。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，不包含在 `AliyunBailian*` 系列策略中。
- **生产环境建议**：按环境（dev/test/prod）或业务线划分独立业务空间，并通过超级管理员统一分配配额与限流，避免资源争抢与权限扩散。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


