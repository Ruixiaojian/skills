# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 连接流 + 私有知识库三要素实现开箱即用的智能问答能力，无需编码即可在 10 分钟内完成部署。核心逻辑为：用户请求经渠道（如网页/企微）触发 → AppFlow 调用百炼 API → 百炼应用执行 Prompt + 知识检索 → 返回结构化或自然语言响应。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `qwen-plus`（即文档中所述“千问-Plus”），其推理效果、成本与速度介于 `qwen-max` 和 `qwen-turbo` 之间，适用于通用客服问答场景 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **可选模型**：`qwen-max`（高精度）、`qwen-turbo`（低延迟）、`qwen3.5-plus`（文档 1 中明确指定，但其他文档未提及，需注意版本一致性）；`qwen-turbo` 特别适用于微信公众号未认证场景下的 5 秒响应限制 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。  
- **RAG 功能**：所有渠道均支持知识库引用，调用方式包括“必定调用”“按需调用”，支持相似度阈值、权重配置及全文引用/切片检索/自定义处理三种文件处理模式 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **本地 RAG 扩展**：提供独立的本地知识库构建方案，支持自定义文档切分、本地嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）、多类目/数据表管理，适用于对数据主权和切分策略有强控需求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 明确要求模型选择 `Qwen3.5-Plus`，而文档 2、3、4 均使用 `千问-Plus`（即 `qwen-plus`）。二者为不同模型版本，`Qwen3.5-Plus` 是更新迭代版本，建议以百炼控制台最新可用模型为准，避免因模型下线导致配置失效。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制生成随机性 | 0.1–0.7（客服场景建议 ≤0.3） |
| | `max_tokens` | 最大输出 token 数 | 512（简短回复可设为 256） |
| | `top_p` | 核采样阈值 | 0.95 |
| **RAG 层** | `retrieval_top_k` | 召回片段数 | 3–5（默认 3） |
| | `similarity_threshold` | 相似度阈值（0–1） | 0.3–0.7（值越高过滤越严） |
| | `context_window` | 携带上下文轮数 | 1–5（单轮问答建议设为 1） |
| **渠道层** | Web 悬浮挂件 `dragEnabled` | 是否启用图标拖拽 | `true`/`false` |
| | 企微/钉钉 `WebhookUrl` | AppFlow 生成的回调地址 | 由连接流自动分配，需填入对应平台后台 |

## 使用方式

1. **创建百炼应用**：统一入口为 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。  
2. **准备私有知识**：  
   - *云端知识库*：上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，创建知识库并绑定至应用 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
   - *本地知识库*：解压 `local_rag.zip`，上传文件至 `File/Unstructured` 或 `File/Structured`，通过“创建知识库”界面生成向量库 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
3. **配置渠道连接流**：  
   - *网站*：AppFlow 创建“AI助手”，导入百炼应用凭证，生成悬浮挂件脚本并嵌入 HTML。  
   - *企业微信/微信公众号/钉钉*：使用对应 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），配置平台凭证（AgentId/Secret 或 AppID）与百炼 API Key，获取 `WebhookUrl` 并填入各平台后台。  
4. **验证与日志**：  
   - 各渠道均支持直接对话测试（如点击网页右下角图标、在企微搜索应用、公众号发送消息）。  
   - 如需审计，可在 AppFlow 连接流中添加 SLS 日志节点，记录 `user_input`、`model_output`、`retrieved_docs` 等字段 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程所需资源；超出后按 token 计费，需关注 `qwen-max` 等高成本模型的调用量 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **渠道能力差异**：  
  - 微信公众号未认证时，仅支持被动回复且响应必须 ≤5 秒，建议搭配 `qwen-turbo` 或精简 Prompt；认证后支持主动消息与更长响应窗口。  
  - 钉钉机器人需开通 `Card.Streaming.Write` 权限，且 **消息接收模式必须为 HTTP 模式**（Stream 模式不兼容 AppFlow） [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。  
- **知识文件限制**：云端知识库单文档 ≤100MB / 1000 页，图片 ≤20MB；本地 RAG 方案受限于 Embedding API 限流，不建议上传 >100MB 文件 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **可信 IP 与域名**：企业微信/钉钉要求配置可信 IP 白名单；若使用非备案域名，需通过 AppFlow Nginx 代理或计算巢实例解决主体校验问题 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **调试建议**：上线前务必进行人工评测，重点验证知识召回准确性、Prompt 引导有效性及超时边界行为；错误排查优先检查 `应用ID` 是否含空格、`WebhookUrl` 是否填错、平台凭证是否过期。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


