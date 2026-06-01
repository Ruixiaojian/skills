# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，涵盖权限管理、内容安全审核、传输加密、私网访问和安全存储等方面。开发者可以根据业务需求，灵活组合这些功能以满足不同场景下的安全合规要求。

## 合规资质与隐私保护

百炼已通过 SOC 2 审计（无保留意见），在安全、可用性和保密性方面符合国际标准。详细资质可查阅[阿里云合规文档中心](https://security.aliyun.com/compliance-repository)。

关于数据隐私，参见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)，核心要点如下：

- **不用于训练**：阿里云不会将用户数据用于模型训练。
- **传输加密**：数据传输采用 AES-256 加密。
- **数据存储**：根据法规要求，百炼将存储模型与应用调用时产生的数据，具体条款见《阿里云百炼服务协议》。

### 算法备案与应用上架

根据《生成式人工智能服务管理暂行办法》，面向 C 端用户提供 AIGC 服务的应用需完成合规备案。详细流程参见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

**备案主体信息（关键）**：

| 大模型 | 算法名称 | 备案主体 | 备案号 |
|--------|---------|---------|--------|
| 千问 | 达摩院交互式多能型合成算法 | 阿里巴巴达摩院(杭州)科技有限公司 | 网信算备330110507206401230035号 |
| 万相（图像） | 达摩院图像合成算法 | 阿里巴巴达摩院(杭州)科技有限公司 | 网信算备330110507206401230027号 |
| 万相（视频） | 通义万相视频生成算法 | 通义云启（杭州）信息技术有限公司 | 网信算备330106003156001240091号 |

> **注意**：备案信息应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准，建议定期核验。

**典型需备案场景**：
1. **面向 C 端且无舆论属性**：需提供算法备案信息 + 合作协议。
2. **面向 C 端且有舆论属性**：额外需安全评估报告和企业自主算法备案。
3. **企业内部使用**：可能不直接适用上述法规，但需关注数据安全合规。

## 权限管理

百炼基于**业务空间**实现精细化权限控制。单个业务空间是权限管理和账单分账的最小管理单元，不能跨地域存在。详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 角色体系

| 能力 | 超级管理员 | 业务空间管理员 | 普通用户 |
|------|-----------|-------------|---------|
| 模型调用授权 & 限流 | ✅ | ❌ | ❌ |
| 模型调优/部署授权 | ✅ | ❌ | ❌ |
| 用户管理 | ✅ | ✅ | ❌ |
| 页面权限管理 | ✅ | ✅ | ❌ |
| API Key 管理 | ✅ | ✅ | ❌ |
| 访问被授权资源 | ✅ | ✅ | ✅ |

- **超级管理员**：阿里云主账号，或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户。
- **业务空间管理员**：拥有某个业务空间**权限管理**页面访问权限的 RAM 用户。

### API Key 权限

- 单个 API Key 只能归属一个地域内的一个业务空间和一个用户，不可转移。
- API Key 的可调用功能和模型限流与归属业务空间的权限一致，不受用户控制台权限影响。
- 自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号。
- 华北2（北京）地域支持为 API Key 设置 IP 访问白名单。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的知识库、Prompt 工程等 OpenAPI。需由主账号在 RAM 控制台添加以下权限之一：

- `AliyunBailianDataFullAccess`：所有 API 权限
- `AliyunBailianDataReadOnlyAccess`：只读 API 权限

### 生产环境最佳实践

- **空间规划**：按环境（dev/test/prod）或业务线划分独立业务空间。
- **限流策略**：将主账号总配额按比例分配给各空间，预留 10% 作为缓冲。

## 输入输出 AI 安全护栏

百炼支持接入 AI 安全护栏服务，对模型输入输出进行额外的违规内容检测（涉黄、涉政、广告等）。目前支持文本和图片类型的模型。

### 接入方式

1. **开通服务**：在 AI 安全护栏购买页面创建服务关联角色并完成开通。
2. **授权设置**：在百炼控制台的安全管理页面完成授权。
3. **设置请求头**：在 API 调用中添加 `X-DashScope-DataInspection` header：

