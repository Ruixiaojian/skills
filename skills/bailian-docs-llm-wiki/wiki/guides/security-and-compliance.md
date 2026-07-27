# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、传输加密、内容安全、模型备案、私网隔离及数据存储安全等关键维度。所有功能均面向企业级生产环境设计，开发者需结合自身业务场景（如C端应用上架、内部系统部署）选择适配的安全策略与合规动作。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型的输入输出内容审核，通过 `X-DashScope-DataInspection` 请求头启用，可独立配置 input/output 检查开关 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，防止公网传输敏感数据泄露；DashScope SDK 提供开箱即用的自动加解密支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/encrypted-access-to-model-inference.md)。
- **私网访问通道**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（ECS、容器等）以私网方式调用百炼 API，流量不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：面向高敏感场景（如金融、政务），提供反向终端节点 + MSE 网关 + 私有云组件（OSS/ADB/ES）的全链路私有化数据存储方案，适用于已开通该服务的客户 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数 | 说明 | 使用位置 |
|------|------|----------|
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏，`cip` 表示调用内容安全服务 | HTTP Header（OpenAI/DashScope SDK 均支持） |
| `X-DashScope-EncryptionKey: {"public_key_id":"1","encrypt_key":"...","iv":"..."}` | 加密请求必需头，含 RSA 加密后的 AES 密钥与 IV | HTTP Header（仅 DashScope Endpoint 支持） |
| `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java） | DashScope SDK 自动加解密开关 | SDK 调用参数 |
| `base_url`（OpenAI SDK） / `dashscope.base_http_api_url`（DashScope SDK） | 替换为终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）以启用私网访问 | SDK 初始化配置 |

> **注意**：文档 7 明确指出 OpenAI 兼容模式（`/compatible-mode/v1`）Endpoint **不支持** `X-DashScope-EncryptionKey` 加密机制，仅 DashScope 原生 Endpoint（`/api/v1`）支持。若需加密，请统一使用 DashScope SDK 或 HTTP 调用原生接口。

## 使用方式

### 1. 权限与空间隔离
- 按环境（dev/test/prod）或业务线创建独立业务空间，通过[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)设置模型调用/训练/部署授权及限流（QPM/TPM），避免跨环境干扰。
- API Key 绑定至单一业务空间与用户，其权限继承自归属空间的模型授权策略，与用户控制台页面权限无关。

### 2. 内容安全接入
- 开通 AI 安全护栏服务后，在请求头添加 `X-DashScope-DataInspection`，无需修改业务逻辑即可拦截违规输入/输出（返回 `400 data_inspection_failed` 错误）。

### 3. 敏感数据加密传输
- **推荐方式**：使用 DashScope Python/Java SDK，设置 `enable_encryption=True` 即可自动完成 AES 密钥生成、RSA 加密、请求体加密与响应解密。
- **手动方式**：先调用 `/api/v1/public-keys/latest` 获取最新 RSA 公钥，再按混合加密流程处理 `input` 字段 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 4. 私网访问配置
- **普通模型/API 调用**：在 VPC 内创建接口终端节点（服务名 `com.aliyuncs.dashscope`），替换 SDK 的 `base_url` 为终端节点域名。
- **安全存储业务空间**：需额外创建反向终端节点 + MSE 网关 + 配置 OSS/ADB/ES 白名单与标签，流程详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **地域限制**：私网访问仅支持华北2（北京）、新加坡地域；美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/access-model-studio-through-privatelink.md)。
- **API Key 归属变更**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 均归属主账号，不可分配给 RAM 用户 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间依赖强耦合**：OSS Bucket 若被释放，将导致安全存储空间**完全不可恢复**，必须重建新空间；ADB/ES 停服或释放也会导致知识库、审计日志等模块不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：即使使用百炼提供的已备案模型（如千问、万相），应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


