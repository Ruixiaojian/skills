# security and compliance

阿里云百炼平台提供多层次安全与合规能力，覆盖模型调用、数据传输、存储、内容审核及监管备案等关键环节。开发者可通过权限控制、加密传输、私网接入、AI安全护栏及算法备案信息复用等方式，满足企业级安全要求与国内监管合规（如《生成式人工智能服务管理暂行办法》）。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需显式启用，且与模型自动绑定，具体支持范围请参见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对请求体中 `input` 字段（含 [prompt](prompt.md) 和 messages）进行 AES-RSA 混合加密，全程在推理链路中保持密文状态，适用于处理敏感数据场景。该能力仅适用于 DashScope 原生 Endpoint，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（如 `/compatible-mode/v1/chat/completions`），详见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问通道**：
  - **正向私网访问**：通过 PrivateLink 创建接口终端节点，使 VPC 内资源（如 ECS、容器）以私网方式调用百炼 API，流量不出公网。当前仅支持华北2（北京）和新加坡地域，美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **反向私网接入（安全存储空间）**：为百炼安全存储业务空间配置反向终端节点，使其可安全访问客户 VPC 内的 ElasticSearch、ADB、OSS 等资源，实现数据不出域。该能力需商务开通并严格限定于华北2（北京）地域 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办算法备案及大模型备案，并公示备案号与主体信息，供开发者用于上架合规申报 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4 中提及“万相”对应两个不同备案主体（阿里巴巴达摩院与通义云启），而文档 3 的表格中未体现此区分；实际备案查询应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时结果为准，开发者须按具体使用的模型版本核验对应备案号。

## 关键参数

| 参数 | 说明 | 使用位置 | 示例值 |
|------|------|----------|--------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，控制输入/输出检查开关 | HTTP Header | `{"input":"cip","output":"cip"}` |
| `X-DashScope-EncryptionKey` | 加密调用必需头，携带 RSA 加密后的 AES 密钥及 IV | HTTP Header | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` |
| `enable_encryption` / `enableEncrypt` | SDK 层开关，启用自动加解密逻辑 | Python/Java SDK 调用参数 | `True` / `true` |
| `dashscope.base_http_api_url` | DashScope SDK 自定义基础 URL，用于私网调用 | Python SDK 全局配置 | `"http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1"` |

## 使用方式

### 1. 启用内容安全护栏
1. 在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务授权；
2. 在 API 请求 Header 中添加 `X-DashScope-DataInspection`，值为 JSON 字符串 `{"input":"cip","output":"cip"}`；
3. 调用时若触发拦截，将返回 `400` 状态码及 `data_inspection_failed` 错误码。

### 2. 启用请求体加密（SDK 方式）
- **Python**：调用 `dashscope.Generation.call(..., enable_encryption=True)`；
- **Java**：构建 `GenerationParam` 时 `.enableEncrypt(true)`；
- SDK 自动完成 AES 密钥生成、RSA 加密、`input` 加密及响应解密，无需手动处理密钥。

### 3. 私网调用百炼 API（VPC 内资源访问百炼）
1. 在[终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/endpoints)创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
2. 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
3. 将 SDK 或 HTTP 请求的 base URL 替换为该域名（注意协议：HTTPS 需用自定义域名）。

### 4. 安全存储空间（百炼访问客户 VPC 内资源）
1. 创建安全存储类型业务空间；
2. 在[终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/reverseEndpoints)创建**反向终端节点**，关联百炼提供的专网通道服务；
3. 在业务空间管理页点击“连接”，确认状态为“已连接”；
4. 配置 MSE 网关、可用区 VIP 及白名单，最终在“资源配置”页绑定 OSS/ADB/ES 实例。

## 限制和注意事项

- **API Key 权限隔离**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可转移；其模型调用权限与所属业务空间的模型授权完全一致，**不受用户控制台页面权限影响** [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限需主账号授权**：RAM 用户默认无权调用知识库、记忆库等 OpenAPI；必须由阿里云主账号在 RAM 控制台为其附加 `AliyunBailianDataFullAccess` 或自定义策略，**RAM 用户自身无法自助开通** [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性限制**：HTTP 加密调用仅支持 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），**不兼容 OpenAI 兼容模式的 `/compatible-mode/v1/...` 接口**；若使用 OpenAI SDK，必须切换至 DashScope SDK 或原生 HTTP 调用。
- **安全存储空间地域锁定**：反向终端节点、MSE 网关、OSS/ADB/ES 等所有组件**必须全部部署在华北2（北京）地域**，且专有网络需包含可用区 G/H/L 中至少两个；跨地域或跨境部署将导致连接失败。
- **备案信息非自动继承**：百炼公示的模型备案号仅用于参考；当开发者应用涉及“舆论属性或社会动员能力”时，仍需自行完成《具有舆论属性或社会动员能力的互联网信息服务安全评估规定》要求的安全评估报告及独立算法备案，百炼不替代开发者履行法定主体责任 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


