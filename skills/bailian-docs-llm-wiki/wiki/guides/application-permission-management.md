# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的行为均继承其归属业务空间的模型权限策略，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等模型的控制台体验与 OpenAPI 调用；需在业务空间级开通模型调用权限，并为用户分配 `模型体验-操作` 等控制台权限或分配有效 API Key。  
- **模型调优（训练）**：支持 LoRA、全参微调等调优方式，需业务空间级开通调优权限，并为用户分配 `模型调优-操作`、`数据管理-操作`、`我的模型-操作` 等权限（控制台）或使用具备该空间权限的 API Key（API）。  
- **模型部署**：调优完成后可部署为服务化模型，需业务空间级开通部署权限及用户侧 `模型部署-操作` 权限。  
- **应用与知识库相关功能**：如 [Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)、知识库索引等 OpenAPI 接口默认关闭，需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 详见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。  
- **账单与预付费管理**：RAM 用户默认无权查看账单或购买预付费资源，需主账号额外授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` —— 具体权限映射见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“账单查看与预付费权限管理”章节。

## 关键参数

| 参数 | 说明 | 是否必需 | 备注 |
|------|------|----------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求路由与权限校验 | 是 | 获取方式见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 常见问题第1条 |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户的认证凭证 | 是（API 场景） | 不可跨空间/跨用户复用；状态随用户归属关系变化（如移出空间后失效） |
| `model_id` | 模型唯一标识（如 `qwen-max`），须已在目标业务空间显式启用调用/调优/部署权限 | 是（模型操作场景） | 默认业务空间不支持配置权限，所有模型自动可用 |
| `qpm_limit` / `tpm_limit` | 每分钟请求数 / 每分钟 [Token](../concepts/token.md) 数限流值 | 否（但强烈建议设置） | 由超级管理员在业务空间维度统一配置，API Key 自动继承 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）创建业务空间并配置模型权限。  
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色。  

2. **模型权限开通**  
   - 超级管理员进入目标业务空间的「模型管理」页，勾选允许调用/调优/部署的模型，并设置 QPM/TPM 限流值。  
   - *注意*：默认业务空间无法配置上述限制，所有模型自动开放且不限流。  

3. **用户权限分配**  
   - 控制台使用：在「权限管理」→「用户权限」中为 RAM 用户分配具体页面权限（如 `模型体验-操作`、`模型调优-操作`）。  
   - API 使用：为用户在对应业务空间生成 API Key（需已授予 `API-Key 管理` 权限），该 Key 自动继承空间级模型权限。  

4. **OpenAPI 特殊授权**  
   > **注意**：应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)）权限**不通过百炼控制台配置**，必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此要求与常规模型调用权限机制分离，开发者务必单独处理。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一业务空间名称在不同地域代表完全独立的实体。  
- **API Key 绑定刚性**：一个 API Key 仅归属一个地域 + 一个业务空间 + 一个 RAM 用户，不可迁移、不可复用；华北2（北京）地域自 2026年3月25日起，新创建 API Key 默认归属主账号。  
- **控制台权限 ≠ API 权限**：用户在控制台的页面可见性（如能否看到「模型调优」菜单）与其 API 调用能力完全解耦；API 调用仅取决于 API Key 所属业务空间的模型权限配置。  
- **默认空间例外**：默认业务空间不支持任何模型级权限配置（调用/调优/部署均自动开启且不限流），生产环境应避免使用，默认空间仅适用于快速试用。  
- **OpenAPI 权限特殊性**：`AliyunBailianData*Access` 系列策略需主账号在 RAM 控制台手动绑定，百炼控制台内任何操作均无法开通此能力 —— 这一设计与文档中其他权限模型存在显著差异，需特别注意。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


