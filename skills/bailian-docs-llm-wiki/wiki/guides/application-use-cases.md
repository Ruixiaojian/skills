# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库实现端到端闭环，开发者无需自建推理服务或编写业务胶水代码即可交付生产级智能客服能力。核心流程高度一致：创建百炼应用 → 配置知识库 → 通过 AppFlow 关联第三方平台 → 发布并验证。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `qwen-plus`（即文档中提及的“千问-Plus”或“Qwen3.5-Plus”），该模型在效果、速度与成本间取得平衡，适用于通用问答场景 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **可选模型**：`qwen-max`（高精度）、`qwen-turbo`（低延迟）亦被明确支持，尤其在微信公众号等对响应时长敏感的场景中，`qwen-turbo`可用于规避 5 秒超时限制 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。  
- **RAG 增强**：所有用例均依赖百炼知识库能力，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.png`, `.jpg` 等格式（单文件 ≤100MB），知识检索方式支持“必定调用”、相似度阈值与权重配置 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **本地 RAG 变体**：除云端托管方案外，还提供基于 `local_rag.zip` 的本地部署选项，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及灵活参数调优 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中模型名称写作 “Qwen3.5-Plus”，而文档 2、3、4 统一使用 “千问-Plus”。经核实，百炼控制台当前实际可用模型 ID 为 `qwen-plus`，`Qwen3.5-Plus` 属于过时命名，应以控制台显示为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型取值 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制输出随机性 | 0.1–0.7（生产环境建议 ≤0.3） |
| | `max_tokens` | 生成回复最大 token 数 | 512–2048（需匹配前端展示空间） |
| | `top_p` | 核采样概率阈值 | 0.9–1.0 |
| **RAG 层** | `retrieval_top_k` | 检索召回片段数 | 3–5（过多易引入噪声） |
| | `similarity_threshold` | 相似度过滤阈值 | 0.2–0.6（0 表示不过滤） |
| | `context_window` | 历史对话轮数 | 1–5（影响上下文连贯性） |
| **平台适配** | Web 悬浮挂件 `dragEnabled` | 是否启用拖拽功能 | `true`/`false`（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)） |
| | 微信公众号 `response_timeout` | 被动回复超时限制 | **严格 ≤5s**（未认证号强制约束） |

## 使用方式

1. **统一入口**：所有集成均始于百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 创建“智能体应用”，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。  
2. **凭证管理**：通过 [API Key 页面](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建密钥，与应用 ID 一同用于 AppFlow 授权。  
3. **渠道对接**：  
   - **网站**：使用 AppFlow 创建“AI助手”，通过 `<script>` 标签嵌入悬浮挂件脚本 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；  
   - **企业微信/钉钉/微信公众号**：使用对应平台的 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），按向导配置企业 ID/AgentId/AppID/ClientSecret 等凭证，并获取 Webhook URL；  
   - **本地部署**：解压 `local_rag.zip`，`pip install -r requirements.txt`，配置 `BAI_LIAN_API_KEY` 环境变量后运行 `uvicorn main:app --port 7866`。  
4. **知识注入**：上传文件至百炼 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，在知识库页面关联并设置调用策略。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费，需关注 `qwen-max` 的 token 成本显著高于 `qwen-turbo` [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **平台合规约束**：  
  - 微信公众号未认证时，被动回复必须 ≤5 秒，否则失败；建议 Prompt 中添加“请总是给出简短的回答”或切换 `qwen-turbo` [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；  
  - 企业微信要求可信 IP 白名单，若使用第三方代理（如 AppFlow 默认域名），需通过计算巢 Nginx 代理或自有 ECS 实例解决 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
  - 钉钉机器人必须配置为 **HTTP 模式**（非 Stream 模式），否则无法返回消息 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。  
- **知识库时效性**：上传文件后需等待 1–6 分钟解析完成，期间知识库不可用；修改知识库内容后，需重新发布百炼应用才能生效。  
- **日志与监控**：AppFlow 连接流支持集成 SLS 日志服务记录对话，用于效果分析与问题排查，需在连接流中新增 SLS 步骤并配置凭证 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


