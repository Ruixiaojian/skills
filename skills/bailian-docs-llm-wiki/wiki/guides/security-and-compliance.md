# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、加密传输、私网接入、AI安全护栏和算法备案信息等机制，满足生产环境下的数据安全、隐私保护与法规遵从要求。

## 支持的模型/功能

百炼支持多种安全与合规相关功能，适用于不同场景：

- **AI安全护栏服务**：对输入输出内容进行实时合规检测，支持文本和图片类型模型，可识别涉黄、涉政、广告等高风险内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：通过AES-RSA混合加密机制，对请求体中 `input` 字段加密，防止敏感数据在公网传输中被窃听或篡改 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）不经过公网直连百炼 API；同时支持反向终端节点，用于安全存储业务空间与客户私有网络的双向隔离通信 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **安全存储业务空间**：提供专属隔离网络环境，支持对接客户自有 OSS、ADB、ElasticSearch 等私有云组件，实现数据不出域、存储可控 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

> **注意**：文档 8 明确指出美国（弗吉尼亚）地域暂不支持私网访问；而文档 9 和 10 均限定仅支持“华北2（北京）”地域的安全存储业务空间部署。二者地域支持范围不一致，实际部署前请以控制台最新能力为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}`，表示对输入和输出均启用内容检查 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv`（初始向量） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 中启用自动加解密的开关参数，SDK 封装全部密钥管理逻辑 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `ep-{实例ID}.privatelink.aliyuncs.com` 或 `vpc-{实例ID}.{地域ID}.dashscope.aliyuncs.com` | 终端节点服务域名，用于替换默认 API endpoint 实现私网调用 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用 AI 安全护栏
- 在[安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)完成服务授权；
- 调用时在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 响应返回 `400` 及 `data_inspection_failed` 错误码时，表示内容未通过审核。

### 2. 启用传输加密（SDK 方式）
- 安装最新版 DashScope SDK（Java/Python）；
- Python 示例：`Generation.call(..., enable_encryption=True)`；
- Java 示例：`.enableEncrypt(true)`；
- SDK 自动处理 AES 密钥生成、RSA 加密、请求体加密及响应解密，返回明文结果。

### 3. 启用私网访问
- **正向访问（VPC → 百炼）**：在 VPC 中创建接口终端节点，服务选择 `com.aliyuncs.dashscope`，获取终端节点域名后替换 API `base_url`；
- **反向访问（百炼 → 客户私有网络）**：为安全存储业务空间创建反向终端节点，并关联客户 VPC；后续需配置 MSE 网关、可用区 VIP 及 OSS/ADB/ES 等资源白名单与授权 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

### 4. 获取备案信息
- 所有已接入百炼的模型均公示算法备案号与大模型备案号，例如千问对应 `网信算备330110507206401230035号`；
- 开发者可直接引用该信息用于《生成式人工智能服务管理暂行办法》要求的上架备案 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 和 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 限制和注意事项

- **API Key 归属不可迁移**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，无法转移；自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限需主账号授权**：RAM 用户默认无权调用[知识库](../concepts/knowledge-base.md)、Prompt 工程等 OpenAPI，必须由阿里云主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用不兼容 OpenAI 兼容模式**：`X-DashScope-EncryptionKey` 机制仅适用于 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`）**不支持**该加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储业务空间强地域绑定**：当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中至少两个；跨地域或境外 VPC 无法直接接入 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **OSS/ADB/ES 故障影响全局服务**：若配置的 OSS Bucket 被释放、ADB 或 ES 实例停止计费或被释放，将导致安全存储业务空间、[知识库](../concepts/knowledge-base.md)、审计日志等功能完全不可用且**无法恢复**，需重建业务空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


