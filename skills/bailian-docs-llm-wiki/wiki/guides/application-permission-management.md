# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）的多维度控制，覆盖模型调用/调优/部署、页面访问、API Key 管理及 OpenAPI 接口调用等核心能力。权限策略与地域强绑定，且默认业务空间不具备精细化限流与模型管控能力，需通过显式创建非默认业务空间实现。详细设计与约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型在指定业务空间内独立配置以下能力：
  - 调用权限（含控制台与 API 双通道）及 QPM/[Token](../concepts/token.md) 限流；
  - 调优（训练）权限及调优后模型部署权限；
  - 直接部署权限（无需先调优）。
- **页面级控制**：支持为 RAM 用户分配细粒度控制台菜单权限（如“模型体验-操作”“批量推理-操作”“模型调优-操作”等），但**不影响其归属 API Key 的调用能力**。
- **API Key 级控制**：单个 API Key 绑定唯一地域 + 唯一业务空间 + 唯一用户，其可调用模型范围与限流策略完全继承自所属业务空间的模型权限配置，[详见原文说明](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，该权限**不随业务空间管理员角色自动赋予**，且仅主账号可添加 —— 此限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

> **注意**：文档中多次出现“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。根据上下文及控制台实际行为，此处指由主账号首次登录时自动创建的、名称为 `default-workspace`（或类似标识）的初始空间；该空间不可删除、不可修改权限模型，所有模型均默认启用。此隐含定义需开发者主动识别，[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 未提供命名规范或查询方法。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求路由与权限校验 | 必须通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu) 获取，不可猜测 |
| `region_id` | 地域标识（如 `cn-beijing`, `ap-southeast-1`, `us-east-1`） | 业务空间与地域强绑定，跨地域调用需使用对应地域的 API Endpoint 和 workspace_id |
| `api_key` | 认证凭证，绑定至单一 `region_id` + `workspace_id` + `user_id` | 不可跨空间/跨地域复用；华北2（北京）新创建的 API Key 默认归属主账号 |
| `qpm_limit` / `token_limit` | 模型级每分钟请求数与 [Token](../concepts/token.md) 总量上限 | 仅对非默认业务空间生效；需超级管理员在全局管理菜单中配置 |

## 使用方式

1. **创建业务空间**：超级管理员通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）新建空间，**避免依赖默认空间**。
2. **配置模型权限**：
   - 超级管理员在全局管理中为该空间开通目标模型的“调用”“调优”“部署”开关；
   - 业务空间管理员在本空间“权限管理”页签中，为 RAM 用户分配对应页面操作权限（如“模型体验-操作”）。
3. **分配 API Key**：
   - 在“权限管理”页签中为 RAM 用户开启“API-Key 管理”权限；
   - 该用户即可在本空间内创建/查看/删除 API Key；Key 的模型访问范围由空间级模型开关决定。
4. **开通 OpenAPI 权限**：**必须由阿里云主账号**在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，[原文明确指出](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 此操作不可由任何管理员角色替代。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格绑定单一地域，跨地域资源不可共享；即使同名空间在不同地域也完全独立。
- **默认空间能力缺失**：`default-workspace` 不支持任何模型级限流与权限开关，生产环境必须使用显式创建的非默认空间。
- **API Key 生命周期依赖用户状态**：RAM 用户被移出业务空间后，其 API Key **临时失效**（重新加入即恢复）；若该 RAM 用户在 RAM 控制台被彻底删除，则 API Key **永久失效且不可恢复**。
- **页面权限 ≠ API 权限**：控制台菜单权限（如“模型调优-操作”）仅控制前端可见性与操作入口，**不影响 API Key 的实际调用能力**；后者完全由业务空间模型开关与 OpenAPI 策略共同决定。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，与百炼业务空间权限无关联。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


