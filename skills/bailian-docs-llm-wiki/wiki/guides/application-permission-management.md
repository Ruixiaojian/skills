# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心能力。权限体系分为超级管理员、业务空间管理员和普通用户三级，各角色能力边界明确，且与阿里云 RAM 体系深度集成。所有权限策略均需结合业务空间上下文生效，**默认业务空间不支持限流与模型级细粒度授权**，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型调用控制**：支持对指定模型（如 Qwen 系列、通义万相等）在业务空间内启用/禁用调用，并配置 QPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流。
- **模型调优（训练）控制**：可授权特定模型在业务空间内进行微调（Fine-tuning），并控制调优后模型的快照管理、评测与部署能力。
- **模型部署控制**：支持限制模型是否可在该业务空间直接部署为服务（含 API 服务与 Web 应用）。
- **控制台页面级权限**：按功能模块（如「模型体验」「批量推理」「模型观测」等）授予或屏蔽 RAM 用户的控制台操作权限。
- **API Key 级权限继承**：API Key 的模型调用范围与限流策略严格继承自其归属的业务空间，**不受用户控制台权限影响**（见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **OpenAPI 接口权限**：需通过 RAM 策略（如 `AliyunBailianDataFullAccess`）显式授予，**不随业务空间权限自动继承**（见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用、调优、部署限制”，但部分旧版界面截图仍显示默认空间存在限流开关。实际行为以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的说明为准——**默认空间始终全量开放，不可配置任何模型级限制**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 调用时指定上下文 | 必填；需通过 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `model_name` | 模型名称（如 `qwen-max`, `wanx-v1`），须与百炼控制台注册名完全一致 | 仅对已开通该模型权限的业务空间有效 |
| `qpm_limit` / `tpm_limit` | 每分钟请求/[Token](../concepts/token.md) 限流值 | 最小值为 1；0 表示禁用该模型调用 |
| `api_key` | 绑定至单一业务空间与 RAM 用户的密钥凭证 | 不可跨空间/用户迁移；华北2（北京）新创建的 API Key 默认归属主账号 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users)授予权限，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)）统一配置。  
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户分配「管理员」角色。

2. **模型权限开通（超级管理员操作）**  
   在全局管理菜单 → 「业务空间管理」→ 选择目标空间 → 「模型管理」中启用具体模型，并设置调用/调优/部署开关。

3. **用户权限分配（超级管理员或业务空间管理员）**  
   - 控制台权限：在业务空间内「权限管理」→ 「用户权限」中勾选对应功能模块（如「模型体验-操作」）。  
   - API Key 权限：在「权限管理」→ 「API Key 管理」中为用户开启「创建/删除/查看」权限，再由该用户自行生成 Key。

4. **OpenAPI 权限开通（仅主账号）**  
   必须由阿里云主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，**业务空间管理员无权操作**（见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单地域，跨地域资源（如北京空间的模型）无法被新加坡空间直接调用或管理。
- **默认空间不可控**：默认业务空间（default workspace）不支持任何模型级限流或开关控制，所有模型默认可用且无配额约束。
- **API Key 绑定不可变**：一个 API Key 仅归属一个地域+一个业务空间+一个 RAM 用户，创建后无法转移或解绑。
- **控制台权限 ≠ API 权限**：用户在控制台被禁止访问「模型调优」页面，不代表其 API Key 不能调用调优接口；反之亦然。二者权限体系独立。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，均需在 RAM 控制台单独授予，不包含在百炼基础权限策略中。
- **失效场景**：RAM 用户被移出业务空间后，其 API Key 将失效（重新加入后恢复）；若该 RAM 用户在 RAM 控制台被删除，则 API Key 永久失效。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


