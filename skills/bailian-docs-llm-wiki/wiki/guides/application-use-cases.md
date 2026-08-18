# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业协作与客户触点渠道中，包括企业微信、钉钉、微信公众号及自有网站。所有方案均基于低代码/无代码方式实现，核心依赖百炼应用（智能体）、AppFlow 连接流（或本地 RAG 框架）和可选的私有知识库（RAG）。开发者可按需选择云端托管或本地部署模式，适用于客服应答、内部知识助手、产品导购等典型场景。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（平衡效果、速度与成本），也支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）、`qwen3.5-plus`（文档 5 中明确指定）等通义千问系列商业模型。  
- **核心功能**：  
  - 智能体（Agent）应用：支持角色设定（Prompt）、多轮对话、工具调用（如知识检索）；  
  - RAG 增强：通过知识库实现私域问答，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv` 等格式（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；  
  - 多端适配：提供预置 AppFlow 模板，覆盖企业微信、钉钉、微信公众号、网站四类入口；  
  - 本地 RAG 框架：支持完全本地化部署，含文档切分、嵌入模型（云端 API 或本地 ModelScope 模型）、向量存储（`VectorStore` 目录）全流程控制（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 和文档 2 均建议使用 `qwen-plus`，但文档 5 明确要求使用 `Qwen3.5-Plus`（注意大小写与版本号差异），实际配置时请以百炼控制台当前可用模型列表为准，避免因模型下线导致调用失败。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **应用级** | 应用 ID | 百炼应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| | API Key | 用于 AppFlow 或前端调用鉴权，需在 [API Key](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建 | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| **RAG 级** | 相似度阈值 | 控制知识检索召回片段的最低相关性，范围通常为 0–1，值越高过滤越严格 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | 召回片段数 | 检索后传递给大模型的上下文片段数量，影响信息量与噪声水平 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **连接流级** | WebhookUrl | AppFlow 生成的 HTTP 回调地址，需配置到企业微信/钉钉/公众号后台 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型、Prompt 并发布；  
2. **准备知识（可选）**：上传文件至 [数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center)，创建知识库并绑定至应用；  
3. **配置连接流或集成**：  
   - **IM/通讯平台（企业微信/钉钉/公众号）**：使用 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），配置三方凭证（企业 ID/AgentId/Secret 或 AppID）与百炼凭证（API Key + 应用 ID），发布后获取 WebhookUrl 并填入对应平台后台；  
   - **网站**：在 AppFlow 的 **AI助手 > Web页面集成** 中生成悬浮挂件脚本，插入 HTML 即可；  
   - **本地部署**：下载 [local_rag.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/odwvrb/local_rag.zip)，配置环境变量（API Key）、运行 `uvicorn main:app --port 7866` 启动服务；  
4. **验证与日志**：通过实际消息交互测试，并可选在 AppFlow 连接流中添加 SLS 日志节点记录对话（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。

## 限制和注意事项

- **文件限制**：单文件最大 100 MB 或 1000 页，图片单张 ≤20 MB，一次最多上传 200 个文件（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；  
- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用全功能（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；  
- **可信 IP 与域名**：企业微信/钉钉要求配置可信 IP 白名单；若使用自定义域名，需完成备案且主体一致，否则需通过 AppFlow 内网代理或 Nginx 转发解决（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；  
- **钉钉机器人模式**：必须选择 **HTTP 模式**，Stream 模式不兼容（[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）；  
- **本地 RAG 性能**：Embedding 模型 API 有流控，大文件可能导致知识库创建耗时显著增加，不建议单次上传 >100 MB 文件（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)


