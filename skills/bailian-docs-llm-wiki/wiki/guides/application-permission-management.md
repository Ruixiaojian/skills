# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）和资源维度（模型调用、调优、部署、页面访问、API Key、OpenAPI）的精细化控制。权限策略与地域强绑定，同一业务空间不可跨地域存在，且默认业务空间不具备模型级限流与功能开关能力。所有权限配置均需通过百炼控制台或 RAM 系统策略协同生效。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用控制**：在指定业务空间内启用/禁用特定模型（如 Qwen 系列、通义万相等），并设置 QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流；该能力[仅对非默认业务空间生效](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优与部署控制**：允许/禁止在业务空间内进行模型微调（SFT/RLHF）、调优后模型快照管理、模型部署及服务发布；同样[不适用于默认业务空间](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **控制台页面级权限**：为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型观测-操作”等细粒度菜单权限，控制其在控制台可访问的功能模块。
- **API Key 管理与绑定**：每个 API Key 严格归属单一地域、单一业务空间、单一用户，其调用能力与所属空间的模型权限完全一致，不受用户控制台权限影响。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI，需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 —— 此限制已在[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)中明确说明。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。根据实际控制台行为，通常指首次开通百炼服务时自动创建的、名称含 `default` 或未显式命名的初始空间；建议始终新建独立业务空间用于生产，避免依赖默认空间行为。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用中指定作用域；可通过[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)文档获取 | 必填（除默认空间外） |
| `region_id` | 地域 ID（如 `cn-beijing`），与业务空间强绑定；API Key 和权限配置均按地域隔离 | 必填 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 tokens/minute；由超级管理员在业务空间模型管理页设置 | 仅对非默认空间有效 |
| `api_key` | 绑定至单个 workspace + region + user 的凭证；其权限继承自所属空间的模型开关与限流策略，**不继承用户控制台权限** | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 明确指出该关键特性 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已授予 `AliyunBailianFullAccess` 的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置。
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通流程**  
   - 超级管理员 → 进入目标地域的全局管理 → 选择业务空间 → 「模型管理」→ 开启目标模型的「调用」「调优」「部署」开关。
   - 业务空间管理员 → 进入该空间「权限管理」→ 为用户分配对应功能权限（如「模型调优-操作」）。

3. **API 调用准备**  
   - 确保 API Key 所属业务空间已开通目标模型权限；
   - 请求 Header 中携带 `Authorization: Bearer <api_key>`，并在 Query 或 Body 中显式传入 `workspace_id` 与 `region_id`；
   - 若调用 OpenAPI（如 `/v1/apps/{app_id}/invoke`），还需确保 RAM 用户已被授予 `AliyunBailianDataFullAccess`。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间与地域一一绑定，跨地域资源不可共享；例如 `cn-beijing` 下的 `prod-workspace` 与 `ap-southeast-1` 下同名空间完全独立。
- **默认空间能力缺失**：所有模型级权限控制（调用开关、限流、调优开关）均[不适用于默认业务空间](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)，生产环境必须使用显式创建的业务空间。
- **API Key 不可迁移**：一个 API Key 创建后即锁定其归属的地域、业务空间与用户，无法转移或复用；删除用户将导致其 API Key 失效（重新加入空间可恢复）。
- **OpenAPI 权限独立于控制台**：即使用户在控制台拥有完整模型权限，若未被授予 `AliyunBailianDataFullAccess`，仍无法调用任何应用类 OpenAPI —— 此为常见权限误配根源。
- **账单与预付费权限需额外授权**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不包含在百炼基础权限策略中。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


