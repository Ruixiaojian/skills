# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、加密传输、私网访问、AI安全护栏及算法备案信息查询等机制，满足企业级安全要求和中国及国际主流合规标准（如 SOC 2、《生成式人工智能服务管理暂行办法》）。所有能力均深度集成于控制台与 SDK，支持开箱即用或细粒度定制。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需显式开通并配置请求头启用，具体模型支持范围请参见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对 `input` 字段进行 AES-RSA 混合加密，防止敏感数据在公网传输中被窃听或篡改。该能力仅适用于 DashScope 原生 Endpoint（如 `/api/v1/generation`），[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问通道**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）对百炼 API 的零公网流量调用；同时支持反向终端节点，为安全存储业务空间构建专属私网连接 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息公示**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已依法完成算法备案与大模型备案，并在平台公示备案号及主体信息，供开发者用于应用上架合规材料准备。

> **注意**：文档 8 明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，但文档 1 中全局管理菜单链接包含弗吉尼亚入口，且未说明该地域是否支持终端节点。实际部署时请以控制台可用选项为准，弗吉尼亚地域当前不支持 PrivateLink 访问。

## 关键参数

| 参数 | 说明 | 使用场景 |
|------|------|----------|
| `X-DashScope-DataInspection` | 请求头，启用 AI 安全护栏。值为 `{"input":"cip","output":"cip"}` 表示同时检查输入与输出 | 所有需内容审核的模型调用（如 `qwen-plus`） |
| `X-DashScope-EncryptionKey` | 请求头，携带 RSA 加密后的 AES 密钥、公钥 ID 和 IV，用于解密请求体 | HTTP 手动加密调用（仅 DashScope Endpoint） |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | SDK 参数，自动处理 AES 密钥生成、加解密逻辑 | DashScope SDK 加密调用（推荐方式） |
| `base_url` 替换为终端节点域名 | 如 `http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1` | 私网调用百炼 API（OpenAI SDK 或 DashScope SDK 均适用） |

## 使用方式

### 启用 AI 安全护栏
1. 在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权；
2. 调用时在请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
3. 若触发拦截，响应状态码为 `400`，错误类型为 `data_inspection_failed` 或 `DataInspectionFailed`。

### 启用传输加密（SDK 方式）
- **Python**：调用 `dashscope.Generation.call(..., enable_encryption=True)`
- **Java**：构建 `GenerationParam` 时调用 `.enableEncrypt(true)`
- SDK 自动获取公钥、生成 AES 密钥、加解密 input 及 response，返回明文结果。

### 启用私网访问
- **正向访问（VPC → 百炼）**：在 VPC 中创建接口终端节点，服务选择 `com.aliyuncs.dashscope`，将 API `base_url` 替换为终端节点域名；
- **反向访问（百炼 → 客户 VPC）**：为安全存储业务空间创建反向终端节点，并关联客户 VPC 的专有网络与交换机（仅限华北2北京地域）；
- **安全存储配套**：需依次完成 [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)、[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) 和 [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)，方可激活安全存储空间。

## 限制和注意事项

- **API Key 权限隔离**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可跨空间或跨用户转移；其可调用模型及限流策略完全继承自所属业务空间的模型授权配置，与用户控制台页面权限无关。
- **OpenAPI 权限独立管控**：RAM 用户默认无权调用百炼应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)），必须由阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **加密调用兼容性限制**：HTTP 手动加密方式仅支持 DashScope 原生接口；OpenAI 兼容模式（`/compatible-mode/v1`）不支持 `X-DashScope-EncryptionKey` 头及 input 加密。
- **安全存储地域约束**：安全存储业务空间及其配套的终端节点、OSS、ADB、ES、MSE 网关等资源，**强制要求全部部署在华北2（北京）地域**，且专有网络需包含可用区 G/H/L 中至少两个；其他地域暂不支持。
- **备案信息时效性**：模型备案号以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，建议定期核验；文档 3 与文档 4 中部分备案号存在格式差异（如 `网信算备...号` vs `网信算备...`），应以备案系统截图为准。

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


