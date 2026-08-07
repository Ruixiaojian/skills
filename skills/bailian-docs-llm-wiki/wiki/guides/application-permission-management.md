# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持基于角色（超级管理员、业务空间管理员、普通用户）的多维度控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及限流策略等核心场景。权限策略严格绑定地域与业务空间，不跨地域生效，且 API Key 权限继承自归属业务空间而非用户账号权限 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级控制**：支持对单个模型配置调用、调优（训练）、部署三类权限，每类均可独立开启/关闭。默认业务空间无法限制，所有模型均默认开放 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **功能模块粒度授权**：控制台中按“模型体验”“批量推理”“模型调优”“我的模型”“[模型部署](../concepts/model-deployment.md)”“模型评测”“数据管理”“模型观测”等子功能分配操作权限，需显式授予才能使用对应能力。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI；必须由阿里云主账号在 RAM 控制台为其附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，调用 API 时必需传入，用于路由到对应空间的模型与资源 | 每个地域内独立，不可跨地域复用 |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户，其可用模型与限流策略完全继承自归属业务空间 | 不可转移；华北2（北京）新创建的 API Key 默认归属主账号 |
| `qpm_limit` / `tpm_limit` | 模型级每分钟请求数（QPM）与 [Token](../concepts/token.md) 数（TPM）限流值，由超级管理员在业务空间模型管理页设置 | 默认业务空间不支持配置 |
| `ip_whitelist` | 仅华北2（北京）地域支持为 API Key 设置 IP 白名单 | 其他地域暂不支持 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或具备 `AliyunRAMFullAccess` 的 RAM 用户，在 RAM 控制台为指定 RAM 用户授予 `AliyunBailianFullAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。  
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台「权限管理」页签中为 RAM 用户勾选「管理员」角色。

2. **模型权限开通**  
   - 超级管理员需先在全局管理菜单中为业务空间启用目标模型的「调用」「调优」「部署」开关；  
   - 再由超级管理员或业务空间管理员，在该空间「权限管理」中为具体 RAM 用户分配对应功能模块（如「模型调优-操作」）权限。

3. **API 调用准备**  
   - 为 RAM 用户在目标业务空间创建 API Key（通过「权限管理 → API Key 管理」）；  
   - 请求 Header 中携带 `Authorization: Bearer <api_key>`，并显式传入 `x-bailian-workspace-id`；  
   - 模型调用能力与限流策略自动继承自该 API Key 所属业务空间的配置。

> **注意**：用户控制台页面权限（如能否访问「模型调优」页面）与 API 调用权限完全解耦——即使用户无控制台「模型调优-操作」权限，只要其 API Key 所属业务空间已开通模型调优权限，仍可通过 API 发起训练任务。

## 限制和注意事项

- **地域隔离强制约束**：业务空间严格绑定地域，同一业务空间 ID 在不同地域代表不同实体；跨地域资源（如模型、应用、知识库）不可共享，权限亦不互通。
- **默认业务空间不可控**：所有默认业务空间（如 `default-workspace`）均无法配置模型调用/调优/部署开关，也无法设置 QPM/TPM 限流，仅可用于快速试用。
- **API Key 生命周期依赖账号状态**：RAM 用户被移出业务空间后，其 API Key 将失效（重新加入后恢复）；若该 RAM 用户在 RAM 控制台被删除，则 API Key 永久失效，不可恢复。
- **OpenAPI 权限需主账号授权**：`AliyunBailianDataFullAccess` 等策略仅能由阿里云主账号在 RAM 控制台授予，超级管理员（RAM 用户）无权分配此类策略。
- **账单与预付费权限独立管理**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不随百炼权限自动继承。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


