# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、权限管控及监管备案等关键环节。开发者可通过细粒度权限管理、端到端加密、私网访问、AI安全护栏及完整算法备案信息，满足企业级安全要求与《生成式人工智能服务管理暂行办法》等法规遵从。所有能力均基于实际生产环境验证，无需额外部署即可集成。

## 支持的模型/功能

- **模型备案支持**：所有百炼接入的大模型（如千问、万相、DeepSeek、Moonshot 等）均已通过国家网信办算法备案及大模型备案，备案号可在控制台及[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)中直接查证。
- **AI 安全护栏**：支持对文本和图片类模型的输入输出内容进行实时合规检测（涉政、涉黄、广告等），需显式启用 `X-DashScope-DataInspection` 请求头 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理**：支持 AES-RSA 混合加密机制，对请求体 `input` 字段及响应结果全程加密，适用于敏感数据场景；DashScope SDK 提供开箱即用的 `enable_encryption` 参数封装 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：
  - 通用模型/API：通过 PrivateLink 创建接口终端节点，实现 VPC 内流量不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - 安全存储业务空间：需配置反向终端节点 + MSE 云原生网关 + 可用区 VIP + 私有云资源（OSS/ADB/ES），构建全链路私网隔离环境 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 8 明确指出美国（弗吉尼亚）地域暂不支持私网访问，但文档 1 中全局管理链接却包含弗吉尼亚控制台入口（`https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management`）。该链接仅用于跨空间用户/模型管理，**不表示弗吉尼亚地域支持私网终端节点**。实际私网接入仅限华北2（北京）和新加坡地域。

## 关键参数

| 参数 | 说明 | 使用位置 | 示例值 |
|------|------|----------|--------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，控制输入/输出检查开关 | HTTP Header | `{"input":"cip","output":"cip"}` |
| `X-DashScope-EncryptionKey` | 传输加密必需头，含 `public_key_id`、`encrypt_key`（RSA 加密的 AES 密钥）、`iv` | HTTP Header | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"aBcDeFgH..."}` |
| `enable_encryption` / `enableEncrypt` | SDK 封装参数，自动处理加解密逻辑 | Python/Java SDK 调用参数 | `True` / `true` |
| `dashscope.base_http_api_url` | DashScope Java SDK 自定义 endpoint（用于私网访问） | Java SDK 初始化 | `"http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1"` |

## 使用方式

### 1. 权限管理（按空间隔离）
- **超级管理员**（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户）：通过全局管理菜单统一配置多业务空间的模型调用/训练/部署权限、API Key 及限流策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **业务空间管理员**：在所属空间内管理用户页面权限、模型授权状态（开关控制调用/训练/部署）及空间级限流（QPM/TPM）。
- **普通用户**：仅能使用被授权的模型与页面，其 API Key 权限完全继承自归属业务空间，**不受账号控制台权限影响**。

### 2. 启用安全护栏
1. 在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权；
2. 所有调用请求必须携带 `X-DashScope-DataInspection` header；
3. 违规请求将返回 `400` 状态码及 `data_inspection_failed` 错误码。

### 3. 启用传输加密（SDK 方式）
- Python：调用 `dashscope.Generation.call(..., enable_encryption=True)`；
- Java：`GenerationParam.builder().enableEncrypt(true).build()`；
- SDK 自动获取公钥、生成 AES 密钥、加解密 input/output，开发者无需手动处理密钥。

### 4. 私网访问（两种模式）
- **通用模型/API**：创建接口终端节点 → 获取服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）→ 替换 SDK 或 HTTP 请求中的 `base_url`；
- **安全存储业务空间**：需严格按顺序执行四步操作：① 创建反向终端节点；② 配置 MSE 网关与路由；③ 配置可用区 VIP；④ 授权并配置 OSS/ADB/ES 私有资源 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 限制和注意事项

- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026年3月25日起，华北2（北京）新创建的 API Key 均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用知识库、Prompt 工程等 OpenAPI，必须由**阿里云主账号**在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性**：`X-DashScope-EncryptionKey` 仅适用于 DashScope Endpoint（`/api/v1/...`），**不支持 OpenAI 兼容模式（`/compatible-mode/v1/...`）** [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储业务空间依赖强耦合**：OSS Bucket 若被释放、ADB/ES 若停止计费或被释放，将导致整个安全存储业务空间**不可用且无法恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案信息时效性**：算法备案号应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，文档中列出的备案号可能随监管更新而变更 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


