# 安全与合规

安全与合规是百炼平台面向生产环境构建的核心保障能力，指通过技术手段与管理机制，确保模型服务在内容安全、数据传输、访问控制、隐私保护、算法备案及监管适配等维度符合国家法规（如《生成式人工智能服务管理暂行办法》）和企业安全策略要求。该能力不是单一功能，而是贯穿模型调用、应用部署、权限治理与可观测性全链路的横切约束。

## 在百炼平台的不同场景中，这个概念如何使用

- **内容安全防护**：在模型输入/输出环节启用 AI 安全护栏（需显式开通并配置请求头），实时拦截涉政、涉黄、广告、暴力等高风险内容，响应返回标准化错误码 `data_inspection_failed`，便于业务快速熔断或降级。
- **数据传输加密**：对敏感 Prompt 或用户数据启用端到端加密（仅 DashScope 原生 Endpoint 支持），使用 RSA 加密 AES 密钥 + AES-CBC 加密请求体，防止公网传输中明文泄露；OpenAI 兼容模式不支持此能力。
- **网络与访问隔离**：  
  - 通用场景：通过 PrivateLink 终端节点将 VPC 流量直连百炼 API，实现私网访问；  
  - 高敏场景：使用「安全存储业务空间」+ 反向终端节点 + MSE 网关 + 私有云资源（OSS/ADB/ES），确保训练数据、知识库、推理结果全程不出私网。
- **权限最小化管控**：以业务空间为单元，通过角色（超级管理员/空间管理员/普通用户）+ 模型级开关（调用/调优/部署）+ RAM 策略（OpenAPI 权限）三层授权，实现“谁在什么空间、能调什么模型、能做什么操作”的精准控制；API Key 权限严格继承自所属空间配置，与用户控制台权限解耦。
- **合规可追溯性**：  
  - 所有上线模型（含千问、万相及第三方模型）均公示算法备案号与大模型备案号，支撑应用上架备案；  
  - 推理日志（需开通）完整记录输入/输出内容，配合模型监控中的 `model_call_failure_count`（含内容安全拦截次数）指标，满足审计与溯源要求；  
  - 临时 API Key（`st-***`）提供短时效凭证，适用于前端/移动端等不可信环境，避免长期密钥暴露。

## 关键参数和配置

| 参数名 | 作用 | 必填条件 | 示例值 | 使用场景 |
|--------|------|----------|--------|----------|
| `X-DashScope-DataInspection` | 启用输入/输出内容安全检测 | 启用护栏时必填 | `{"input":"cip","output":"cip"}` | HTTP Header 中传递，触发 AI 安全护栏 |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥信息 | 启用传输加密时必填 | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | HTTP Header 中传递，用于端到端解密 |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | SDK 层自动处理加解密逻辑 | 使用 SDK 且需加密时必填 | `True` / `true` | 替代手动构造加密请求，推荐生产环境使用 |
| `base_url` | 指向私网终端节点域名 | 使用 PrivateLink 或反向终端节点时必填 | `https://vpc-cn-beijing.dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | 替换默认公网地址，所有请求走私网 |
| `workspace_id` | 显式指定目标业务空间 | 所有跨空间 API 调用必填 | `ws-abc123xyz` | 通过 `X-Workspace-ID` Header 或请求体传入，决定权限上下文与计费归属 |

> ⚠️ 注意：  
> - OpenAI 兼容模式（`/compatible-mode/v1`）**不支持**传输加密与部分安全头（如 `X-DashScope-DataInspection`）；  
> - 「默认业务空间」无法配置模型权限开关与限流，**严禁用于生产环境**；  
> - 安全存储业务空间必须使用**反向终端节点**（非接口终端节点），且仅支持华北2（北京）地域指定可用区。

## 面向开发者，简洁实用

- ✅ **快速启用内容安全**：开通服务 → 控制台完成授权 → 请求头加 `X-DashScope-DataInspection` → 监控 `model_call_failure_count` 指标看拦截效果。  
- ✅ **私网访问两步走**：  
  ① 控制台创建终端节点（PrivateLink 或反向）→ 获取私网域名；  
  ② 将 SDK 的 `base_url` 或请求 URL 替换为该域名（注意路径保持一致）。  
- ✅ **权限调试口诀**：API 调用是否成功？先查 `workspace_id` 是否正确 → 再查该空间是否已开通目标模型调用权限 → 最后确认 RAM 用户是否被授予 `AliyunBailianDataFullAccess`（如需调用 OpenAPI）。  
- ✅ **合规备案就绪检查**：调用前确认模型备案号已在控制台公示；上架应用前完成[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)。  
- 🚫 **避坑提醒**：不要在默认空间跑生产流量；不要用 OpenAI SDK 调用加密接口；不要在临时 API Key 场景执行高权限操作（如模型调优）。

## 关联主题页

- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [more](../api/more.md)
- [application support](../guides/application-support.md)
- [model monitoring](../guides/model-monitoring.md)


