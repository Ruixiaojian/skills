# security and compliance

阿里云百炼平台提供多层次安全与合规能力，覆盖模型备案、数据传输加密、私网访问、内容安全防护、权限隔离及存储安全等关键维度。所有能力均面向企业级生产环境设计，开发者需根据自身业务场景（如C端上架、内部系统、高敏感数据处理）选择适配的组合方案，并独立承担《生成式人工智能服务管理暂行办法》等法规定义的服务提供者责任。

## 支持的模型/功能

- **已备案模型**：平台接入的千问、万相、智谱 AI、DeepSeek、Moonshot 等主流大模型均已取得国家网信办算法备案号及大模型备案号，完整清单见[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。其中千问系列备案主体为阿里巴巴达摩院(杭州)科技有限公司，万相视频生成算法备案主体为通义云启（杭州）信息技术有限公司。
- **AI 安全护栏**：支持对文本和图片类模型的输入输出进行实时内容审核，自动识别涉黄、涉政、广告等违规内容，需在请求头中配置 `X-DashScope-DataInspection` 参数启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高合规要求客户，提供基于私网终端节点、MSE网关、OSS/ADB/ES三重资源隔离的安全存储业务空间，适用于金融、政务等敏感场景 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **加密传输能力**：支持 AES+RSA 混合加密机制，对请求体中的 `input` 字段及响应结果全程加密，防止公网传输中敏感数据泄露 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

> **注意**：文档 1 和文档 2 中关于万相的算法备案号存在不一致——文档 1 列出两个万相备案号（网信算备330110507206401230027号、网信算备330106003156001240091号），而文档 2 明确区分了“达摩院图像合成算法”（主体：达摩院）与“通义万相视频生成算法”（主体：通义云启），且后者发放日期为2024-12-20。建议以[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)中按备案编号实时查询的结果为准。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-DataInspection` | 启用AI安全护栏，控制输入/输出检查开关 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 传输加密时携带RSA加密后的AES密钥、公钥ID及IV | `{"public_key_id":"1","encrypt_key":"...","iv":"..."}` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的开关 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `base_url` | 替换为终端节点服务域名实现私网调用 | `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1` | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

- **合规备案材料获取**：面向C端上架的应用，需准备所用模型的算法备案截图（通过[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)按备案编号查询）及阿里云合作协议；具有舆论属性的场景还需额外完成安全评估报告与自主算法备案 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **启用内容安全**：开通AI安全护栏服务后，在调用请求头中添加 `X-DashScope-DataInspection`，值为 JSON 字符串 `{"input":"cip","output":"cip"}`；若仅需检查输入，可设为 `{"input":"cip"}`。
- **启用传输加密**：
  - 使用 DashScope SDK：设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动处理密钥获取、加解密全流程；
  - 使用 HTTP 调用：先调用 `/api/v1/public-keys/latest` 接口获取 RSA 公钥及 ID [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)，再用该公钥加密 AES 密钥，最后将加密后 input 和密钥信息填入请求头。
- **私网访问部署**：创建接口终端节点（类型：接口终端节点，服务：`com.aliyuncs.dashscope`），获取终端节点服务域名，替换原 API 的 `base_url` 域名即可；安全存储空间需额外配置反向终端节点 + MSE网关 + OSS/ADB/ES资源绑定 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **模型备案责任归属**：阿里云百炼仅作为“服务技术支持者”完成算法备案，应用/小程序开发者是《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立履行内容审核、用户标识、日志留存等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **地域与网络限制**：
  - 私网终端节点仅支持华北2（北京）、新加坡地域，美国（弗吉尼亚）暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - 安全存储空间强制要求专有网络位于华北2（北京），且可用区需为G/H/L中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **权限与配额约束**：
  - 默认业务空间无法设置模型调用限流、训练或部署权限；精细化控制需新建业务空间并由超级管理员授权 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)；
  - API Key 仅归属单个地域、单个业务空间、单个用户，不可跨空间转移；华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密与兼容性**：AES+RSA 加密机制**仅适用于 DashScope Endpoint**，OpenAI 兼容模式（`/compatible-mode/v1`）不支持该加密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

## 来源文档

- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)


