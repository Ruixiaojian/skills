# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限控制、加密传输、私网接入、AI安全护栏及算法备案信息复用等机制，满足企业级数据安全要求和中国境内生成式人工智能服务监管规范（如《生成式人工智能服务管理暂行办法》）。所有能力均基于阿里云统一安全底座，已通过 SOC 2 审计，并默认启用 AES-256 传输加密。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本与图片类模型的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容。调用时需在请求头中显式启用，具体配置见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理通道**：支持对 `input` 字段进行端到端 AES-RSA 混合加密，适用于敏感数据场景。该能力仅适用于 DashScope 原生 Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过 PrivateLink 创建接口终端节点，实现 VPC 内资源（如 ECS、容器）直连百炼 API，流量全程不经过公网。当前仅支持华北2（北京）和新加坡地域，美国（弗吉尼亚）地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：面向高合规要求客户，提供私有网络隔离的数据存储方案，支持对接客户自有 OSS、ADB 和 Elasticsearch 实例，所有组件均部署于客户 VPC 内，实现数据物理隔离。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 `{"input":"cip","output":"cip"}`，表示同时检查输入与输出 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv`（初始向量） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 中启用自动加解密的布尔开关，SDK 封装密钥生成、加密、解密全流程 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 用于手动加密流程的 RSA 公钥元数据，需先调用 `/api/v1/public-keys/latest` 接口获取 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

> **注意**：文档 10 与文档 11 均描述加密能力，但文档 10 明确指出“OpenAI 兼容（Chat Completions API 和 Responses API）的 Endpoint 不支持此加密机制”，而文档 12 的 OpenAI SDK 示例中未提示该限制。实际使用中，若采用 OpenAI 兼容模式（`base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`），**无法使用加密功能**，必须切换至 DashScope 原生 Endpoint（`base_url="https://dashscope.aliyuncs.com/api/v1"`）并使用 DashScope SDK。

## 使用方式

### 1. 启用 AI 安全护栏
- 在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务开通与授权；
- 调用模型时，在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 若触发拦截，响应状态码为 `400`，错误类型为 `data_inspection_failed`。

### 2. 启用加密推理（推荐 SDK 方式）
- 安装最新版 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）；
- Python 示例：`Generation.call(..., enable_encryption=True)`；Java 示例：`.enableEncrypt(true)`；
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并构造 `X-DashScope-EncryptionKey` 头。

### 3. 配置私网访问
- 在目标 VPC 所在地域的[终端节点控制台](https://vpc.console.aliyun.com/endpoint/)创建**接口终端节点**，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 API 请求中的 `base_url` 域名替换为该私网域名，其余参数（API Key、model、messages 等）保持不变。

### 4. 部署安全存储业务空间（高隔离场景）
- 申请开通“安全存储空间”类型业务空间；
- 依次完成：[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) → [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) → [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) → [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)；
- 最终激活业务空间，所有知识库、记忆库、审计日志等数据将落盘至客户自有 OSS/ADB/ES。

## 限制和注意事项

- **权限粒度**：API Key 的模型调用权限完全继承自其归属的**业务空间**，与用户（RAM 账号）的控制台页面权限无关；用户被移出业务空间后，其 API Key 将立即失效（文档 1 明确说明）。
- **地域绑定**：API Key 严格绑定单个地域内的单个业务空间，不可跨地域或跨空间复用；自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 默认归属主账号。
- **OpenAPI 权限**：RAM 用户默认无权调用百炼应用层 OpenAPI（如知识库、Prompt 工程），必须由阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或自定义策略，文档 1 中明确指出“OpenAPI 接口权限”需主账号操作。
- **备案信息时效性**：模型算法备案号（如 `网信算备330110507206401230035号`）和大模型备案号（如 `ZheJiang-TongYiQianWen-20230901`）均需以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，文档 3 与文档 5 中公示的编号一致，但文档 5 强调“应以系统实时查询结果为准，建议定期核验”。
- **安全存储依赖强耦合**：OSS Bucket 若被释放，将导致安全存储业务空间**永久不可用且无法恢复**；ADB 或 ES 若停止计费或被释放，将导致知识库、审计日志等模块不可用（文档 8 明确警告）。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)


