# Token

Token 是百炼平台中用于计量模型调用资源消耗的核心计费与观测单位，代表模型处理输入（[prompt](../guides/prompt.md)）和生成输出（completion）过程中所消耗的文本单元。在百炼体系中，Token 不仅是 Credits 抵扣、用量监控和成本分析的基础粒度，也是性能诊断（如首 Token 延时）、模型评测（裁判模型计费）及多模态资源折算（图像/音频等按规则换算为等效 Token）的统一标尺。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额**：Token Plan 团队版以 Credits 统一抵扣，1 Credit = 1,000 Tokens（文本模型），图像生成按张数折算为等效 Token（如 `qwen-image-2.0` 每张 ≈ 500 Tokens），抵扣顺序为「坐席月度额度 → 共享用量包 → 暂停服务」。
- **可观测性**：  
  - 应用观测（Application Monitoring）中，LLM 节点的「Token 总量」= 输入 Token + 输出 Token；Embedding 节点仅统计向量化输入的 Token 量；  
  - 模型监控（Model Monitoring）提供细粒度 `input_tokens` / `output_tokens` / `cache_tokens` 等 `usage_type` 指标，支持按业务空间、模型、API Key 下钻分析；  
  - 所有 Token 消耗均分钟级同步（高级监控）或小时级聚合（基础监控）。
- **模型评测**：大模型评估类维度需调用裁判模型（如 `qwen3.7-max`），其评分过程产生的输入与输出 Token 单独计费，费用计入评测任务账单；规则评估与人工评估不产生 Token 费用。
- **API 调用约束**：`max_tokens` 参数直接限制输出长度上限（单位：Token），超限将触发 `Range of max_tokens should be [1, xxx]` 错误；多模态模型（如 `qwen3-vl-plus`）的 `messages.content` 中每张图片、每段视频均按预设规则折算为 Token 并计入总限额。

## 关键参数和配置

- `max_tokens`：必填整数，指定最大输出 Token 数，取值范围由模型文档明确限定（如 `qwen3.6-plus` 为 `[1, 8192]`），不可设为 0 或负数。
- `input_tokens` / `output_tokens`：只读指标，由平台自动统计，用于监控、告警与账单结算，开发者无需手动传入。
- Token 折算规则（非 API 参数，但影响用量）：
  - 文本：UTF-8 编码下，中文字符约 1–2 Token/字，英文单词平均 1.3 Token/词；
  - 图像：`qwen-image-2.0` 默认 500 Tokens/张，`qwen-image-2.0-pro` 为 1,200 Tokens/张；
  - 音频/视频：按时长与模型规格折算（如 `cosyvoice-v3-flash` 每秒语音 ≈ 15 Tokens）；
  - 缓存 Token（`cache_tokens`）：启用 KV Cache 时复用历史计算结果，按实际节省量计为负 Token，降低总消耗。

## 面向开发者，简洁实用

- ✅ **务必检查 `max_tokens` 上限**：调用前查阅对应模型文档，避免因超限返回 400 错误。
- ✅ **用环境变量管理 API Key**：设置 `DASHSCOPE_API_KEY=sk-ws-xxx`，杜绝硬编码与日志泄露。
- ✅ **监控 Token 用量防超支**：在控制台开启「高级监控」，配置 `model_usage{usage_type="total_tokens"}` 告警，阈值建议设为月度预算的 80%。
- ✅ **图像/多模态调用需显式声明**：文本模型（如 `qwen3.6-plus`）不支持 `image_url`；必须使用 `qwen-image-2.0` 等专用模型 ID，并通过 `/multimodal-generation` endpoint 调用。
- ❌ **不要跨地域混用 Key 与 Base URL**：Token Plan 专属 Key 仅支持华北2（北京）地域，且必须搭配其指定 Base URL（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
- ❌ **勿在自动化脚本中滥用 Token Plan**：该套餐仅限交互式工具（Cursor/Claude Code 等）使用，批量调用将触发封禁。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


