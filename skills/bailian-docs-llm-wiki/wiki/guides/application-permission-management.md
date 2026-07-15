# application permission management

百炼平台的权限管理以“业务空间”为最小单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略严格遵循阿里云 RAM 体系，需结合控制台操作与 RAM 策略协同配置。详细设计逻辑请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型级管控**：支持对单个模型在指定业务空间内独立设置：
  - 调用权限（含控制台 & API）
  - 调优（训练）权限
  - 部署权限  
- **资源维度隔离**：业务空间按地域物理隔离，同一地域内可创建多个业务空间，但**单个业务空间不能跨地域存在**（详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **角色能力矩阵**：
  | 功能 | 超级管理员 | 业务空间管理员 | 普通用户 |
  |---|---|---|---|
  | 模型调用 & 限流 | ✅ | ❌ | ❌ |
  | 模型调优 | ✅ | ❌ | ❌ |
  | 模型部署 | ✅ | ❌ | ❌ |
  | 用户管理 | ✅ | ✅ | ❌ |
  | 页面权限管理 | ✅ | ✅ | ❌ |
  | API Key 管理 | ✅ | ✅ | ❌ |
  | OpenAPI 接口权限 | ❌（仅主账号可开通） | ❌ | ❌ |

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台实时提示为准，避免依赖默认空间进行生产环境权限隔离 —— 此点与 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“应用于生产环境”章节推荐的按环境划分空间策略存在隐含冲突。

## 关键参数

- **业务空间 ID（Workspace ID）**：API 调用必需参数，用于标识资源归属空间，获取方式见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。
- **API Key 归属约束**：单个 API Key 仅绑定**一个地域 + 一个业务空间 + 一个 RAM 用户**，不可迁移；其可用模型与限流策略完全继承自归属业务空间的配置（[API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **限流粒度**：支持 QPM（每分钟请求数）和 Token 限流两种模式，均在业务空间维度配置。
- **OpenAPI 权限策略**：必须由阿里云主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`，RAM 用户默认无权调用应用、知识库、Prompt 工程等核心 OpenAPI（[OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 使用方式

1. **角色初始化**：
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) / [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一配置。
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置步骤）**：
   - 超级管理员需先在全局管理菜单中为业务空间启用目标模型的**调用、调优或部署权限**（默认业务空间自动全开，但不支持限流）。

3. **用户权限分配**：
   - 控制台操作：在业务空间「权限管理」页签中，为 RAM 用户勾选对应功能模块权限（如「模型体验-操作」「模型调优-操作」「批量推理-操作」等）。
   - API 调用：为用户在目标业务空间创建 API Key，Key 的能力范围由该空间模型权限决定，**不受用户控制台权限影响**。

4. **OpenAPI 授权**：
   - 主账号登录 RAM 控制台 → 找到目标 RAM 用户 → 添加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）系统策略。

## 限制和注意事项

- **地域强绑定**：业务空间与地域一一对应，API Key、模型限流、用户权限均不可跨地域复用。
- **默认空间限制**：默认业务空间无法配置模型调用/调优/部署限制，且不支持限流，**严禁用于生产环境**（[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 明确建议按环境或业务线新建独立空间）。
- **API Key 生命周期**：RAM 用户被移出业务空间后，其 API Key **立即失效**（重新加入后恢复）；若在 RAM 控制台删除该用户，则 Key **永久失效**。
- **账单与预付费权限**：RAM 用户需额外授予 `AliyunBSSReadOnlyAccess`（查看账单）或 `AliyunBSSOrderAccess`（购买预付费）策略，且这些权限作用于**全部阿里云产品**，非百炼专属，授权需谨慎。
- **IP 白名单支持范围**：仅华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


