# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、数据传输加密、内容安全防护、模型备案支持及私有化部署等关键维度。开发者可通过控制台配置、API 调用或 SDK 集成等方式，按需启用对应能力，满足金融、政务、企业内网等高敏感场景的监管与安全要求。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型（如 `qwen-plus`、`wanxiang`）的输入输出进行实时内容审核，识别涉黄、涉政、广告等违规内容。该服务需显式开通并配置请求头，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办算法备案与大模型备案，并公示备案号及主体信息，供开发者用于应用上架合规申报，详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **安全存储业务空间**：面向高安全需求客户，支持通过反向终端节点、MSE 网关、OSS/ADB/ES 私有资源集成构建端到端私有化数据链路，适用于金融、政务等强监管场景。

> **注意**：文档 8 和文档 10 均描述“安全存储业务空间”的配置流程，但文档 8 要求专有网络必须包含“可用区G、H、L中任意两个”，而文档 10 在 ADB/ES 配置步骤中仅要求“任选其一”可用区，二者存在矛盾。实际部署应以文档 8 的双可用区要求为准，确保高可用性。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，指定 input/output 审核策略 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 启用传输加密时必需的请求头，封装 RSA 加密后的 AES 密钥及 IV | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `enableEncrypt(true)` (Java) | DashScope SDK 中启用自动加解密的布尔开关 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url`（私网调用） | 替换为终端节点服务域名（如 `http://ep-xxx.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1`）实现 VPC 内网直连 | `http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

- **权限控制**：通过业务空间（Workspace）实现最小粒度权限隔离。超级管理员可跨空间管理模型调用/训练/部署限流；业务空间管理员仅能管理本空间内用户、页面、API Key 及模型授权状态；普通用户权限由分配的角色决定。[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 文档详细定义了各角色能力矩阵。
- **传输加密**：
  - *SDK 方式*：在 DashScope Python/Java SDK 中设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动完成 AES 加密、RSA 公钥加密密钥、请求构造与响应解密。
  - *HTTP 方式*：先调用 `/api/v1/public-keys/latest` 获取最新 RSA 公钥（见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)），再手动执行 AES 加密 `input`、RSA 加密 AES 密钥、构造 `X-DashScope-EncryptionKey` 头。
- **私网访问**：
  - *模型/API 调用*：在 VPC 内创建接口终端节点（Endpoint），绑定服务 `com.aliyuncs.dashscope`，将 SDK 或 cURL 的 `base_url` 替换为终端节点域名。
  - *安全存储空间*：需依次完成反向终端节点创建、可用区 VIP 配置、OSS/ADB/ES 私有资源授权与白名单设置、MSE 网关路由配置，最终激活空间。

## 限制和注意事项

- **地域限制**：私网访问仅支持华北2（北京）和新加坡地域；美国（弗吉尼亚）地域暂不支持；安全存储业务空间当前仅支持华北2（北京）地域。
- **API Key 绑定**：单个 API Key 严格绑定一个地域、一个业务空间和一个用户，不可跨空间或跨用户复用；自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用百炼应用层 OpenAPI（知识库、[Prompt 工程](../concepts/prompt-engineering.md)等），必须由阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **加密兼容性**：AES-RSA 混合加密机制**仅适用于 DashScope 原生 Endpoint**（`/api/v1/...`），OpenAI 兼容 Endpoint（`/compatible-mode/v1/...`）不支持该加密流程。
- **安全存储依赖项**：OSS Bucket 若被释放、ADB/ES 若停止计费或被释放，将导致安全存储业务空间完全不可用且无法恢复，需重建空间。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


