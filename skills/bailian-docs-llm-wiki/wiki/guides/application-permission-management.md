# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流配置及账单管理等全链路场景。权限策略严格遵循阿里云 RAM 体系，需结合系统策略（如 `AliyunBailianFullAccess`）与百炼控制台内细粒度授权协同生效。详细设计原则和基础概念请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心能力维度：

- **模型调用**：控制特定模型在业务空间内是否允许通过控制台或 OpenAPI 调用，并支持独立设置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（Fine-tuning），以及调优后模型快照的管理、评测与部署。
- **模型部署**：控制是否允许将官方模型或调优后的模型直接部署为可调用服务。
- **控制台页面访问**：按菜单项（如“模型体验”“批量推理”“模型调优”“我的模型”等）授予或限制 RAM 用户对控制台功能的可见性与操作权。
- **API-Key 管理**：授权用户创建、查看、删除所属业务空间内的 API Key；Key 的模型调用权限继承自业务空间配置，**不受用户控制台权限影响**。
- **OpenAPI 接口权限**：需显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 等 RAM 策略，否则默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等核心 OpenAPI —— 此限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

> **注意**：文档中多次指出“默认业务空间无法设置模型调用/调优/部署限制”，但未说明其是否可被删除或替代。实践中应避免在默认空间承载生产流量，推荐按环境或业务线新建独立空间，该实践建议源自 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的“应用于生产环境”章节。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识符，API 调用必需（如 `X-Workspace-ID` Header 或请求体）。获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。 | 必须与 API Key 所属空间一致，不匹配将返回 `403 Forbidden` |
| `qpm_limit` / `token_limit` | 模型级限流阈值，由超级管理员在全局管理菜单中为指定空间+模型组合配置。普通用户不可见、不可修改。 | 仅对非默认业务空间生效；默认空间限流始终为“不限” |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的凭证。其模型调用范围、限流策略完全继承自归属空间的模型权限配置。 | 不可跨空间/跨用户迁移；华北2（北京）新创建 Key 默认归属主账号（见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)） |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 统一纳管所有空间。
   - 业务空间管理员：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，仅可管理该空间内用户、模型权限及 API Key。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为**目标业务空间**启用具体模型的：
   - ✅ 调用权限（含 QPM/[Token](../concepts/token.md) 限流）
   - ✅ 调优权限（含训练、评测、部署）
   - ✅ 部署权限（独立于调优权限）  
   > 默认业务空间自动开通全部模型权限，但**不可配置限流** —— 此关键限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中重复出现三次，开发者必须规避。

3. **用户权限分配**  
   - 控制台权限：在业务空间「权限管理」→「用户权限」中勾选对应菜单项（如“模型体验-操作”、“模型调优-操作”）。
   - API-Key 权限：需单独勾选「API-Key 管理」权限，否则用户无法创建/查看本空间 Key。

4. **OpenAPI 调用授权**  
   必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— **业务空间管理员无权完成此操作**。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域资源（如模型、API Key、账单）不可共享。同一业务名称在不同地域代表完全独立的空间。
- **默认空间能力受限**：默认业务空间无法配置任何模型级权限开关或限流策略，且不支持设为生产环境 —— 这是强制性设计限制，非配置疏漏。
- **API Key 与用户权限解耦**：用户控制台权限（如禁用“模型调优”菜单）**不影响**其 API Key 的调用能力；Key 的能力仅取决于归属空间的模型开通状态与限流配置。
- **OpenAPI 权限独立于百炼控制台权限**：即使用户拥有完整控制台权限，若未在 RAM 控制台授予 `AliyunBailianData*Access` 策略，所有应用类 OpenAPI 均返回 `403`。
- **账单与预付费权限需额外授权**：RAM 用户默认无权查看账单或购买预付费资源，必须单独授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` —— 具体页面级权限粒度详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的表格说明。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


