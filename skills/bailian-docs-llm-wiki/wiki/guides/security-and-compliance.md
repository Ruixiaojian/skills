# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、存储及合规备案的全链路安全与合规能力，面向企业级开发者支持细粒度权限控制、端到端加密通信、私网隔离访问、AI内容安全护栏及完整算法/模型备案信息。所有能力均基于阿里云基础设施安全体系构建，并通过 SOC 2 审计认证。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容，需显式启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据泄露；该机制仅适用于 DashScope Endpoint（不兼容 OpenAI 兼容模式）[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问通道**：支持通过 PrivateLink 创建接口终端节点（华北2 北京、新加坡地域），实现 VPC 内资源直连百炼 API，流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：面向高敏感场景提供专属业务空间类型，支持对接客户私有网络中的 OSS、ADB、Elasticsearch 等资源，实现数据不出客户 VPC [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 8 明确指出美国（弗吉尼亚）地域暂不支持私网访问，但文档 1 中全局管理菜单链接包含弗吉尼亚入口。该链接仅用于跨地域空间管理，**不表示弗吉尼亚地域支持私网终端节点**，实际私网接入能力仅限华北2（北京）和新加坡。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}`，表示同时检查输入与输出 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv`（初始向量） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | DashScope SDK 中启用自动加解密的开关参数，SDK 自动完成密钥获取、AES 加密、RSA 封装与响应解密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `ep-{id}.privatelink.aliyuncs.com` 或 `vpc-{id}.{region}.dashscope.aliyuncs.com` | 私网终端节点服务域名，需替换默认 `dashscope.aliyuncs.com` 域名后使用 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用 AI 安全护栏
- 首先在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权；
- 在 API 请求 Header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 若触发拦截，将返回 `400` 状态码及 `data_inspection_failed` 错误码。

### 2. 启用传输加密（推荐 SDK 方式）
- Python：调用 `dashscope.Generation.call()` 时传入 `enable_encryption=True`；
- Java：构造 `GenerationParam` 时调用 `.enableEncrypt(true)`；
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、封装并解密，开发者无需手动处理密钥。

### 3. 配置私网访问
- 在 VPC 所在地域创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名；
- **注意**：OpenAI 兼容模式需使用 HTTP 协议（非 HTTPS）的默认服务域名，而 DashScope SDK 可使用 HTTPS 自定义域名。

### 4. 部署安全存储业务空间（高合规要求场景）
- 创建类型为“安全存储空间”的业务空间；
- 配置反向终端节点并建立连接；
- 按顺序完成：配置可用区 IP → 配置 OSS/ADB/ES → 配置 MSE 云原生网关 → 激活空间；
- 所有存储组件必须部署在同一地域（华北2）且与终端节点同 VPC。

## 限制和注意事项

- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性限制**：`X-DashScope-EncryptionKey` 机制**仅适用于 DashScope Endpoint**（如 `https://dashscope.aliyuncs.com/api/v1`），OpenAI 兼容模式（`/compatible-mode/v1`）**不支持**该加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问地域限制**：仅华北2（北京）、新加坡地域支持私网终端节点；美国（弗吉尼亚）、德国（法兰克福）等其他地域控制台链接仅用于空间管理，**不提供私网接入能力**。
- **安全存储业务空间依赖强耦合**：OSS Bucket 若被释放，将导致整个安全存储空间不可用且**无法恢复**，必须重建新空间；ADB/ES 停止计费或释放亦会导致对应模块不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **OpenAPI 权限独立授权**：RAM 用户默认无权调用知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI，需主账号在 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


