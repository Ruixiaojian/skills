# security and compliance

阿里云百炼围绕"合规资质、身份与空间权限、内容安全护栏、传输加密、私网接入、安全存储业务空间"6 个维度提供安全合规能力。开发者按需组合即可满足从模型备案、生产环境隔离到端到端加密的全链路安全要求；本页汇总相关功能的配置入口、关键参数与已知限制。

## 合规资质、算法备案与隐私

百炼以无保留意见通过 SOC 2 审计，所有训练 / 应用调用数据均采用 **AES-256** 加密落盘，且**不会被用于模型训练**，详见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

接入百炼的大模型均已完成《互联网信息服务算法备案》（生成合成类）。常用备案号摘录：

| 模型 | 算法备案号 | 大模型备案号 |
| --- | --- | --- |
| 通义千问 | 网信算备330110507206401230035号 | ZheJiang-TongYiQianWen-20230901 |
| 通义万相（图像） | 网信算备330110507206401230027号 | Shanghai-TongYiWanXiang-202410090024 |
| 通义万相（视频） | 网信算备330106003156001240091号 | — |
| DeepSeek | 网信算备110108970550101240011号 | Beijing-DeepseekChat-202404280016 |
| Moonshot | 网信算备110108896786101240023号 | Beijing-MoonShot-20231016 |
| 可灵 AI | 网信算备110108413760701250055号 | Beijing-KeLing-202409250032 |

完整列表（含智谱、MiniMax、阶跃、Vidu、Tripo、PixVerse、Xiaomi MiMo 等）以及免责声明请见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

若需将基于上述模型构建的 APP / 小程序上架，开发者还需根据《生成式人工智能服务管理暂行办法》自行完成应用层备案：

- **面向 C 端且无舆论属性**：提供算法备案信息 + 应用主体与阿里云的合作协议（向商务经理获取）。
- **面向 C 端且有舆论属性**：在上述基础上叠加企业自主完成的安全评估报告与算法备案。
- **企业内部使用**：不直接受办法约束，但仍需关注数据安全与保密合规。

> **注意**：百炼仅作为"服务技术支持者"提供模型备案信息，应用 / 小程序开发者仍是法规定义的"服务提供者"，需自行履行内容审核、用户保护、数据安全、标识规范等全部法定义务。详见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 身份、业务空间与 API Key 权限

百炼的最小权限管理单元是**业务空间**，按地域划分，不可跨地域。共有三类角色：

| 角色 | 跨空间管理 | 模型授权 / 限流 | 用户与页面管理 | API Key 管理 |
| --- | --- | --- | --- | --- |
| 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户） | 支持 | 支持 | 支持 | 支持 |
| 业务空间管理员（被授予某空间管理员权限的 RAM 用户） | 不支持 | 不支持 | 支持（限当前空间） | 支持（限当前空间） |
| 普通用户 | 不支持 | 不支持 | 不支持 | 不支持 |

模型级管控分三类：**模型调用 + 限流（请求数 / Token 数）**、**模型训练（含调优后部署）**、**模型部署**。需要注意默认业务空间无法做模型授权与限流，所有可用模型默认开放。完整开关位置与生产环境的空间规划 / 限流建议（按环境或业务线划分、按比例分配 QPM）见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

**API Key 关键约束**：

- 一个 API Key 只归属一个地域 + 一个业务空间 + 一个用户，**不可转移**；可调用功能与归属空间权限保持一致，不受控制台权限影响。
- 主账号 API Key 不会因任何操作失效（除主动删除）；RAM 用户 API Key 在用户被移出空间时会失效，重新加入可恢复；在 RAM 控制台删除账号则永久失效。
- 自 **2026 年 3 月 25 日**起，**华北 2（北京）** 地域新创建的 API Key 一律归属主账号。
- 华北 2（北京）地域支持为 API Key 设置 **IP 访问白名单**。

**OpenAPI 接口权限**：RAM 用户默认无权调用应用 / 知识库 / 长期记忆等 OpenAPI，需主账号在 RAM 控制台为其加 `AliyunBailianDataFullAccess`（全量）或 `AliyunBailianDataReadOnlyAccess`（只读）。

## AI 安全护栏（内容审核）

大模型自带合规检查；如需更强的入参 / 出参合规识别（涉黄、涉政、广告等），可接入 **AI 安全护栏服务**。开通后在调用请求头中加入：

