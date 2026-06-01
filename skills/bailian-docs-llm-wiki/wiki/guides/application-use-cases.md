# application [use cases](use-cases.md)

百炼平台支持多种应用场景，帮助开发者将大模型能力快速集成到不同渠道（网站、钉钉、企业微信、微信公众号等），或基于本地知识库构建 RAG 应用。核心流程通常包括：创建百炼应用、获取 API 凭证、通过 AppFlow 或代码将模型能力接入目标平台，并可选地配置知识库以增强回答准确性。

## 支持的集成渠道

| 渠道 | 集成方式 | 是否需要编码 | 关键依赖服务 |
|------|----------|------------|-------------|
| 网站 | AppFlow AI 助手 + 悬浮挂件脚本 | 仅需粘贴少量 HTML 代码 | AppFlow |
| 钉钉 | AppFlow 连接流 + 机器人配置 | 无需编码 | AppFlow、钉钉开放平台 |
| 企业微信 | AppFlow 连接流 + 应用配置 | 无需编码 | AppFlow、企业微信开发者中心 |
| 微信公众号 | AppFlow 连接流 + 公众号授权 | 无需编码 | AppFlow、微信公众平台 |
| 本地 RAG | Python 应用 + Gradio 界面 | 需要编码 | Python 3.8-3.12、LlamaIndex |

## 通用流程

所有场景均遵循以下核心步骤：

### 1. 创建百炼应用

在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建**智能体应用**，选择合适的模型，配置 Prompt 后发布。

### 2. 获取 API 凭证

- **应用 ID**：在应用管理页面查看
- **API Key**：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建

### 3. 连接目标平台

根据渠道不同，通过 AppFlow 模板或代码嵌入方式完成连接。详见各渠道文档：
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md)
- [10分钟在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat-in-10-minutes.md)

### 4. 配置知识库（可选）

通过上传文档、创建知识库、关联应用三步实现 RAG 能力，使 AI 助手能回答私域问题。

## 关键参数

### 模型选择

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| Qwen3.5-Plus / 千问-Plus | 效果、成本、速度均衡 | 通用客服场景 |
| 千问-Max (qwen-max) | 性能最优 | 对回答质量要求高的场景 |
| 千问-Turbo (qwen-turbo) | 速度快、价格低 | 对响应速度敏感的场景 |

> **注意**：不同文档中推荐的默认模型有差异——[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)推荐 Qwen3.5-Plus，而其他渠道文档推荐千问-Plus。请根据实际需求和最新模型列表选择。

### RAG 参数（本地知识库场景）

根据[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)的说明：

- **召回片段数**：控制参考文本段数量，值越大信息越多但噪声也可能增加
- **相似度阈值**：剔除相似度低于该值的文本段，为 0 时不做剔除
- **温度参数**：控制生成随机性
- **最大回复长度**：控制输出 token 数
- **携带上下文轮数**：控制历史对话参考轮数

### 知识库配置

- **向量存储类型**：可选默认存储或 ADB-PG（适合集中管理多应用向量数据）
- **调用方式**：云端知识库关联应用时建议选择"必定调用"
- **文档解析时间**：通常 1~6 分钟，取决于文档大小

## 本地 RAG 与云端 RAG 对比

| 维度 | 云端 RAG（百炼知识库） | 本地 RAG |
|------|----------------------|---------|
| 部署方式 | 0 代码，控制台操作 | 需配置 Python 环境 |
| 文档管理 | 通过百炼控制台 | 本地文件系统 |
| 嵌入模型 | 百炼提供的 API | 可选百炼 API 或本地模型 |
| 切分策略 | 平台默认 | 可自定义 |
| 适用场景 | 快速上线 | 需灵活控制检索流程 |

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖教程所需消耗，超出后按 token 计费
- **微信公众号未认证**：被动回复消息有 5 秒超时限制，超时将无法回复。建议完成认证或在 Prompt 中要求简短回答
- **钉钉机器人**：消息接收模式必须选择 HTTP 模式，AppFlow 不支持 Stream 模式
- **企业微信可信 IP**：同一 IP 仅能用于一个企业，多企业场景需使用 ECS 或 Nginx 代理转发
- **本地 RAG 文件限制**：支持 pdf、docx、txt、xlsx、csv；不建议传入超过 100 MB 的文件
- **应用上线前**：建议组织业务人员进行人工评测，通过优化提示词、补充知识、调整切分策略改进效果

## 日志与监控

钉钉和微信公众号场景均支持通过 AppFlow 添加 SLS 日志节点，将对话内容记录到阿里云日志服务中进行分析。配置方式为在 AppFlow 连接流中于百炼步骤之后添加 SLS 日志云服务节点。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)

