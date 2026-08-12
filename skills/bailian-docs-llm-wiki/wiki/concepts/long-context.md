# 长上下文

长上下文（Long Context）指模型在单次推理中能够接收、理解并有效利用的输入文本（或结构化内容）的最大长度，以 [Token](token.md) 数量为计量单位。它决定了模型处理长文档摘要、法律合同分析、代码库理解、多轮复杂对话等任务的能力边界；百炼平台部分文本模型支持最高达 1000 万 [Token](token.md) 的上下文窗口，是当前业界领先水平。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成任务**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-long` 等模型原生支持超长上下文。例如，向 `qwen-long` 输入 800 万 [Token](token.md) 的财报 PDF 文本（经 OCR 或解析后转为纯文本），可直接执行全文摘要、跨章节问答或关键数据提取，无需分块切片或外部 RAG 检索。
  
- **模型部署配置**：在 MU（模型单元）部署时，可通过 `max_context_length` 参数显式指定服务端允许接收的最大输入长度（如设为 `2000000` 表示 200 万 Token），该值不可超过模型自身能力上限；PTU 部署则依赖模型固有规格，超出时自动触发溢出计费（响应头含 `x-dashscope-ptu-overflow:true`）。

- **RAG 与知识增强**：长上下文可替代或补充传统 RAG 流程——当检索结果总长度 ≤ 模型上下文余量时，可将 top-k chunk 直接拼入 system/user message，避免 embedding 失真与重排序误差；但需注意：过长上下文会显著增加首 Token 延迟（TTFT）和总耗时，建议结合 `enable_thinking=false` 关闭思考模式以提速。

- **多模态输入约束**：视觉/视频模型虽也标称“1M 上下文”，但其 Token 计算方式不同（如图像 ≈ `h×w/(32×32)+2`）。此时“长上下文”实际体现为支持高分辨率图、长时视频（最长 2 小时）或多帧密集采样，而非纯文本长度。

> ⚠️ 注意：`qwen-long` 仅支持纯文本长上下文，**不支持 Function Calling、内置工具（联网搜索/代码解释器）及结构化 JSON 输出**；若需工具调用能力，请选用 `qwen3.8-max`（1M Token）并配合分块+RAG 或异步任务编排。

## 关键参数和配置

| 场景 | 参数名 | 取值说明 | 是否必需 |
|------|--------|----------|----------|
| API 调用 | `max_tokens`（输出限制） | 控制生成内容长度，不影响输入容量；与上下文长度无关 | 否（默认由模型决定） |
| MU 部署 | `max_context_length` | 整数，单位 Token；必须 ≤ 模型原生上限（如 `qwen3.7-plus` 最大为 `1048576`） | 是（部署时显式声明） |
| PTU 部署 | `ptu_capacity.input_tpm` | 输入吞吐量配额（KTPM），影响并发处理长输入的能力 | 是 |
| 所有文本模型 | `enable_thinking` | 设为 `false` 可降低长上下文下的延迟；`true` 会显著增加 TTFT 和总耗时 | 否（默认 `false`） |
| 客户端 SDK | 连接池配置（如 `connectionPoolSize`） | 长上下文请求体大、耗时长，建议增大连接池（如设为 `64`）避免连接阻塞 | 推荐 |

- **Token 计算参考**：
  - 中文文本：约 1 个汉字 ≈ 1.3–1.5 Token（取决于分词粒度）
  - 英文文本：约 1 个单词 ≈ 1.2–1.3 Token
  - 代码：Python/Java 等语法丰富语言，Token 效率更低（1KB ≈ 1200–1500 Token）

- **调试建议**：首次使用长上下文前，先用 `GET /api/v1/models` 查询目标模型的 `max_context_length` 字段确认能力；调用时监控响应头 `x-dashscope-usage-input-tokens` 和 `x-dashscope-usage-output-tokens`，验证实际消耗是否符合预期。

面向开发者，请始终以模型广场实时参数为准，避免依赖文档中已过期的快照模型 ID（如 `qwen3.7-plus-2026-05-26`）——其上下文能力可能低于主干版本。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [more about models](../api/more-about-models.md)
- [get started with models](../guides/get-started-with-models.md)


