# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的 AI 应用快速落地，核心模式为“大模型应用（LLM） + 知识增强（RAG） + 多端集成”。所有方案均基于统一的百炼应用作为推理后端，通过 AppFlow 实现零代码连接主流企业通讯与内容平台（如网站、企业微信、钉钉、微信公众号），并支持本地化知识库部署。开发者可复用同一套 Prompt 工程、知识库配置和评测流程，显著降低多渠道 AI 助手的构建与维护成本。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（即文档中提及的“千问-Plus”或“Qwen3.5-Plus”），在效果、速度与成本间取得平衡；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（超低成本）。> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均写为“千问-Plus”，二者实际为同一模型的不同命名；当前控制台显示名称以 `qwen-plus` 为准，建议开发者以控制台实际可选模型列表为准 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **核心能力**：
  - 智能体（Agent）应用：支持角色设定（Prompt）、工具调用（如知识库检索）、多轮对话管理；
  - RAG 增强：通过知识库实现私有领域问答，支持 PDF/DOCX/TXT/Excel 等格式上传与向量化；
  - 多模态支持：文档 2、4、5 均明确列出 `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif` 等图片格式支持，适用于产品图谱、说明书图像理解等场景。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制生成随机性，值域通常为 0.0–1.0 | 百炼应用配置页、[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的 Gradio 界面 |
| | `max_tokens` | 限制模型输出最大 token 数 | 同上 |
| | `top_p` / `top_k` | 影响采样多样性 | 百炼应用高级设置（部分模型支持） |
| **RAG 层** | `retrieval_top_k` | 召回片段数（如“召回 3 个最相关段落”） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的 Gradio 界面；百炼知识库引用配置中对应“相似度阈值”与“权重” |
| | `similarity_threshold` | 过滤低相关性召回结果的阈值（0–1） | 百炼应用配置页 > 知识库 > “相似度阈值”字段 |
| | `chunk_size` / `chunk_overlap` | 文档切分粒度（影响检索精度） | 百炼知识库创建时的“索引设置”；本地 RAG 应用中可自定义切分逻辑 |

## 使用方式

1. **统一后端：创建百炼应用**  
   所有场景均始于百炼控制台的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建**智能体应用** → 配置模型、Prompt 与知识库。应用发布后获得唯一 `AppID` 和调用所需的 `API Key`。

2. **前端集成：通过 AppFlow 连接目标平台**  
   - **网站嵌入**：使用 AppFlow 创建 AI 助手 → 关联百炼应用 → 生成悬浮挂件脚本 → 插入 HTML 即可 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
   - **企业微信/钉钉/微信公众号**：使用 AppFlow 预置模板（如“企业微信自建应用大模型自动回复”）→ 分别配置平台凭证（企业 ID/AgentId/Secret 或 Client ID/Secret 或 AppID）与百炼凭证 → 获取 Webhook URL → 在对应平台后台完成消息接收配置。

3. **知识增强：配置知识库（可选但推荐）**  
   - 上传文件至百炼[数据中心](https://bailian.console.aliyun.com/?tab=app#/data-center) 或[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；  
   - 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建标准版知识库；  
   - 在应用配置页启用知识库，设置调用方式（如“必定调用”）及相似度阈值。

## 限制和注意事项

- **免费额度与计费**：新用户享有百炼免费额度，覆盖教程全部操作；额度耗尽后按 token 计费，具体见 [新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota) [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **文件限制**：单文档最大 100 MB 或 1000 页，单图片最大 20 MB，最多上传 200 个文件；知识库创建过程需等待解析（通常 1–6 分钟）。
- **平台特异性约束**：
  - 微信公众号：未认证订阅号仅支持被动回复（5 秒超时限制），建议完成认证或选用 `qwen-turbo` 模型提速 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；
  - 企业微信：配置 API 接收消息时需通过域名主体校验，若无自有备案域名，需通过 AppFlow 的 Nginx 代理或计算巢实例解决 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
  - 钉钉：机器人消息接收模式**必须选择 HTTP 模式**，Stream 模式不兼容 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
- **本地 RAG 场景**：适用于需完全私有化部署、灵活控制文档切分与嵌入模型的场景，但需自行维护 Python 环境（3.8–3.12）及依赖，且不直接集成百炼控制台的统一监控与评测能力 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


