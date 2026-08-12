# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、内容安全及监管备案等关键环节。开发者可通过权限控制、加密传输、私网访问、AI安全护栏及算法备案信息等机制，满足企业级安全要求和中国及国际主流合规标准（如《生成式人工智能服务管理暂行办法》、SOC 2）。所有能力均通过控制台、OpenAPI 或 SDK 提供，无需额外部署。

## 支持的模型/功能

- **模型范围**：AI 安全护栏服务支持文本和图片类模型（如 `qwen-plus`、`wanxiang`），具体支持列表见[面向阿里云百炼用户的AI安全护栏服务](https://help.aliyun.com/zh/document_detail/2923687.html)；加密传输（AES+RSA）与私网终端节点（PrivateLink）适用于所有 DashScope 接口模型（含 `qwen-flash`、`qwen-plus` 等），但**不支持 OpenAI 兼容模式的 Chat Completions API 和 Responses API 的加密调用** [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储业务空间**：仅限已开通该服务的用户使用，支持对接客户 VPC 内的 OSS、ADB、Elasticsearch 等资源，实现数据不出私网 [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)。
- **备案模型**：平台公示千问、万相、DeepSeek、Moonshot 等 14 款大模型的算法备案号与大模型备案号，覆盖生成合成类、交互式内容生成等算法类型 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 示例值 |
|------|--------|------|------|--------|
| AI 安全护栏 | `X-DashScope-DataInspection` | Header (JSON) | 启用输入/输出内容审核 | `{"input":"cip","output":"cip"}` |
| 加密传输 | `X-DashScope-EncryptionKey` | Header (JSON) | 封装 RSA 加密后的 AES 密钥及 IV | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` |
| 加密传输 | `input` 字段 | Base64 编码字符串 | 经 AES 加密后的原始 input 内容 | `"+J2aT8GNBUD..."` |
| 私网访问 | `base_url` | URL | 替换为终端节点服务域名（非公网 dashscope.aliyuncs.com） | `https://vpc-cn-beijing.dashscope.aliyuncs.com/api/v1` |
| IP 白名单 | API Key 设置 | 控制台配置 | 所有地域均支持 IPv4 白名单，美国（弗吉尼亚）仅支持 IPv4 | `192.168.0.0/24` |

> **注意**：文档 7 明确指出“OpenAI 兼容（Chat Completions API 和 Responses API）的 Endpoint **不支持**此加密机制”，而文档 8 的私网访问示例中却包含 OpenAI Python SDK 调用方式。二者存在矛盾——实际加密能力仅作用于 DashScope 原生接口，OpenAI 兼容层无法透传加密头或解密响应。开发者若需端到端加密，**必须使用 DashScope SDK 或 HTTP 直连 DashScope Endpoint**。

## 使用方式

### 1. 启用 AI 安全护栏
- 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 创建服务关联角色；
- 授权：进入 [安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)，单击“去授权”并确认；
- 调用时在请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

### 2. 启用传输加密（推荐 SDK 方式）
- **Python/Java SDK**：设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动完成密钥获取、AES 加密、RSA 加密密钥、请求构造与响应解密；
- **HTTP 手动调用**：
  - 调用 `GET /api/v1/public-keys/latest` 获取最新 `public_key_id` 和公钥 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)；
  - 生成 AES-256 密钥与 IV，用公钥加密密钥；
  - 对 `input` JSON 字符串进行 AES-CBC 加密（PKCS#7 填充）；
  - 构造 `X-DashScope-EncryptionKey` 头并发送请求。

### 3. 私网访问（VPC 内调用）
- 创建接口终端节点（PrivateLink），服务选择 `com.aliyuncs.dashscope`，地域选“华北2（北京）”或“新加坡”；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 4. 配置安全存储业务空间（高隔离场景）
- 申请开通安全存储业务空间；
- 按顺序完成：创建反向终端节点 → 配置可用区 VIP → 配置 OSS/ADB/ES → 配置 MSE 网关 → 激活空间 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **权限粒度**：默认业务空间**无法设置模型调用/训练/部署限制**，仅自建业务空间支持精细化模型级授权；超级管理员可跨空间管理，但 OpenAPI 权限（如知识库、记忆库操作）**必须由阿里云主账号在 RAM 控制台单独授予** [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **地域约束**：
  - 私网访问仅支持华北2（北京）、新加坡，**美国（弗吉尼亚）暂不支持**；
  - 安全存储业务空间当前仅支持华北2（北京）地域；
  - API Key IP 白名单在弗吉尼亚地域**仅支持 IPv4**。
- **数据隐私**：阿里云**绝不会将您的输入数据用于模型训练**；所有传输数据默认经 AES-256 加密；但根据协议，调用日志等元数据将被存储用于审计与计费 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
- **备案责任**：阿里云提供模型算法备案号及主体信息，但应用上架所需的**安全评估报告、企业自主算法备案等义务完全由开发者承担**；即使使用百炼模型，开发者仍是《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立履行内容审核、标识规范等法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **服务依赖风险**：OSS/ADB/ES 等外部存储组件若被释放或欠费停服，将导致安全存储业务空间**不可用且无法恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


