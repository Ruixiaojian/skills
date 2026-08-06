# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、加密传输、私网接入、AI安全护栏及算法备案信息等机制，满足企业级安全要求和中国《生成式人工智能服务管理暂行办法》等法规义务。

## 支持的模型/功能

- **AI安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容合规检测（涉黄、涉政、广告等），需显式启用；具体支持范围及计费详见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理通道**：支持对请求体 `input` 字段进行 AES-RSA 混合加密，防止敏感数据在公网传输中被窃取或篡改；该机制仅适用于 DashScope Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）不经公网直连百炼 API；当前仅华北2（北京）和新加坡地域支持，美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：面向高敏感场景提供独立部署的隔离环境，支持将知识库、审计日志等数据落库至客户自有 VPC 内的 OSS、ADB 或 Elasticsearch，全程不经过公网；需配合反向终端节点、MSE 网关及可用区 IP 配置完成 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 8 与文档 9 存在地域约束差异——文档 8 明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，而文档 9 的前提条件仅要求专有网络地域为“华北2（北京）”，未提及其他地域兼容性。实际部署时应以文档 8 的限制为准，弗吉尼亚地域无法使用私网接入能力。

## 关键参数

| 参数名 | 说明 | 使用场景 | 来源 |
|--------|------|----------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}` | 内容审核 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv` | 传输加密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 封装的加密开关，自动处理加解密逻辑 | SDK 快速接入 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` 替换为终端节点域名 | 如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/...` | 私网调用 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用 AI 安全护栏
- 在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务授权；
- 调用时在请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 响应返回 `400` 及 `data_inspection_failed` 错误码表示拦截成功。

### 2. 启用传输加密
- **SDK 方式（推荐）**：Python 中设置 `enable_encryption=True`，Java 中设置 `.enableEncrypt(true)`，无需手动管理密钥；
- **HTTP 手动方式**：
  - 调用 `/api/v1/public-keys/latest` 获取 RSA 公钥及 `public_key_id` [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)；
  - 生成 AES 密钥与 IV，用 RSA 公钥加密 AES 密钥；
  - 构造 `X-DashScope-EncryptionKey` 请求头并加密 `input` 字段；
- 注意：仅 DashScope Endpoint（`https://dashscope.aliyuncs.com/api/v1`）支持，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持。

### 3. 私网接入百炼 API
- 在 VPC 所在地域创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名；
- 验证调用是否成功且流量不出公网（可通过 VPC 流量监控确认）。

### 4. 配置安全存储业务空间（高密场景）
- 创建类型为“安全存储空间”的业务空间；
- 配置反向终端节点并建立连接；
- 创建 MSE 云原生网关，配置可用区 VIP；
- 授权并绑定客户 VPC 内的 OSS、ADB、Elasticsearch 实例；
- 最终激活业务空间，所有数据路径均限定于客户私网内。

## 限制和注意事项

- **权限粒度**：默认业务空间无法设置模型调用/训练/部署权限及限流，仅自建业务空间支持精细化管控；超级管理员可跨空间管理，但 OpenAPI 接口权限（如知识库、Prompt 工程）必须由阿里云主账号在 RAM 控制台单独授予 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 绑定**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **模型备案责任**：阿里云提供千问、万相等模型的算法备案号与大模型备案号公示，但应用上架合规主体为开发者自身；若应用具备舆论属性或社会动员能力，开发者须自主完成安全评估报告及算法备案，阿里云不替代履行该义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **加密与私网互斥性**：加密调用（`X-DashScope-EncryptionKey`）与私网终端节点可同时启用，但需确保加密后请求仍能被终端节点正确转发；目前无已知冲突，建议在测试环境中验证端到端链路。
- **安全存储依赖项强耦合**：OSS Bucket 若被释放、ADB/ES 若停止计费或被释放，将导致安全存储业务空间完全不可用且**无法恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

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


