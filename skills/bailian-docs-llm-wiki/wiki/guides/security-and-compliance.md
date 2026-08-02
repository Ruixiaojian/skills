# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储、内容审核及监管备案等关键环节。所有功能均基于阿里云成熟的云安全体系构建，支持企业级权限隔离、端到端加密、私网访问、AI安全护栏及全量模型备案信息公示，满足金融、政务、医疗等强监管场景的合规要求。

## 支持的模型/功能

- **AI安全护栏服务**：支持文本与图片类模型的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容，需显式启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot等）均完成国家网信办算法备案及大模型备案，备案号实时可查，详情见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **安全存储业务空间**：面向高敏感数据场景提供独立部署的私有网络环境，支持对接客户自建的OSS、ADB、ElasticSearch等后端存储资源，并通过反向终端节点实现双向隔离访问，相关配置指南见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **传输加密能力**：支持两种加密模式：
  - *RSA+AES混合加密*：对`input`字段进行端到端加密，密钥由百炼托管RSA公钥加密传输；
  - *私网终端节点（PrivateLink）*：VPC内资源通过阿里云内网直连百炼API，流量不经过公网。

> **注意**：文档7中明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，但文档1未提及该限制；实际使用时应以文档7为准，避免在弗吉尼亚地域尝试配置私网终端节点。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `X-DashScope-DataInspection` | Header | 启用AI安全护栏，值为 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | Header | AES密钥加密封装体，含 `public_key_id`、`encrypt_key`、`iv` 字段 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` / `public_key` | Response field | 用于RSA加密的公钥ID及对应公钥值，需通过 `/api/v1/public-keys/latest` 接口获取 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `ep-{id}.privatelink.aliyuncs.com` | Domain | 私网终端节点默认服务域名，用于替换原始API base_url | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 1. 启用AI安全护栏
- 在[安全管理](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)页面完成服务授权；
- 调用时在请求Header中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 响应返回 `400` + `data_inspection_failed` 错误码表示拦截成功。

### 2. 启用传输加密（SDK方式）
- Python/DashScope SDK：设置 `enable_encryption=True`；
- Java/DashScope SDK：设置 `.enableEncrypt(true)`；
- SDK自动完成AES密钥生成、RSA加密、input加密、响应解密全流程。

### 3. 配置私网访问
- 创建接口终端节点，服务选择 `com.aliyuncs.dashscope`（适用于客户端调用百炼）；
- 或创建反向终端节点，服务选择 `百炼公共云生产环境-北京站点-安全存储空间专网通道接入点`（适用于百炼访问客户VPC资源）；
- 替换API请求域名（如 `dashscope.aliyuncs.com` → `vpc-cn-beijing.dashscope.aliyuncs.com`）。

### 4. 配置安全存储业务空间
- 先创建安全存储类型业务空间；
- 按顺序完成：配置终端节点 → 获取可用区VIP → 配置MSE网关 → 绑定OSS/ADB/ES资源；
- 所有资源必须位于华北2（北京）地域，且与终端节点同VPC、同交换机。

## 限制和注意事项

- **地域限制**：私网终端节点仅支持华北2（北京）和新加坡地域；弗吉尼亚地域不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key归属**：自2026年3月25日起，华北2（北京）地域所有新创建的API Key均归属主账号，不可分配给RAM用户 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密兼容性**：`X-DashScope-EncryptionKey` 加密机制**仅适用于 DashScope Endpoint**，OpenAI兼容模式（`/compatible-mode/v1`）不支持该加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **安全存储依赖**：OSS Bucket若被释放，将导致安全存储业务空间**不可恢复**；ADB/ES若停止计费或释放，同样导致业务空间不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：即使使用百炼提供的已备案模型，应用开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)


