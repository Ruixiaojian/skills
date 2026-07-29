# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，支持跨地域、多角色的精细化控制，覆盖模型调用、调优、部署、API Key 使用及控制台页面访问等全链路能力。权限体系分为超级管理员、业务空间管理员和普通用户三级，分别对应全局管控、空间级运营和资源使用角色。所有权限策略均与阿里云 RAM 体系深度集成，需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

百炼权限管理覆盖以下核心能力：

- **模型调用控制**：在业务空间维度开关特定模型（如 Qwen、Qwen-VL、Qwen-Audio）的调用权限，并设置 QPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流阈值。默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）控制**：控制是否允许在该业务空间内对支持调优的模型进行训练、评测、快照管理和部署。默认业务空间不限制调优能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **[模型部署](../concepts/model-deployment.md)控制**：独立开关模型直接部署权限（如部署为 API 服务），与调优后部署权限分离。
- **控制台页面级权限**：按菜单项（如“模型体验”“批量推理”“模型观测”）粒度授权，不影响 API 调用行为。
- **API Key 全生命周期管理**：包括创建、删除、查看、IP 白名单设置；Key 的模型调用范围与限流策略严格继承其归属业务空间的配置 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **OpenAPI 接口权限**：需通过 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则 RAM 用户无法调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台界面为准——若某地域默认空间已开放限流入口，则以界面行为为准。

## 关键参数

| 参数 | 说明 | 来源层级 | 备注 |
|------|------|----------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求中的 `X-Workspace-ID` Header 或 SDK 初始化 | 业务空间级 | 必须与 API Key 所属空间一致，否则请求被拒绝；获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) |
| `qpm_limit` / `tpm_limit` | 模型级限流阈值，单位分别为 QPM 和 TPM | 业务空间 → 模型维度 | 仅对已开通调用权限的模型生效；默认空间无此配置项 |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户的密钥凭证 | 用户级（绑定空间） | 不可跨空间复用；华北2（北京）新创建 Key 默认归属主账号 |
| `ip_whitelist` | API Key 级 IP 白名单（仅华北2支持） | API Key 级 | 配置后仅白名单 IP 可发起请求，空列表表示不限制 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` + `AliyunRAMFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users)授予权限。  
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)），选择目标业务空间 → “模型管理”，启用所需模型并配置限流。

3. **用户控制台权限分配（超级/空间管理员）**  
   在业务空间内进入 **权限管理 → 用户管理**，为 RAM 用户勾选对应功能模块权限（如“模型体验-操作”、“模型调优-操作”等）。

4. **API Key 分配与使用**  
   - 在 **权限管理 → API Key 管理** 中为用户创建 Key（自动绑定当前空间）。  
   - 调用时需在请求 Header 中携带 `Authorization: Bearer <api_key>` 和 `X-Workspace-ID: <workspace_id>`。

5. **OpenAPI 权限开通（仅主账号）**  
   主账号需在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用 `/v1/applications/*`、`/v1/knowledgebases/*` 等路径接口。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一业务空间名称在不同地域代表完全独立的实体。
- **默认空间限制**：所有默认业务空间（如 `default-workspace`）均**不支持**模型调用/调优/部署的细粒度开关与限流配置，必须新建自定义业务空间才能启用这些能力。
- **API Key 绑定不可变**：Key 创建后无法迁移至其他业务空间或用户；若用户被移出空间，其 Key 将失效（重新加入后恢复）。
- **OpenAPI 权限独立于控制台权限**：即使用户拥有完整控制台权限，若未在 RAM 控制台授予 `AliyunBailianData*Access` 策略，仍无法调用 OpenAPI。
- **账单与预付费权限需额外授权**：RAM 用户默认无权查看账单或购买预付费产品，需单独授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` 策略。
- **时间敏感变更**：自 2026年3月25日起，华北2（北京）新创建 API Key 默认归属主账号，不再自动关联 RAM 用户 —— 此规则已在文档中明确，开发集成时需适配鉴权逻辑。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


