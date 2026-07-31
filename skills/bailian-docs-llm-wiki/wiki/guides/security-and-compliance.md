# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖权限隔离、数据传输加密、内容安全防护、模型备案支持及私有化部署等关键维度。所有功能均基于阿里云统一安全体系构建，满足企业级生产环境对数据主权、审计合规和网络隔离的严苛要求。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
- **加密传输能力**：支持对 `input` 字段进行 AES-RSA 混合加密，防止敏感数据在公网传输中被窃听或篡改 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **私网访问通道**：通过 PrivateLink 终端节点实现 VPC 内流量直连百炼 API，完全规避公网暴露 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
- **安全存储业务空间**：支持反向终端节点 + MSE 网关 + 专有云资源（OSS/ADB/ES）的全链路私有化数据存储方案，适用于金融、政务等强合规场景 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **模型备案信息**：公示千问、万相、智谱、DeepSeek 等全部接入模型的算法备案号与大模型备案号，便于客户完成《生成式人工智能服务管理暂行办法》要求的上架合规动作 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 3 和文档 5 均列出千问模型备案号，但文档 3 中备案主体为“阿里巴巴达摩院(杭州)科技有限公司”，而文档 5 中未明确主体；实际备案信息应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，建议开发者自行核验。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥 | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | SDK 级加密开关 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` (OpenAI SDK) / `dashscope.base_http_api_url` (DashScope SDK) | 替换为私网终端节点域名 | `https://vpc-cn-beijing.dashscope.aliyuncs.com/...` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用内容安全护栏
- 开通 AI 安全护栏服务（需主账号操作）；
- 在请求 Header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 错误响应码为 `400`，`code` 字段为 `data_inspection_failed` 或 `DataInspectionFailed`。

### 2. 启用传输加密
- 调用 `/api/v1/public-keys/latest` 接口获取最新 `public_key_id` 和 RSA 公钥；
- 生成 AES 密钥（推荐 256 位）和 IV，用 RSA 公钥加密 AES 密钥；
- 将加密后的 `input` 和 `X-DashScope-EncryptionKey` 请求头一并发送；
- **或直接使用 DashScope SDK**：设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动处理加解密。

### 3. 私网访问百炼 API
- 在 VPC 中创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名；
- **注意**：美国（弗吉尼亚）地域暂不支持私网访问。

### 4. 配置安全存储业务空间（私有化部署）
- 创建类型为“安全存储空间”的业务空间；
- 配置反向终端节点，关联 VPC 及交换机；
- 部署 MSE 云原生网关，配置路由指向私有云资源（OSS/ADB/ES）；
- 为 OSS Bucket 添加标签 `bailian-safe-workspace-oss-access=ReadAndWrite`，并配置 CORS 规则；
- 将交换机网段加入 ES 白名单，确保网络连通性。

## 限制和注意事项

- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可跨空间或跨用户转移；自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
- **加密调用兼容性**：AES-RSA 加密机制**仅适用于 DashScope Endpoint**（如 `https://dashscope.aliyuncs.com/api/v1`），OpenAI 兼容模式（`/compatible-mode/v1`）**不支持**该加密机制 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **安全存储业务空间地域限制**：当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **备案责任主体**：阿里云提供模型备案信息及合作协议模板，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。  
- **数据隐私承诺**：阿里云百炼**绝不会将客户数据用于模型训练**，所有传输数据默认经 AES-256 加密；但根据协议，调用日志等元数据将被存储用于运维与审计 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


