# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景的快速落地，核心围绕“大模型能力+私域知识”构建智能交互应用。开发者可基于统一的百炼应用（Application）作为推理后端，通过 AppFlow 连接不同前端渠道（如网站、企业微信、微信公众号、钉钉），并结合知识库实现 RAG 增强。所有方案均无需编码，10 分钟内即可完成端到端部署，且新用户可完全使用免费额度完成验证。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 明确指定）或 `qwen-plus`（文档 5 中对应商业模型命名），该模型在效果、速度与成本间取得平衡，适用于客服问答、知识检索等通用任务；也可选用 `qwen-max`（高精度）或 `qwen-turbo`（低延迟）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **核心能力**：
  - 智能体（Agent）应用：支持 [Prompt 工程](../concepts/prompt-engineering.md)配置角色与行为约束（如“请总是给出简短的回答”）；
  - RAG 增强：通过知识库实现私有文档检索与引用，支持 PDF/DOCX/TXT/Excel 等格式；
  - [多模态](../concepts/multi-modal.md)支持：文档 2 和 4 均明确列出 `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif` 等图片格式上传能力。
- **本地化扩展**：文档 5 提供完整本地 RAG 架构，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及 Gradio Web UI，适用于对数据主权或网络隔离有要求的场景 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 推荐 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。根据百炼控制台最新模型列表，`Qwen3.5-Plus` 是 `千问-Plus` 的迭代版本，二者 API 兼容，但前者性能更优。建议优先采用 `Qwen3.5-Plus`。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制生成随机性，值越高越发散（默认 0.8） | 文档 5 的 `chat.py` 配置项；AppFlow 流中不可直接调，需在百炼应用内配置 |
| | `max_tokens` | 限制输出长度（token 数） | 同上 |
| | `top_p` | 核采样阈值（默认 0.95） | 同上 |
| **RAG 层** | `retrieval_top_k` | 召回片段数（默认 3） | 文档 5 的 Web UI 或 `chat.py`；百炼应用知识库配置中无此参数，由 AppFlow 或本地代码控制 |
| | `similarity_threshold` | 相似度过滤阈值（0~1，0 表示不过滤） | 文档 5 明确说明；百炼知识库配置页支持设置（见文档 1、2、4 的“相似度阈值”字段） |
| **交互层** | `context_window` | 携带历史对话轮数 | 文档 5 的 `chat.py` 配置项 |

## 使用方式

1. **创建百炼应用**：统一入口为 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型、Prompt 及知识库引用（文档 1、2、3、4 均遵循此流程）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
2. **集成前端渠道**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>` 底部；
   - **企业微信/微信公众号/钉钉**：使用 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`）→ 配置三方凭证（企业 ID/AgentId/AppID/Client ID）→ 绑定百炼应用 ID 和 API Key → 发布连接流 → 在对应平台完成 Webhook/IP 白名单配置。
3. **知识库配置**：统一入口为 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，支持“标准版”创建，数据源可选“文件”或“数据连接器”，索引类型推荐 `ADB-PG`（集中管理多应用向量）。

## 限制和注意事项

- **文件限制**：单文档最大 100MB 或 1000 页，单图片最大 20MB，最多上传 200 个文件（文档 2 明确）；本地 RAG 方案（文档 5）额外提示“不建议传入超过 100 MB 的文件”以防 Embedding API 限流超时。
- **认证依赖**：
  - 微信公众号：未认证账号仅支持被动回复（5 秒超时限制），必须完成认证才能启用客户消息接口（文档 3 强调）；
  - 企业微信/钉钉：需确保应用具备对应权限（如企业微信需开通“接收消息”事件，钉钉需授予 `Card.Streaming.Write` 权限）。
- **网络与安全**：
  - 企业微信/钉钉要求配置可信 IP 白名单（文档 2、4），若使用 AppFlow Webhook，需将 AppFlow 提供的 IP 加入；
  - 域名主体校验失败时（文档 2 常见问题），需配置自有备案域名或通过 Nginx 代理转发。
- **日志与可观测性**：所有 AppFlow 连接流均支持通过添加 SLS 日志节点记录完整对话（文档 2、3、4 的“记录 AI 助理对话日志”章节提供详细步骤），便于效果评测与问题排查。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


