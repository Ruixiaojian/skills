# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业协作与客户触点渠道中，包括网站、企业微信、微信公众号、钉钉等。所有方案均基于“百炼应用 + AppFlow 连接流”架构，无需编写后端代码即可完成端到端部署，核心流程统一为：创建百炼智能体应用 → 配置知识库（可选）→ 通过 AppFlow 关联第三方平台 → 发布并验证。该模式适用于客服应答、私域运营、内部知识助手等典型 RAG 场景。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `Qwen3.5-Plus` 或 `千问-Plus`，该模型在效果、速度与成本间取得平衡，适用于通用问答任务 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **可选模型**：本地 RAG 方案明确支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 三档商业模型，开发者可根据延迟敏感度与质量要求灵活切换 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **核心功能**：  
  - 全渠道嵌入式交互（悬浮窗、群聊机器人、公众号对话、企业微信应用）；  
  - RAG 知识增强：支持上传 `.pdf`、`.docx`、`.txt` 等格式文档，自动解析并构建向量知识库；  
  - [多模态](../concepts/multi-modal.md)支持：文档识别支持图片（`.png`, `.jpg` 等），但需注意文档解析耗时 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；  
  - 日志追踪：可通过 AppFlow 集成 SLS 日志服务记录完整对话链路。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均使用 `千问-Plus`。经核实，`Qwen3.5-Plus` 是 `千问-Plus` 的新版命名，二者为同一模型，控制台显示名称可能因地域或版本略有差异，实际调用无兼容性问题。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值建议 |
|----------|--------|------|-----------|
| **模型配置** | `temperature` | 控制生成随机性 | 0.1–0.6（客服场景推荐低值） |
| | `max_tokens` | 最大输出长度 | 512–2048（长答案需提高） |
| | `top_p` | 核采样阈值 | 0.9（默认） |
| **RAG 配置** | `retrieval_top_k` | 召回片段数 | 3–5（平衡精度与噪声） |
| | `similarity_threshold` | 相似度阈值 | 0.3–0.7（低于此值的片段被过滤） |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（仅本地 RAG 可调） | 非结构化文本建议 `512`+`50` |
| **集成参数** | `WebhookUrl` | AppFlow 生成的回调地址 | 必须正确填入目标平台（企业微信/钉钉/公众号） |
| | `Token` & `EncodingAESKey` | 企业微信消息加解密密钥 | 由 AppFlow 凭证页生成，不可手动修改 |

## 使用方式

1. **创建百炼应用**：  
   - 进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择 **智能体应用**，填写 Prompt（如 `你叫小助，解答产品选购问题`）；  
   - 模型选择 `Qwen3.5-Plus` 或 `千问-Plus`，发布前务必测试基础问答能力。

2. **配置知识库（可选但推荐）**：  
   - 上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；  
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库，绑定文档；  
   - 在应用配置中启用知识库，调用方式设为 `必定调用`。

3. **对接目标平台**：  
   - **网站**：使用 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>` 底部；  
   - **企业微信/钉钉/公众号**：使用对应 AppFlow 模板 → 授权平台凭证（企业 ID/AgentId/Secret 或 AppID/AppSecret）→ 绑定百炼 API Key 与应用 ID → 获取 WebhookUrl 并填入平台后台；  
     > 注意：公众号未认证时仅支持 5 秒内被动回复，超时需改用认证号或切换 `qwen-turbo` 模型提速 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

4. **验证与迭代**：  
   - 所有渠道均支持实时对话测试；  
   - 建议上线前组织人工评测，依据结果优化 Prompt、调整知识库切分策略或补充文档。

## 限制和注意事项

- **文件限制**：云端知识库单文档最大 100 MB 或 1000 页，图片单张 ≤ 20 MB，最多上传 200 个文件；本地 RAG 方案不建议上传 >100 MB 文件，以防 Embedding API 限流超时 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **地域约束**：上传的文档默认存储于新加坡区域，若业务合规要求数据不出境，需选用本地 RAG 方案或确认百炼实例所在 Region。  
- **平台权限**：  
  - 钉钉应用需开发者权限，并开通 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限；  
  - 企业微信配置可信 IP 时，若报错“IP 属于第三方服务商”，必须使用 ECS 或托管实例代理请求，不可直接使用 AppFlow 默认出口 IP [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。  
- **调试提示**：AppFlow “运行一次” 功能不模拟真实输入，无法用于测试；排查失败需查看 **执行日志**，重点核对百炼应用 ID 是否含空格、凭证是否过期、WebhookUrl 是否被平台拦截。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


