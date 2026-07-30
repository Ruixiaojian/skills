# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及资质认证等关键环节。开发者可通过权限管理、加密传输、私网接入、AI安全护栏等机制，满足金融、政务、医疗等高敏感场景的合规要求。所有能力均基于阿里云统一安全基座构建，并通过国际权威审计与国内算法备案。

## 支持的模型/功能

- **模型备案支持**：所有接入百炼的主流大模型（如通义千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办《生成式人工智能服务算法备案》及《大模型备案号》，具体清单详见[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **AI 安全护栏**：支持文本与图片类模型的输入输出内容合规检测（涉政、涉黄、广告等），需显式启用 `X-DashScope-DataInspection` 请求头，详细配置见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储业务空间**：提供独立网络域的私有化部署能力，支持通过反向终端节点 + MSE 网关 + OSS/ADB/ES 组合实现数据不出专有网络（VPC），适用于对数据驻留有强要求的客户。
- **加密传输能力**：支持 AES-RSA 混合加密机制，对请求体 `input` 字段端到端加密，防止公网传输中敏感数据泄露；该能力仅适用于 DashScope 原生 Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 —— 详见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

> **注意**：文档 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 中声明“美国（弗吉尼亚）地域暂不支持私网访问”，但文档 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 的全局管理菜单链接明确包含弗吉尼亚控制台入口（`https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management`），表明该地域已支持部分私网能力（如业务空间管理），但模型/API 的终端节点私网接入尚未开通。实际使用前请以控制台可用性为准。

## 关键参数

| 参数名 | 位置 | 类型 | 说明 | 来源 |
|--------|------|------|------|------|
| `X-DashScope-DataInspection` | HTTP Header | JSON string | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP Header | JSON string | 启用端到端加密时必需，含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | SDK 参数 | boolean | DashScope SDK 自动加解密开关，仅限 Python/Java SDK | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应 | string | 获取 RSA 公钥用于手动加密，必须在每次加密前调用该接口获取最新公钥 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

### 1. 权限与空间隔离
- 创建独立业务空间（如 `project-prod-workspace`），按环境或业务线划分，避免权限交叉；
- 超级管理员通过[全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)统一分配模型调用/训练/部署权限及限流策略；
- RAM 用户需被授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 才能调用 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)等），此权限**必须由阿里云主账号在 RAM 控制台配置** —— 见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 2. 内容安全防护
- 开通 AI 安全护栏服务后，在请求 Header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 若请求触发拦截，响应状态码为 `400`，错误类型为 `data_inspection_failed`，需捕获并处理该异常。

### 3. 数据传输加密
- **SDK 方式（推荐）**：升级 DashScope SDK 至最新版，设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动完成 AES 密钥生成、RSA 加密、加解密全流程；
- **HTTP 手动方式**：先调用 `GET /api/v1/public-keys/latest` 获取公钥 ID 和值；再生成随机 AES 密钥，用 RSA 公钥加密该密钥，同时用 AES 加密 `input` 字段；最后将加密密钥、IV 等封装至 `X-DashScope-EncryptionKey` Header 发送。

### 4. 私网访问与安全存储
- 对于高敏感数据场景，申请**安全存储业务空间**，通过反向终端节点打通 VPC 与百炼内网；
- 配置 MSE 网关 + OSS/ADB/ES 私有资源，确保所有数据读写均在客户 VPC 内完成，不经过公网；
- 全流程操作指南见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)、[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)及后续资源配置文档。

## 限制和注意事项

- **API Key 绑定不可迁移**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，无法转移；北京地域新创建的 API Key 默认归属主账号（自 2026年3月25日起）。
- **加密能力范围受限**：AES-RSA 加密仅支持 DashScope 原生 Endpoint（如 `https://dashscope.aliyuncs.com/api/v1`），**不支持 OpenAI 兼容模式（`/compatible-mode/v1`）**。
- **安全存储空间依赖性强**：OSS Bucket 或 ADB/ES 实例若被释放或停止计费，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建空间。
- **地域能力差异**：弗吉尼亚地域目前支持业务空间管理，但**不支持终端节点私网访问模型/API**；北京、新加坡地域完整支持私网接入。
- **默认业务空间无细粒度控制**：默认业务空间无法设置模型调用/训练/部署授权及限流，必须新建业务空间才能启用精细化权限管控。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)


