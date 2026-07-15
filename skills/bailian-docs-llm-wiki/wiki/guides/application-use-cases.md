# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成至多种主流企业级通信与网站渠道，构建面向客户、员工或私域用户的 AI 助手。典型场景包括在网站、企业微信、微信公众号、钉钉等平台嵌入 RAG 增强的智能问答服务，全程无需编码，依托 AppFlow 实现低代码连接，结合百炼应用配置与知识库管理完成端到端交付。所有方案均兼容新用户免费额度，适用于快速验证与轻量级生产部署。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）或 `千问-Plus`（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），该模型在效果、速度与成本间取得平衡；亦支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）等变体，适用于不同响应 SLA 要求。
- **RAG 增强能力**：所有用例均依赖百炼知识库实现私有知识注入，支持 PDF/DOCX/TXT/Excel 等格式上传（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），并提供“必定调用”“按需调用”等知识引用策略。
- **本地化 RAG 选项**：对于需完全控制文档切分、嵌入模型与向量存储的场景，可采用 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 方案，支持自定义切分逻辑、本地部署嵌入模型（如 GTE-Chinese-Large）及 Gradio API 对接。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus`。二者为不同代际模型，`Qwen3.5-Plus` 是更新版本，具备更强推理与多轮对话能力；若需一致性建议优先选用 `Qwen3.5-Plus`，除非业务明确要求兼容旧版 `千问-Plus` 接口行为。

## 关键参数

- **百炼应用 ID 与 API Key**：所有集成方案必需，用于 AppFlow 或客户端调用百炼推理服务（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 第 1.2 节）。
- **平台凭证**：
  - 企业微信：需 `企业 ID`、`AgentId`、`Secret`（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 第 2.2 节）；
  - 微信公众号：需 `AppID` 及管理员扫码授权（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 第 2 节）；
  - 钉钉：需 `Client ID` 与 `Client Secret`（见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 第 2.2 节）；
  - 网站嵌入：仅需前端脚本，无后端凭证（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 第 3.2 节）。
- **RAG 参数**（本地 RAG 场景）：包括 `召回片段数`、`相似度阈值`、`温度`、`最大回复长度` 等，可在 `chat.py` 中直接调整（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 第三节）。

## 使用方式

1. **创建百炼应用**：统一通过百炼控制台 → 应用管理 → 创建智能体应用，配置 Prompt（如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`）并发布。
2. **配置知识库**：上传文档 → 创建知识库 → 在应用配置中绑定知识库并设为“必定调用”（各文档均采用此流程，细节略有差异：文档 1 使用“数据连接”页签，文档 2/3/5 使用“文件”或“知识库”页签）。
3. **集成至目标平台**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；
   - **企业微信/钉钉/微信公众号**：使用 AppFlow 预置模板 → 配置平台凭证与百炼凭证 → 获取 Webhook URL → 在对应平台后台完成消息接收配置（如企业微信的“API接收消息”、钉钉的“HTTP模式机器人”、公众号的“服务器配置”）。
4. **验证与日志**：各平台均支持直接对话测试；如需审计，可通过 AppFlow 添加 SLS 日志节点记录对话（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 第 4 节）。

## 限制和注意事项

- **认证要求**：微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用主动消息能力（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 第 2 节说明）。
- **可信 IP 与域名**：企业微信/钉钉要求配置可信 IP 白名单；若使用 AppFlow Webhook，需通过计算巢 Nginx 代理或自有域名解析解决主体校验问题（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) “常见问题”章节）。
- **文件限制**：云端知识库单文档上限为 100 MB 或 1000 页；本地 RAG 方案亦不建议上传超 100 MB 文件（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 第三节）。
- **模型兼容性**：`Qwen3.5-Plus` 为文档 1 所指定，其余文档未更新至该版本，开发者需自行确认控制台可用模型列表，避免因模型下线导致配置失败。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


