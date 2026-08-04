# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，支持对模型调用、调优、部署及控制台页面访问等维度进行授权与限流。权限体系由超级管理员、业务空间管理员和普通用户三级角色构成，API Key 权限与归属业务空间强绑定，不随用户控制台权限变化而动态调整。详细设计可参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型调用**：支持在控制台和 OpenAPI 中调用文生文、文生图、语音合成等模型；需业务空间显式开通模型调用权限（默认业务空间除外）。
- **模型调优（训练）**：支持通过控制台或 API 对指定模型进行微调，并管理数据集、评测、快照与部署；需业务空间开通调优权限。
- **模型部署**：支持将调优后的模型一键部署为服务端点；部署权限独立于调用和调优权限。
- **应用与知识库功能**：包括 [Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)、知识库构建等，其 OpenAPI 调用需额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **细粒度页面控制**：支持按菜单项（如“模型体验”“批量推理”“模型评测”）为 RAM 用户分配控制台操作权限，但不影响其 API Key 的实际调用能力。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该空间是否支持创建子业务空间或继承主账号配额。实践中应避免在默认空间承载生产流量，推荐参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的“应用于生产环境”章节，按环境或业务线新建独立业务空间。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求头 `x-bailian-workspace-id` 和 SDK 初始化 | 必填；需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`），用于模型调用与限流配置 | 需已在该业务空间开通调用/调优权限 |
| `qpm_limit` / `tpm_limit` | 每分钟请求数（QPM）与 [Token](../concepts/token.md) 数（TPM）限流阈值 | 整数 ≥ 0；设为 `0` 表示禁止调用 |
| `api_key` | 归属单个地域+单个业务空间+单个用户的密钥凭证 | 不可跨空间/跨用户复用；华北2（北京）新创建的 API Key 默认归属主账号 |

## 使用方式

1. **角色配置**  
   - 超级管理员：通过 RAM 控制台为 RAM 用户附加 `AliyunBailianFullAccess` 策略，并使用全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) \| [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) \| [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一管理所有空间。  
   - 业务空间管理员：在百炼控制台 → **权限管理** 页签中为 RAM 用户开启“管理员”权限（见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

2. **模型权限开通**  
   - 超级管理员在全局管理菜单中为指定业务空间启用目标模型的「调用」「调优」「部署」开关，并配置 QPM/TPM 限流值。

3. **用户控制台权限分配**  
   - 在业务空间内进入 **权限管理 → 用户权限**，勾选对应功能模块（如“模型体验-操作”“模型调优-操作”），该设置仅影响控制台页面可见性与操作按钮可用性。

4. **API 调用授权**  
   - 为用户在目标业务空间创建 API Key（需具备“API-Key 管理”权限）；调用时必须携带 `x-bailian-workspace-id` 请求头与有效 `api_key`，权限策略以该 Key 所属业务空间的模型配置为准。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一业务空间名称在不同地域代表完全独立的实体。
- **默认空间限制**：默认业务空间不支持模型级权限开关与限流配置，所有模型默认全量开放，**严禁用于生产环境**。
- **API Key 绑定刚性**：API Key 一旦创建即锁定所属地域、业务空间与用户，不可迁移；删除用户或将其移出业务空间将导致其 API Key 失效（重新加入后可恢复）。
- **OpenAPI 权限独立**：应用类 OpenAPI（数据、知识库、Prompt 等）默认关闭，必须由阿里云主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`，超级管理员的 `AliyunBailianFullAccess` **不包含**此类权限（此为关键权限分离设计，非文档矛盾）。
- **账单与预付费权限**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，与百炼自身权限策略无关。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


