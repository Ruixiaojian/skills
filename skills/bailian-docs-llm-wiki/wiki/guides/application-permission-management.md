# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流策略及账单管理等全场景。权限体系严格区分超级管理员、业务空间管理员与普通用户职责，确保生产环境隔离性与安全合规性。详细设计原则和基础概念请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限控制覆盖以下核心模型能力与功能模块：

- **模型调用**：控制台体验、批量推理、API 调用（含文生文、文生图、语音合成等所有支持模型）  
- **模型调优（训练）**：数据集管理、超参配置、训练任务提交、调优后模型快照管理  
- **模型部署**：将调优完成的模型发布为可调用服务（含在线/离线部署模式）  
- **模型观测**：[Token](../concepts/token.md) 消耗统计、请求量监控、延迟分析（需显式授权）  
- **应用与[知识库](../concepts/knowledge-base.md)**：通过 OpenAPI 访问应用、Prompt 工程、[知识库](../concepts/knowledge-base.md)、[长期记忆](../concepts/memory.md)等功能（需额外 RAM 策略）  
- **账单与预付费**：查看消费明细、导出账单、购买资源包等（依赖 BSS 相关 RAM 权限）  

> **注意**：默认业务空间（如 `default-workspace`）**不支持**任何模型级权限限制（调用、调优、部署均无白名单控制），所有模型默认可用且不可限流；如需精细化管控，必须创建非默认业务空间 —— 此行为在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

## 关键参数

| 参数 | 说明 | 来源上下文 |
|------|------|------------|
| `workspace_id` | 业务空间唯一标识符，用于 API 请求头 `x-bailian-workspace-id` 或 SDK 配置，决定权限作用域 | 参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 常见问题第1条 |
| `qpm_limit` / `token_per_minute_limit` | 模型级每分钟请求数与 [Token](../concepts/token.md) 数限流阈值，由超级管理员在全局管理菜单中为指定业务空间+模型设置 | 见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) “业务空间权限管理”章节 |
| `api_key` | 绑定至单一地域、单一业务空间、单一 RAM 用户的认证凭证；其模型访问范围与限流策略**完全继承归属业务空间的配置**，不受用户控制台权限影响 | 明确定义于 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) “API-Key 权限”小节 |

## 使用方式

### 1. 角色与权限分配
- **超级管理员**：需主账号或已授予 `AliyunBailianFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 添加该策略，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management)｜[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）统一管理所有空间。
- **业务空间管理员**：由超级管理员或同空间管理员，在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色。
- **普通用户**：通过“权限管理 → 用户管理 → 编辑权限”分配细粒度页面与模型能力（如“模型体验-操作”、“模型调优-操作”等）。

### 2. 模型能力开通流程（非默认空间）
1. 超级管理员在全局管理菜单中为该业务空间**启用目标模型的调用/调优/部署权限**；  
2. 业务空间管理员为具体 RAM 用户分配对应控制台操作权限（如“模型调优-操作”）；  
3. 为该用户在**同一业务空间内创建 API Key**（API Key 不跨空间、不跨地域）；  
4. 调用时需携带 `x-bailian-workspace-id: <workspace_id>` 与有效 `Authorization: Bearer <api_key>`。

### 3. OpenAPI 特殊权限
RAM 用户默认**无权调用应用类 OpenAPI**（如 `/v1/apps`, `/v1/knowledgebases`）。必须由主账号在 RAM 控制台为其附加以下任一策略：
- `AliyunBailianDataFullAccess`（全读写）  
- `AliyunBailianDataReadOnlyAccess`（只读）  
该限制独立于业务空间模型权限，属于阿里云 IAM 层面控制 —— 具体策略说明见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) “OpenAPI 接口权限”章节。

## 限制和注意事项

- ✅ **业务空间不可跨地域**：即使名称相同，北京、新加坡、弗吉尼亚的 `my-prod-workspace` 是三个完全独立的空间，权限、模型配置、API Key 均不互通。  
- ⚠️ **API Key 与用户权限解耦**：用户被禁用某项控制台功能（如“模型调优-操作”），**不影响其 API Key 调用已授权模型的能力**；反之亦然。  
- ⚠️ **华北2（北京）地域 API Key 归属变更**：自 2026年3月25日起，新创建的 API Key 默认归属主账号，不再绑定 RAM 用户（旧 Key 不受影响）。  
- ❌ **OpenAPI 权限不可由业务空间管理员配置**：`AliyunBailianData*Access` 等策略**仅主账号可在 RAM 控制台添加**，业务空间管理员无此能力。  
- 📌 **默认空间无权限控制能力**：所有模型调用、调优、部署均自动开放，且无法设置限流；生产环境务必使用自建业务空间。  
- 📌 **账单与预付费权限需单独授权**：`AliyunBSSReadOnlyAccess` / `AliyunBSSOrderAccess` 属于阿里云 BSS 产品策略，与百炼自身权限无关，需在 RAM 控制台独立配置。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


