# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用安全、数据传输加密、私网隔离、权限管控、算法备案及隐私保护等关键环节。开发者可通过配置请求头、启用 SDK 加密、设置终端节点、管理业务空间权限等方式，满足生产环境对数据安全、内容合规和监管备案的刚性要求。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容。该服务需显式启用，不默认生效 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办《互联网信息服务算法备案》及《生成式人工智能服务备案》，备案号与主体信息在控制台及文档中公示 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **安全存储业务空间**：面向高敏感场景提供专属隔离环境，支持通过私网连接（PrivateLink）对接客户自建的 OSS、ADB 和 Elasticsearch，实现数据不出专有网络 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **传输加密能力**：支持对 `input` 字段进行 AES-RSA 混合加密，适用于公网传输敏感提示词或用户数据的场景；该能力仅适用于 DashScope 原生 Endpoint，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

> **注意**：文档 7 中明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，但文档 3 的全局管理菜单链接中仍包含弗吉尼亚地域入口。实际使用时，请以文档 7 的说明为准，弗吉尼亚地域无法配置 PrivateLink 终端节点。

## 关键参数

| 参数名 | 位置 | 类型 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `X-DashScope-DataInspection` | 请求 Header | JSON 字符串 | 启用 AI 安全护栏，指定 input/output 审核策略 | `{"input":"cip","output":"cip"}` |
| `X-DashScope-EncryptionKey` | 请求 Header | JSON 字符串 | 启用传输加密时携带的密钥元数据（含 `public_key_id`、`encrypt_key`、`iv`） | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` |
| `enable_encryption` / `enableEncrypt` | SDK 参数 | Boolean | DashScope Python/Java SDK 中启用自动加解密的开关 | `True` / `true` |
| `base_url` | SDK 初始化 | URL 字符串 | 替换为 PrivateLink 终端节点域名以启用私网访问 | `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1` |

## 使用方式

### 启用内容安全审核
1. 开通 [AI 安全护栏服务](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn)，创建服务关联角色；
2. 在 [安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set) 完成授权；
3. 调用时在请求 Header 中添加 `X-DashScope-DataInspection`，值为 `{"input":"cip","output":"cip"}`。

### 启用传输加密（推荐 SDK 自动模式）
- **Python**：调用 `dashscope.Generation.call()` 时传入 `enable_encryption=True`；
- **Java**：构建 `GenerationParam` 时调用 `.enableEncrypt(true)`；
- SDK 自动完成 AES 密钥生成、RSA 加密、input 加密、响应解密全流程，无需手动处理密钥。

### 启用私网访问
1. 在 VPC 控制台创建 **接口终端节点**，服务选择 `com.aliyuncs.dashscope`；
2. 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
3. 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名；
4. 确保终端节点安全组放行 443 端口入向流量。

### 配置安全存储业务空间（高隔离场景）
按顺序执行以下步骤：
- 创建反向终端节点 → 配置可用区 VIP → 授权 OSS/ADB/ES → 配置 MSE 网关 → 激活空间；
- 所有操作均需在华北2（北京）地域完成，且依赖同一专有网络与交换机；
- 详细流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 及后续配套文档。

## 限制和注意事项

- **AI 安全护栏**：仅对 `input` 和 `output` 内容做实时拦截，不修改模型原始输出逻辑；触发拦截时返回 `400` 错误码 `data_inspection_failed`，无 fallback 行为。
- **传输加密**：仅支持 DashScope 原生 API（如 `/api/v1/services/aigc/text-generation/generation`），[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）**不支持**该加密机制 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：仅支持华北2（北京）和新加坡地域；弗吉尼亚地域明确不支持，文档中相关链接为历史残留，不可用。
- **API Key 权限**：单个 API Key 严格绑定一个业务空间和一个用户，不可跨空间或跨用户复用；2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间**：OSS Bucket、ADB 实例、Elasticsearch 实例一旦释放或欠费，将导致整个安全存储空间不可用且**无法恢复**，必须重建空间。

## 来源文档

- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)


