# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的行为均受其归属业务空间的模型权限约束，与用户账号的控制台权限相互独立。

## 支持的模型/功能

权限管理覆盖以下核心能力：

- **模型调用**：控制特定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：控制是否允许在业务空间内进行模型微调（Fine-tuning），以及调优后是否可部署为服务。默认业务空间不限制调优能力 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：控制是否允许直接部署基础模型（如 Qwen 系列）为在线服务。该权限独立于调优权限，需单独开通。
- **控制台页面级权限**：为 RAM 用户分配具体菜单项（如“模型体验”“批量推理”“模型观测”等）的操作权限，但**不影响其 API Key 的调用能力**。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI；必须由阿里云主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时，请确认当前地域是否已启用自定义业务空间（非默认空间）——仅自定义空间支持上述权限开关。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求中的 `X-Workspace-ID` Header 或请求体字段 | 必填；需通过 [获取 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) 获取 |
| `model_name` | 模型标识符（如 `qwen-max`, `qwen-plus`），用于模型级权限配置 | 必须已在业务空间中显式开通调用/调优/部署权限 |
| `qpm_limit` / `token_limit` | 每分钟请求数上限、[Token](../concepts/token.md) 消耗上限 | 仅对已开通调用权限的模型生效；默认业务空间不支持设置 |
| `api_key` | 绑定至单一业务空间与用户的密钥凭证 | 不可跨空间/用户转移；其权限继承自归属业务空间的模型策略，**不受用户控制台权限影响** |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：需具备 `AliyunBailianFullAccess` 策略（主账号或授权 RAM 用户），通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一管理多空间模型、用户、API Key。
- **业务空间管理员**：由超级管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，仅可管理该空间内的用户、页面权限及 API Key。
- **普通用户**：由管理员分配具体功能权限（如“模型体验-操作”“批量推理-操作”），其 API Key 行为由业务空间模型策略决定。

### 2. 模型权限开通流程（以调用为例）
1. 超级管理员在全局管理菜单中，为目标业务空间开通目标模型的「调用 & 限流」权限；
2. 业务空间管理员在该空间「权限管理」页签中，为用户分配「模型体验-操作」等控制台权限；
3. 为用户创建或分配 API Key（归属同一业务空间），该 Key 自动继承空间级模型调用权限。

### 3. OpenAPI 权限开通
RAM 用户需由**阿里云主账号**在 [RAM 控制台](https://ram.console.aliyun.com/users) 显式附加以下任一策略：
- `AliyunBailianDataFullAccess`：全量读写权限；
- `AliyunBailianDataReadOnlyAccess`：仅只读类接口（如 `DescribeFile`, `GetIndexJobStatus`）。

## 限制和注意事项

- **API Key 与用户权限解耦**：用户控制台权限（如能否访问“模型调优”页面）**不影响**其 API Key 的调用能力；API Key 的模型可用性、限流策略完全由其归属业务空间的配置决定。
- **地域隔离**：业务空间严格绑定单一地域，跨地域需分别创建空间并独立配置权限；默认业务空间在各地域均为独立实体。
- **默认空间限制**：所有权限控制（模型调用/调优/部署开关、限流）**仅对自定义业务空间生效**；默认业务空间始终开放全部能力，不可配置限制。
- **主账号特权**：`OpenAPI 接口权限` 和 `账单/预付费管理`（如 `AliyunBSSOrderAccess`）仅支持由阿里云主账号在 RAM 控制台授予；RAM 用户无法自助开通。
- **API Key 生命周期**：RAM 用户被移出业务空间时，其 API Key **临时失效**（重新加入后恢复）；若 RAM 用户被删除，则 API Key **永久失效且不可恢复**。
- **IP 白名单**：仅华北2（北京）地域的 API Key 支持设置 IP 访问白名单，其他地域暂不支持。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


