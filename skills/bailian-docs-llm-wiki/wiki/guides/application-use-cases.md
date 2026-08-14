# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库三要素实现，无需自行部署模型或维护推理服务。开发者可复用同一套百炼应用配置，在不同渠道间快速迁移和扩展。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。  
- **RAG 能力**：所有渠道均支持知识库接入，包括结构化（xlsx/csv）与非结构化（pdf/docx/txt 等）文档，支持向量检索与全文引用两种模式 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **本地 RAG 扩展**：除云端知识库外，还提供本地知识库构建方案，支持自定义文档切分、嵌入模型替换（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及参数调优 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **消息交互能力**：支持文本问答、卡片消息（钉钉）、悬浮挂件（网站）、被动/主动回复（微信公众号）等多种交互形式。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均使用 `千问-Plus`。当前控制台实际可用模型列表以 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面为准，`Qwen3.5-Plus` 为较新版本，若未显示则需确认地域与权限；旧文档中“千问-Plus”可能指向 `qwen-plus` 的历史命名，二者应视为同一模型系列。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制输出随机性，建议 0.1–0.6 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中 `chat.py` 或百炼应用配置页 |
| | `max_tokens` | 限制生成长度，影响响应详略 | 同上 |
| | `top_p` / `top_k` | 影响采样范围，通常保持默认 | 百炼应用配置页高级设置 |
| **RAG 层** | `retrieval_top_k` | 召回片段数，默认 3–5 | 百炼应用「知识库」配置页或本地 RAG 应用界面 |
| | `similarity_threshold` | 相似度阈值，0 表示不过滤 | 同上；值越接近 1 过滤越严格 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（仅本地 RAG 可调） | `create_kb.py` 或 LlamaIndex 配置 |
| **渠道层** | `WebhookUrl` | AppFlow 生成的回调地址，用于企业微信/钉钉/公众号 | AppFlow 连接流发布后获取 |
| | `IP 白名单` | 企业微信/钉钉要求的可信 IP，需手动填入其后台 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中 4.2 节 |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。  
2. **准备知识库（可选但推荐）**：  
   - *云端*：上传文件至「数据连接」或「文件」页签 → 创建知识库 → 在应用中启用「必定调用」；  
   - *本地*：解压 `local_rag.zip` → 安装依赖 → 上传文件至 `File/Unstructured` 或 `File/Structured` → 创建知识库 → 在 Gradio 界面加载使用。  
3. **配置渠道连接流**：  
   - 网站：AppFlow 创建「AI助手」→ 关联百炼应用 → 获取悬浮挂件脚本 → 插入 HTML；  
   - 企业微信/钉钉/公众号：AppFlow 使用对应模板 → 授权凭证（企业 ID/AgentId/Secret 或 AppID）→ 填写百炼 API Key 与应用 ID → 发布并配置 Webhook 或机器人。  
4. **验证与日志**：各渠道均支持对话测试；如需审计，可在 AppFlow 连接流中添加 SLS 日志节点记录对话 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中 5.3 节。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **微信公众号认证要求**：未认证订阅号仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口；若无法认证，需在 Prompt 中强调「简短回答」或切换至 `qwen-turbo` 模型提速 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。  
- **钉钉机器人模式限制**：仅支持 HTTP 模式接收消息，Stream 模式不可用，否则无法返回响应 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。  
- **文件处理限制**：云端知识库单文档 ≤ 100 MB 或 1000 页，图片 ≤ 20 MB；本地 RAG 不建议上传 > 100 MB 文件，以防 Embedding API 限流超时 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **可信 IP 冲突**：企业微信报错「第三方服务商 IP」时，需通过 ECS 或 Nginx 代理转发，并将代理 IP 加入企业微信可信 IP 列表 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中常见问题部分。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


