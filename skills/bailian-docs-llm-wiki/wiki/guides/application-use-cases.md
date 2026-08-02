# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到多种主流业务场景中，包括企业微信、微信公众号、钉钉和网站等渠道。所有方案均基于低代码/无代码方式实现，通过 AppFlow 连接流串联第三方平台与百炼应用，并可选配 RAG [知识库](../concepts/knowledge-base.md)提升领域问答准确性。核心流程统一为：创建百炼应用 → 获取凭证 → 配置连接流 → 集成前端 →（可选）配置[知识库](../concepts/knowledge-base.md)。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（即文档中所述“千问-Plus”），适用于效果、速度与成本的均衡场景；`qwen-turbo` 适合对响应延迟敏感的场景（如未认证公众号的 5 秒限制）；`qwen-max` 适用于高精度复杂推理；最新文档已明确支持 `Qwen3.5-Plus` [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **核心功能**：
  - 智能体应用（Agent）：支持角色设定、多轮对话、工具调用（当前各文档未启用工具，仅聚焦问答）。
  - RAG 增强：通过[知识库](../concepts/knowledge-base.md)注入私域数据，支持 `.pdf`, `.docx`, `.txt`, `.xlsx` 等格式，单文件上限 100 MB 或 1000 页 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
  - 多端适配：提供针对企业微信、微信公众号、钉钉、Web 的专用连接流模板与配置指引。

> **注意**：文档 4 提供的本地 RAG 方案（`local_rag.zip`）与前述云端方案存在架构差异——其检索环节在本地执行，生成环节调用百炼 API，适用于需自主控制文档切分与嵌入模型的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。该方案不依赖 AppFlow，也不属于“开箱即用”的标准应用用例，而是面向有定制化需求的开发者。

## 关键参数

- **模型参数**：
  - `temperature`：控制输出随机性，值越高越发散（默认 0.7–1.0）。
  - `max_tokens`：限制生成长度，影响回答详略程度。
  - `history_rounds`：控制上下文记忆轮数（设为 1 表示不参考历史）。
- **RAG 参数**（适用于云端知识库）：
  - `retrieval_top_k`：召回片段数，通常设为 3–5。
  - `similarity_threshold`：相似度阈值，0 表示不限制，建议 0.3–0.6。
  - `retrieval_mode`：调用方式，`必定调用`（`must_call`）确保每次查询都触发知识检索。
- **文件处理参数**：在应用配置中可选择 `全文引用`、`切片检索` 或 `自定义处理`，影响知识召回粒度。

## 使用方式

1. **创建百炼应用**：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 创建智能体应用，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），并发布。
2. **获取凭证**：记录应用 ID 与 API Key（[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)）。
3. **配置连接流**：
   - 企业微信/钉钉/公众号：使用对应 AppFlow 模板，分别填入平台凭证（企业 ID + AgentId + Secret / Client ID + Client Secret / AppID）及百炼 API Key 和应用 ID。
   - 网站：在 AppFlow 的 **模型服务 > AI助手** 中创建，导入百炼模型并绑定凭证与应用 ID，再生成 Web 悬浮挂件脚本 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
4. **集成前端**：
   - 企业微信/钉钉/公众号：在各自平台后台配置 Webhook URL（即 AppFlow 生成的 `WebhookUrl`）及 Token/EncodingAESKey（企业微信）或完成 OAuth 授权（公众号/钉钉）。
   - 网站：将 AppFlow 生成的悬浮挂件脚本插入 HTML `<head>` 或 `<body>` 底部。
5. **（可选）配置知识库**：上传文件 → 创建知识库 → 在应用中启用并关联知识库 → 发布。

## 限制和注意事项

- **平台限制**：
  - 微信公众号未认证时，仅支持被动回复且响应超时为 5 秒，需选用 `qwen-turbo` 或精简 Prompt 以保障时效 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
  - 企业微信要求配置可信 IP 或自有域名（含备案），否则 API 接收消息校验失败；AppFlow 提供 Nginx 代理或计算巢一键部署方案解决此问题 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
  - 钉钉机器人必须配置为 **HTTP 模式**，Stream 模式不兼容 AppFlow [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
- **知识库限制**：云端知识库文件存储于新加坡区域；本地 RAG 方案受限于 Embedding API 限流，不建议上传 >100 MB 文件 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **调试与日志**：所有方案均支持在 AppFlow 中添加 SLS 日志节点记录对话，便于效果分析与问题排查 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **上线前必做**：正式发布前务必进行 [人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)，验证回答准确性，并根据结果优化 Prompt 或知识库。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)


