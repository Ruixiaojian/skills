# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限管理、数据传输加密、私网隔离、内容安全防护及监管合规支持。开发者可通过控制台和 API 精细管控模型调用、训练与部署权限；对敏感数据启用端到端加密传输；通过 PrivateLink 实现 VPC 内私网访问；集成 AI 安全护栏拦截违规输入输出；并获取已备案的算法与模型资质信息，满足《生成式人工智能服务管理暂行办法》等监管要求。

## 支持的模型/功能

- **权限管理**：支持基于业务空间（Workspace）的三级角色体系（超级管理员、业务空间管理员、普通用户），可按地域、模型、功能维度精细化授权，包括模型调用限流、模型调优、模型部署、API Key 管理等 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **AI 安全护栏**：支持文本与图片类模型的输入输出内容审核，需显式在请求头中设置 `X-DashScope-DataInspection` 参数启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输**：支持对 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据泄露，DashScope SDK 提供开箱即用的自动加解密能力 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：通过阿里云 PrivateLink 创建接口终端节点（Endpoint），实现 VPC 内资源（如 ECS、容器）直接调用百炼 API，流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：支持创建隔离的私有网络环境，集成 OSS、ADB、ElasticSearch 等后端存储组件，并通过 MSE 云原生网关统一路由与访问控制 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **合规备案信息**：提供千问、万相等自研模型及第三方模型（如 DeepSeek、Moonshot、MiniMax）的算法备案号与大模型备案号公示，便于应用上架前完成监管备案 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 3 与文档 4 均列出千问模型的算法备案号 `网信算备330110507206401230035号`，但文档 3 中描述备案主体为“阿里巴巴达摩院(杭州)科技有限公司”，而文档 4 未明确主体；文档 4 新增了智谱 AI、DeepSeek 等第三方模型备案信息，覆盖更广。建议以[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)为准，因其为最新汇总页且含更多模型。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，控制输入/输出审核开关 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传输加密时携带 RSA 加密后的 AES 密钥及 IV | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"a1b2c3..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` (OpenAI SDK) / `dashscope.base_http_api_url` (DashScope SDK) | 替换为终端节点服务域名以启用私网访问 | `https://vpc-cn-beijing.dashscope.aliyuncs.com/...` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 权限配置
- 超级管理员通过全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)）统一管理多业务空间；
- 业务空间管理员在对应空间内通过「模型列表」页签开关控制模型调用、训练、部署权限，并设置 QPM/[Token](../concepts/token.md) 限流；
- API Key 绑定至单一业务空间与用户，其权限继承空间模型授权策略，不受用户控制台页面权限影响 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 2. 启用 AI 安全护栏
- 首先在 [安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 页面完成服务授权；
- 在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 若触发拦截，响应状态码为 `400`，错误类型为 `data_inspection_failed` 或 `DataInspectionFailed` [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

### 3. 加密调用模型
- **SDK 方式（推荐）**：安装最新版 DashScope SDK，调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动处理加解密；
- **HTTP 手动方式**：先调用 `/api/v1/public-keys/latest` 获取 RSA 公钥与 `public_key_id`，再生成 AES 密钥与 IV，加密 `input` 并封装 `X-DashScope-EncryptionKey` 请求头 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 4. 私网访问配置
- 在 VPC 所在地域的 [终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/endpoints) 创建「接口终端节点」，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 的 `base_url` 或 HTTP 请求域名替换为该域名即可 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 5. 合规材料准备
- 应用上架前，从 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 输入备案号（如 `网信算备330110507206401230035号`）查询并截图千问等模型的备案详情；
- 向商务经理申请阿里云与应用主体的《合作协议》，协议需包含算法名称或备案编号；
- 对具有舆论属性的应用，需自行完成安全评估报告与算法备案 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 限制和注意事项

- **地域限制**：私网访问仅支持华北2（北京）和新加坡地域，美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **默认业务空间不可限流**：默认业务空间无法设置模型调用限流与训练授权，必须新建业务空间才能启用精细化管控 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 生命周期绑定**：API Key 归属固定业务空间与用户，不可迁移；若用户被移出空间，其 API Key 失效（重新加入后恢复）；RAM 用户的 API Key 在 RAM 账号被删除后不可恢复 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密调用兼容性**：AES-RSA 加密机制**仅适用于 DashScope Endpoint**（`https://dashscope.aliyuncs.com/api/v1/...`），**不支持 OpenAI 兼容模式**（`/compatible-mode/v1/...`） [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储业务空间依赖强耦合**：OSS Bucket、ADB 实例或 ES 集群一旦被释放或欠费停服，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据均经 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


