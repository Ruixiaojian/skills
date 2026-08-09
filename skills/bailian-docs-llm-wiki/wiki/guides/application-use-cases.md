# application [use cases](use-cases.md)

阿里云百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将大模型问答能力嵌入网站、企业微信、微信公众号、钉钉等主流渠道，无需自行部署模型或构建后端服务。所有方案均基于百炼应用 API 和 AppFlow 连接流实现，支持灵活配置模型、知识库与交互样式。

## 支持的模型/功能

- **基础模型**：当前主流方案默认使用 `Qwen3.5-Plus`（见[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）或 `千问-Plus`（见[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），二者能力均衡，适用于通用客服问答；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（超低成本）等变体。
- **RAG 增强**：所有渠道均支持通过百炼知识库或本地知识库实现检索增强。云端知识库支持 PDF/DOCX/TXT/MD/PPTX/XLSX 等格式（单文件 ≤100 MB），自动解析并构建向量索引；本地 RAG 方案（见[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）则允许自定义文档切分、嵌入模型（如 GTE-Chinese-Large）及向量存储位置。
- **交互能力**：支持文本问答、预置问题、悬浮挂件（Web）、卡片消息（钉钉/企业微信）、被动/主动消息回复（微信公众号），并可扩展日志记录（SLS）、DeepSeek 思考过程展示、文档来源引用等高级功能。

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2–4 统一使用 `千问-Plus`。二者为同一模型的不同命名版本（Qwen3.5-Plus 即千问-Plus 的迭代命名），实际调用时以控制台显示的模型 ID 为准，开发者应以百炼控制台当前可用模型列表为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型值 |
|----------|--------|------|--------|
| **模型层** | `temperature` | 控制生成随机性 | `0.1–0.7`（客服场景建议 ≤0.3） |
| | `max_tokens` | 限制响应长度 | `512–2048`（Web/公众号建议 ≤1024） |
| | `top_p` | 核采样阈值 | `0.9–1.0` |
| **RAG 层** | `retrieval_top_k` | 召回片段数 | `3–5`（过多易引入噪声） |
| | `similarity_threshold` | 相似度过滤阈值 | `0.3–0.7`（0 表示不过滤） |
| | `retrieval_mode` | 检索模式 | `full_text` / `vector` / `hybrid` |
| **集成层** | `webhook_timeout` | 钉钉/企微回调超时 | `5s`（未认证公众号强制限制） |
| | `agent_id` / `app_id` | 各平台应用标识 | 由对应平台后台获取 |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置模型、Prompt（如 `你叫小助，帮助解答产品选购问题`）并发布。
2. **配置知识源**：
   - *云端知识库*：上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center) → 创建知识库 → 在应用配置中启用「必定调用」；
   - *本地知识库*：运行 `local_rag` 示例（见[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)），上传文件并创建 VectorStore。
3. **集成到目标平台**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>` 底部；
   - **企业微信/钉钉/微信公众号**：使用 AppFlow 对应模板（如 `tl-qiyeweixinself0813shzoa`）→ 配置平台凭证（AgentId/Secret 或 AppID）和百炼凭证（API Key + App ID）→ 发布连接流 → 在平台侧配置 Webhook URL 或机器人。
4. **验证与调优**：在目标渠道发起测试对话；若效果不佳，优先检查知识库召回质量、Prompt 引导逻辑及 `retrieval_top_k` 参数。

## 限制和注意事项

- **免费额度限制**：新用户享有百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费（见[新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)）。
- **平台合规约束**：
  - 微信公众号未认证时，消息响应必须 ≤5 秒，否则失败；建议选用 `qwen-turbo` 或精简 Prompt（见[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；
  - 企业微信要求配置可信 IP 白名单，且单个 IP 仅能绑定一个企业（见[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 钉钉机器人必须使用 HTTP 模式接收消息，Stream 模式不兼容（见[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）。
- **知识库限制**：云端知识库文件解析耗时 1–6 分钟；单次上传最多 200 个文件，总大小无明确上限但受内存限制；本地 RAG 方案不支持 >100 MB 文件（见[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **调试建议**：首次部署后务必通过 AppFlow「运行日志」排查失败步骤（如凭证错误、App ID 复制带空格、Webhook URL 未更新等），详见各文档「常见问题」章节。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


