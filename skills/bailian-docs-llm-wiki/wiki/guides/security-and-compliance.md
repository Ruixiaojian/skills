# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、存储及合规备案全链路的安全与合规能力，支持企业级权限隔离、端到端加密通信、私网安全访问、AI内容安全护栏及监管要求的算法与大模型备案信息公示。所有能力均基于阿里云基础设施安全基线构建，并通过 SOC 2 审计验证。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需主动开通并显式启用，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)文档详细说明了配置流程与请求头设置方式。
- **加密传输能力**：支持对 `input` 字段进行 AES-RSA 混合加密，防止敏感数据在公网传输中被窃听或篡改。该能力适用于 DashScope Endpoint（不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)），详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（如 ECS、容器）对百炼 API 的零公网流量调用；同时支持反向终端节点模式，供百炼安全存储业务空间访问客户侧私有云组件（如 ES、ADB、OSS）。两种模式分别见于 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办《生成式人工智能服务管理暂行办法》要求的算法备案与大模型备案，备案号及主体信息已在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中公开可查。

> **注意**：文档 4 中提及“万相”对应两个不同备案主体（阿里巴巴达摩院与通义云启），而文档 3 仅列出单一备案号。实际备案应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，开发者须按具体使用模型版本核验对应备案编号。

## 关键参数

| 参数 | 用途 | 说明 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏 | Header 值为 `{"input":"cip","output":"cip"}`，表示同时校验输入与输出；支持 `"none"`、`"input"`、`"output"` 组合。 |
| `X-DashScope-EncryptionKey` | 传输加密密钥封装 | 仅用于 HTTP 手动加密调用，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv`（初始向量）；SDK 自动管理时无需手动构造。 |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | SDK 加密开关 | DashScope SDK 提供开箱即用的加解密封装，仅支持 Python 和 Java；其他语言需使用 [HTTP调用（手动密钥管理）](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 方式。 |
| `base_url`（OpenAI SDK） / `base_http_api_url`（DashScope SDK） | 私网访问域名替换 | 必须替换为终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com` 或 `ep-xxx.privatelink.aliyuncs.com`），否则仍走公网。 |

## 使用方式

1. **权限控制**：通过业务空间（Workspace）实现最小粒度隔离。超级管理员可在全局管理菜单中跨空间配置模型调用/训练/部署权限及限流；业务空间管理员仅能管理本空间内用户、API Key 及模型授权状态。[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 文档明确了各角色能力边界与操作路径。
2. **安全护栏启用**：先在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权，再在每次请求 Header 中添加 `X-DashScope-DataInspection`。
3. **传输加密接入**：
   - SDK 方式：安装最新版 DashScope SDK，调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
   - HTTP 方式：先调用 `/api/v1/public-keys/latest` 获取公钥（见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)），再生成 AES 密钥、加密 `input`、RSA 加密 AES 密钥并构造 `X-DashScope-EncryptionKey` Header。
4. **私网访问配置**：
   - 客户侧调用百炼：在 VPC 中创建接口终端节点，关联 `com.aliyuncs.dashscope` 服务，替换 SDK 或 curl 的 `base_url`；
   - 百炼调用客户侧资源（安全存储场景）：创建反向终端节点，绑定客户 VPC，并在百炼控制台完成连接确认与 OSS/ADB/ES 资源授权。

## 限制和注意事项

- **地域限制**：私网访问仅支持华北2（北京）和新加坡地域；美国（弗吉尼亚）地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密能力范围**：AES-RSA 加密仅适用于 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/chat/completions`）**不支持**该机制。
- **安全存储业务空间依赖强耦合**：OSS Bucket、ADB 实例或 ES 集群若被释放或欠费停服，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **合规责任主体**：即使使用百炼提供的已备案模型，应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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


