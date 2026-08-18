# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、传输加密、内容安全、模型备案、数据隐私及私有网络接入等关键维度。所有功能均面向生产环境设计，支持企业级精细化管控和审计要求。开发者可根据业务敏感度和部署场景，组合使用权限隔离、AI 安全护栏、端到端加密、PrivateLink 私网访问等机制。

## 支持的模型/功能

- **模型备案**：所有接入百炼的第三方大模型（如 Qwen、DeepSeek、Moonshot、MiniMax 等）均已按《生成式人工智能服务管理暂行办法》完成算法备案与大模型备案，备案号在[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)中完整列出。
- **AI 安全护栏**：支持对文本与图片类模型输入输出进行实时内容风险识别（涉黄、涉政、广告等），需显式启用；具体支持的模型范围及计费规则详见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理**：支持对 `input` 字段进行 AES-RSA 混合加密，适用于敏感数据传输场景；该功能仅适用于 DashScope 原生 Endpoint，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**（见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)）。
- **私网访问**：通过 PrivateLink 接口终端节点实现 VPC 内流量全程走阿里云内网，支持华北2（北京）、新加坡地域；美国（弗吉尼亚）地域暂不支持（见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)）。
- **安全存储空间**：面向高合规要求客户，提供基于 MSE 网关 + 反向终端节点 + 专有网络资源（OSS/ADB/ES）的全链路私有化数据存储方案，需商务开通（见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。

> **注意**：文档 7（配置可用区IP）与文档 9（配置终端节点并发起连接）存在流程依赖矛盾——文档 9 要求先创建反向终端节点再进入“管理安全存储空间”页面，而文档 7 的步骤3却要求在“终端节点配置”页面点击“下一步”进入“可用区IP配置”，但该页面仅在反向终端节点已创建并连接成功后才可进入。实际操作应严格遵循文档 9 的顺序：先完成反向终端节点创建与连接（状态为“已连接”），再执行文档 7 的可用区IP配置。

## 关键参数

| 参数名 | 用途 | 是否必需 | 来源文档 |
|--------|------|----------|----------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，值为 JSON 字符串（如 `{"input":"cip","output":"cip"}`） | 是（启用护栏时） | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传输加密请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv` | 是（启用加密推理时） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 中启用自动加解密的开关 | 是（使用 SDK 加密时） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url`（OpenAI SDK） / `dashscope.base_http_api_url`（DashScope SDK） | 替换为 PrivateLink 终端节点服务域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/...`） | 是（私网访问时） | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

- **权限控制**：通过业务空间（Workspace）实现最小粒度隔离。超级管理员可在全局管理菜单中分配模型调用/训练/部署权限、设置限流（QPM/TPM）、管理 API Key；业务空间管理员仅能管理本空间内用户与页面权限。普通用户权限由其所属空间的模型授权决定，**API Key 权限不受用户控制台权限影响**（见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **启用 AI 安全护栏**：需主账号在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务开通与授权，然后在请求头中添加 `X-DashScope-DataInspection`（见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)）。
- **启用传输加密**：
  - SDK 方式：Python/Java SDK 设置 `enable_encryption=True` 或 `.enableEncrypt(true)` 即可，无需手动处理密钥（推荐）；
  - HTTP 方式：需先调用 `/api/v1/public-keys/latest` 获取 RSA 公钥（见[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)），再用其加密 AES 密钥，并对 `input` 内容 AES 加密。
- **私网访问**：在 VPC 中创建接口终端节点（服务为 `com.aliyuncs.dashscope`），获取终端节点服务域名，替换 SDK 或 cURL 请求中的 `base_url` 或 `host`（见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)）。
- **安全存储空间**：仅限商务开通的专属空间类型，需依次完成反向终端节点创建 → 连接确认 → 配置可用区IP → 配置 OSS/ADB/ES → 激活，全流程依赖 MSE 网关与私有网络资源（见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。

## 限制和注意事项

- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，不可转移给 RAM 用户（见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用知识库、记忆库等 OpenAPI，必须由主账号在 RAM 控制台附加 `AliyunBailianDataFullAccess` 或自定义策略（如限定 `sfm:CreateIndex` 等 Action）（见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **加密功能限制**：DashScope SDK 加密仅支持 Java/Python；HTTP 加密方式**不兼容 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**（Chat Completions API），仅适用于 DashScope 原生 `/api/v1/services/aigc/text-generation` 类路径（见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)）。
- **地域支持差异**：
  - 私网访问：仅支持华北2（北京）、新加坡；弗吉尼亚不支持（见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)）；
  - 安全存储空间：当前仅支持华北2（北京）地域（见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据均经 AES-256 加密（见[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


