# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库三要素实现，无需自行部署模型或维护推理服务。开发者可复用同一套知识库和提示词配置，在不同渠道间快速迁移与迭代。

## 支持的模型/功能

- **核心模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。  
- **RAG 能力**：所有渠道均支持知识库检索增强，知识源支持 PDF、DOCX、TXT、XLSX、CSV、PPTX、PNG/JPG 等格式（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 均明确列出支持格式）。  
- **本地 RAG 扩展**：除云端托管方案外，还提供基于本地知识库的完整 RAG 应用模板，支持自定义文档切分、嵌入模型替换（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及参数调优（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。当前控制台实际可用模型列表以 [应用配置页面](https://bailian.console.aliyun.com/?tab=app#/app-center) 实时展示为准，`Qwen3.5-Plus` 为较新版本，若旧文档未同步更新可能存在版本偏差。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制生成随机性 | `0.3`（确定性回复）~`0.7`（适度创造性） |
| | `max_tokens` | 最大输出长度 | `512`（平衡详略）~`2048`（长文本摘要） |
| | `top_p` | 核采样阈值 | `0.9`（常用） |
| **RAG 层** | `retrieval_top_k` | 召回片段数 | `3`~`5`（文档 5 推荐） |
| | `similarity_threshold` | 相似度过滤阈值 | `0.2`~`0.6`（0 表示不过滤） |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（本地 RAG） | `512` tokens / `128` tokens（文档 5） |
| **集成层** | `WebhookUrl` | AppFlow 生成的回调地址（企业微信/钉钉/公众号必需） | 由连接流发布后自动生成 |
| | `Token` & `EncodingAESKey` | 企业微信消息加解密凭证（文档 2） | 由 AppFlow 凭证配置页生成并需手动填入 |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。  
2. **准备知识库**（可选但推荐）：  
   - *云端方案*：上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，创建知识库并在应用中启用「必定调用」。  
   - *本地方案*：运行 `local_rag` 示例，通过 Gradio 界面上传文件、创建知识库并调整切分与嵌入参数（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。  
3. **配置渠道连接流**：  
   - **网站**：在 AppFlow 创建「AI助手」→ 关联百炼应用 → 获取悬浮挂件脚本 → 插入 HTML（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。  
   - **企业微信/钉钉/公众号**：使用对应 AppFlow 模板 → 配置平台凭证（企业 ID/AgentId/Secret 或 AppID/Client ID）→ 关联百炼应用 → 获取 WebhookUrl → 在平台后台填写回调地址与 [Token](../concepts/token.md)（文档 2、3、4）。  
4. **验证与日志**：各渠道均支持对话测试；如需分析效果，可在 AppFlow 连接流中添加 SLS 日志节点记录原始请求与响应（文档 2、3、4 均提供详细步骤）。

## 限制和注意事项

- **免费额度与计费**：新用户享有免费额度，覆盖教程全部资源消耗；额度用尽后按 token 计费（文档 1、2、3、4 均强调此点）。  
- **认证依赖**：微信公众号未认证时仅支持被动回复（5秒超时限制），建议完成认证以启用主动消息能力（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。  
- **可信 IP 限制**：企业微信/钉钉要求配置可信 IP 白名单，若使用 AppFlow 默认域名可能触发校验失败，需通过 Nginx 代理或计算巢实例转发（文档 2、4 的「常见问题」章节明确说明）。  
- **模型响应时效**：`qwen-turbo` 适合对延迟敏感场景（如公众号未认证环境），但效果弱于 `qwen-plus`；`qwen-max` 适合复杂推理但成本更高（文档 5 的「优化回复效果」部分对比明确）。  
- **知识库规模**：单文档上限 100MB 或 1000 页，单次上传最多 200 个文件（文档 2）；本地 RAG 方案建议避免单文件 >100MB（文档 5）。  
- **权限要求**：钉钉应用创建需开发者权限（文档 4 强调「重要」提示），企业微信需主管理员扫码授权（文档 2、3）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


