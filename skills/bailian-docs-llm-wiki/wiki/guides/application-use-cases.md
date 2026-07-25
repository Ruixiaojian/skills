# application [use cases](use-cases.md)

百炼平台支持多种主流企业通信与内容平台的 AI 助手集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构：通过百炼创建大模型问答应用作为推理后端，结合 AppFlow 低代码连接流完成渠道对接，并可选配私有知识库提升领域回答准确性。核心流程为「创建百炼应用 → 配置渠道凭证 → 绑定知识库 → 发布上线」，全程无需编码，新用户可依托免费额度快速验证效果。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `qwen-plus`（即文档中所述“千问-Plus”或“Qwen3.5-Plus”），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **可选模型**：`qwen-max`（高精度）、`qwen-turbo`（低延迟）亦被明确支持，尤其在微信公众号等有 5 秒响应限制的渠道中，`qwen-turbo` 是规避超时的关键选项 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。  
- **本地 RAG 扩展**：除云端托管方案外，还提供基于本地知识库的完整 RAG 应用模板，支持自定义文档切分、嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及模型参数调优 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
> **注意**：文档 1 中提及的 `Qwen3.5-Plus` 与文档 2–4 中统一使用的 `千问-Plus` 实际指向同一模型版本，但命名不一致易引发混淆；开发者应以控制台实际可选模型列表为准，避免硬编码模型名。

## 关键参数

- **身份凭证**：所有集成均需 `App ID`（百炼应用唯一标识）与 `API Key`（百炼密钥），二者在百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 和 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面获取。  
- **渠道凭证**：  
  - 网站：无需额外凭证，依赖悬浮挂件脚本自动注入；  
  - 企业微信：需 `企业ID`、`AgentId`、`Secret`；  
  - 微信公众号：需 `AppID`（认证状态影响工作流选择）；  
  - 钉钉：需 `Client ID`、`Client Secret`。  
- **知识库配置**：  
  - **调用方式**：`必定调用`（强制检索）、`按需调用`（仅当问题触发关键词时）；  
  - **召回控制**：`相似度阈值`（过滤低相关片段）、`召回片段数`（控制参考文本量）；  
  - **存储类型**：`ADB-PG`（集中管理多应用向量）或默认向量库。  

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `qwen-plus`）→ 配置 Prompt（例如 `"你叫小助，帮助解答产品选购问题"`）→ 发布。  
2. **配置渠道连接流**：  
   - 访问 AppFlow 控制台 → 使用预置模板（如[企业微信自建应用大模型自动回复](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-qiyeweixinself0813shzoa?from=solution)）→ 分步配置渠道凭证（企业微信/公众号/钉钉）与百炼凭证 → 填写百炼 `App ID` → 发布并获取 `WebhookUrl` 或悬浮脚本。  
3. **渠道侧配置**：  
   - 网站：将 AppFlow 生成的悬浮挂件脚本插入 HTML `<head>` 或 `<body>` 底部；  
   - 企业微信/钉钉/公众号：在对应平台后台填写 `WebhookUrl`、`Token`、`EncodingAESKey`（企业微信）或启用服务器配置（公众号）。  
4. **添加私有知识**（可选）：  
   - 上传文件至百炼 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；  
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库；  
   - 在应用配置页绑定知识库，设置调用方式后重新发布。  

## 限制和注意事项

- **响应时效约束**：微信公众号未认证时，被动回复接口严格限制响应时间 ≤5 秒；超时将导致消息丢失。此时必须选用 `qwen-turbo` 或优化 Prompt（如添加 `"请总是给出简短的回答"`）[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。  
- **凭证安全要求**：企业微信要求可信 IP 白名单，若使用第三方代理（如非阿里云 ECS），需通过 AppFlow 内网代理配置并手动添加代理机器公网 IP 至企业微信可信 IP 列表 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **文件处理限制**：百炼云端知识库单文档最大 100MB 或 1000 页，图片单张 ≤20MB；本地 RAG 方案则建议避免上传 >100MB 文件以防 Embedding API 限流 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **认证依赖**：微信公众号未认证时无法同时启用服务器配置与自定义菜单，需通过微信 API 接口重建菜单 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


