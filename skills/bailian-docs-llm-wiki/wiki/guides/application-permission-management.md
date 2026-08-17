# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流配置及账单管理等全链路场景。权限策略严格遵循阿里云 RAM 体系，需结合系统策略（如 `AliyunBailianFullAccess`）与百炼控制台内细粒度授权协同生效。详细设计原则和基础概念请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心能力维度：

- **模型调用**：控制特定模型在业务空间内是否允许通过控制台或 OpenAPI 调用，并支持独立设置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（Fine-tuning），以及调优后模型快照的管理、评测与部署。
- **模型部署**：控制是否允许将官方模型或调优后的模型直接部署为可调用服务。
- **控制台页面访问**：按菜单项（如“模型体验”“批量推理”“模型调优”“数据管理”等）授予或限制 RAM 用户对控制台功能的可见性与操作权。
- **API-Key 管理**：授权用户创建、查看、删除所属业务空间内的 API Key；Key 的模型调用权限继承自业务空间配置，**不受用户控制台页面权限影响**。
- **OpenAPI 接口权限**：需显式为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 等 RAM 策略，否则默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI —— 此限制独立于业务空间模型权限，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确其是否支持 OpenAPI 权限开通。根据 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“OpenAPI 接口权限”章节，该能力**仅主账号可在 RAM 控制台开通**，与业务空间类型无关，因此默认空间的 RAM 用户仍需主账号授权策略方可调用 OpenAPI。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求中的 `X-Workspace-ID` Header 或请求体字段。必须与 API Key 所属空间一致。 | 不可跨地域复用；可通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 查询 |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的密钥凭证。调用模型时需在 `Authorization: Bearer <api_key>` 中传递。 | 华北2（北京）新创建 Key 默认归属主账号；RAM 用户 Key 在被移出空间后失效（重新加入可恢复） |
| `qpm_limit` / `token_limit` | 模型级限流阈值，由超级管理员在业务空间模型管理页配置，作用于该空间内所有调用者（含 API Key 和控制台用户）。 | 默认空间不支持配置；限流单位为“每分钟”和“每分钟总 [Token](../concepts/token.md) 数” |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`），权限控制粒度精确到此层级。调优后模型使用 `custom:<snapshot_id>` 格式标识。 | 权限需在业务空间维度显式开启，即使模型本身已发布 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或持有 `AliyunBailianFullAccess` 的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 统一纳管多空间。  
   - 业务空间管理员：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，仅可管理指定空间。  

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在目标业务空间中启用具体模型的调用、调优或部署权限（[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“业务空间权限管理”章节详述操作路径）。

3. **用户权限分配**  
   - **控制台权限**：在业务空间「权限管理」→「用户权限」页签中，为 RAM 用户勾选对应功能模块（如“模型体验-操作”“模型调优-操作”）。  
   - **API-Key 权限**：在「权限管理」→「API-Key 管理」页签中，为用户开启「创建/查看/删除 API-Key」权限；随后用户可在自身工作台生成 Key。  
   - **OpenAPI 权限**：主账号需登录 [RAM 控制台](https://ram.console.aliyun.com/users)，为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略。

4. **调用验证**  
   - 控制台调用：用户登录后仅可见已授权的菜单与模型列表。  
   - API 调用：使用所属空间的 `api_key` + 正确 `X-Workspace-ID`，若模型未在该空间启用或超出限流，将返回 `403 Forbidden` 或 `429 Too Many Requests`。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间严格绑定单一地域（如北京、新加坡），**不可跨地域存在**，且不同地域的“默认业务空间”互为独立实体。全局管理菜单需按地域分别访问。
- **默认业务空间特权**：默认空间自动开放全部模型调用、调优、部署能力，且**不支持配置任何限流或禁用策略**。生产环境务必使用自建业务空间替代。
- **API-Key 与用户权限解耦**：API-Key 的模型调用范围、限流策略完全继承自其归属的业务空间配置，**与该 Key 所属 RAM 用户在控制台的页面权限无关**。例如：用户被禁止访问“模型调优”页面，但仍可用其 API Key 提交调优任务（只要空间已开通该模型调优权限）。
- **OpenAPI 权限独立性**：即使某 RAM 用户在业务空间内拥有全部模型调用权限，若未被主账号授予 `AliyunBailianDataFullAccess` 等 RAM 策略，其 API Key 仍无法调用 `/v1/apps/`、`/v1/knowledgebases/` 等应用层接口。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，**不包含在 `AliyunBailianFullAccess` 内**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


