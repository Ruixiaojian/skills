# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将大模型问答能力嵌入网站、企业微信、微信公众号、钉钉等主流渠道，无需自行部署模型或构建后端服务。所有方案均基于百炼应用 API 与 AppFlow 连接流实现，支持灵活配置知识库、提示词和模型参数。

## 支持的模型/功能

- **基础模型**：官方推荐使用 `Qwen3.5-Plus`（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）或 `千问-Plus`（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)），二者能力均衡，适用于通用客服问答；也可选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（超低成本）等变体，具体需结合响应速度、准确率与 token 成本权衡。
- **RAG 增强**：所有集成方案均支持通过百炼知识库接入私有文档（PDF/DOCX/TXT 等），并支持 `必定调用`、`按需调用` 等知识引用策略；[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供更细粒度控制，允许自定义切分逻辑、嵌入模型及召回参数。
- **多模态支持**：知识库上传支持图片（PNG/JPG/BMP/GIF）、表格（XLSX/CSV）及富文本（PPTX/MD），但需注意文档解析耗时（通常 1–6 分钟）。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均写为 `千问-Plus`。根据百炼控制台最新命名规范，`千问-Plus` 是 `Qwen3.5-Plus` 的旧称，实际为同一模型。建议统一使用 `Qwen3.5-Plus` 以避免混淆。

## 关键参数

| 参数类别 | 可配置项 | 说明 | 来源参考 |
|----------|----------|------|----------|
| **模型层** | `temperature`、`max_tokens`、`top_p` | 控制生成随机性、输出长度与采样范围；默认值通常已优化，生产环境建议人工评测后调整 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **RAG 层** | `召回片段数`、`相似度阈值`、`文档处理方式`（全文引用/切片检索/自定义处理） | 影响检索精度与上下文质量；阈值过低易引入噪声，过高则可能漏检关键信息 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **集成层** | `WebhookUrl`、`Token`、`EncodingAESKey`、`IP 白名单` | 用于第三方平台（企微/钉钉/公众号）安全通信；其中 `IP 白名单` 必须与 AppFlow 或代理服务器出口 IP 严格一致 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）并发布。
2. **准备知识库（可选）**：
   - *云端方式*：上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)，再通过 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建并绑定到应用。
   - *本地方式*：运行 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供的 Python 服务，支持结构化/非结构化数据上传与向量库本地存储。
3. **配置渠道集成**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML。
   - **企业微信/钉钉/公众号**：使用对应 AppFlow 模板 → 配置平台凭证（AgentId/Secret 或 AppID）与百炼凭证（API Key + 应用 ID）→ 发布连接流 → 在目标平台完成 Webhook 或机器人配置。
4. **验证与迭代**：在目标渠道发起测试对话；若效果不佳，优先检查知识库覆盖度、Prompt 引导性及参数阈值，而非直接更换模型。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费，详见 [新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
- **文件上传限制**：单文档最大 100 MB 或 1000 页，图片单张 ≤20 MB，最多 200 个文件；本地 RAG 方案建议单文件 ≤100 MB，避免 Embedding API 限流超时。
- **认证依赖**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），必须配置 `qwen-turbo` 或精简 Prompt 保时效；认证后可用客户消息接口，无此限制（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。
  - 企业微信/钉钉需配置可信 IP 白名单，且同一 IP 不能复用于多个企业（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。
- **调试建议**：上线前务必执行人工评测（[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)），重点关注知识召回准确性、回答简洁性与业务合规性；日志分析可通过 AppFlow 集成 SLS 实现（见各文档“记录 AI 助理对话日志”章节）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


