# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离及监管备案等关键环节。开发者可通过权限管理、AI安全护栏、端到端加密、私网访问及合规资质材料获取等机制，满足企业级安全要求与国内生成式AI监管规范（如《生成式人工智能服务管理暂行办法》）。所有能力均基于阿里云基础设施的合规底座（如SOC 2）构建，确保数据隐私、传输安全与责任可追溯。

## 支持的模型/功能

- **AI安全护栏服务**：支持对文本和图片类模型的输入输出内容进行实时合规检测（涉黄、涉政、广告等），需显式启用 `X-DashScope-DataInspection` 请求头 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理通道**：支持通过AES-RSA混合加密机制对请求体 `input` 字段加密，防止公网传输中敏感信息泄露；该功能仅适用于 DashScope Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：
  - 普通业务空间：支持通过 PrivateLink 创建**接口终端节点**，实现 VPC 内资源直连百炼 API（限华北2北京、新加坡地域）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - 安全存储业务空间：需配置**反向终端节点** + MSE 网关 + 私有云资源（OSS/ADB/ES），构建完全隔离的数据存储与处理环境 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办算法备案号与大模型备案号，可在控制台或[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)页面查询。

> **注意**：文档 8 与文档 9 描述的私网访问路径存在适用范围差异——前者面向通用模型/API调用，后者专用于**安全存储业务空间**（需商务开通），二者网络架构、终端节点类型（接口 vs 反向）及依赖组件（无MSE vs 必须MSE）均不同，不可混用。

## 关键参数

| 参数名 | 用途 | 来源/说明 |
|--------|------|-----------|
| `X-DashScope-DataInspection` | 启用AI安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，含 `public_key_id`、`encrypt_key`（RSA加密的AES密钥）、`iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | DashScope SDK 开箱即用加密开关 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id`, `public_key` | 通过 `/api/v1/public-keys/latest` 接口获取，用于客户端RSA加密AES密钥 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **权限控制**  
   - 超级管理员通过全局管理菜单（如[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)）统一管控多业务空间模型授权、限流与API Key；  
   - 业务空间管理员在对应空间内配置模型调用/训练/部署权限，并管理用户控制台页面权限；  
   - API Key 继承归属业务空间的模型权限，不受用户控制台权限影响。

2. **启用AI安全护栏**  
   - 在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务授权；  
   - 所有调用请求必须携带 `X-DashScope-DataInspection` 头，否则不触发审核。

3. **加密推理调用**  
   - **SDK方式（推荐）**：Python/Java SDK 设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，自动处理加解密；  
   - **HTTP方式**：  
     a) 调用 `/api/v1/public-keys/latest` 获取公钥；  
     b) 生成AES密钥并加密 `input` 字段；  
     c) 用RSA公钥加密AES密钥，构造 `X-DashScope-EncryptionKey` 头；  
     d) 解密响应体获取明文结果。

4. **私网访问配置**  
   - **普通场景**：在VPC中创建接口终端节点，关联 `com.aliyuncs.dashscope` 服务，替换API Base URL为终端节点域名；  
   - **安全存储场景**：  
     a) 创建反向终端节点并确认连接；  
     b) 配置MSE网关、可用区VIP及交换机网段；  
     c) 授权并绑定OSS/ADB/ES等私有云资源；  
     d) 激活业务空间。

## 限制和注意事项

- **地域限制**：私网访问仅支持华北2（北京）和新加坡地域；美国（弗吉尼亚）地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key 约束**：单个API Key仅归属一个地域内的一个业务空间和一个用户，不可转移；自2026年3月25日起，华北2（北京）新创建的API Key均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性**：仅 DashScope Endpoint 支持加密，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1`）不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储业务空间依赖**：OSS Bucket 若被释放，将导致安全存储空间**不可恢复**；ADB/ES 若停止计费或释放，相关模块（知识库、审计日志等）将不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：使用百炼模型的应用开发者是《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务，阿里云仅提供模型及备案信息支持 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


