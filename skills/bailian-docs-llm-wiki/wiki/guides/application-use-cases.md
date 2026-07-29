# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的大模型应用落地，核心围绕“模型能力+私有知识+渠道集成”展开。开发者可基于百炼构建 RAG 应用，并通过 AppFlow 低代码连接主流企业通讯与网站渠道（如网站、企业微信、微信公众号、钉钉），实现 7×24 小时智能客服、私域问答等能力。所有方案均复用统一的百炼应用配置与知识库管理能力，仅需一次构建，多端部署。

## 支持的模型/功能

- **基础模型**：支持 Qwen-Max、Qwen-Plus、Qwen-Turbo、Qwen3.5-Plus 等通义千问系列商业模型；其中 Qwen-Plus 被多个用例推荐为效果、速度与成本的均衡选择 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 增强**：所有渠道集成均依赖百炼知识库（Knowledge Base）实现私有知识注入，支持文档上传、切片检索、相似度阈值与权重配置 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地 RAG 可选**：除云端知识库外，也支持完全本地化部署的 RAG 架构，允许用户自主管理文档切分、选用本地或云端 embedding 模型，并对接百炼大模型 API 进行生成 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均使用 `千问-Plus`（即 Qwen-Plus）。二者为不同版本模型，能力与性能存在差异。实际部署时应以控制台当前可用模型列表为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值 |
|----------|--------|------|-----------|
| **模型层** | `temperature` | 控制输出随机性 | 0.1–0.7（生产环境建议 ≤0.3） |
| | `max_tokens` | 限制生成长度 | 512–2048 |
| | `top_p` | 核采样阈值 | 0.9–1.0 |
| **RAG 层** | `retrieval_top_k` | 召回文档片段数 | 3–5（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中明确提及） |
| | `similarity_threshold` | 相似度过滤阈值 | 0.3–0.8（0 表示不过滤） |
| | `retrieval_mode` | 检索模式 | `full_text` / `vector` / `hybrid`（知识库配置页可选） |
| **渠道层** | `webhook_url` | AppFlow 生成的回调地址 | 由连接流发布后自动生成 |
| | `call_mode` | 知识调用方式 | `must_call`（必定调用）、`auto_call`（按需调用） |

## 使用方式

1. **统一建模**：在百炼控制台创建「智能体应用」，配置 Prompt（如角色设定）、选择模型，并发布应用；
2. **统一纳管知识**：通过「数据连接」上传文件 → 「知识库」创建并关联 → 在应用配置中启用「必定调用」；
3. **渠道解耦集成**：
   - **网站嵌入**：使用 AppFlow 创建「AI助手」→ 配置 Web 集成 → 复制悬浮挂件脚本插入 HTML；
   - **IM 渠道（企微/公众号/钉钉）**：使用 AppFlow 预置模板 → 授权对应平台凭证（AppID/AgentId/Client ID + Secret）→ 绑定百炼应用 ID → 发布连接流 → 在对应平台后台配置 Webhook 或机器人；
4. **验证与日志**：各渠道均支持对话测试；如需审计，可在 AppFlow 连接流中追加 SLS 日志节点记录原始请求与响应。

## 限制和注意事项

- **免费额度适用性**：所有用例均声明新用户免费额度可覆盖初始资源消耗，但超出后按 token 计费；需注意不同模型的 token 成本差异（如 Qwen-Max > Qwen-Plus > Qwen-Turbo）；
- **文件上传限制**：云端知识库单文档最大 100 MB 或 1000 页，图片单张 ≤20 MB，最多 200 个文件；本地 RAG 方案无此限制，但受本地磁盘与 embedding API 限流约束 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
- **认证与安全要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口；
  - 企业微信/钉钉需配置可信 IP 白名单，且同一 IP 不可复用于多个企业（否则触发服务商校验失败）；
  - 钉钉机器人必须使用 HTTP 模式，Stream 模式不兼容 AppFlow；
- **调试建议**：首次集成失败时，优先检查 AppFlow 运行日志、Webhook URL 是否正确、API Key 与应用 ID 是否复制带空格、平台凭证是否为主管理员授权。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


