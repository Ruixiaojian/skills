# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、权限管理及监管备案等关键环节。开发者可通过配置安全护栏、启用加密传输、使用私网访问、精细化权限控制，并结合官方备案信息完成应用合规上线。所有能力均基于阿里云基础设施的 SOC 2 合规认证与严格的数据隐私保护机制构建。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型的输入输出内容安全检测，自动匹配对应模型（如 `qwen-plus`、`wanxiang` 等），识别涉黄、涉政、广告等高风险内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
- **加密推理**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，全程在推理链路内解密与加密响应，适用于敏感数据场景 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **私网访问**：通过 PrivateLink 终端节点实现 VPC 内流量直连百炼 API（北京、新加坡地域），避免公网暴露；另支持反向终端节点对接安全存储业务空间 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
- **安全存储业务空间**：专为高敏感场景设计，支持将知识库、审计日志等数据落库至客户私有 VPC 内的 OSS、ADB 或 Elasticsearch，需配合 MSE 网关与可用区 VIP 配置 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **模型备案信息**：提供千问、万相、DeepSeek、Moonshot 等主流模型的算法备案号与大模型备案号，满足《生成式人工智能服务管理暂行办法》要求 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 3 中提及“万相”对应两个不同备案主体（达摩院与通义云启），而文档 2 的表格仅列出一个备案号。实际备案应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn)实时查询结果为准，建议开发者按文档 3 的查询步骤核验最新状态。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，指定输入/输出检查策略 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需头，携带 RSA 加密后的 AES 密钥与 IV | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 快速启用加密模式 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |

## 使用方式

### 启用安全护栏
1. 开通 [AI 安全护栏服务](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 并创建服务关联角色；  
2. 在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成内容安全授权；  
3. 调用时在请求头添加 `X-DashScope-DataInspection`，值为 JSON 字符串（需转义）。

### 启用加密推理
- **SDK 方式（推荐）**：Python/Java SDK 设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动处理加解密；  
- **HTTP 手动方式**：  
  a) 调用 `/api/v1/public-keys/latest` 获取公钥 ID 与值；  
  b) 生成 AES 密钥（128/192/256 bit）与 IV，用 RSA 公钥加密 AES 密钥；  
  c) 对 `input` 字段明文进行 AES 加密；  
  d) 构造 `X-DashScope-EncryptionKey` 请求头并发送；  
  e) 响应体中 `output.text` 为 AES 加密结果，需用原始 AES 密钥解密。

### 私网访问配置
- **普通模型/API 访问**：创建接口终端节点（服务 `com.aliyuncs.dashscope`），替换 base_url 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com`）；  
- **安全存储业务空间**：需先创建反向终端节点，再配置 MSE 网关、可用区 VIP 及后端资源（OSS/ADB/ES），最终激活业务空间。

## 限制和注意事项

- **AI 安全护栏**：仅支持文本与图片类模型；不支持语音、视频等其他模态；错误响应码为 `400`，类型为 `data_inspection_failed`。  
- **加密推理**：仅 DashScope Endpoint 支持，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1`）**不支持**该加密机制；目前仅 Python 和 Java SDK 提供开箱即用封装，其他语言需手动实现 [HTTP调用（手动密钥管理）](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。  
- **私网访问**：美国（弗吉尼亚）地域暂不支持接口终端节点；反向终端节点仅适用于安全存储业务空间，且必须部署在华北2（北京）地域，可用区需包含 G/H/L 中至少两个。  
- **权限管理**：API Key 权限完全继承其归属业务空间的模型授权策略，与用户控制台权限无关；OpenAPI 接口（如知识库、记忆库）需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 等策略。  
- **备案责任**：阿里云提供模型算法备案信息作为参考，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、安全评估、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


