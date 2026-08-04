# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库三者协同实现，无需开发即可在 10 分钟内完成部署。核心能力包括：多模态文档解析、向量检索增强、模型参数灵活调控、对话日志可追溯。

## 支持的模型/功能

- **基础模型**：默认推荐 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。> **注意**：文档 1 明确指定 `Qwen3.5-Plus`，而文档 2–4 均使用 `千问-Plus`，二者为不同版本模型，实际调用时需确认控制台中模型可用性及命名一致性。
- **RAG 能力**：所有用例均依赖知识库增强，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。
- **本地 RAG 扩展**：提供完整本地部署方案，支持自定义文档切分、本地 embedding 模型（如 GTE-Chinese-Large）、结构化/非结构化数据混合索引（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制输出随机性，范围 0.0–1.0 | 本地 RAG 应用（文档 5）的 Gradio 界面或 `chat.py`；百炼应用配置页（文档 1–4）未显式暴露，需通过 Prompt 或系统参数间接影响 |
| | `max_tokens` | 限制生成长度 | 同上 |
| | `top_p` / `top_k` | 影响采样策略 | 仅本地 RAG 应用（文档 5）支持，百炼标准应用不开放 |
| **RAG 层** | `retrieval_top_k` | 召回片段数（默认 3–5） | 本地 RAG 应用（文档 5）；百炼知识库引用配置中无直接等效项，由“相似度阈值”和“调用方式”间接控制 |
| | `similarity_threshold` | 相似度过滤阈值（0.0–1.0） | 百炼应用配置页“知识库”区域（文档 2、4）；文档 1 和 3 未提及该参数，存在功能差异 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度 | 仅本地 RAG 应用（文档 5）支持自定义；百炼使用默认智能切分（文档 1–4） |

## 使用方式

1. **创建百炼应用**：统一入口为 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **准备私有知识**：
   - 云端方案：上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，再通过 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建并绑定至应用（文档 1–4）；
   - 本地方案：解压 `local_rag.zip`，上传文件至 `File/Unstructured` 或 `File/Structured`，通过 Web UI 创建知识库（文档 5）。
3. **配置渠道连接流**：
   - 网站：使用 AppFlow 创建 AI 助手 → 配置百炼凭证 → 生成悬浮挂件脚本嵌入 HTML（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；
   - 企业微信/微信公众号/钉钉：使用对应 AppFlow 模板 → 授权平台凭证（企业 ID/AgentId/Secret 或 AppID/AppSecret 或 Client ID/Secret）→ 配置百炼凭证 → 获取 Webhook URL 并填入平台后台（文档 2–4）。
4. **验证与日志**：各渠道均支持实时对话测试；如需分析对话，可在 AppFlow 连接流中添加 SLS 日志节点（文档 2、3、4）。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；额度用尽后按 token 计费（文档 1、2、3、4 均强调此点）。
- **文件限制**：云端知识库单文件 ≤ 100 MB 或 1000 页，单次最多上传 200 个文件（文档 2）；本地 RAG 不建议上传 > 100 MB 文件（文档 5）。
- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），必须配置简短 Prompt 或 Turbo 模型规避超时（文档 3）；企业微信/钉钉需确保凭证权限完备（如企业微信需配置可信 IP，钉钉需开通 `Card.Streaming.Write` 权限）。
- **模型兼容性风险**：文档 1 使用 `Qwen3.5-Plus`，其余均用 `千问-Plus`，若控制台未同步更新模型别名，可能导致配置失败。> **注意**：跨文档模型命名不一致，生产环境应以百炼控制台实际可选模型列表为准，避免硬编码。
- **本地部署约束**：本地 RAG 方案要求 Python 3.8–3.12，且需手动配置 API Key 环境变量（文档 5）；Windows 用户需额外安装 `msvc-runtime`（文档 5）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


