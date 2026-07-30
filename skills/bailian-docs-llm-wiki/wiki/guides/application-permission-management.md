# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）的多维度控制，覆盖模型调用/调优/部署、页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略与地域强绑定，且默认业务空间不具备精细化限流与模型管控能力，需通过新建业务空间实现隔离与治理。详细设计与约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型配置调用、调优（训练）、部署三类权限，每类权限可独立开关。  
- **资源维度**：支持模型请求 QPM 限流、[Token](../concepts/token.md) 限流；支持知识库、[Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)等应用能力的 OpenAPI 访问控制。  
- **空间粒度**：所有权限均按“地域 + 业务空间”两级生效，跨地域业务空间完全隔离，互不影响。  
- **用户角色**：  
  - 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户）可跨空间管理模型、用户、API Key 及限流策略；  
  - 业务空间管理员仅可管理所属空间内的用户权限、页面可见性及模型可用性；  
  - 普通用户仅能使用被显式授权的模型与功能，其 API Key 行为严格继承归属空间的模型权限。  
> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际操作中，请以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中北京、新加坡、弗吉尼亚三地全局管理菜单的实际能力为准。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识，调用 API 时必需，可通过控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 | 必填，且必须与 API Key 所属空间一致 |
| `qpm_limit` / `token_limit` | 模型级每分钟请求数与 [Token](../concepts/token.md) 消耗上限，由超级管理员在业务空间模型管理页设置 | 仅对非默认业务空间生效，[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 明确指出默认空间不支持限流 |
| `api_key` | 绑定至单一地域、单一业务空间、单一用户的密钥，其可调用模型范围与限流策略完全继承自归属空间 | 不可迁移，不可复用；华北2（北京）新创建 API Key 默认归属主账号 |

## 使用方式

1. **角色初始化**：  
   - 超级管理员需在 RAM 控制台为 RAM 用户附加 `AliyunBailianFullAccess` 策略；  
   - 业务空间管理员由超级管理员或同级管理员在控制台 **权限管理 → 用户管理** 中授予“管理员”角色。  

2. **模型权限开通**：  
   - 超级管理员进入全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)），为指定业务空间启用目标模型的“调用”“调优”或“部署”开关；  
   - 业务空间管理员在本空间内为用户分配对应控制台权限（如“模型体验-操作”“模型调优-操作”等），详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“常用设置”章节。  

3. **API 调用授权**：  
   - 为用户生成归属该业务空间的 API Key；  
   - 若需调用应用类 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)），主账号须额外在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略——**RAM 用户默认无此权限**。  

## 限制和注意事项

- **地域隔离刚性**：业务空间与地域强绑定，同一业务空间名称在不同地域视为完全独立实体，权限不互通。  
- **默认空间能力缺失**：默认业务空间不支持模型调用/调优/部署的开关控制，也不支持任何限流配置，生产环境务必使用新建业务空间。  
- **API Key 绑定不可变**：一个 API Key 仅归属一个地域、一个业务空间、一个用户，删除用户或将其移出空间将导致 API Key 失效（重新加入可恢复）。  
- **OpenAPI 权限独立授权**：控制台页面权限与 OpenAPI 调用权限分离，即使用户拥有完整控制台权限，若未被授予 `AliyunBailianData*Access` 策略，仍无法调用应用相关 OpenAPI。  
- **账单与预付费权限需单独配置**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需主账号在 RAM 控制台显式授予。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)




