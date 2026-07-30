# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、网络隔离、算法备案及隐私保护等关键环节。开发者可通过权限管理、AI安全护栏、加密传输、私网接入和合规材料获取等功能，满足生产环境下的安全要求与监管合规义务。所有功能均需结合业务空间（Workspace）粒度进行配置，且部分能力（如私网访问、安全存储）依赖特定地域与资源组合。

## 支持的模型/功能

- **AI安全护栏服务**：支持文本与图片类模型的输入输出内容审核，需显式启用 `X-DashScope-DataInspection` 请求头 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对请求体 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据泄露；仅适用于 DashScope Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：通过阿里云 PrivateLink 创建接口终端节点（Endpoint），实现 VPC 内资源直连百炼 API，流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：支持在私有网络中集成 OSS、ADB、ElasticSearch 等云组件，构建端到端隔离的数据存储与处理环境，需配合终端节点、可用区 IP 和 MSE 网关完成部署 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 7 与文档 8 均描述私网接入，但适用场景不同：文档 7 针对「安全存储业务空间」（反向终端节点 + 安全存储组件），文档 8 针对「通用模型/API 调用」（接口终端节点 + 直接访问 DashScope）。二者不可混用，且文档 7 明确限定于华北2（北京）地域，而文档 8 同时支持华北2（北京）和新加坡地域。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}`，表示对输入和输出均执行内容检查 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv`（初始向量） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | DashScope SDK 中启用自动加解密的开关参数，SDK 内部封装密钥管理与加解密逻辑 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| 终端节点服务域名 | 如 `vpc-cn-beijing.dashscope.aliyuncs.com`（自定义）或 `ep-xxx.privatelink.aliyuncs.com`（默认），用于替换 API `base_url` 实现私网调用 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用 AI 安全护栏
- 在控制台 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权；
- 调用时在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 违规请求将返回 `400` 错误及 `data_inspection_failed` code，响应体含具体拦截原因。

### 2. 启用请求体加密
- **SDK 方式（推荐）**：使用 DashScope Python/Java SDK，设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，无需手动管理密钥；
- **HTTP 手动方式**：
  - 调用 `/api/v1/public-keys/latest` 获取最新 RSA 公钥及 `public_key_id` [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)；
  - 生成 AES 密钥与 IV，用 RSA 公钥加密 AES 密钥；
  - 将加密后 `input` Base64 编码值、`X-DashScope-EncryptionKey` 头（含 `public_key_id`、`encrypt_key`、`iv`）一并发送；
  - 响应体中 `output` 字段为 AES 加密结果，需用原始 AES 密钥解密。

### 3. 私网访问百炼 API
- 在 VPC 所在地域创建「接口终端节点」，服务选择 `com.aliyuncs.dashscope`；
- 开启「自定义服务域名」获取 HTTPS 可用域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名，保持其他参数（如 `model`、`messages`、`DASHSCOPE_API_KEY`）不变。

### 4. 配置安全存储业务空间（高隔离场景）
- 创建类型为「安全存储空间」的业务空间；
- 按顺序完成：  
  （1）[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) →  
  （2）[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) →  
  （3）[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)（OSS/ADB/ES）→  
  （4）[配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) →  
  （5）最终激活业务空间。

## 限制和注意事项

- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI，需主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **模型备案责任主体**：阿里云提供模型算法备案号公示，但应用上架合规（如《生成式人工智能服务管理暂行办法》要求）的主体责任由开发者承担，阿里云不替代履行内容审核、安全评估等法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **加密调用兼容性**：仅 DashScope Endpoint（如 `https://dashscope.aliyuncs.com/api/v1`）支持加密，OpenAI 兼容 Endpoint（`/compatible-mode/v1`）不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网地域限制**：美国（弗吉尼亚）地域暂不支持私网访问；安全存储业务空间仅支持华北2（北京）地域，且专有网络需满足可用区 G/H/L 组合要求 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


