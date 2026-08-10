# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、内容审核及监管备案等关键环节。开发者可通过权限隔离、端到端加密、私网访问、AI安全护栏及算法备案支持，满足企业级安全要求与国内监管合规（如《生成式人工智能服务管理暂行办法》）。

## 支持的模型/功能

- **AI安全护栏服务**：支持文本与图片类模型的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容，需显式启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据泄露；该机制仅适用于 DashScope 原生 Endpoint，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)）。
- **私网访问能力**：
  - 通用模型/API：通过 PrivateLink 创建**接口终端节点**，实现 VPC 内流量直连百炼服务（华北2 北京、新加坡地域），避免公网暴露 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - 安全存储业务空间：需配置**反向终端节点** + MSE 网关 + 私有云资源（OSS/ADB/ES），构建双向可控的专有网络隔离环境 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **合规备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办算法备案与大模型备案，信息实时公示于 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 页面。

> **注意**：文档 8 与文档 9 描述的私网接入机制存在定位差异——前者面向通用模型调用（正向访问），后者专用于**安全存储业务空间**（反向接入客户私有资源）。二者不可混用，且安全存储方案强制要求华北2（北京）地域、特定可用区（G/H/L）及 MSE 网关组件，不具备跨地域灵活性。

## 关键参数

| 参数名 | 用途 | 来源文档 | 备注 |
|--------|------|----------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) | 必须在请求 header 中设置，否则不触发审核 |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥及 IV，用于端到端加密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) | 仅 DashScope 原生接口支持；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不识别此 header |
| `public_key_id`, `encrypt_key`, `iv` | 构成 `X-DashScope-EncryptionKey` 的 JSON 字段 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) | 需先调用 `/api/v1/public-keys/latest` 接口获取最新公钥 |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | SDK 层开关，自动完成加解密逻辑 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) | 仅支持 Python 和 Java SDK；其他语言需手动实现 HTTP 加密流程 |

## 使用方式

### 1. 启用内容安全审核
- 开通 AI 安全护栏服务（需主账号操作）；
- 在安全管理页面完成授权；
- **所有调用请求必须携带 `X-DashScope-DataInspection` header**，否则不生效。

### 2. 启用传输加密
- **推荐方式**：使用 DashScope SDK 并设置 `enable_encryption=True`（Python）或 `enableEncrypt(true)`（Java），SDK 自动处理密钥生成、加密、解密；
- **手动方式**：调用 `/api/v1/public-keys/latest` 获取公钥 → 生成 AES 密钥与 IV → 加密 `input` → RSA 加密 AES 密钥 → 构造 `X-DashScope-EncryptionKey` header → 发送请求 → 解密响应体。

### 3. 私网访问模型 API
- 创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 替换 API 请求 base_url 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/...`）；
- 注意：美国（弗吉尼亚）地域暂不支持私网访问。

### 4. 配置安全存储业务空间（高隔离场景）
- 仅限已开通安全存储业务空间的客户；
- 严格按顺序执行：创建反向终端节点 → 配置 MSE 网关 → 配置可用区 VIP → 授权 OSS/ADB/ES → 激活空间；
- 所有资源（VPC、交换机、安全组、网关）必须位于华北2（北京）且满足可用区约束。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理的最小单元，**默认业务空间无法设置模型调用/训练/部署限制**，仅自建业务空间支持精细化控制 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key **均归属主账号**，不再支持 RAM 用户独立创建；RAM 用户的 API Key 在其被移出业务空间后立即失效（重新加入可恢复）。
- **OpenAPI 权限**：RAM 用户默认无权调用知识库、Prompt 工程等 OpenAPI，需主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **加密兼容性**：DashScope SDK 的自动加密功能**不支持自定义密钥**；若需自定义密钥，必须使用 HTTP 手动加密流程。
- **备案责任主体**：阿里云提供模型算法备案号及合作协议模板，但应用/小程序上架所需的全部合规动作（含安全评估、算法备案、内容审核机制建设）由**开发者作为服务提供者独立承担法律责任** [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **SOC 2 合规**：百炼已通过 SOC 2 Type II 审计（安全、可用性、保密性），但**未覆盖处理中的客户数据内容本身**，客户仍需自行确保输入输出内容合法合规。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


