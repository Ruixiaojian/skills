# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构：通过百炼创建大模型问答应用作为核心推理引擎，借助 AppFlow 低代码连接流完成渠道对接，并可选配私有知识库提升专业性。整个流程无需编码，10 分钟内即可完成端到端部署，且新用户可使用免费额度零成本启动。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1 明确指定）或 `千问-Plus`（文档 2、3、4 均采用），该模型在效果、速度与成本间取得平衡，适用于通用客服问答；对延迟敏感场景可选用 `qwen-turbo`（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **关键能力**：
  - 多渠道嵌入：支持 Web 悬浮挂件、企业微信应用、微信公众号消息回复、钉钉机器人四种交付形态；
  - RAG 增强：所有方案均支持上传 `.pdf/.docx/.txt` 等格式文档构建知识库，并配置“必定调用”等检索策略；
  - 可视化配置：AppFlow 提供预置模板（如[企业微信自建应用大模型自动回复](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），大幅降低集成门槛。

> **注意**：文档 1 中模型名称为 `Qwen3.5-Plus`，而文档 2、3、4 统一写作 `千问-Plus`。二者实为同一模型的不同命名方式，官方 SDK 和控制台中以 `qwen-plus` 为准，开发时应统一使用该标识符。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **认证凭证** | `API Key` | 百炼平台密钥，用于调用大模型应用 API，需在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `App ID` | 百炼应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| | `WebhookUrl` | AppFlow 连接流生成的回调地址，需填入企业微信/钉钉/公众号后台 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| **知识库配置** | `调用方式` | 控制知识检索行为，`必定调用`确保每次请求均触发 RAG | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| | `相似度阈值` | 过滤低相关性检索片段，默认 0（不过滤），建议生产环境设为 0.3–0.6 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **模型调优** | `温度（temperature）` | 控制输出随机性，客服场景建议设为 0.1–0.3 以保证稳定性 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建大模型应用**：在百炼控制台选择「智能体应用」，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`），并发布应用；
2. **准备知识数据**：上传私有文档至百炼「文件」或「[数据连接](../concepts/data-connection.md)」页签，解析完成后在「知识库」页面创建标准版知识库；
3. **配置渠道连接流**：
   - 网站：使用 AppFlow 创建「AI助手」，导入百炼应用凭证，生成悬浮挂件脚本并嵌入 HTML；
   - 企业微信/钉钉/公众号：使用对应 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），按向导配置平台凭证（企业 ID/AgentId/Secret 或 AppID）与百炼凭证；
4. **渠道侧配置**：在企业微信「API接收消息」、钉钉「机器人配置」或公众号「服务器配置」中填入 WebhookUrl 及 [Token](../concepts/token.md) 等参数；
5. **验证与迭代**：通过人工评测验证回答质量，必要时优化 Prompt、调整知识库切分策略或更换嵌入模型。

## 限制和注意事项

- **渠道限制**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证后使用客户消息接口；
  - 钉钉机器人必须配置为 **HTTP 模式**（非 Stream 模式），否则无法返回消息；
  - 企业微信需配置可信 IP 白名单，若使用第三方代理（如 Nginx），须通过 AppFlow 内网代理功能解决安全校验问题。
- **知识库限制**：
  - 单文档最大 100MB 或 1000 页，图片单张不超过 20MB，最多上传 200 个文件；
  - 文档解析耗时 1–6 分钟，大规模知识库建议分批上传。
- **调试与监控**：
  - 若对话无响应，优先检查 AppFlow 执行日志（见 [配置完成后，与公众号对话没有反应，如何排查问题？](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；
  - 生产环境建议接入 SLS 日志服务记录对话，便于效果分析与合规审计（详见各渠道文档的「记录 AI 助理对话日志」章节）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


