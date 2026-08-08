# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、数据传输加密、内容安全防护、模型备案合规、私网隔离访问及安全存储等关键环节。所有功能均面向企业级生产环境设计，支持开发者在满足国内监管要求（如《生成式人工智能服务管理暂行办法》）的同时，构建高可信的AI应用。

## 支持的模型/功能

- **AI 安全护栏服务**：支持对文本和图片类模型的输入输出进行实时内容审核，识别涉黄、涉政、广告等高风险内容。该服务需显式启用，且与模型自动绑定，具体支持范围请参见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已通过国家网信办算法备案及大模型备案，并公示备案号与主体信息，便于开发者完成上架合规材料准备。详细清单见[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **安全存储业务空间**：专为敏感数据场景设计，支持通过反向终端节点、MSE网关、可用区VIP等机制，将知识库、审计日志、历史记录等数据完全隔离于客户私有网络内，不经过公网传输。该能力需商务开通，配置流程详见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 8 与文档 9 中关于终端节点类型的描述存在差异——文档 8 描述的是**正向终端节点**（VPC 内资源主动访问百炼 API），而文档 9 描述的是**反向终端节点**（百炼服务主动访问客户 VPC 内资源）。二者网络流向、适用场景及控制台入口均不同，不可混用。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}`，表示同时检查输入与输出 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 启用传输加密时必需的请求头，包含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）和 `iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 中启用端到端加密的开关参数，SDK 自动处理加解密逻辑 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |

## 使用方式

### 1. 权限与空间隔离
- 按环境（开发/测试/生产）或业务线创建独立**业务空间**，超级管理员通过[全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)统一分配模型调用、训练、部署权限及限流配额。
- RAM 用户需被授予**业务空间管理员**角色方可管理该空间内用户、页面及 API Key；普通用户权限由空间内分配的控制台权限与所属空间的模型授权共同决定。

### 2. 内容安全接入
- 开通 AI 安全护栏服务后，在调用请求中添加 `X-DashScope-DataInspection` 请求头即可生效。若输入或输出触发风控，API 返回 `400` 错误码 `data_inspection_failed`，响应体含明确提示。

### 3. 数据传输加密
- **推荐方式**：使用 DashScope SDK（Java/Python），设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥并完成混合加解密。
- **手动方式**：先调用 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 接口，再用 RSA 公钥加密 AES 密钥，用 AES 密钥加密 `input` 字段，最后通过 `X-DashScope-EncryptionKey` 头传递密钥元数据。

### 4. 私网访问百炼 API
- 对于 VPC 内调用，创建**接口终端节点**（Interface Endpoint），服务名称为 `com.aliyuncs.dashscope`，替换 API `base_url` 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com`）。
- 对于百炼访问客户 VPC 内资源（如 ES/ADB/OSS），需开通**安全存储业务空间**，创建**反向终端节点**，并完成 MSE 网关、可用区 VIP、资源白名单等完整链路配置。

## 限制和注意事项

- **API Key 绑定严格**：每个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移；华北2（北京）地域新创建的 API Key 默认归属主账号。
- **OpenAPI 权限独立**：RAM 用户默认无权调用百炼应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)），需主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。
- **加密兼容性限制**：AES-RSA 混合加密仅支持 DashScope 原生 Endpoint（如 `/api/v1/services/aigc/text-generation/generation`），**不支持 OpenAI 兼容模式**（`/compatible-mode/v1/chat/completions`）。
- **地域支持差异**：私网访问（PrivateLink）目前仅支持华北2（北京）和新加坡地域；美国（弗吉尼亚）地域暂不支持。安全存储业务空间当前仅支持华北2（北京）地域。
- **备案责任主体**：百炼提供模型算法备案号供参考，但根据《生成式人工智能服务管理暂行办法》，应用/小程序开发者作为“服务提供者”，须自行完成算法备案、安全评估及合作协议签署等法定义务。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


