# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，包括网站、企业微信、微信公众号、钉钉等。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库三要素实现，无需自建模型服务或编写后端逻辑，开发者可 10 分钟内完成端到端部署。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2–4），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。  
- **RAG 能力**：所有用例均依赖百炼知识库实现私域知识增强，支持 PDF/DOCX/TXT/XLSX 等格式（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)），单文件上限 100 MB（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。  
- **本地 RAG 扩展**：除云端知识库外，还提供本地部署方案，支持自定义文档切分、嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及向量存储（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`。当前控制台实际可用模型列表以 [应用配置页面](https://bailian.console.aliyun.com/?tab=app#/app-center)为准，`Qwen3.5-Plus` 为较新版本，若旧版应用模板未同步更新，可能导致配置不一致。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制输出随机性，建议值 0.1–0.5（生产环境） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中的 Gradio 界面或 `chat.py` |
| | `max_tokens` | 限制回复长度，避免超长响应 | 同上 |
| | `top_p` / `top_k` | 影响 token 采样范围，影响多样性 | 百炼应用配置页（未在原始文档中显式提及，但控制台支持） |
| **RAG 层** | `retrieval_top_k` | 召回片段数，默认 3–5，过高易引入噪声 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `similarity_threshold` | 相似度阈值，0 表示不过滤，建议 0.3–0.7 | 同上；云端知识库在应用配置 > 知识库 > 高级设置中配置 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（仅本地 RAG 可调） | `create_kb.py` 或 LlamaIndex 自定义切分器 |

## 使用方式

1. **创建百炼应用**：统一入口为 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）并发布。  
2. **配置知识源**：  
   - *云端*：通过 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 上传 → [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建 → 应用配置中启用「必定调用」。  
   - *本地*：解压 `local_rag.zip` → 上传文件至 `File/Unstructured` 或 `File/Structured` → 在「创建知识库」界面选择类目/数据表生成向量库（存于 `VectorStore`）。  
3. **对接渠道**：使用 AppFlow 预置模板（如企业微信、钉钉、微信公众号模板）完成连接流配置，关键步骤包括：  
   - 添加凭证（企业微信 ID/AgentId/Secret、钉钉 Client ID/Secret、公众号 AppID、百炼 API Key）；  
   - 绑定百炼应用 ID；  
   - 获取并配置 Webhook URL（企业微信/钉钉）或悬浮挂件脚本（网站）。  
4. **验证与日志**：  
   - 网站：插入脚本后访问右下角图标；  
   - IM 工具：在对应群聊或对话中 @ 机器人/发送消息；  
   - 日志记录：可在 AppFlow 连接流中添加 SLS 日志节点（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 和 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 均提供详细步骤）。

## 限制和注意事项

- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），必须完成认证才能启用客户消息接口（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。  
- **可信 IP 限制**：企业微信/钉钉要求配置可信 IP 白名单，AppFlow 默认 IP 可能被识别为第三方服务商；需通过 ECS/Nginx 代理或计算巢 Nginx 实例解决（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中「配置企业可信 IP」章节）。  
- **文件解析区域**：云端知识库上传的文件默认存储于新加坡区域（文档 2），若业务合规要求数据不出境内，应优先选用本地 RAG 方案或确认百炼知识库地域选项。  
- **模型 [Token](../concepts/token.md) 计费**：新用户享有免费额度，额度耗尽后按输入+输出 token 计费（所有文档均强调此点），建议在调试阶段监控 token 消耗（如通过百炼应用日志）。  
- **本地 RAG 环境约束**：Python 版本需为 3.8–3.12，Windows 用户需额外安装 `msvc-runtime`（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


