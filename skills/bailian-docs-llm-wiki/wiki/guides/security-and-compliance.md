# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型输入输出内容安全、权限管控、数据传输加密、私网隔离、算法与模型备案、隐私保护及安全存储等关键维度。所有功能均面向生产环境设计，开发者需根据业务场景选择组合使用，以满足《生成式人工智能服务管理暂行办法》等监管要求及企业内部安全策略。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型的输入/输出内容实时检测，识别涉黄、涉政、广告等高风险内容。该服务需显式启用，不默认生效，且仅对已开通服务的模型生效 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
- **加密传输（AES+RSA）**：支持对请求体 `input` 字段进行端到端加密，防止公网传输中敏感数据泄露。该机制仅适用于 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），**OpenAI 兼容模式（`/compatible-mode/v1`）不支持** [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **私网访问能力**：提供两种私网方案：  
  - **终端节点（PrivateLink）**：适用于普通业务空间，通过接口终端节点将 VPC 流量直连百炼 API，支持华北2（北京）和新加坡地域 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；  
  - **安全存储业务空间**：专为高敏感场景设计，需配合反向终端节点、MSE 网关及私有云资源（OSS/ADB/ES）部署，实现数据不出私网、存储完全隔离 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **模型与算法备案信息**：公示千问、万相等自研模型及智谱、DeepSeek、Moonshot 等第三方模型的算法备案号与大模型备案号，供开发者用于上架合规材料 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 8 与文档 9 描述的私网方案存在适用范围差异——前者面向通用 API 调用，后者仅限“安全存储业务空间”这一特定空间类型，二者不可混用。安全存储空间必须使用反向终端节点（而非文档 8 中的接口终端节点），且强制要求华北2（北京）地域及指定可用区。

## 关键参数

| 参数名 | 作用 | 必填 | 示例值 | 来源 |
|--------|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏 | 是（启用时） | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传递 RSA 加密后的 AES 密钥 | 是（加密调用时） | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | SDK 层启用自动加解密 | 是（SDK 方式） | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` (OpenAI SDK) / `dashscope.base_http_api_url` (DashScope SDK) | 替换为私网终端节点域名 | 是（私网访问时） | `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 启用内容安全检测
1. 开通 [AI 安全护栏服务](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn)；  
2. 在控制台 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成授权；  
3. 在请求 Header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`。  
   > 响应返回 `400` + `data_inspection_failed` 错误码表示拦截成功，无需额外解析响应体。

### 启用传输加密（SDK 方式）
- **Python**：调用 `dashscope.Generation.call(..., enable_encryption=True)`；  
- **Java**：构建 `GenerationParam` 时调用 `.enableEncrypt(true)`；  
- SDK 自动处理 AES 密钥生成、RSA 加密、请求体加密及响应体解密，返回明文结果。

### 配置私网访问（终端节点方式）
1. 在 [VPC 终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/endpoints) 创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；  
2. 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；  
3. 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名。

### 部署安全存储业务空间（高隔离场景）
需严格按顺序执行：  
1. 创建安全存储类型业务空间 →  
2. 创建反向终端节点并绑定 →  
3. 配置 MSE 网关及可用区 VIP →  
4. 授权并配置 OSS/ADB/ES 私有资源 →  
5. 激活空间。  
完整流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 及后续文档。

## 限制和注意事项

- **AI 安全护栏**：仅支持部分模型，具体兼容性请查阅 [面向阿里云百炼用户的AI安全护栏服务](https://help.aliyun.com/zh/document_detail/2923687.html)，不支持所有第三方模型。  
- **加密传输**：  
  - 不支持 OpenAI 兼容模式（`/compatible-mode/v1`）Endpoint；  
  - Java/Python SDK 提供开箱即用支持，其他语言需手动实现 [HTTP调用（手动密钥管理）](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)；  
  - AES 密钥长度建议使用 256 位。  
- **私网访问**：  
  - 美国（弗吉尼亚）地域暂不支持终端节点私网访问；  
  - 安全存储业务空间仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中至少两个；  
  - 反向终端节点的安全组需放行 MSE NLB 的 VIP（非整个交换机网段）。  
- **备案信息**：  
  - 第三方模型（如 DeepSeek、Moonshot）的备案信息由其提供方负责，阿里云百炼仅作公示，不承担验证责任 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；  
  - 应用上架前，开发者须自行完成算法备案及安全评估，阿里云不替代履行《生成式人工智能服务管理暂行办法》规定的“服务提供者”主体责任 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。  
- **数据隐私**：百炼承诺不将用户数据用于模型训练，传输过程默认启用 TLS 1.2+，静态数据采用 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


