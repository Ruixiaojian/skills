# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、AI安全护栏、私网接入、端到端加密等机制，满足企业级数据安全、等保要求及《生成式人工智能服务管理暂行办法》等法规义务。所有功能均基于阿里云统一安全底座，支持SOC 2审计认证，并默认禁用客户数据用于模型训练。

## 支持的模型/功能

- **AI安全护栏**：支持文本与图片类模型（如`qwen-plus`、`wanxiang`）的输入输出内容审核，需显式启用 `X-DashScope-DataInspection` 请求头 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理**：支持对请求体中 `input` 字段进行AES-RSA混合加密，仅适用于DashScope原生Endpoint（不支持OpenAI兼容模式），需配合公钥接口获取最新密钥 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **私网访问**：支持通过PrivateLink终端节点实现VPC内私网调用百炼API，当前覆盖华北2（北京）和新加坡地域，美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储空间**：面向高敏感场景提供独立业务空间类型，支持配置OSS、ADB、ElasticSearch等私有网络资源，并强制要求终端节点+可用区IP+MSE网关三级网络隔离 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用AI安全护栏，控制输入/输出检查开关 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需头，含`public_key_id`、`encrypt_key`、`iv` | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK加密开关，自动处理加解密逻辑 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `dashscope.base_http_api_url` | SDK自定义API基础地址，用于私网终端节点调用 | `"http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1"` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

> **注意**：文档12中明确指出OpenAI兼容模式（`/compatible-mode/v1`）**不支持**加密调用，但文档10未强调此限制，实际使用时必须避免在OpenAI兼容Endpoint上设置`X-DashScope-EncryptionKey`或启用SDK加密参数，否则将返回400错误。

## 使用方式

### 1. 启用AI安全护栏
- 开通AI安全护栏服务并完成RAM授权；
- 在请求Header中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 检查响应状态码：400且`code="data_inspection_failed"`表示内容被拦截。

### 2. 启用端到端加密推理
- 调用 `/api/v1/public-keys/latest` 接口获取最新`public_key_id`和公钥；
- 生成AES密钥（推荐256位）和IV，用公钥加密AES密钥；
- 对`input`字段JSON序列化后AES加密，Base64编码；
- 设置`X-DashScope-EncryptionKey`头并发送请求；
- **或直接使用DashScope SDK**（Java/Python）：设置`enable_encryption=True`，SDK自动完成全流程。

### 3. 私网调用百炼API
- 在VPC中创建接口终端节点，服务选择`com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如`vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将SDK或HTTP请求的`base_url`替换为该域名；
- 确保VPC安全组放行80/443端口入方向流量。

### 4. 配置安全存储空间（高密场景）
- 创建类型为“安全存储空间”的业务空间；
- 依次完成：终端节点配置 → 可用区IP配置 → OSS/ADB/ES资源配置 → MSE网关路由配置；
- 所有资源必须位于同一地域（仅支持华北2（北京））、同一专有网络，且交换机跨至少两个可用区。

## 限制和注意事项

- **权限粒度**：默认业务空间无法设置模型调用/训练/部署限流；仅超级管理员可跨空间管理，业务空间管理员无权操作OpenAPI权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key归属**：自2026年3月25日起，华北2（北京）地域所有新创建API Key均归属主账号，不可分配给RAM用户 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **地域限制**：
  - 安全存储空间仅支持华北2（北京）；
  - 私网终端节点不支持美国（弗吉尼亚）地域；
  - 模型备案信息需以[互联网信息服务算法备案系统](https://beian.cac.gov.cn)实时查询结果为准，文档中备案号可能滞后 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **加密兼容性**：加密功能**仅适用于DashScope原生Endpoint**（`/api/v1/...`），OpenAI兼容Endpoint（`/compatible-mode/v1/...`）不支持，强行使用将导致请求失败。
- **存储依赖风险**：OSS Bucket或ES实例若被释放，将导致安全存储空间**不可恢复**，必须重建整个业务空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)


