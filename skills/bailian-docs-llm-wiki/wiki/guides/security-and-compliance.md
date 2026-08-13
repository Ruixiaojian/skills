# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、存储及合规备案全链路的安全与合规能力，支持企业级权限隔离、端到端加密、私网访问、AI安全护栏及完整算法/大模型备案信息。所有能力均基于阿里云基础设施安全体系构建，并通过 SOC 2 审计认证。

## 支持的模型/功能

- **AI 安全护栏服务**：对输入输出内容进行实时合规检测，支持文本和图片类型模型，自动匹配对应模型（如 `qwen-plus`），需显式启用 [原文标题](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输能力**：支持对请求体中 `input` 字段 AES 加密 + RSA 公钥封装密钥的混合加密机制，适用于敏感数据场景；DashScope SDK 提供开箱即用的 `enable_encryption` 参数支持 [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：
  - 通用模型/API：通过 PrivateLink 创建**接口终端节点**，支持华北2（北京）、新加坡地域，不支持美国（弗吉尼亚）地域 [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - 安全存储业务空间：需配置**反向终端节点** + MSE 云原生网关 + 可用区 VIP，仅限华北2（北京）地域，且专有网络需满足可用区 G/H/L 中至少两个 [原文标题](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **备案模型支持**：已接入千问、万相、DeepSeek、Moonshot 等主流模型，全部完成国家网信办《互联网信息服务算法备案》及《生成式人工智能服务备案》，备案号及主体信息可公开查询 [原文标题](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 7 明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，但文档 1 中全局管理菜单链接包含弗吉尼亚控制台入口，该入口仅用于跨地域业务空间管理，**不表示弗吉尼亚地域支持私网终端节点**；实际私网接入能力以文档 7 为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，JSON 格式字符串 | `{"input":"cip","output":"cip"}` | [原文标题](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 手动加密调用必需请求头，含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv` | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"a1b2c3..."}` | [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption` (Python SDK) / `enableEncrypt` (Java SDK) | SDK 层自动加密开关，启用后无需手动实现加解密逻辑 | `True` / `true` | [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 通过 `/api/v1/public-keys/latest` 接口获取，用于手动加密流程 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

### 1. 启用 AI 安全护栏
- 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn)，创建服务关联角色并完成购买。
- 授权设置：进入 [安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)，单击“去授权”并确认。
- 请求头注入：在 API 调用时添加 `X-DashScope-DataInspection` 头（见上表），示例代码覆盖 Python（DashScope/OpenAI）、Java（OpenAI）、Node.js（OpenAI）等主流 SDK。

### 2. 启用传输加密
- **SDK 自动模式（推荐）**：安装最新 DashScope SDK（Java/Python），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动完成密钥生成、AES 加密、RSA 封装及响应解密。
- **HTTP 手动模式**：先调用 `/api/v1/public-keys/latest` 获取公钥 ID 和值 → 生成 AES 密钥与 IV → AES 加密 `input` → RSA 加密 AES 密钥 → 构造 `X-DashScope-EncryptionKey` 头 → 发送请求 → 响应体 AES 解密。

### 3. 配置私网访问
- **通用模型/API（接口终端节点）**：
  1. 在 VPC 控制台创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
  2. 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
  3. 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名。
- **安全存储业务空间（反向终端节点）**：
  1. 在百炼控制台创建“安全存储空间”；
  2. 在 VPC 控制台创建反向终端节点，服务选择“百炼公共云生产环境-北京站点-安全存储空间专网通道接入点”；
  3. 在百炼控制台确认连接状态为“已连接”；
  4. 后续需配置 MSE 网关、可用区 VIP、OSS/ADB/ES 等资源（详见文档 9–12）。

## 限制和注意事项

- **权限粒度**：API Key 权限完全继承其归属业务空间的模型授权策略，**不受用户控制台页面权限影响**；普通用户无法管理 API Key，仅超级管理员和业务空间管理员可操作 [原文标题](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **地域约束**：
  - 私网访问（接口终端节点）：仅支持华北2（北京）、新加坡，**弗吉尼亚不支持**；
  - 安全存储业务空间：仅支持华北2（北京），且专有网络必须包含可用区 G/H/L 中至少两个；
  - 新建 API Key 归属：自 2026年3月25日起，华北2（北京）地域所有新 API Key 默认归属主账号，不可分配给 RAM 用户。
- **加密限制**：
  - 混合加密仅适用于 DashScope 原生 Endpoint（`https://dashscope.aliyuncs.com/api/v1`），**不支持 OpenAI 兼容模式（`/compatible-mode/v1`）**；
  - SDK 自动加密仅支持 Java 和 Python，其他语言需使用 HTTP 手动模式。
- **备案责任**：阿里云提供模型算法备案号及主体信息，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，**须独立承担内容审核、用户保护、数据安全等全部法定义务**，备案材料（如安全评估报告）需自行准备 [原文标题](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **存储依赖风险**：安全存储业务空间强依赖 OSS/ADB/ES 服务状态；若任一组件被释放或欠费停服，将导致整个安全存储空间不可用且**无法恢复**，必须重建空间 [原文标题](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


