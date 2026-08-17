# security and compliance

阿里云百炼平台提供多层次安全与合规能力，覆盖模型调用、数据传输、存储、内容审核及监管备案等关键环节。开发者可通过权限控制、加密传输、私网接入、AI安全护栏及算法备案信息复用等机制，满足企业级安全要求与《生成式人工智能服务管理暂行办法》等法规落地需求。

## 支持的模型/功能

- **AI安全护栏服务**：支持对文本和图片类模型（如 `qwen-plus`、`wanxiang`）的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
- **加密传输能力**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，保障敏感数据在公网传输过程中的机密性与完整性，适用于所有 DashScope Endpoint（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持） [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **私网访问通道**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（ECS、容器等）以私网方式调用百炼 API，流量全程不经过公网；同时支持为安全存储业务空间配置反向终端节点，打通百炼服务与客户私有云组件（OSS/ADB/ES）的安全连接 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **模型备案信息公示**：提供千问、万相、DeepSeek、Moonshot 等主流模型的算法备案号与大模型备案号，供开发者用于上架合规申报 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4 中提及“万相”对应两个不同备案主体（阿里巴巴达摩院与通义云启），且备案号 `网信算备330106003156001240091号` 的发放日期为 2024-12-20，明显晚于当前时间（2025年）。该日期应为笔误，实际应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准。

## 关键参数

| 参数名 | 说明 | 使用场景 | 来源 |
|--------|------|----------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 `{"input":"cip","output":"cip"}` | 内容审核 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv`（初始向量） | 传输加密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | DashScope SDK 封装的加密开关，启用后自动完成加解密 | SDK 快速接入 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url`（OpenAI SDK） / `dashscope.base_http_api_url`（DashScope SDK） | 替换为私网终端节点域名（如 `http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/...`）以启用私网调用 | 私网访问 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

- **启用内容审核**：开通 AI 安全护栏服务后，在请求 header 中添加 `X-DashScope-DataInspection`，无需修改请求体结构。触发拦截时返回 `400` 及 `data_inspection_failed` 错误码。  
- **启用传输加密**：  
  - 推荐使用 DashScope SDK（Java/Python），仅需设置 `enable_encryption=True` 或 `enableEncrypt(true)`，SDK 自动处理密钥获取、AES 加密、RSA 加密及响应解密；  
  - 若需手动管理密钥，须先调用 `/api/v1/public-keys/latest` 获取 RSA 公钥及 `public_key_id`，再自行完成 AES 密钥生成、`input` 加密、密钥 RSA 加密等步骤 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。  
- **启用私网访问**：  
  - 对普通 API 调用：在 VPC 内创建接口终端节点（服务为 `com.aliyuncs.dashscope`），获取终端节点域名后替换 SDK 或 HTTP 请求中的 `base_url`；  
  - 对安全存储业务空间：需依次完成反向终端节点创建、可用区 VIP 配置、OSS/ADB/ES 等资源授权与白名单设置，并最终激活业务空间 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  

## 限制和注意事项

- **权限粒度**：API Key 权限完全继承自其归属的业务空间，与用户（RAM 账号）的控制台页面权限无关；且单个 API Key 仅能归属一个地域内的一个业务空间，不可迁移 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
- **地域限制**：私网访问仅支持华北2（北京）和新加坡地域；美国（弗吉尼亚）地域暂不支持私网访问，且其 API Key IP 白名单仅支持 IPv4 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
- **安全存储依赖强耦合**：OSS Bucket 或 ADB/ES 实例若被释放或停止计费，将导致整个安全存储业务空间不可用且无法恢复，必须重建 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。  
- **合规责任主体**：即使使用百炼提供的已备案模型，应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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


