# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格遵循阿里云 RAM 体系，需结合系统策略（如 `AliyunBailianFullAccess`）与控制台细粒度配置协同生效。所有权限均绑定至具体地域内的业务空间，**默认业务空间不支持限流与模型级权限管控**，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级操作权限**：支持对单个模型设置调用、调优（训练）、部署三类开关，且可独立配置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。  
- **控制台页面级权限**：通过“权限管理”页签为 RAM 用户分配菜单项（如“模型体验-操作”“批量推理-操作”“模型调优-操作”等），控制其在控制台中可见与可操作的功能范围。  
- **API Key 绑定与继承**：每个 API Key 仅归属一个地域+一个业务空间+一个用户，其可调用模型列表、限流阈值完全继承自所属业务空间的模型权限配置，**不受用户控制台权限影响**（参见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。  
- **OpenAPI 接口权限**：需通过 RAM 控制台为 RAM 用户显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则无法调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等核心 OpenAPI（详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用时指定上下文。必须与 API Key 所属空间一致。 | 从控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取；不同地域空间 ID 不互通 |
| `model_name` | 模型名称（如 `qwen-max`, `qwen2-vl-72b`），用于在业务空间内启用/禁用该模型的调用、调优或部署能力 | 仅对非默认业务空间生效；默认空间所有模型自动启用且不可关闭 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 [Token](../concepts/token.md)/s | 必须由超级管理员在全局管理菜单中设置；业务空间管理员无权修改 |
| `api_key` | 认证凭证，绑定至单一业务空间与用户，自动继承该空间全部模型权限 | 华北2（北京）地域新创建的 API Key 默认归属主账号（自 2026-03-25 起） |

> **注意**：文档中多次提及“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。根据 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中描述，它指各地域预置的、名称为 `default` 的初始空间，该空间不具备模型权限开关能力，生产环境应避免使用。

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 管理跨空间资源。  
   - 业务空间管理员：由超级管理员在控制台“权限管理”页签中为 RAM 用户授予“管理员”角色，仅可管理指定空间内用户、页面、API Key 及模型开关（不含限流）。  

2. **模型权限开通流程**  
   - 超级管理员进入全局管理 → 选择目标业务空间 → 开启所需模型的“调用”“调优”“部署”开关；  
   - 业务空间管理员进入该空间“权限管理” → 为用户分配对应菜单权限（如“模型体验-操作”）；  
   - 若需 API 调用，须为该用户在**同一业务空间内生成 API Key**（参见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。  

3. **OpenAPI 权限开通**  
   - **必须由阿里云主账号**在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略；仅配置控制台权限无效。

## 限制和注意事项

- **地域隔离**：业务空间严格按地域划分，`北京` 地域的 `workspace-a` 与 `新加坡` 地域的同名空间互不关联，权限不可复用。  
- **默认空间限制**：默认业务空间（`default`）不支持任何模型级权限开关与限流配置，所有模型自动启用，**严禁用于生产环境**。  
- **API Key 绑定不可迁移**：API Key 创建后无法转移至其他业务空间或用户，删除后不可恢复；账号被移出空间时 API Key 失效（重新加入后恢复）。  
- **控制台权限 ≠ API 权限**：用户在控制台拥有的页面操作权限（如“模型调优-操作”）**不影响其 API Key 的调用能力**；API 能力完全由业务空间模型开关 + OpenAPI 策略共同决定。  
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，与百炼自身权限无关。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


