# application [use cases](use-cases.md)

百炼平台支持多种主流企业通讯与网站渠道的 AI 助手快速集成，核心模式为“大模型应用 + RAG 知识增强 + 低代码连接流”，适用于客服、内部支持、产品咨询等场景。所有方案均基于百炼托管的大模型 API 和 AppFlow 的可视化编排能力，无需自行部署模型或编写后端逻辑。

## 支持的模型/功能

- **基础模型**：统一推荐使用 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2–4），该模型在效果、速度与成本间取得平衡，适用于通用问答任务；`qwen-turbo` 可用于对响应延迟敏感的场景（如未认证公众号的 5 秒限制），但需权衡生成质量 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **RAG 增强**：所有用例均支持通过知识库注入私有文档（PDF/DOCX/TXT 等），知识检索策略包括“必定调用”“按需调用”及相似度阈值控制，且支持全文引用、切片检索或自定义处理 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地 RAG 模式**：除云端知识库外，还提供完全本地化部署方案，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及灵活参数调优，适用于对数据不出域有强要求的场景 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中指定模型为 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`。二者为同一模型的不同命名（Qwen3.5-Plus 即千问-Plus 的最新迭代版本），实际调用时以控制台当前可用模型列表为准，建议优先选用 `Qwen3.5-Plus` 以获得最佳效果。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值 |
|----------|--------|------|-----------|
| **模型层** | `temperature` | 控制输出随机性 | `0.1–0.5`（客服场景建议偏低） |
| | `max_tokens` | 最大生成长度 | `512`（兼顾完整性与响应速度） |
| **RAG 层** | `top_k`（召回片段数） | 检索返回的最相关段落数 | `3–5`（过多易引入噪声） |
| | `similarity_threshold` | 过滤低相关片段的阈值 | `0.3–0.7`（默认 `0.5`） |
| | `retrieval_mode` | 知识调用方式 | `must_use`（必定调用）、`on_demand`（按需） |
| **连接流层** | `WebhookUrl` | AppFlow 生成的回调地址 | 需配置到微信/企微/钉钉后台 |
| | `Token` & `EncodingAESKey` | 企微消息加解密凭证 | 由 AppFlow 创建连接凭证时生成 |

## 使用方式

1. **创建百炼应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择 `Qwen3.5-Plus` 或 `千问-Plus`，配置 Prompt（如 `你叫小助，帮助解答产品选购问题`），发布前务必测试基础问答能力。
2. **配置知识库（可选但推荐）**：
   - 上传文件至百炼「文件」或「数据连接」页签；
   - 在「知识库」页签创建标准版知识库，关联上传文件；
   - 在应用配置中启用知识库并设为 `必定调用`。
3. **构建连接流**：
   - 进入 AppFlow 控制台，使用对应平台模板（[网站助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[微信公众号](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)、[企业微信](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[钉钉](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）；
   - 分步配置：添加微信/企微/钉钉凭证 → 添加百炼 API Key 凭证 → 填写百炼应用 ID → 发布连接流。
4. **渠道侧集成**：
   - **网站**：复制 Web 集成脚本，粘贴至 HTML `<head>` 或 `<body>` 底部；
   - **微信公众号**：完成服务器配置，将 WebhookUrl 填入开发者后台；
   - **企业微信/钉钉**：在应用后台配置接收消息地址（HTTP 模式）或机器人 Webhook，并设置可信 IP/域名。

## 限制和注意事项

- **免费额度与计费**：新用户享有免费额度，覆盖教程全部资源消耗；额度用尽后按 token 计费，详见 [新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota) [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **微信认证约束**：未认证公众号受 5 秒响应限制，超时即失败；建议完成认证或改用 `qwen-turbo` 模型提速 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **文件限制**：云端知识库单文件 ≤100 MB、≤1000 页；本地 RAG 方案不建议上传 >100 MB 文件，以防 Embedding API 限流超时 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **域名与 IP 安全**：企业微信/钉钉要求配置可信域名/IP，若使用 AppFlow 默认域名失败，需通过计算巢 Nginx 代理或自有 ECS 转发解决 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **日志与可观测性**：所有连接流均可扩展 SLS 日志节点，记录对话原始输入/输出，用于效果分析与问题排查 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


