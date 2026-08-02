# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）的多维度控制，覆盖模型调用/调优/部署、页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格绑定地域与业务空间，不跨地域生效，且默认业务空间不具备限流与模型级细粒度管控能力。详细设计与约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级操作控制**：支持对单个模型配置调用（含控制台 & API）、调优（训练）、部署三类权限。每类权限均可独立开启/关闭，并可设置 QPM（每分钟请求数）和 Token 限流阈值。
- **页面级访问控制**：通过“权限管理”页签为 RAM 用户分配具体控制台功能权限，如“模型体验-操作”“批量推理-操作”“模型调优-操作”等子项，实现细粒度 UI 功能可见性控制。
- **API Key 绑定与继承**：每个 API Key 严格归属单一地域内的一个业务空间和一个用户；其可用模型范围、限流策略完全继承自所属业务空间的模型权限配置，**不受用户控制台权限影响**（详见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **OpenAPI 接口权限隔离**：RAM 用户默认无权调用应用、[知识库](../concepts/knowledge-base.md)、[Prompt 工程](../concepts/prompt-engineering.md)等核心 OpenAPI；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（参见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用中指定作用域。可通过控制台 URL 或 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取。 | 必填；不同地域的同名空间 ID 不同，不可复用。 |
| `model_id` | 模型唯一标识（如 `qwen-max`），用于在业务空间内启用/禁用该模型的调用、调优或部署能力。 | 需先由超级管理员在全局管理菜单中为该空间开通对应模型权限。 |
| `qpm_limit` / `token_limit` | 模型级限流参数，单位分别为“次/分钟”和“Token/分钟”。仅对非默认业务空间生效。 | 默认业务空间不支持设置（[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 明确说明）。 |
| `api_key` | 认证凭证，绑定至特定 workspace + user + region。其权限范围由所属业务空间的模型开关与限流策略决定。 | 不可跨空间/跨用户迁移；华北2（北京）新创建的 API Key 默认归属主账号。 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已授予 `AliyunBailianFullAccess` 的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置空间与用户。
   - 业务空间管理员：由超级管理员在目标空间的“权限管理”页签中授予“管理员”权限。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为指定业务空间启用目标模型的“调用”“调优”或“部署”开关（默认业务空间无需此步，但无法限流）。

3. **用户权限分配**  
   - 控制台权限：在业务空间“权限管理”页签中，为 RAM 用户勾选对应功能项（如“模型体验-操作”）。
   - API 权限：为用户创建 API Key（需具备“管理 API-Key”权限），该 Key 自动继承业务空间模型策略。

4. **OpenAPI 调用授权**  
   主账号需在 RAM 控制台为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则所有 `/v1/applications/`、`/v1/knowledgebases/` 等路径接口均返回 `403 Forbidden`。

> **注意**：文档中关于“业务空间管理员可管理用户可用页面”的描述与实际控制台能力存在偏差——当前版本中，“用户可用页面管理”功能仅对超级管理员开放，业务空间管理员无法配置页面级可见性（仅能分配功能操作权限）。该矛盾已在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的表格中隐含体现，但未明确警示，开发者应以控制台实际界面为准。

## 限制和注意事项

- **地域强绑定**：业务空间与地域一一对应，同一空间 ID 在不同地域代表不同资源；API Key、模型权限、限流配置均不跨地域共享。
- **默认空间限制**：默认业务空间无法设置模型调用/调优/部署开关，也无法配置 QPM/Token 限流，仅适用于快速试用，**严禁用于生产环境**。
- **API Key 生效逻辑**：API Key 的模型可用性与限流策略**完全继承自业务空间配置**，与用户是否拥有“模型体验-操作”等控制台权限无关。即使用户无控制台权限，只要 API Key 所属空间开通了某模型调用，即可通过 API 调用。
- **OpenAPI 权限独立性**：控制台权限（如“模型调优-操作”）**不自动赋予 OpenAPI 调用能力**；必须额外在 RAM 控制台授予 `AliyunBailianData*Access` 系统策略。
- **账单与预付费权限**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者需单独授权，且权限粒度覆盖全阿里云产品，非百炼专属。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


