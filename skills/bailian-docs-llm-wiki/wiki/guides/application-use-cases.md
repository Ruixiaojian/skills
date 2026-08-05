# application [use cases](use-cases.md)

百炼平台支持多种主流企业通讯与内容平台的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 私有知识库三要素实现，无需自行部署模型或维护推理服务。开发者可复用同一套知识库和提示词配置，在不同渠道快速落地智能客服能力。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1 明确指定）或 `千问-Plus`（文档 2、3、4 均采用），该模型在效果、速度与成本间取得平衡，适用于通用问答与客服场景。`qwen-turbo` 可用于对响应延迟敏感的场景（如未认证公众号的 5 秒限制），但需权衡生成质量 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **关键能力**：
  - 多模态文档解析（PDF/DOCX/TXT/PPTX/XLSX 等，见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）
  - RAG 知识检索增强（支持向量存储类型 ADB-PG 集中管理多应用知识）
  - 多端 UI 集成（网站悬浮挂件、企业微信应用、公众号消息流、钉钉机器人卡片）
  - 对话日志记录（通过 AppFlow + SLS 日志服务实现）

> **注意**：文档 1 指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均写为 `千问-Plus`。实际调用时二者为同一模型的不同命名方式（Qwen3.5-Plus 即千问-Plus 的最新版本），但开发者应以控制台当前可用模型列表为准，避免硬编码模型名。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源 |
|------|------|----------|------|
| **应用 ID** | 百炼应用唯一标识 | 在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制，注意去除首尾空格 | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| **API Key** | 百炼 API 认证凭证 | 在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建，妥善保管 | 同上 |
| **知识库调用方式** | 控制知识检索触发逻辑 | `必定调用`（强依赖私有知识）、`按需调用`（仅当问题匹配时触发） | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| **相似度阈值** | 过滤低相关性检索片段 | 默认 0.3~0.6；值越高召回越严格，值为 0 表示不过滤 | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **召回片段数** | 检索返回给模型的上下文段数 | 通常设为 3~5；过多易引入噪声，过少信息不足 | 同上 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 Qwen3.5-Plus）→ 配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）→ 发布。
2. **配置知识库**（可选但推荐）：
   - 上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) 或 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库 → 关联上传文件 → 在应用配置中启用并设置调用方式
3. **构建连接流**：
   - 进入 AppFlow 控制台 → 选择对应平台模板（如[企业微信自建应用大模型自动回复](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-qiyeweixinself0813shzoa?from=solution)）
   - 分步配置凭证（平台凭证 + 百炼 API Key）→ 填写百炼应用 ID → 发布获取 Webhook URL
4. **平台侧对接**：
   - **网站**：在 HTML 中插入悬浮挂件脚本（见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）
   - **企业微信/钉钉/公众号**：将 Webhook URL 填入平台后台的“接收消息”或“机器人 HTTP 地址”配置项，并完成可信 IP/域名校验

## 限制和注意事项

- **免费额度限制**：新用户可享百炼免费额度，覆盖教程全部资源消耗；超出后按 token 计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **文件限制**：
  - 单文档最大 100 MB 或 1000 页，单图片最大 20 MB，最多上传 200 个文件（企业微信场景明确说明）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
  - 本地 RAG 方案不建议上传 >100 MB 文件，因 Embedding API 限流可能导致创建失败 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **认证依赖**：
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），必须配置 `qwen-turbo` 或精简 Prompt 以保障响应时效 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
  - 企业微信/钉钉需配置可信 IP 白名单，且一个 IP 仅能绑定一个企业（多企业需代理转发）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **调试与监控**：
  - 排查无响应问题时，优先检查 AppFlow 执行日志、百炼应用 ID/Key 是否含空格、平台凭证是否匹配 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
  - 生产环境上线前，必须进行人工评测（[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)）或自动化评测，验证回答准确性。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