```json
{
    "X-DashScope-DataInspection": {
        "input": "cip",
        "output": "cip"
    }
}
```

**触发安全护栏时的响应**：返回 HTTP 400，错误码 `data_inspection_failed`，错误类型 `data_inspection_failed`。OpenAI 兼容模式和 DashScope 原生接口的错误格式略有不同，但错误码一致。

## 传输安全

### 加密调用模型推理

当请求涉及敏感信息时，可对 `input` 字段进行加密传输。采用混合加密机制：数据由 AES 对称加密，AES 密钥通过 RSA 非对称加密传输。参见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

**两种接入方式**：

| 方式 | 适用场景 | 支持语言 |
|------|---------|---------|
| DashScope SDK（自动加密） | 开箱即用，不支持自定义密钥 | Java、Python |
| HTTP 调用（手动密钥管理） | 需要自定义密钥或其他语言 | 任意语言 |

**SDK 接入示例**（Java）：
```java
GenerationParam param = GenerationParam.builder()
    .enableEncrypt(true)  // 启用加密
    .build();
```

**SDK 接入示例**（Python）：
```python
response = dashscope.Generation.call(
    enable_encryption=True  # 启用加密
)
```

> **注意**：HTTP 手动加密方式仅适用于 DashScope Endpoint，不支持 OpenAI 兼容的 Endpoint（Chat Completions API 和 Responses API）。

**AES 密钥要求**：
- 长度：128/192/256 位（256 位安全性最高）
- 随机性：使用密码学安全随机源生成
- 唯一性：单次请求有效，禁止复用

RSA 公钥通过 `GET /api/v1/public-keys/latest` 接口获取。

### 私网访问（PrivateLink）

通过在 VPC 中创建接口终端节点，可实现不经过公网的私网调用百炼 API。

**支持地域**（公共云）：华北2（北京）、新加坡。

> **注意**：美国（弗吉尼亚）地域暂不支持私网访问。

**接入步骤**：
1. 创建接口终端节点，选择终端节点服务 `com.aliyuncs.dashscope`。
2. 获取终端节点服务域名（默认域名仅支持 HTTP，自定义域名支持 HTTPS）。
3. 将 API base_url 中的域名替换为终端节点服务域名。

**跨地域私网访问**：
- **同境内/同境外**：启用跨地域端点（推荐）。
- **跨境**：通过云企业网（CEN）实现 VPC 互通。

## 安全存储业务空间

安全存储业务空间为企业提供数据完全隔离的运行环境，数据存储在客户自有的 ElasticSearch、AnalyticDB（ADB）和 OSS 中，通过私网连接访问。

> **注意**：安全存储业务空间需要联系商务人员申请开通，目前仅支持华北2（北京）地域。

### 配置流程

整体配置按以下顺序进行：

1. **创建安全存储业务空间**：在业务空间管理页面，选择空间类型为"安全存储空间"。
2. **配置终端节点**：创建反向终端节点，建立百炼与客户 VPC 的私网连接。专有网络需要包含可用区 G、H、L 中任意两个。
3. **配置可用区 IP**：创建 MSE 云原生网关（2 核 4G，2 节点），获取可用区 VIP 并填入百炼配置。
4. **配置私有网络资源**：
   - **OSS**：创建 Bucket 并设置标签 `bailian-safe-workspace-oss-access: ReadAndWrite`，配置跨域规则。
   - **ADB**：购买 AnalyticDB PostgreSQL 6.0 标准版实例，开启向量引擎优化。
   - **ES**：购买 Elasticsearch 7.10 内核增强版实例，将交换机网段添加到白名单。
5. **配置 MSE 网关路由**：创建服务（DNS 域名方式）和路由规则。
6. **激活空间**：确认所有资源配置无误后，在百炼控制台激活安全存储空间。

> **注意**：如果 OSS Bucket 或 ES 实例被释放，将导致安全存储空间不可用且无法恢复，需重新创建。停止计费（停服）则可通过续费恢复。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)

