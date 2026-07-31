# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、加密传输、私网接入、AI安全护栏及算法备案信息查询等机制，满足企业级安全要求和中国及国际主流合规标准（如 SOC 2、《生成式人工智能服务管理暂行办法》）。所有能力均面向生产环境设计，支持细粒度控制与可审计操作。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容合规检测（涉黄、涉政、广告等），需显式启用 [X-DashScope-DataInspection 请求头](../../raw/model-user-guide/security-and-compliance/content-security.md)。该服务自动匹配调用模型，无需按模型单独配置。
- **加密推理通道**：支持对 `input` 字段进行 AES-RSA 混合加密，防止敏感数据在公网传输中被窃取或篡改。该能力仅适用于 DashScope Endpoint（不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）不经公网直连百炼 API，适用于对网络隔离有强要求的场景 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：提供端到端私网闭环方案，支持将知识库、审计日志等数据存储于客户自有 VPC 内的 OSS、ADB、ElasticSearch 等资源，全程不经过公网 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：公示所接入大模型的算法备案号与大模型备案号，涵盖千问、万相、DeepSeek、Moonshot 等主流模型，供开发者用于上架合规材料准备 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4 中提及“万相”对应两个不同备案主体（阿里巴巴达摩院与通义云启），而文档 3 的表格中未区分视频生成与图像合成算法。实际备案应以 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 实时查询结果为准，建议开发者按具体使用算法类型（如“通义万相视频生成算法”）独立核查备案号。

## 关键参数

| 参数名 | 用途 | 来源/说明 |
|--------|------|-----------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，含 `public_key_id`、`encrypt_key`（RSA 加密的 AES 密钥）、`iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的开关参数 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `dashscope.base_http_api_url` | DashScope Java/Python SDK 自定义 API 域名，用于私网访问替换 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用内容安全护栏
- 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 并创建服务关联角色。
- 授权：在 [安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 单击“去授权”完成。
- 调用：在请求 header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`。触发违规时返回 `400` 及 `data_inspection_failed` 错误码。

### 2. 启用加密推理
- **SDK 方式（推荐）**：安装最新版 DashScope SDK（Java/Python），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动处理加解密。
- **HTTP 手动方式**：
  - 调用 `/api/v1/public-keys/latest` 获取当前 RSA 公钥及 `public_key_id` [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)；
  - 生成 AES 密钥与 IV，用 RSA 公钥加密 AES 密钥；
  - 将加密后的 `input` Base64 编码，放入请求体；
  - 将 `public_key_id`、加密后的 AES 密钥、IV 组装为 JSON 放入 `X-DashScope-EncryptionKey` header；
  - 响应体中的 `output` 为加密内容，需用 AES 密钥解密。

### 3. 私网访问百炼 API
- 创建终端节点：在 [终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/endpoints) 选择地域（北京/新加坡），服务选 `com.aliyuncs.dashscope`，开启自定义域名。
- 替换 base_url：将 SDK 或 curl 的 `base_url` 替换为终端节点服务域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com`）。
- > **注意**：美国（弗吉尼亚）地域暂不支持私网访问 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 4. 配置安全存储业务空间（高隔离场景）
需按顺序完成以下步骤：
1. 创建反向终端节点（[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）；
2. 创建 MSE 云原生网关并配置可用区 VIP（[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)）；
3. 在 VPC 内配置 OSS/ADB/ES，并设置标签、白名单及跨域规则（[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)）；
4. 在业务空间管理页激活空间（[配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)）。

## 限制和注意事项

- **权限粒度**：默认业务空间无法设置模型调用、训练、部署的细粒度授权；仅自建业务空间支持限流（QPM/[Token](../concepts/token.md)）与模型级开关控制 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 归属**：华北2（北京）地域新创建的 API Key 默认归属主账号，且不可转移至其他业务空间或用户；RAM 用户的 API Key 在其被移出业务空间后失效（重新加入可恢复）。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用知识库、Prompt 工程等 OpenAPI，必须由阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **加密兼容性**：AES-RSA 加密仅支持 DashScope Endpoint（`https://dashscope.aliyuncs.com/api/v1/...`），[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/...`）不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **备案责任主体**：阿里云提供模型算法备案信息供参考，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **SOC 2 范围**：百炼已通过 SOC 2 Type II 审计（安全、可用性、保密性），但不覆盖客户侧代码、配置及数据治理责任 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


