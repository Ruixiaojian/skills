# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可通过百炼创建智能体应用，结合 AppFlow 或本地 SDK 快速对接网站、企业微信、微信公众号、钉钉等主流渠道，实现 7×24 小时自动化客服、知识问答等业务功能。所有方案均基于统一的模型调用与知识库管理机制，确保效果一致性与运维可维护性。

## 支持的模型/功能

- **基础模型**：当前主流方案默认使用 `Qwen3.5-Plus`（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）或 `千问-Plus`（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），该模型在效果、速度与成本间取得平衡；亦支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）等变体，适用于不同 SLA 要求场景。
- **RAG 增强能力**：所有渠道集成方案均依赖百炼知识库实现私域知识注入，支持 PDF/DOCX/TXT/Excel 等格式上传、自动切分与向量检索，调用方式可设为“必定调用”或“按需调用”。
- **[多模态](../concepts/multi-modal.md)与扩展能力**：文档 4 中的本地 RAG 方案支持自定义嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及结构化数据（CSV/XLSX）处理，提供更灵活的文档切分与召回控制；[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 明确区分本地检索与云端生成环节，适用于对数据主权或切分逻辑有强定制需求的客户。

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus` —— 实际为同一模型的命名差异（`千问-Plus` 即 `Qwen3.5-Plus` 的旧称），非版本冲突。开发者应以控制台实际可选模型列表为准，避免硬编码模型名。

## 关键参数

| 参数类别 | 可配置项 | 说明 |
|----------|----------|------|
| **模型层** | `temperature`、`max_tokens`、`top_p` | 控制生成随机性、输出长度与采样范围；本地 RAG 方案（文档 4）明确支持调整这些参数。 |
| **RAG 层** | `召回片段数`、`相似度阈值`、`文档处理方式`（全文引用/切片检索/自定义） | 影响检索质量与上下文供给效率；文档 2 和文档 5 在知识库引用环节提供“相似度阈值”和“权重”配置，文档 4 提供更细粒度的 `召回片段数` 与 `相似度阈值` 控制。 |
| **集成层** | `WebhookUrl`、`Token`、`EncodingAESKey`（企微）、`Client ID/Secret`（钉钉）、`AppID`（公众号） | 各渠道认证与消息路由必需凭证；AppFlow 模板自动填充大部分字段，但需开发者确认来源准确性。 |

## 使用方式

1. **统一应用创建**：所有场景均始于百炼控制台 → [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建“智能体应用”，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **知识库配置**：通过百炼 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面上传文件、创建知识库，并在应用配置中绑定，调用方式建议设为“必定调用”以保障私域问题覆盖。
3. **渠道集成**：
   - **Web 站点**：使用 AppFlow 创建 AI 助手 → Web 页面集成 → 获取悬浮挂件脚本 → 注入 HTML（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
   - **企业微信/钉钉/微信公众号**：通过 AppFlow 预置模板（如 `企业微信自建应用大模型自动回复`）一键创建连接流，完成三方凭证（企业 ID/AgentId/Secret 或 Client ID/Secret 或 AppID）与百炼 API Key 的双向绑定。
   - **本地部署**：下载 `local_rag.zip`，配置 Python 环境与 API Key，运行 `uvicorn main:app --port 7866` 启动 Gradio 服务，支持临时文件上传或持久化知识库创建（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
4. **日志与监控**：所有 AppFlow 连接流均可在编辑流程中追加 SLS 日志节点，将对话内容写入阿里云日志服务，用于效果分析与问题排查。

## 限制和注意事项

- **免费额度与计费**：新用户享有百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费（见各文档开篇提示）。AppFlow 连接流调用本身不额外收费，但触发的百炼 API 调用计入额度。
- **渠道能力差异**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），必须优化 Prompt 或选用 `qwen-turbo` 保响应时效（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；
  - 企业微信需配置可信 IP 与域名主体校验，否则 API 接收失败（见文档 2 “常见问题”章节）；
  - 钉钉机器人必须选择 HTTP 模式接收消息，Stream 模式不兼容（见文档 5 “4.1 配置钉钉机器人”）。
- **知识库限制**：单文档最大 100MB 或 1000 页，图片单张 ≤20MB；文件解析耗时 1–6 分钟，期间不可查询（文档 2、3、5 均强调此点）。
- **调试与验证**：正式上线前务必执行人工评测（文档 1、2、3、5 均强调），利用百炼控制台右侧调试区或渠道端真实对话验证效果；若失败，优先检查应用 ID、API Key 是否含空格，以及知识库是否已发布生效。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


