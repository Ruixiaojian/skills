# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、传输加密、内容安全、模型备案、私网隔离及数据存储安全等关键维度。所有功能均面向生产环境设计，开发者需结合自身业务场景（如C端上架、企业内网部署、敏感数据处理）选择对应能力组合，并严格遵循《生成式人工智能服务管理暂行办法》等监管要求。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本与图片类模型的输入输出内容审核，自动匹配模型类型并拦截涉黄、涉政、广告等违规内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已通过国家网信办算法备案及大模型备案，备案号实时公示，可用于应用上架合规材料准备 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。  
- **安全存储业务空间**：专为高敏感场景设计，支持通过反向终端节点、MSE网关、OSS/ADB/ES私有化配置实现数据不出VPC、存储资源完全隔离 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **SOC 2 合规资质**：平台已通过无保留意见 SOC 2 审计，在安全、可用性、保密性三方面具备国际标准保障能力。

> **注意**：文档 9 和文档 11 均提及“安全存储业务空间”，但文档 9 要求专有网络必须包含北京可用区 G/H/L 中任意两个，而文档 11 在 ADB 配置中允许选择“华北2可用区I”——该可用区未在文档 9 的前提条件中列出。实际部署时请以控制台最新可用区列表为准，避免因可用区不匹配导致终端节点创建失败。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用AI安全护栏的请求头，值为 `{"input":"cip","output":"cip"}`，表示同时校验输入与输出 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | AES密钥加密传输头，包含 `public_key_id`、`encrypt_key`（RSA加密后的AES密钥）、`iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | DashScope SDK 内置加密开关，启用后自动完成加解密，无需手动处理密钥 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` 替换为终端节点域名 | 私网访问时需将默认 `dashscope.aliyuncs.com` 替换为 `ep-xxx.privatelink.aliyuncs.com` 或 `vpc-cn-beijing.dashscope.aliyuncs.com` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用内容安全
开通 AI 安全护栏服务后，在调用请求头中添加 `X-DashScope-DataInspection` 即可生效。OpenAI 兼容模式与 DashScope SDK 均支持，响应状态码 `400` + `data_inspection_failed` 表示拦截成功。

### 2. 加密传输敏感数据
- **SDK 方式（推荐）**：Python/Java SDK 设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动获取公钥、生成AES密钥、加解密 input 字段及响应体。  
- **HTTP 手动方式**：先调用 `GET /api/v1/public-keys/latest` 获取 RSA 公钥及 ID [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)，再按混合加密流程（AES加密input + RSA加密AES密钥）构造请求。

### 3. 私网访问百炼 API
- **普通模型/API 访问**：在 VPC 内创建接口终端节点（Endpoint），服务名称选 `com.aliyuncs.dashscope`，替换 base_url 即可。  
- **安全存储业务空间**：需创建**反向终端节点**（Reverse Endpoint），关联百炼侧生成的服务，并配置 MSE 网关、OSS/ADB/ES 白名单与标签授权，最终激活空间。

### 4. 模型备案材料准备
- 算法备案号（如 `网信算备330110507206401230035号`）和大模型备案号（如 `ZheJiang-TongYiQianWen-20230901`）均在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中完整列出，可直接用于上架提交。  
- 备案截图须从 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 实时查询导出，确保状态为“正常”。

## 限制和注意事项

- **权限继承规则**：API Key 的模型调用权限与限流策略**仅继承自所属业务空间**，与用户控制台页面权限无关；删除 RAM 用户会导致其 API Key 失效且不可恢复（主账号 API Key 不受影响）[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
- **地域限制**：  
  - 私网访问仅支持华北2（北京）和新加坡地域，美国（弗吉尼亚）暂不支持；  
  - 安全存储业务空间强制要求专有网络位于华北2（北京），且可用区需满足特定组合（G/H/L）；  
  - 北京地域新创建的 API Key 默认归属主账号（自2026年3月25日起）。  
- **加密兼容性**：AES-RSA 混合加密**仅适用于 DashScope Endpoint**（`dashscope.aliyuncs.com/api/v1`），OpenAI 兼容 Endpoint（`dashscope.aliyuncs.com/compatible-mode/v1`）不支持该机制。  
- **存储依赖强耦合**：OSS/ADB/ES 任一组件停止服务或被释放，将导致安全存储业务空间整体不可用且无法恢复，需提前规划续费与灾备策略 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。  
- **备案责任主体**：即使使用百炼提供的已备案模型，应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法评估等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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


