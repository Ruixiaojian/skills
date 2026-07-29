# application [use cases](use-cases.md)

百炼平台支持多种主流业务场景下的 AI 应用快速落地，涵盖网站嵌入、企业微信、钉钉、微信公众号等私域渠道的智能客服/助手集成，以及本地化知识库驱动的 RAG 应用。所有方案均基于百炼大模型 API 与 AppFlow 低代码连接能力构建，无需自建推理服务或编写复杂集成逻辑，开发者可聚焦于业务逻辑与效果调优。

## 支持的模型/功能

- **核心模型**：统一支持通义千问系列商用模型，包括 `qwen-max`（高精度）、`qwen-plus`（均衡型，[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中明确推荐用于网站助手场景）、`qwen-turbo`（低延迟）及 `qwen3.5-plus`（文档 1 中指定为最新推荐版本）。  
- **RAG 能力**：所有集成方案均默认支持知识库增强，通过百炼控制台的「知识库」模块接入结构化/非结构化文档（PDF、DOCX、TXT、XLSX 等），支持向量检索与全文引用两种模式。  
- **多端交互能力**：提供开箱即用的 Web 悬浮挂件、企业微信应用、钉钉机器人、微信公众号智能客服四类标准化集成形态，均支持自定义 Prompt、图标、预置问题及对话样式。  
- **本地 RAG 扩展**：除云端知识库外，[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供基于本地文件系统 + 百炼 Embedding API 的轻量级 RAG 方案，适用于对数据驻留有强要求的场景。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`（即 `qwen-plus`）。二者为同一模型的不同命名表述，实际调用时应以百炼控制台当前可用模型列表为准；若控制台未显示 `Qwen3.5-Plus`，请选用 `qwen-plus`。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制生成随机性，范围 0–2，推荐值 0.3–0.7 | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的「优化回复效果」章节 |
| | `max_tokens` | 最大输出长度，影响响应详略程度 | 同上 |
| | `top_p` / `top_k` | 核采样参数，控制候选 token 范围 | 百炼应用配置页「高级设置」 |
| **RAG 层** | `retrieval_top_k` | 召回片段数，默认 3–5 | 百炼应用配置页「知识库」→「调用方式」旁设置项；本地 RAG 方案见 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `similarity_threshold` | 相似度阈值，过滤低相关片段，默认 0.3–0.6 | 同上 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（仅本地 RAG 可调） | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的「优化切分方法」章节 |

## 使用方式

1. **创建百炼应用**：在百炼控制台「应用管理」中创建「智能体应用」，选择目标模型（如 `qwen-plus`），配置 Prompt（例如 `"你叫小助，帮助解答产品选购、使用问题"`），发布应用并记录 `AppID` 与 `API Key`。  
2. **配置知识库（可选但推荐）**：  
   - 上传文档至「数据连接」或「文件」页签；  
   - 在「知识库」页签创建标准版知识库，关联上传文件；  
   - 在应用配置中启用知识库，设置调用方式为「必定调用」。  
3. **集成到目标平台**：  
   - **网站**：通过 AppFlow 创建「AI助手」→ 配置百炼凭证 → 获取悬浮挂件脚本 → 插入 HTML。  
   - **企业微信/钉钉/微信公众号**：在对应平台创建应用获取凭证（AgentId/Secret 或 ClientID/ClientSecret 或 AppID），再通过 AppFlow 预置模板（如「企业微信自建应用大模型自动回复」）一键绑定百炼应用与 Webhook。  
4. **验证与调优**：在目标渠道发起测试对话，结合人工评测结果调整 Prompt、知识库覆盖范围或 RAG 参数。

## 限制和注意事项

- **免费额度限制**：新用户享有百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费，详见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中的额度说明。  
- **微信公众号认证约束**：未认证公众号仅支持被动回复（5 秒超时限制），已认证方可启用客户消息接口；若未认证且需稳定响应，建议切换至 `qwen-turbo` 模型或优化 Prompt 缩短响应时间。  
- **知识库文件限制**：单文档最大 100 MB 或 1000 页，图片单张最大 20 MB，总文件数上限 200 个（文档 2 明确说明）；本地 RAG 方案同样不建议上传 >100 MB 文件（文档 5 提示）。  
- **可信 IP 与域名校验**：企业微信/钉钉等平台要求配置可信 IP 和主体备案域名。当 AppFlow 自动生成的 Webhook 域名校验失败时，需按文档 2 的「常见问题」章节配置二级域名或 Nginx 代理。  
- **模型兼容性**：钉钉机器人必须使用 HTTP 模式接收消息（文档 3 强调），Stream 模式将导致消息无法返回；企业微信需严格配置 [Token](../concepts/token.md) 和 EncodingAESKey（文档 2 的 4.1 节）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


