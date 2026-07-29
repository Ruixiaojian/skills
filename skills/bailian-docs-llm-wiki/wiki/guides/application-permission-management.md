# application permission management

百炼平台的权限管理以“业务空间”为最小单元，支持跨地域、多角色的精细化控制，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限策略由超级管理员统一规划，业务空间管理员负责本空间内执行，普通用户按分配权限使用资源。所有权限配置均需结合阿里云 RAM 体系协同生效。

## 支持的模型/功能

- **模型级控制**：支持对单个模型设置调用（含控制台 & API）、调优（训练）和直接部署三类开关，且可分别配置 QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流。默认业务空间不支持此类限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **角色分级**：定义三类角色——超级管理员（跨空间全局管控）、业务空间管理员（单空间内用户/模型/页面/Key 管理）、普通用户（仅使用已授权资源）。其中 OpenAPI 接口权限（如应用、知识库、Prompt 工程相关 API）**仅主账号可开通**，RAM 用户需额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **细粒度页面权限**：支持按菜单项（如“模型体验”“批量推理”“模型调优”“我的模型”等）为 RAM 用户分配操作权限，但该控制**仅影响控制台行为，不影响归属该用户的 API Key 调用能力** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识，API 调用必需参数（如 `X-Workspace-ID` Header 或请求体中显式传入） | 每个 API Key 仅绑定一个 `workspace_id`，不可跨空间复用 |
| `model_name` | 模型标识符（如 `qwen-max`, `qwen-vl-plus`），用于在业务空间内启用/禁用特定模型 | 需由超级管理员先在全局为该空间开通模型调用/调优/部署权限 |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 tokens/minute | 仅对非默认业务空间生效；默认空间无限制且不可配置 |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的密钥凭证 | 不可转移；华北2（北京）自 2026-03-25 起新创建的 API Key 默认归属主账号 |

> **注意**：文档中多次提及“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。实际指各地域下系统自动创建的初始空间（如 `default-workspace`），其 ID 通常不可见且无管理入口。开发者应主动创建自定义业务空间以获得完整权限控制能力。

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 创建/管理业务空间，并为 RAM 用户分配策略。
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中授予「管理员」角色。

2. **模型权限开通流程**  
   - 超级管理员 → 全局管理 → 目标业务空间 → 「模型管理」→ 启用目标模型并配置限流。
   - 业务空间管理员 → 控制台「权限管理」→ 为目标 RAM 用户勾选对应模型权限（如「模型体验-操作」「模型调优-操作」等）。

3. **API 调用准备**  
   - 为 RAM 用户在目标业务空间创建 API Key（控制台「权限管理」→ 「API Key 管理」）。
   - 请求时必须携带 `X-Workspace-ID: <workspace_id>` 及有效 `Authorization: Bearer <api_key>`，否则返回 `403 Forbidden`。

## 限制和注意事项

- **地域隔离**：业务空间严格绑定地域，同一逻辑空间在不同地域（北京/新加坡/弗吉尼亚）视为独立实体，权限、模型配置、API Key 均不互通。
- **API Key 生效范围**：API Key 的模型调用权限完全继承自其归属业务空间的模型开关与限流设置，**不受用户控制台页面权限影响**；即用户即使无「模型体验」页面权限，只要 API Key 有效且空间允许调用该模型，API 仍可成功。
- **OpenAPI 权限特殊性**：百炼应用层 OpenAPI（如 `/v1/apps/*/invoke`）默认关闭，必须由**阿里云主账号**在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`，RAM 用户自身无法自助开通 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **账单与预付费权限**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均为阿里云通用策略，非百炼专属，且授权后将影响所有阿里云产品账单视图。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


