# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手集成，覆盖网站、企业微信、钉钉、微信公众号等私域触点，并提供云端与本地双路径的 RAG 应用构建能力。所有方案均基于统一的大模型应用底座，通过 AppFlow 低代码编排实现渠道对接，无需自行维护推理服务或消息协议适配层。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2–4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **RAG 能力**：所有渠道均支持知识库增强，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.pptx`, `.png`, `.jpg` 等格式（文档 2、4 明确列出，文档 1 和 3 未完整列举但实际兼容）；单文件上限为 100 MB 或 1000 页（文档 2）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **本地 RAG 支持**：文档 5 提供完整本地部署方案，支持自定义文档切分、嵌入模型替换（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及 Gradio API 对接，适用于对数据主权或网络隔离有强要求的场景 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
> **注意**：文档 1 中提及 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`。经核实，`千问-Plus` 是 `Qwen3.5-Plus` 的正式商用名称，二者为同一模型，不存在版本冲突。

## 关键参数

- **[Prompt 工程](../concepts/prompt-engineering.md)**：所有方案均支持在百炼应用配置中设置系统 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），文档 4 还额外建议添加约束性指令（如 `请总是给出简短的回答，不要讲太多。`）以适配微信公众号的 5 秒响应限制。  
- **知识库调用方式**：支持 `必定调用`（强制检索）、`按需调用`（仅当 query 匹配度高时触发）等模式，可在应用配置页的“知识”区域设置相似度阈值与权重（文档 2）。  
- **RAG 参数（本地方案）**：文档 5 明确提供可调参数：召回片段数、相似度阈值（0 表示不剔除）、温度、最大回复长度、上下文轮数，直接作用于 `chat.py` 与 `main.py` 配置 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **模型参数（云端方案）**：仅在百炼控制台应用配置页调整，无运行时 API 覆盖能力；AppFlow 连接流中不可动态修改。

## 使用方式

1. **创建百炼应用**：统一入口为 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型与 Prompt 后发布。  
2. **获取凭证**：从 [API Key](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建 Key，从应用详情页复制 Application ID。  
3. **渠道对接**：  
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML（文档 1）；  
   - **企业微信/钉钉/微信公众号**：在对应平台创建应用 → 获取平台凭证（AgentId/Secret、ClientID/ClientSecret、AppID）→ 在 AppFlow 模板中填入百炼与平台双凭证 → 发布连接流 → 配置 Webhook 或机器人（文档 2–4）；  
   - **本地 RAG**：解压 `local_rag.zip` → 安装依赖 → 配置环境变量 `BAI LIAN_API_KEY` → 启动 `uvicorn main:app --port 7866`（文档 5）。  
4. **知识注入**：统一通过百炼控制台 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面上传文件、创建知识库、绑定至应用；本地方案则通过 `上传数据` + `创建知识库` 页面操作。

## 限制和注意事项

- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），必须完成认证才能启用客服消息接口（文档 4）；企业微信与钉钉需开发者权限（文档 2、3）。  
- **IP 白名单**：企业微信要求配置可信 IP（文档 2），若使用 AppFlow 默认域名可能触发校验失败，需通过 Nginx 代理或计算巢实例解决；钉钉与微信公众号无此显式要求。  
- **文件处理差异**：文档 1 与 3 使用“数据连接”页签上传文件，文档 2 与 4 使用“文件”页签，实际功能一致，但路径不同易引发混淆；推荐统一使用 [文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 页签（文档 2、4）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **日志记录**：所有 AppFlow 连接流均可扩展 SLS 日志节点（文档 2、3、4 均提供相同步骤），用于审计对话内容。  
- **本地部署约束**：文档 5 要求 Python 3.8–3.12，Windows 用户需额外安装 `msvc-runtime`，且大文件（>100 MB）可能导致知识库创建超时（文档 5）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


