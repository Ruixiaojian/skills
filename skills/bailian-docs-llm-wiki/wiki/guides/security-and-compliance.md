# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及法规遵从等关键环节。开发者可通过权限控制、私网接入、端到端加密、AI安全护栏及算法备案支持，构建符合国内监管要求（如《生成式人工智能服务管理暂行办法》）和国际标准（如 SOC 2）的生产级 AI 应用。所有安全能力均深度集成于平台 API 与控制台，无需额外部署即可启用。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需显式开通并配置请求头，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 文档详细说明了开通流程与 OpenAI/DashScope SDK 的集成方式。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已依法完成算法备案与大模型备案，备案号及主体信息在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中完整公开，可直接用于应用上架合规材料准备。
- **安全存储业务空间**：面向高敏感数据场景，提供基于私有网络（VPC）的隔离式存储方案，支持对接客户自有 OSS、ADB 和 Elasticsearch 实例，实现数据不出专有网络。该能力依赖完整的私网基础设施链路，包括终端节点、MSE 网关、可用区 IP 配置等，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 及后续配套文档。
- **传输加密**：支持两种加密模式：
  - **HTTPS + 私网终端节点**：通过 PrivateLink 建立 VPC 内网直连，流量全程不经过公网，适用于模型/API 调用场景；
  - **端到端 AES-RSA 混合加密**：对 `input` 字段明文加密，密钥由百炼托管的 RSA 公钥保护，适用于公网传输敏感提示词或对话历史的场景。

> **注意**：文档 10 中明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，但文档 1 中全局管理菜单链接却包含弗吉尼亚控制台入口。实际可用性以文档 10 的声明为准，弗吉尼亚地域当前不支持 PrivateLink 接入。

## 关键参数

| 参数 | 用途 | 来源/说明 |
|------|------|-----------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥及 IV，格式为 JSON 字符串 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 用于 AES 密钥加密的 RSA 公钥标识与值，需通过 `/api/v1/public-keys/latest` 接口获取 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `ep-{id}.privatelink.aliyuncs.com` 或 `vpc-{region}.dashscope.aliyuncs.com` | 私网终端节点服务域名，用于替换 API `base_url` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用内容安全审核
- 开通 AI 安全护栏服务（需主账号操作）；
- 在调用请求的 `headers` 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 错误响应码为 `400`，`code` 字段为 `data_inspection_failed` 或 `DataInspectionFailed`。

### 2. 启用端到端加密（SDK 方式）
- 使用 DashScope Python/Java SDK ≥ v1.14.0 / ≥ v2.12.0；
- 构造 `GenerationParam` 或 `call()` 时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
- SDK 自动完成密钥生成、AES 加密、RSA 封装、请求构造及响应解密，返回明文结果。

### 3. 配置私网访问
- 在目标 VPC 所在地域创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（默认或自定义），替换原 API `base_url`；
- 确保安全组放行 80/443 端口，且终端节点关联的交换机跨至少两个可用区以保障高可用。

### 4. 部署安全存储业务空间
- 创建类型为“安全存储空间”的业务空间；
- 依次完成：配置反向终端节点 → 配置可用区 VIP → 创建 MSE 网关 → 配置 OSS/ADB/ES 资源 → 激活空间；
- 所有资源（OSS Bucket、ADB 实例、ES 集群）必须与业务空间位于同一地域（仅支持华北2 北京），且归属同一 VPC。

## 限制和注意事项

- **权限粒度**：API Key 的权限完全继承自其归属的业务空间，与用户控制台权限无关；一个 API Key 仅绑定单个地域内的单个业务空间与单个用户，不可迁移。
- **地域限制**：
  - 私网终端节点仅支持华北2（北京）和新加坡地域，弗吉尼亚地域不支持（见文档 10）；
  - 安全存储业务空间仅支持华北2（北京），且专有网络需满足特定可用区组合（G/H/L 中任选两个）。
- **模型限流**：默认业务空间无法设置模型调用/训练/部署权限及限流策略；仅非默认业务空间支持精细化管控，且限流单位为“请求数/[Token](../concepts/token.md) 数 per 时间窗口（1–60 秒）”。
- **备案责任**：阿里云提供模型算法备案号及主体信息，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务，[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 明确强调此责任边界。
- **加密兼容性**：端到端 AES-RSA 加密仅适用于 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），**不支持 OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`）**。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)


