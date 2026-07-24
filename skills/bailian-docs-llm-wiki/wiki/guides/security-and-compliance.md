# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、存储、权限与合规备案的全链路安全与合规能力，面向企业级生产环境设计。核心能力包括基于业务空间的精细化权限控制、输入输出内容安全护栏、端到端传输加密、私网隔离访问、安全存储资源纳管，以及符合中国法规要求的算法与大模型备案支持。所有功能均通过 API 与控制台统一管理，开发者可按需组合使用。

## 支持的模型/功能

- **AI 安全护栏服务**：支持文本和图片类模型（如 `qwen-plus`、`wanxiang`）的输入输出内容审核，自动识别涉黄、涉政、广告等高风险内容 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密推理**：支持对请求体中 `input` 字段进行 AES-RSA 混合加密，适用于敏感数据场景；当前仅 Python 和 Java SDK 提供开箱即用的 `enable_encryption` / `enableEncrypt` 参数封装 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过阿里云 PrivateLink 创建终端节点，实现 VPC 内资源（ECS、容器等）不经过公网直连百炼 API；华北2（北京）和新加坡地域可用，美国（弗吉尼亚）地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储资源**：支持将知识库、审计日志等数据落盘至客户自有 VPC 内的 OSS、ADB（AnalyticDB）和 Elasticsearch 实例，实现数据物理隔离 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **模型备案信息**：提供千问、万相、DeepSeek、Moonshot 等全部接入模型的算法备案号与大模型备案号，满足《生成式人工智能服务管理暂行办法》要求 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4 中提及“万相”对应两个不同备案主体（阿里巴巴达摩院与通义云启），但文档 3 仅列出一个算法备案号 `网信算备330110507206401230027号`。实际备案应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，开发者须分别验证 `网信算备330110507206401230027号`（图像合成）和 `网信算备330106003156001240091号`（视频生成）两条记录。

## 关键参数

| 参数名 | 说明 | 使用位置 | 示例值 |
|--------|------|----------|--------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，控制输入/输出检查开关 | HTTP Header | `{"input":"cip","output":"cip"}` |
| `X-DashScope-EncryptionKey` | 加密调用必需请求头，含 `public_key_id`、`encrypt_key`（RSA 加密后的 AES 密钥）、`iv` | HTTP Header | `{"public_key_id":"1","encrypt_key":"MIIBIj...","iv":"a1b2c3..."}` |
| `enable_encryption` (Python) / `enableEncrypt` (Java) | SDK 封装的加密开关，启用后自动完成加解密 | DashScope SDK 调用参数 | `True` / `true` |
| `base_url` | OpenAI 兼容模式下替换为私网终端节点域名 | OpenAI SDK 初始化 | `"https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1"` |

## 使用方式

### 1. 启用内容安全护栏
- 开通 AI 安全护栏服务（需主账号在[安全管理页面](https://bailian.console.aliyun.com/?globalset=1#/efm/global_set)授权）；
- 在请求 Header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 接收 `400` 响应及 `data_inspection_failed` 错误码时，表示内容被拦截。

### 2. 启用传输加密（SDK 方式）
- 安装最新版 DashScope SDK（Python ≥ 1.20.0，Java ≥ 2.15.0）；
- 调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
- SDK 自动获取公钥、生成 AES 密钥、加解密 input/output，返回明文响应。

### 3. 私网访问百炼 API
- 在 VPC 所在地域创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 获取终端节点服务域名（如 `vpc-cn-beijing.dashscope.aliyuncs.com`）；
- 将 SDK 或 HTTP 请求的 `base_url` 替换为该域名；
- 确保终端节点安全组放行 443/80 端口入方向流量。

### 4. 配置安全存储（OSS/ADB/ES）
- 先完成[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)与[配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)；
- 在业务空间“资源配置”页，分别授权并绑定已创建的 OSS Bucket（需打标签 `bailian-safe-workspace-oss-access: ReadAndWrite`）、ADB 实例、ES 实例；
- 最后执行“激活”操作使安全存储空间生效。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理最小单元，**默认业务空间无法设置模型调用/训练/部署限制**，必须新建自定义业务空间才能启用限流与授权控制 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，不可分配给 RAM 用户；RAM 用户的 API Key 在其被移出业务空间后立即失效且不可恢复。
- **加密调用兼容性**：`X-DashScope-EncryptionKey` 机制**仅适用于 DashScope Endpoint（`/api/v1`）**，OpenAI 兼容模式（`/compatible-mode/v1`）不支持该加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网地域限制**：美国（弗吉尼亚）地域暂不支持私网访问；跨地域私网访问需结合 CEN 或跨地域终端节点，且中国内地与境外之间必须使用 CEN [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储依赖强耦合**：OSS Bucket 或 ADB/ES 实例若被释放，将导致对应安全存储业务空间**永久不可用且无法恢复**，必须重建整个业务空间。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


