# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖模型调用、数据传输、存储隔离、内容审核及监管备案等关键环节。开发者可通过权限管理、AI安全护栏、私网接入、端到端加密及合规资质材料获取等机制，满足企业级安全要求和中国及国际监管规范（如《生成式人工智能服务管理暂行办法》、SOC 2）。所有能力均基于业务空间粒度进行精细化控制，支持生产环境的环境隔离与最小权限实践。

## 支持的模型/功能

- **AI安全护栏**：支持文本与图片类模型的输入输出内容审核，自动匹配对应护栏服务，需显式启用（详见[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)）。
- **安全存储业务空间**：提供私有网络隔离的数据存储能力，支持对接OSS、AnalyticDB（ADB）和Elasticsearch（ES）等后端资源，适用于高敏感数据场景（详见[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot等）均完成算法备案与大模型备案，并公示备案号及主体信息（详见[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)）。
- **传输安全增强**：
  - 支持通过终端节点（PrivateLink）实现VPC内私网访问百炼API，流量不经过公网（详见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)）；
  - 支持对`input`字段进行AES-RSA混合加密，防止敏感数据在传输中被窃取（详见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)）。

> **注意**：文档11中明确指出“美国（弗吉尼亚）地域暂不支持私网访问”，而文档6和文档7仅针对“华北2（北京）”地域描述安全存储业务空间的配置流程，未提及其他地域支持情况。若需在新加坡或弗吉尼亚使用安全存储能力，应以最新控制台提示或联系商务确认实际支持范围。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用AI安全护栏的请求头，值为JSON字符串，如 `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 启用端到端加密时必需的请求头，包含`public_key_id`、`encrypt_key`（RSA加密后的AES密钥）和`iv` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK中启用自动加解密的布尔开关，简化开发集成 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `ep-{instanceId}.privatelink.aliyuncs.com` 或 `vpc-{instanceId}.{regionId}.dashscope.aliyuncs.com` | 终端节点服务域名，用于替换API `base_url` 实现私网调用 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

### 权限与空间管理
- 创建独立业务空间实现环境隔离（如 `project-prod-workspace`），超级管理员可在全局管理菜单中统一配置模型调用/训练/部署授权及限流策略；业务空间管理员仅可管理本空间内用户与模型权限（详见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- API Key绑定至单一业务空间与用户，其模型调用权限与限流策略完全继承自归属空间，不受用户控制台页面权限影响。

### 内容安全启用
1. 开通AI安全护栏服务（需主账号操作）；
2. 在安全管理页面完成内容安全授权；
3. 调用时在请求头中添加 `X-DashScope-DataInspection` 参数。

### 私网与加密接入
- **私网访问**：在VPC中创建接口终端节点 → 获取终端节点服务域名 → 替换SDK或HTTP请求中的`base_url`（支持OpenAI兼容模式与DashScope原生API）。
- **端到端加密**：
  - 推荐使用DashScope SDK（Java/Python）并设置`enable_encryption=True`，SDK自动处理密钥生成、加解密与密钥传输；
  - 如需手动管理，先调用`GET /api/v1/public-keys/latest`获取公钥ID与值（详见[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)），再按AES-RSA混合加密流程封装请求。

### 合规材料准备
- 应用上架前，需从[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)查询并截图所用模型的备案信息（如千问备案号 `网信算备330110507206401230035号`）；
- 与阿里云签署含算法名称与备案编号的合作协议（需联系商务经理获取）。

## 限制和注意事项

- **地域限制**：安全存储业务空间仅支持“华北2（北京）”地域；私网访问暂不支持美国（弗吉尼亚）地域（见文档11）；跨地域私网访问需结合CEN或跨地域终端节点（见文档11）。
- **API Key生命周期**：华北2（北京）地域新创建的API Key默认归属主账号；RAM用户API Key在账号被移出业务空间后失效（重新加入可恢复），但在RAM控制台删除账号后不可恢复（见文档1）。
- **加密能力约束**：DashScope SDK加密仅支持Java和Python；OpenAI兼容Endpoint（`/compatible-mode/v1`）不支持`X-DashScope-EncryptionKey`机制（见文档9）。
- **备案责任主体**：即使使用百炼提供的已备案模型，应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案（如适用）等全部法定义务（见文档5）。
- **资源依赖风险**：OSS Bucket、ADB实例或ES集群若被释放或欠费停服，将导致安全存储业务空间及其关联功能（知识库、审计日志等）不可用且无法恢复，需重建空间（见文档8）。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)


