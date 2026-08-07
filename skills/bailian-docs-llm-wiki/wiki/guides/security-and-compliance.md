# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、加密传输、私网访问、AI安全护栏和算法备案信息等机制，满足企业级安全要求与国内监管合规（如《生成式人工智能服务管理暂行办法》）。

## 支持的模型/功能

- **AI安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需主动开通并显式启用，调用时通过 `X-DashScope-DataInspection` 请求头控制开关 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理通道**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，全程保障敏感数据在公网传输中的机密性与完整性，适用于金融、政务等强合规场景 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）以私网方式调用百炼 API，流量不经过公网，显著降低中间人攻击与数据泄露风险 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：面向高敏感数据场景，支持将知识库、审计日志等数据落库至客户自有 VPC 内的 OSS、ADB 或 Elasticsearch，结合 MSE 网关与可用区 VIP 实现网络级隔离与细粒度访问控制 [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)。

> **注意**：文档 8 明确指出美国（弗吉尼亚）地域暂不支持私网访问；而文档 12 中“前提条件”要求专有网络必须位于华北2（北京），且可用区需包含 G/H/L 中任意两个——这与文档 8 所列“阿里云百炼服务所在地域：华北2（北京）、新加坡”一致，但未提及弗吉尼亚是否支持安全存储业务空间。实际部署时请以控制台可用地域为准，弗吉尼亚地域暂不支持安全存储相关能力。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，控制 input/output 审核开关 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥及 IV，用于解密请求体 | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"abc123..."}` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的布尔开关 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `bailian-safe-workspace-oss-access` | 安全存储业务空间绑定 OSS Bucket 的强制标签名称与值 | 标签名：`bailian-safe-workspace-oss-access`，值：`ReadAndWrite` | [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) |

## 使用方式

### 权限与空间管理
- 使用**超级管理员**（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在[全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中创建业务空间、分配模型调用/训练/部署权限，并设置 QPM/TPM 限流。
- **业务空间管理员**可在空间内管理用户控制台页面权限（如“模型体验-操作”），但 API Key 权限由归属空间的模型授权决定，与用户控制台权限解耦 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 加密调用（推荐 SDK 方式）
- Python：设置 `enable_encryption=True`，SDK 自动完成 AES 密钥生成、RSA 加密、`input` 加密及响应解密。
- Java：设置 `.enableEncrypt(true)`，无需手动处理密钥或加解密逻辑。
- HTTP 手动调用需先调用 `/api/v1/public-keys/latest` 获取公钥 ID 与值，再执行混合加密流程 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 私网访问配置
1. 在 VPC 控制台创建**接口终端节点**，服务选择 `com.aliyuncs.dashscope`；
2. 替换 API `base_url` 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/...`）；
3. 对于安全存储业务空间，需额外配置反向终端节点、MSE 网关、可用区 VIP 及后端资源白名单 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **API Key 绑定刚性**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026年3月25日起，华北2（北京）新创建的 API Key 均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用知识库、Prompt 工程等 OpenAPI，需主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储依赖强耦合**：OSS Bucket 若被释放，将导致安全存储业务空间**不可恢复**；ES/ADB 若停止计费或释放，对应模块（知识库、审计日志等）将不可用，需续费或重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体明确**：即使使用百炼提供的已备案模型（如千问、万相），应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)


