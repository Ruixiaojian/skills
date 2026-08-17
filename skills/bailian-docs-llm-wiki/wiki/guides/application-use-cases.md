# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的大模型应用落地，核心围绕“模型能力+业务渠道+私有知识”三位一体架构。开发者可基于百炼托管的大模型 API（如 Qwen 系列）构建 RAG 应用，并通过 AppFlow 低代码集成至网站、企业微信、微信公众号、钉钉等主流触点；亦可选择本地部署检索模块，实现对敏感数据或超大文档的精细化控制。所有方案均默认支持免费额度内快速验证，生产环境按 token 计费。

## 支持的模型/功能

- **基础模型**：官方推荐 `qwen-plus`（即文档中多次提及的“千问-Plus”），在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen3.5-plus`（见[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。> **注意**：文档 1 明确指定 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`，二者为不同版本模型，实际选型需根据控制台可用模型列表及业务需求确认。
- **RAG 能力**：全链路支持知识库配置，包括文件上传（PDF/DOCX/TXT/XLSX/CSV/PNG/JPG 等）、向量化（默认调用百炼 Embedding API 或可替换为本地模型）、索引构建与检索增强。知识库类型支持标准版（默认）及 ADB-PG 向量存储（适用于多应用共享向量库）。
- **集成渠道**：覆盖 Web 端（悬浮挂件）、企业微信（自建应用）、微信公众号（订阅号/服务号）、钉钉（群机器人）四类主流企业级触点，均由 AppFlow 提供预置模板与可视化编排能力。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制输出随机性，建议 0.1–0.6 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的“优化回复效果”章节 |
| | `max_tokens` | 限制生成长度，影响响应详略程度 | 同上 |
| | `top_p` / `top_k` | 影响采样多样性（部分本地 RAG 场景支持） | 同上 |
| **RAG 层** | `retrieval_top_k` | 召回片段数，默认 3–5 | 同上 |
| | `similarity_threshold` | 相似度阈值，0 表示不过滤 | 同上 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（仅本地 RAG 可定制） | 同上 |
| **渠道层** | `WebhookUrl` | AppFlow 连接流对外暴露的回调地址，用于企业微信/钉钉/公众号接收消息 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 等文档中多次出现 |
| | `Token` & `EncodingAESKey` | 企业微信消息加解密凭证 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `qwen-plus`）→ 配置 Prompt → 获取应用 ID 与 API Key。
2. **准备知识库（可选但推荐）**：
   - *云端方式*：在百炼控制台 → 数据中心 → 导入文件 → 知识库 → 创建并关联至应用（调用方式设为“必定调用”）；
   - *本地方式*：下载 [local_rag.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/odwvrb/local_rag.zip) → 配置 Python 环境与 API Key → 运行 `uvicorn main:app --port 7866` → 通过 Gradio 界面上传文件并创建知识库。
3. **集成至目标渠道**：
   - *网站*：AppFlow 创建 AI 助手 → 配置百炼应用凭证 → 生成悬浮挂件脚本 → 插入 HTML；
   - *企业微信/钉钉/公众号*：AppFlow 选用对应模板 → 授权平台账号（获取 AppID/AgentId/ClientID 等）→ 配置百炼凭证 → 发布连接流 → 在平台侧完成 Webhook/可信 IP/机器人配置。
4. **验证与日志**：通过真实渠道发起对话；如需分析，可在 AppFlow 连接流中添加 SLS 日志节点记录对话上下文。

## 限制和注意事项

- **文件限制**：云端知识库单文件 ≤100 MB 或 1000 页，图片 ≤20 MB，最多上传 200 个文件；本地 RAG 不建议上传 >100 MB 文件（受限于 Embedding API 限流）。
- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），必须启用“已认证公众号”工作流；企业微信/钉钉需确保账号具备开发者权限。
- **网络与安全**：
  - 企业微信要求配置可信 IP（AppFlow 会提供白名单，需手动填入）；
  - 若域名主体校验失败（常见于企业微信），需通过 AppFlow 部署 Nginx 代理或配置二级域名（详见[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 钉钉机器人**必须**使用 HTTP 模式，Stream 模式不兼容。
- **调试建议**：首次集成失败时，优先检查 AppFlow 运行日志、百炼应用 ID/API Key 是否含空格、平台凭证是否匹配、Webhook 是否被防火墙拦截。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


