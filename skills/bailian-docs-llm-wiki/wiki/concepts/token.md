# Token

Token 是百炼平台中用于计量大语言模型及多模态模型推理消耗的核心单位，代表模型处理文本、图像、语音等输入内容及生成输出内容的基本计算粒度。在百炼体系中，Token 不仅是计费的基础单元，也是性能监控、成本分析与资源调度的关键指标。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有实时推理调用（含 [prompt](../guides/prompt.md) 输入与 response 输出）均以 Token 总量为计费依据。新人免费额度、Token Plan Credits 消耗、按量付费账单均基于 `输入 Token 数 + 输出 Token 数` 计算，不区分方向，也不单独计费缓存 Token（除非显式启用缓存功能并产生额外缓存 Token）。
  
- **模型监控**：在「模型监控」中，`model_usage` 指标直接上报 Token 消耗量，支持按业务空间、API Key、模型等维度聚合统计；高级监控还提供 `model_generation_duration_per_token`（每 Token 生成耗时）等精细化性能指标。

- **应用观测**：在「应用观测」中，每个 LLM 节点的 Span 明细页展示该次调用的 `输入 Token 数`、`输出 Token 数` 和 `Token 总量`，可结合延时、首 Token 时间等指标诊断推理效率瓶颈；Embedding 节点则仅统计向量化输入的 Token 数。

- **应用评测**：自动评测任务依赖 `qwen-max`/`qwen-plus` 等模型生成评测集和执行评分，其过程本身会产生可观的 Token 消耗——评测规则中的“分类采样数”和所选评测模型直接影响总 Token 用量，需在成本预算中提前评估。

- **Token Plan 与 Coding Plan 隔离**：Token Plan 使用 Credits 抵扣，但 Credits 消耗由底层 Token 数、模型单价、工具调用次数等动态换算得出，**无固定 Token→Credits 比例**；且 Token Plan 专属密钥（`sk-sp-xxx`）与通用密钥（`sk-xxx`）走不同计费通道，Token 消耗互不抵扣。

## 关键参数和配置

- **计量范围**：默认包含 [prompt](../guides/prompt.md) 中全部文本 Token + response 中全部生成 Token；若启用流式响应，Token 统计仍以完整输出为准（非已返回部分）；多模态模型中，图像/音频/视频输入会按平台统一编码规则转换为等效 Token 数（具体换算逻辑由模型实现决定，开发者无需手动计算）。

- **地域约束**：Token 计量与计费严格绑定地域。华北2（北京）是唯一支持新人免费额度、Token Plan 及多数模型高级监控能力的地域；跨地域调用（如华东1）将按量计费，且不计入任何额度。

- **模型快照独立性**：带日期后缀的模型（如 `qwen3.7-max-2026-05-20`）与无后缀版本（如 `qwen3.7-max`）视为不同模型，各自拥有独立的 Token 额度、计费单价与监控数据隔离。

- **缓存 Token**：当启用 Prompt Cache 功能时，重复 [prompt](../guides/prompt.md) 的缓存命中会减少输入 Token 计费量（系统按实际缓存复用后的 Token 数计量），但需注意缓存本身不免费，可能产生额外缓存管理费用。

## 面向开发者，简洁实用

- ✅ **务必检查地域与密钥匹配**：调用前确认 API Key 类型（`sk-` 或 `sk-sp-`）与 Base URL 地域（`cn-beijing`）一致，否则 Token 消耗可能落入错误计费通道。

- ✅ **监控 Token 分布**：在应用观测中按 Span 查看各节点 Token 占比，快速识别高 Token 消耗环节（如过长 system prompt、冗余 RAG 片段、未裁剪的图片 base64）。

- ✅ **估算成本**：使用 [模型调用价格页](https://help.aliyun.com/zh/model-studio/pricing) 查询目标模型的单价（元/千 Token），结合预估输入/输出长度，即可粗算单次调用成本。

- ⚠️ **避免隐式 Token 浪费**：  
  - 不在 prompt 中插入无意义空行或重复指令；  
  - 对多模态输入，优先使用平台推荐的压缩格式（如 WebP 图像、16kHz 语音）；  
  - 工作流中慎用 `RETRIEVER` 返回全文，建议配置 `top_k=3` 并启用内容截断。

- 🔍 **调试技巧**：开启「推理日志」后，在模型监控 → 日志页可查看每次调用的精确 Token 数（含分项 breakdown），是定位异常消耗的首选手段。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [application evaluation](../guides/application-evaluation.md)


