# application [use cases](use-cases.md)

百炼平台支持多种主流企业通讯与网站渠道的 AI 助手快速集成，核心模式为“大模型应用 + RAG 知识增强 + 低代码连接流”。所有方案均基于统一的百炼大模型应用作为推理后端，通过 AppFlow 实现与外部渠道（如网站、企业微信、微信公众号、钉钉）的零编码对接，并支持私有知识库注入以提升领域回答准确性。开发者可复用同一套模型配置和知识库，灵活部署至不同触点。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 明确指定）或 `千问-Plus`（文档 2、3、4 均采用），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景。`qwen-turbo` 可用于对响应延迟敏感的场景（如未认证公众号的 5 秒限制），但需权衡生成质量 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **RAG 能力**：所有集成方案均依赖百炼知识库实现私域知识增强，支持 PDF、DOCX、TXT、XLSX 等格式（文档 2、3、4、5 均明确列出），最大单文件 100 MB（文档 2、5 提及）。
- **扩展能力**：支持对话日志记录至 SLS（文档 2、3、4 均提供详细步骤）、卡片消息渲染（文档 4）、DeepSeek 思考过程展示（文档 4）等高级功能。

> **注意**：文档 1 指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。当前控制台中 `Qwen3.5-Plus` 是 `千问-Plus` 的演进版本，二者 API 兼容，但 `Qwen3.5-Plus` 在中文理解与指令遵循上略有提升。建议新项目优先选用 `Qwen3.5-Plus`，存量项目无需强制迁移。

## 关键参数

- **身份凭证**：所有方案均需百炼 `App ID` 与 `API Key`（文档 1、2、3、4 均要求），用于 AppFlow 调用模型服务；各渠道还需对应平台凭证（如企业微信的 `CorpID/AgentID/Secret`、钉钉的 `Client ID/Client Secret`、微信公众号的 `AppID`）。
- **知识库配置**：
  - 调用方式：推荐设为 `必定调用`（文档 1、2、3、4 均采用），确保知识检索始终生效；
  - 向量存储：可选 `ADB-PG` 以集中管理多应用向量数据（文档 1、2、3、4 均提及）；
  - 文档处理：支持 `全文引用`、`切片检索`、`自定义处理`（文档 2 明确列出）。
- **RAG 参数（本地部署场景）**：文档 5 提供细粒度控制，包括召回片段数、相似度阈值、温度、最大回复长度等，适用于需深度调优的定制化部署 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 使用方式

1. **创建百炼应用**：在百炼控制台选择“智能体应用”，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`），并发布应用（文档 1、2、3、4 均含此步骤）。
2. **配置知识库**：上传私有文档 → 创建知识库 → 在应用配置中绑定知识库并设为“必定调用”（文档 1、2、3、4 流程一致）。
3. **构建连接流**：
   - 网站场景：使用 AppFlow 创建“AI助手”，导入百炼应用，生成悬浮挂件脚本嵌入 HTML（文档 1）；
   - 企业微信/钉钉/微信公众号：使用 AppFlow 预置模板（文档 2、3、4 均提供专属模板链接），完成平台凭证授权与百炼凭证绑定，获取 Webhook URL。
4. **渠道侧配置**：
   - 网站：插入 JS 脚本（文档 1）；
   - 企业微信：配置 API 接收消息（URL=Webhook）与可信 IP（文档 2）；
   - 微信公众号：开启服务器配置，注意认证状态影响消息接口（文档 3 强调已认证/未认证两种工作流）；
   - 钉钉：配置机器人 HTTP 模式接收地址（文档 4 明确要求禁用 Stream 模式）。

> **注意**：文档 3 特别指出，未认证公众号受 5 秒响应限制，若百炼应用超时将导致回复失败，此时需优化 Prompt（如添加“请总是给出简短的回答”）或切换至 `qwen-turbo` 模型 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

## 限制和注意事项

- **免费额度**：新用户可使用百炼免费额度覆盖全部教程资源消耗，额度用尽后按 token 计费（文档 1、2、4 均强调）。
- **文件解析时效**：上传文档后需等待 1–6 分钟完成解析（文档 1、2、3、4 均提示），期间知识库不可用。
- **渠道限制**：
  - 微信公众号未认证时仅支持被动回复，且响应必须 ≤5 秒（文档 3）；
  - 钉钉机器人必须使用 HTTP 模式，Stream 模式不兼容（文档 4）；
  - 企业微信配置需解决域名主体校验与可信 IP 冲突问题（文档 2 提供 Nginx 代理等完整解决方案）。
- **本地部署补充**：文档 5 提供基于 Python 的本地 RAG 方案，适用于需完全掌控文档切分、嵌入模型选择的场景，但需自行维护计算环境 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)




