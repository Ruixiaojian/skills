# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心是将大模型能力通过低代码/无代码方式集成到主流业务渠道（如网站、微信公众号、钉钉、企业微信），并结合私有知识库实现 RAG 增强。所有方案均基于统一的百炼应用底座，通过 AppFlow 连接器完成渠道对接，无需自行维护模型服务与消息协议适配。

## 支持的模型/功能

- **基础模型**：推荐使用 `qwen-plus`（即文档中所述“千问-Plus”或“Qwen3.5-Plus”，三者为同一模型不同命名；[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)明确指定为 Qwen3.5-Plus，而[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)和其余文档均称千问-Plus）。
- **可选模型**：`qwen-max`（高效果）、`qwen-turbo`（高速度/低成本），适用于对响应延迟敏感的场景（如未认证公众号需 5 秒内回复）。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定、多轮对话、工具调用（当前文档未展开，但属百炼智能体应用标准能力）；
  - RAG 知识增强：支持文件上传、知识库创建、引用策略配置（必定调用/按需调用）；
  - [多模态输入](../concepts/multi-modal-input.md)：企业微信文档上传支持 `.pdf`, `.docx`, `.xlsx`, `.png`, `.jpg` 等 15+ 格式（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 本地 RAG 扩展：提供 `local_rag.zip` 示例工程，支持本地文档切分、嵌入模型替换及 API 对接（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 中模型名称为 “Qwen3.5-Plus”，而文档 2、3、5 均称 “千问-Plus”。经核实，Qwen3.5-Plus 是千问-Plus 的最新版本代号，二者为同一模型。开发者应以控制台实际可用模型列表为准，避免硬编码模型 ID。

## 关键参数

| 参数 | 说明 | 典型值 | 来源依据 |
|------|------|--------|----------|
| `application_id` | 百炼应用唯一标识，在应用管理页获取 | `app-xxxxxx` | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) §1.2 |
| `api_key` | 百炼 API 访问密钥，用于 AppFlow 或自定义调用 | `sk-xxxxxxxx` | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) §1.2 |
| `webhook_url` | AppFlow 生成的 HTTP 回调地址，用于钉钉/企业微信/公众号接收消息 | `https://xxx.appflow.aliyuncs.com/...` | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) §3 |
| `knowledge_base_id` | 知识库 ID，用于在应用配置中绑定 | `kb-xxxxxx` | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §5.1 |

## 使用方式

1. **创建百炼应用**  
   进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择 `qwen-plus` 模型 → 配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。

2. **配置知识库（可选但推荐）**  
   - 上传文件：通过「数据连接」或「文件」页签导入 PDF/DOCX/TXT 等（文档 1、2、5 路径略有差异，但功能一致）；  
   - 创建知识库：进入「知识库」页签 → 创建标准版 → 关联已上传文件；  
   - 绑定应用：返回应用配置 → 在「文档」区域添加知识库 → 设置调用方式为「必定调用」。

3. **对接目标渠道**  
   - **网站**：AppFlow 创建 AI 助手 → Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML；  
   - **微信公众号**：AppFlow 使用预置模板 → 授权公众号凭证 → 绑定百炼应用 ID 和 API Key；  
   - **钉钉/企业微信**：先在对应开放平台创建应用（获取 Client ID/Secret 或 AgentId/Secret）→ AppFlow 模板配置 → 填写凭证与 Webhook → 在开放平台配置 HTTP 模式接收地址。

4. **验证与日志**  
   - 实时测试：在渠道端直接发送消息（如 @机器人、公众号对话、企业微信搜索应用）；  
   - 日志追踪：在 AppFlow 连接流中添加 SLS 日志节点，记录输入/输出上下文（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) §常见问题）。

## 限制和注意事项

- **免费额度限制**：新用户享有免费额度，覆盖教程全部资源消耗；超出后按 token 计费（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) §1.1）。
- **文件上传限制**：云端知识库单文件 ≤ 100 MB 或 1000 页；本地 RAG 工程建议不超过 100 MB（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) §传入知识文件）。
- **微信认证影响**：未认证公众号仅支持被动回复（5 秒超时限制），必须选用对应模板并考虑模型响应速度（如切换 `qwen-turbo`）；认证号支持主动客服消息（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) §2）。
- **可信 IP 与域名**：企业微信要求配置可信 IP 和主体备案域名；若无自有域名，需通过 AppFlow 内网代理或计算巢 Nginx 实例转发（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §常见问题）。
- **调试建议**：上线前务必进行人工评测（[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) §总结），重点验证知识库召回准确率与 Prompt 引导效果。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)


