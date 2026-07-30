# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业通讯与内容平台（如网站、企业微信、微信公众号、钉钉），构建面向终端用户的 AI 助手或智能客服。所有方案均基于统一的 RAG 架构：通过百炼创建大模型问答应用作为推理后端，利用 AppFlow 无代码连接器完成渠道对接，并可选配私有知识库提升领域回答准确性。核心流程高度一致，仅在渠道配置细节上存在差异。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `qwen-plus`（即文档中所述“千问-Plus”或“Qwen3.5-Plus”），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **可选模型**：本地 RAG 方案明确支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 三档商业模型，开发者可根据延迟敏感度与质量要求灵活切换 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **关键功能**：
  - 多渠道嵌入（Web 悬浮窗、企业微信应用、微信公众号消息、钉钉机器人）
  - RAG 知识增强（支持文档上传、向量索引、检索调用）
  - 无代码流程编排（AppFlow 连接流模板）
  - 对话日志记录（SLS 日志服务集成）

> **注意**：文档 1 中提及的 `Qwen3.5-Plus` 与文档 2、3、4 中统一使用的 `千问-Plus` 实为同一模型（当前百炼控制台显示名称为 `qwen-plus`）。若控制台未列出 `Qwen3.5-Plus`，请以 `qwen-plus` 为准，避免因版本命名不一致导致配置失败。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值建议 |
|----------|--------|------|-----------|
| **模型层** | `temperature` | 控制生成随机性 | 0.1–0.5（客服场景推荐低值） |
| | `max_tokens` | 限制回复最大 token 数 | 512–1024（平衡完整性与延迟） |
| | `top_p` | 核采样阈值 | 0.8–0.95 |
| **RAG 层** | `retrieval_top_k` | 检索召回片段数 | 3–5（过多易引入噪声） |
| | `similarity_threshold` | 相似度过滤阈值 | 0.3–0.7（0 表示不过滤） |
| | `retrieval_mode` | 调用方式 | `必定调用`（确保知识生效）或 `按需调用` |
| **渠道层** | Web 悬浮窗 | 图标、预置问题、拖拽开关 | 按品牌规范配置 |
| | 企业微信/钉钉/公众号 | Webhook URL、[Token](../concepts/token.md)、EncodingAESKey、可信 IP 白名单 | 严格匹配 AppFlow 输出值 |

## 使用方式

1. **创建百炼应用**  
   进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」→ 配置模型（`qwen-plus`）、Prompt（如 `你叫小助，帮助解答产品选购问题`）→ 发布应用 → 记录 **应用ID** 与 **API Key**。

2. **配置知识库（可选但推荐）**  
   - 上传文件：支持 `.pdf`, `.docx`, `.txt`, `.xlsx` 等格式（单文件 ≤100MB）[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
   - 创建知识库：在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面选择「标准版」→ 关联上传文件 → 设置索引类型（推荐 `ADB-PG` 用于多应用共享）→ 在应用配置中启用并设为「必定调用」。

3. **渠道集成（任选其一）**  
   - **网站**：使用 AppFlow 创建「AI助手」→ 导入百炼应用 → 获取悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>` 底部。  
   - **企业微信/钉钉/微信公众号**：使用对应 AppFlow 模板 → 授权渠道凭证（企业 ID/AgentId/Secret 或 AppID/AppSecret 或 Client ID/Secret）→ 填写百炼 API Key 与应用ID → 获取 Webhook URL → 在渠道后台配置接收地址与可信 IP。

4. **验证与日志**  
   - 直接在目标渠道发起对话测试。  
   - 如需分析效果，可在 AppFlow 连接流中添加 SLS 日志节点，记录输入、输出、耗时等字段。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **微信公众号认证约束**：未认证公众号仅支持被动回复（5秒超时限制），已认证方可使用客户消息接口（无超时）；若未认证，需在 Prompt 中强调简洁回复或选用 `qwen-turbo` 加速 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **钉钉机器人模式限制**：AppFlow 仅支持 HTTP 模式 Webhook，**不可选择 Stream 模式**，否则无法返回消息 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
- **本地 RAG 文件大小限制**：Embedding API 有速率限制，单文件建议 ≤100 MB；超大文件应预切分或改用云端知识库 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **可信 IP 冲突**：企业微信要求每个可信 IP 仅归属单一企业；若复用 IP，需通过 ECS 或 Nginx 代理转发并配置独立白名单 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


