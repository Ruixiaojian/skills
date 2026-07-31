# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流策略及账单管理等全场景。权限体系严格区分超级管理员、业务空间管理员与普通用户职责，确保生产环境隔离性与安全合规性。详细设计逻辑可参见原始文档 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心模型能力与功能模块：

- **模型调用**：支持对文生文、文生图、语音合成等所有百炼托管模型的调用授权（控制台 & OpenAPI），并可配置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）**：支持对支持调优的模型（如 Qwen 系列）开通训练权限，并管理训练数据集、评测任务、模型快照及部署流程。
- **模型部署**：支持对已调优或原生模型开通直接部署权限，部署后方可通过 API 或应用集成调用。
- **应用与知识库功能**：包括 Prompt 工程、[长期记忆](../concepts/long-term-memory.md)、知识库索引与检索等，需额外通过 RAM 授权 OpenAPI 权限（见下文）。
- **观测与分析**：模型调用/评测 [Token](../concepts/token.md) 消耗、批量推理、模型观测等能力均需显式授权对应控制台权限项。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限限制（调用、调优、部署均全部开放且不可配置限流），生产环境必须使用自建业务空间以实现权限收敛。该约束在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求头 `x-bailian-workspace-id` 或 SDK 配置 | 全局唯一字符串，需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `qpm_limit` | 模型每分钟最大请求数 | ≥ 0；0 表示禁用调用 | 控制台模型管理页配置 |
| `token_limit_per_minute` | 模型每分钟最大 [Token](../concepts/token.md) 消耗量 | ≥ 0；0 表示禁用调用 | 控制台模型管理页配置 |
| `api_key` | 绑定至单一业务空间与用户的认证凭证 | 仅归属一个地域 + 一个业务空间 + 一个 RAM 用户，不可迁移 | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `ip_whitelist` | API Key 的 IP 访问白名单 | 仅华北2（北京）地域支持；格式为 CIDR 或单 IP | [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：需主账号或持有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一管理多空间。
- **业务空间管理员**：由超级管理员或同空间管理员在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选「管理员」角色。
- **普通用户**：由管理员在「权限管理 → 用户管理」中为其分配具体页面权限（如「模型体验-操作」「模型调优-操作」等）。

### 2. 模型权限开通（必需前置步骤）
- 超级管理员需先在全局管理菜单中为**目标业务空间**启用指定模型的：
  - 「允许调用 & 限流」
  - 「允许调优」
  - 「允许部署」  
  （默认业务空间无法执行此操作）

### 3. API 调用准备
- 为用户创建 API Key（在「权限管理 → API Key 管理」中操作），该 Key 自动继承所属业务空间的模型权限与限流配置。
- 若需调用应用/知识库/OpenAPI 功能（如 `CreateApp`, `CreateIndexJob`），**必须由阿里云主账号**在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— RAM 用户默认无此权限。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域（如北京、新加坡），跨地域资源不可共享；同一名称的业务空间在不同地域视为完全独立实体。
- **API Key 绑定刚性**：API Key 创建后不可转移至其他业务空间或用户；其权限完全继承自所属业务空间的模型配置，**不受用户控制台页面权限影响**。
- **OpenAPI 权限特殊性**：所有百炼应用层 OpenAPI（数据、知识库、Prompt、[长期记忆](../concepts/long-term-memory.md)）均**不随业务空间权限自动开通**，必须由主账号单独授权 RAM 用户 `AliyunBailianData*Access` 策略 —— 此为关键安全边界，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **默认空间限制**：默认业务空间无法配置任何模型级权限或限流，**严禁用于生产环境**；生产应采用按环境（dev/test/prod）或业务线划分的独立空间。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授予，不包含在百炼策略中。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