```
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

- Python OpenAI SDK：`extra_headers={"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'}`。
- DashScope Python SDK：`headers={"X-DashScope-DataInspection": '{"input":"cip", "output":"cip"}'}`。
- Java OpenAI SDK：`.putAdditionalHeader("X-DashScope-DataInspection", "{...}")`。

命中拦截时返回 HTTP 400 + `data_inspection_failed`（OpenAI 协议）或 `DataInspectionFailed`（DashScope 协议）。开通步骤、计费、模型支持范围与多语言完整示例见 [输入输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 传输加密：端到端加密推理

当请求经公网传输或涉及敏感信息时，可对请求体 `input` 进行加密。百炼采用 **AES 对称加密数据 + RSA 公钥加密 AES 密钥**的混合方案，推理链路全程加密，仅在向量召回与模型推理瞬间解密。

### 方式 A：DashScope SDK 自动加密（推荐）

- **Java**：`GenerationParam.builder().enableEncrypt(true).build()`。
- **Python**：`dashscope.Generation.call(..., enable_encryption=True)`。
- SDK 自动获取公钥、生成密钥、加解密，返回明文响应。
- 限制：仅 Java / Python SDK；不支持自定义密钥。

完整示例与限制详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

### 方式 B：HTTP 手动加密

适用于其他语言或需要自定义密钥的场景，仅支持 **DashScope Endpoint**（OpenAI 兼容协议不支持此机制）。流程：

1. 调用 `GET /api/v1/public-keys/latest`（Header `Authorization: Bearer <key>`）获取 `public_key` 和 `public_key_id`，详见 [获取 RSA 的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
2. 本地生成 AES 密钥（128 / 192 / 256 位）与 IV。
3. AES 加密 `input` 内容；RSA 加密 AES 密钥。
4. 添加请求头 `X-DashScope-EncryptionKey`，内含 `public_key_id`、`encrypt_key`、`iv` 的 JSON 字符串。
5. 收到响应后用同一 AES 密钥解密。

> **注意**：OpenAI 兼容（Chat Completions / Responses API）的 Endpoint **不支持**该加密机制；如需端到端加密请使用 DashScope SDK / DashScope Endpoint，或改用下文 PrivateLink。

## 私网接入百炼 API（PrivateLink）

如果希望调用流量完全留在阿里云内网，可通过 **PrivateLink** 创建接口终端节点：

- 服务地域：**华北 2（北京）**、**新加坡**；美国（弗吉尼亚）暂不支持私网访问。
- 终端节点服务名：`com.aliyuncs.dashscope`。
- 需要在安全组放行 **80（HTTP）** 与 **443（HTTPS）** 入方向；建议至少选两个可用区交换机以实现高可用。
- 调用时把 `dashscope.aliyuncs.com` 替换为接口终端节点提供的服务域名（默认仅 HTTP，自定义域名支持 HTTPS）。
- 跨地域接入：同境内 / 同境外推荐"启用跨地域端点"；跨境（如北京 VPC ↔ 新加坡百炼）需通过 CEN 跨地域 VPC 互通。

完整操作与多语言调用示例见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 安全存储业务空间

"安全存储业务空间"将百炼应用与 OSS / ADB / ES 之间的所有数据交互限制在客户自有 VPC 内，需向商务申请开通。完整链路涉及四步配置，**必须按顺序执行**：

1. **配置反向终端节点**：在 VPC 终端节点控制台选择"反向终端节点"，关联系统生成的"百炼公共云生产环境-北京站点-安全存储空间专网通道接入点"服务，VPC 需位于"华北 2（北京）"且使用可用区 G / H / L 中任意两个；安全组无需配置出入规则、也不要放入其他云组件。详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
2. **配置可用区 IP**：创建一个 2 核 4G、2 节点、私网类型的 **MSE 云原生网关**（启用 TLS 硬件加速、至少两个可用区），从其 NLB 实例获取每个可用区的 VIP 和交换机网段，回填百炼"可用区 IP 配置"页面，并把这些 VIP 加入反向终端节点关联的安全组入方向。详见 [配置可用区 IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)。
3. **配置私网资源（OSS / ADB / ES）**：
    - **OSS Bucket**：必须打上标签 `bailian-safe-workspace-oss-access=ReadAndWrite`；并为 `*bailian.console.aliyun.com` 配置 CORS（GET / POST / PUT / DELETE）。
    - **ADB PostgreSQL**：建议高可用版 + 向量引擎优化，VPC 与可用区须与反向终端节点一致。
    - **ElasticSearch**：内核增强版 7.10，需把交换机网段加入 VPC 私网访问白名单。
4. **配置 MSE 路由并激活**：在 MSE 网关创建 DNS 类型的服务（指向 ES 的私网域名 + 端口、TLS 关闭），再创建路径为 `/` 的单服务路由，发布后回到百炼"资源配置"页面单击**激活**。详见 [配置 MSE 云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) 与 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。

> **注意**：OSS Bucket 停止服务会令安全存储空间不可用（可恢复）；**OSS Bucket 或 ES 被释放**则空间不可恢复，需重新创建。ES 停止计费时安全存储空间、知识库、审计日志、历史记录等模块均不可用。

## 限制与注意事项汇总

- **默认业务空间**无法做模型调用 / 训练 / 部署的限流与开关控制。
- **API Key 主动删除后无法恢复**；RAM 账号被移出空间会失效，被删除则永久失效。
- **OpenAPI 仅主账号可授权 RAM 用户访问**（`AliyunBailianDataFullAccess` / `AliyunBailianDataReadOnlyAccess`）。
- AI 安全护栏目前仅覆盖文本与图片类模型；具体支持范围与计费随产品迭代变化，以官方文档为准。
- DashScope SDK 自动加密仅 Java / Python；其他语言或自定义密钥需走 HTTP 手动加密，且仅 DashScope Endpoint 可用。
- PrivateLink 私网接入暂不支持美国（弗吉尼亚）地域；安全组必须放行 80 / 443 端口。
- 安全存储业务空间所有底层资源（VPC、可用区、安全组、MSE 网关、ES 网段）必须严格一致，任一处不对齐都会导致激活失败。

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
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


