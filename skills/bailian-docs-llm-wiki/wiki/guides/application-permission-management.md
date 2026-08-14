# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度（模型调用/调优/部署、页面访问、API Key、OpenAPI）的精细化控制能力。权限体系分为超级管理员、业务空间管理员和普通用户三级，支持控制台操作与 API 调用双路径管控，适用于环境隔离、成本分账与生产安全等典型场景。详细设计与行为约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限管理覆盖以下核心能力：

- **模型级管控**：对指定模型启用/禁用调用、调优（训练）、部署权限，并可分别设置 QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流（仅非默认业务空间支持）。
- **页面级管控**：控制 RAM 用户在控制台中可访问的菜单与子功能（如“模型体验”“批量推理”“模型调优”等），但**不影响其所属 API Key 的调用能力**。
- **API Key 管控**：单个 API Key 绑定唯一地域、唯一业务空间、唯一用户；其可调用模型范围与限流策略**严格继承自归属业务空间的模型权限配置**，与用户账号的控制台权限无关。
- **OpenAPI 接口管控**：默认 RAM 用户无权调用应用、知识库、Prompt 工程等 OpenAPI；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的 “OpenAPI 接口权限” 小节）。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际使用中，请以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“业务空间权限管理”章节的最新描述为准——该文档明确指出“即使各个地域的默认业务空间，也是不同的空间”，且所有限制均按业务空间粒度生效，与地域无关。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用时指定上下文；可通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取 | 必填（API 场景） |
| `model_name` | 模型名称（如 `qwen-max`, `qwen-vl`），用于在业务空间内开启/关闭特定模型权限 | 须与百炼平台当前支持模型列表一致 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 [Token](../concepts/token.md)/s；仅对非默认业务空间生效 | 需由超级管理员在全局管理菜单中配置 |
| `api_key` | 绑定至单一业务空间与用户的凭证；其权限范围由归属空间决定，不可跨空间复用 | 创建后不可转移；华北2（北京）新创建 API Key 默认归属主账号 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或具备 `AliyunBailianFullAccess` + `AliyunRAMFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users)授予权限；之后可通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一管理所有空间。  
   - 业务空间管理员：由超级管理员或同空间管理员，在控制台 **权限管理 → 用户管理** 中为 RAM 用户分配“管理员”角色。

2. **模型权限开通**  
   - 超级管理员需先在全局管理菜单中为业务空间启用目标模型的“调用”“调优”或“部署”开关（[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“业务空间权限管理”部分有详细操作截图）。  
   - 后续由业务空间管理员在 **权限管理 → 用户权限** 中为具体用户分配对应功能权限（如“模型调优-操作”“模型部署-操作”）。

3. **API 调用授权**  
   - 为用户创建 API Key（在 **权限管理 → API Key 管理**），该 Key 自动继承业务空间已开通的模型权限与限流策略。  
   - 若需调用 OpenAPI，必须由主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` —— 此步骤与 API Key 创建**完全独立**，且不可由 RAM 用户自行完成（参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的 “OpenAPI 接口权限” 小节）。

## 限制和注意事项

- **默认业务空间无权限限制能力**：所有模型默认可调用、可调优、可部署，且不支持设置限流。如需精细化管控，**必须创建自定义业务空间**。
- **API Key 与用户权限解耦**：用户在控制台的页面访问权限（如能否看到“模型调优”菜单）不影响其 API Key 的实际调用能力；反之亦然。API Key 的行为仅由其归属业务空间的模型权限决定。
- **地域隔离刚性约束**：业务空间严格绑定单一地域，不可跨地域存在；不同地域的同名业务空间（如 `project-prod-workspace`）是完全独立的实体，权限需分别配置。
- **OpenAPI 权限需主账号授权**：`AliyunBailianDataFullAccess` 等策略**仅能由阿里云主账号在 RAM 控制台添加**，超级管理员（RAM 用户）无此能力。
- **账单与预付费权限需额外配置**：RAM 用户默认无权查看账单或购买预付费资源；需单独授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess`（详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 的 “账单查看与预付费权限管理” 章节）。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


