# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限控制、加密传输、私网接入、AI安全护栏和算法备案信息查询等机制，满足企业级安全要求与《生成式人工智能服务管理暂行办法》等法规义务。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需主动开通并显式启用，调用时通过 `X-DashScope-DataInspection` 请求头控制生效范围 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据泄露。DashScope SDK 提供开箱即用的 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）封装 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问通道**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）不经公网直连百炼 API；同时支持反向终端节点模式，为安全存储业务空间构建专属内网通道 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息公示**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办算法备案及大模型备案，并在控制台及文档中公示备案号与主体信息 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4 中提及的“万相”备案主体包含两家公司（阿里巴巴达摩院与通义云启），而文档 3 仅列出单一主体。实际备案应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，建议开发者按文档 4 的查询步骤核验最新状态。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，控制 input/output 审核开关 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥及 IV，用于混合加密调用 | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"abc123..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` / `public_key` | 用于加密 AES 密钥的 RSA 公钥元数据 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| 终端节点服务域名 | 替换默认公网 endpoint，实现私网调用 | `vpc-cn-beijing.dashscope.aliyuncs.com` 或 `ep-xxx.privatelink.aliyuncs.com` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用内容安全审核
- 开通 AI 安全护栏服务（需购买并授权）；
- 在安全管理页面完成内容安全设置授权；
- **所有 API 调用必须显式添加 `X-DashScope-DataInspection` 请求头**，否则不触发审核 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

### 2. 启用传输加密
- **SDK 方式（推荐）**：Python 使用 `enable_encryption=True`，Java 使用 `.enableEncrypt(true)`，SDK 自动处理密钥生成、加解密与请求头注入；
- **HTTP 手动方式**：先调用 `/api/v1/public-keys/latest` 获取公钥，再生成 AES 密钥与 IV，加密 `input` 并构造 `X-DashScope-EncryptionKey` 头；响应体需手动解密 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 3. 私网接入百炼服务
- **正向访问（VPC → 百炼）**：创建接口终端节点，关联 `com.aliyuncs.dashscope` 服务，替换 SDK 或 HTTP 请求中的 base URL；
- **反向访问（百炼 → 客户 VPC）**：适用于安全存储业务空间，需创建反向终端节点，并在业务空间管理页完成连接确认 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

### 4. 获取合规备案材料
- 算法备案号与主体信息见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；
- 上架 C 端应用时，需从[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)按备案编号截图验证，不可直接复用文档中静态表格 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 限制和注意事项

- **API Key 权限隔离**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可跨空间/用户转移；其可调用模型与限流策略完全继承自归属业务空间的模型授权配置，与用户控制台权限无关 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性限制**：AES-RSA 混合加密仅支持 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation`），**不支持 OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`）** [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **地域能力差异**：
  - 私网访问：仅支持华北2（北京）、新加坡地域；美国（弗吉尼亚）地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - 安全存储业务空间：仅支持华北2（北京）地域的专有网络，且可用区限定为 G/H/L [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **数据隐私承诺**：阿里云百炼不会将客户输入数据用于模型训练；所有传输数据默认使用 AES-256 加密；但调用日志与推理结果仍按服务协议存储，开发者需自行评估是否启用加密传输或私网接入以满足更高安全要求 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

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
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


