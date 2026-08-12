# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业协作与客户触点渠道中，实现开箱即用的 AI 助手能力。当前典型场景覆盖企业微信、钉钉、微信公众号及自有网站四大入口，均通过 AppFlow 无代码连接流完成模型服务与渠道消息系统的对接，并统一依托百炼应用配置 RAG 知识增强能力。所有方案均支持在免费额度内完成端到端验证。

## 支持的模型/功能

- **核心模型**：推荐使用 `qwen-plus`（文档 1、2、3 均明确指定），兼顾效果、速度与成本；网站场景（文档 5）推荐 `Qwen3.5-Plus`；本地 RAG 场景（文档 4）支持 `qwen-max`/`qwen-plus`/`qwen-turbo` 三档可选。
- **RAG 能力**：所有渠道集成方案均依赖百炼知识库（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)、[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)、[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)），支持 `.pdf`, `.docx`, `.txt` 等 15+ 格式，单文件上限 100MB。
- **部署模式**：提供两种技术路径：
  - **云端托管型**：通过百炼应用 + AppFlow 连接流实现全托管（适用于文档 1–5 所有 SaaS 渠道集成）；
  - **本地混合型**：检索环节本地执行、生成环节调用百炼 API（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)），适用于对文档切分、嵌入模型有强定制需求的场景。

> **注意**：文档 5 中网站场景推荐 `Qwen3.5-Plus`，但该模型未在百炼控制台公开发布，实际创建时需选择 `qwen-plus` 或确认控制台可用模型列表，避免配置失败。

## 关键参数

- **应用 ID 与 API Key**：所有渠道集成均需从百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 和 [API Key](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面获取，用于 AppFlow 连接凭证配置。
- **知识库参数**：
  - **调用方式**：建议设为 `必定调用`（文档 1、2、3、5 均采用），确保私域问题必触发检索；
  - **相似度阈值**：默认 0（不剔除），可根据召回精度调整（文档 4 明确说明其作用）；
  - **召回片段数**：默认 3–5，增大可提升信息覆盖，但可能引入噪声（文档 4 提供调优指导）。
- **模型参数**（仅本地 RAG 场景可细粒度控制）：
  - 温度（temperature）、最大回复长度（max_tokens）、上下文轮数（history_rounds）等均在 `chat.py` 中可配置（文档 4）。

## 使用方式

1. **创建百炼应用**：统一入口为百炼控制台 > 应用管理 > 创建智能体应用，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **准备知识源**：上传结构化/非结构化文档至百炼数据连接或文件中心（文档 1、2、3、5 均指向同一操作路径；文档 4 提供本地上传与知识库创建分离流程）。
3. **创建渠道连接流**：
   - 企业微信：使用 AppFlow 模板 `企业微信自建应用大模型自动回复`（文档 1）；
   - 微信公众号：按认证状态选择对应模板（已认证/未认证）（文档 2）；
   - 钉钉：使用模板 `钉钉机器人连接流`（文档 3）；
   - 网站：通过 AppFlow > 模型服务 > AI助手 > Web页面集成（文档 5）；
   - 本地 RAG：运行 `uvicorn main:app --port 7866` 启动 Gradio 服务（文档 4）。
4. **渠道侧配置**：
   - 企业微信：配置 API 接收消息（Webhook URL、[Token](../concepts/token.md)、EncodingAESKey）及可信 IP（文档 1）；
   - 公众号：开启服务器配置并填写 [Token](../concepts/token.md)、AppSecret（文档 2）；
   - 钉钉：在应用开发中开通 `Card.Streaming.Write` 权限，并配置 HTTP 模式 Webhook（文档 3）；
   - 网站：在 HTML 中插入悬浮挂件部署脚本（文档 5）。

## 限制和注意事项

- **渠道能力差异**：
  - 微信公众号未认证时，响应超 5 秒将失败（文档 2 明确指出），必须优化 Prompt（如添加“请总是给出简短的回答”）或切换至 `qwen-turbo` 模型；
  - 钉钉机器人**必须**选择 HTTP 模式，Stream 模式不兼容（文档 3 强调）；
  - 企业微信要求可信 IP 必须为本企业服务器 IP，第三方服务商 IP 将被拒绝（文档 1 的“配置企业可信 IP”章节详细说明解决方案）。
- **知识库限制**：云端知识库文件解析耗时 1–6 分钟，且存储于新加坡区域（文档 1）；本地 RAG 场景不支持 >100MB 文件（文档 4）。
- **调试与日志**：所有 AppFlow 连接流均支持添加 SLS 日志节点记录对话（文档 1、2、3 均提供相同操作指引），便于问题排查。
- **安全合规**：企业微信/钉钉/公众号集成均需完成主体资质校验；域名备案要求详见文档 1 的“域名主体校验未通过怎么办？”章节。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)


