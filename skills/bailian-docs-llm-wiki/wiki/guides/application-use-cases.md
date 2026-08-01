# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将大模型问答能力嵌入网站、微信公众号、企业微信、钉钉等主流渠道，实现 7×24 小时智能客服、私域知识助手等生产就绪型应用。所有方案均基于统一的百炼应用底座，通过 AppFlow 实现跨平台连接流编排，无需从零开发后端服务。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中一致采用），该模型在效果、速度与成本间取得平衡，适用于通用问答、客服响应等任务；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及，但未在其他文档中复现）。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定（如 `你叫小助...`）、多轮对话、工具调用（隐含于 AppFlow 流程中）；
  - RAG 增强：通过知识库关联文档（PDF/DOCX/TXT 等），支持 `必定调用` 模式确保知识检索生效；
  - 多模态文件解析：支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.png`, `.jpg` 等格式（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 明确列出）；
  - 本地 RAG 可选：提供完整开源方案，支持本地文档切分、自定义嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及向量存储（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2、3、4 统一写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 是其新版命名），但术语不一致可能引发配置混淆，建议以控制台实际下拉选项为准。

## 关键参数

- **身份凭证**：
  - `应用ID`（App ID）：在百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 获取；
  - `API Key`：在百炼控制台 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建；
  - 平台专属凭证：微信需 `AppID`，企业微信需 `CorpID`/`AgentId`/`Secret`，钉钉需 `Client ID`/`Client Secret`（均需在对应平台后台获取）。
- **RAG 相关**：
  - `知识库调用方式`：必须设为 `必定调用` 才能确保私有知识生效（三篇集成文档均强调）；
  - `相似度阈值` 与 `召回片段数`：影响检索精度，在本地 RAG 方案中可显式调节（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）；
  - `文档处理方式`：支持 `全文引用`、`切片检索`、`自定义处理`（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中说明）。
- **生成参数**（本地 RAG 方案特有）：
  - `温度（temperature）`、`最大回复长度（max_tokens）`、`上下文轮数（history_rounds）` 可在 `chat.py` 中调整（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 使用方式

1. **创建百炼应用**：在百炼控制台选择 **智能体应用** → 配置模型（如 `Qwen3.5-Plus`）与 Prompt → 发布；
2. **准备私有知识**：
   - 云端方案：上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) → 创建知识库 → 在应用中绑定并设为 `必定调用`；
   - 本地方案：解压 `local_rag.zip` → 配置 Python 环境与 API Key → 运行 `uvicorn main:app --port 7866` → 通过 Web UI 上传文件并创建知识库；
3. **集成到目标平台**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML；
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号 → 关联百炼应用 ID 与 API Key；
   - **企业微信/钉钉**：创建对应平台应用 → 获取凭证 → 使用 AppFlow 模板配置连接流 → 填写 Webhook URL 与可信 IP；
4. **验证与日志**：所有方案均支持通过 AppFlow 添加 SLS 日志节点记录对话（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 中详述）。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的 [新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)，覆盖教程全部资源消耗（文档 1、3、4 均提及）；
- **文件限制**：
  - 云端上传：单文件 ≤ 100 MB 或 1000 页，图片 ≤ 20 MB，最多 200 个文件（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 本地 RAG：不建议上传 > 100 MB 文件，因 Embedding API 限流可能导致超时（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）；
- **平台特殊约束**：
  - 微信未认证订阅号：仅支持被动回复，响应必须 ≤ 5 秒，否则失败（文档 2 明确警告）；
  - 钉钉机器人：**必须选择 HTTP 模式**，Stream 模式不兼容（文档 4 强调）；
  - 企业微信：需配置可信 IP 或通过 Nginx 代理解决域名主体校验问题（文档 3 详述）；
- **调试与上线**：正式上线前**必须进行人工评测**（[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)），通过优化 Prompt、补充知识、调整切分策略提升效果（文档 1、2、3、4 均要求）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


