# Token

Token 是百炼平台中用于计量模型计算资源消耗的最小单位，代表模型处理文本、图像、语音等内容时所消耗的原子化计算量。在百炼的计费、限流、监控与推理调度体系中，Token 是统一的核心度量基准——无论是输入文本的编码、输出文本的生成、向量嵌入的计算，还是多模态内容的理解，最终均折算为 Token 数量进行资源核算与性能评估。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与资源管理**：所有模型调用（文本生成、多模态、语音、向量等）均按实际消耗的 **输入 Token + 输出 Token** 总量计费；免费额度、资源包、节省计划均以「Token」为单位抵扣；训练任务按训练数据 Token 总量计费；部署费用中的 TPM（Tokens Per Minute）也基于 Token 定义吞吐能力。
  
- **推理控制与优化**：
  - `budgetTokens`（如 OpenCode 的思考模式配置）用于限制单次推理中“思考过程”可消耗的最大 Token 数，防止过度生成；
  - TPM 预留和快速模式均以 Token 为底层计量单位（kTPM = 1000 tokens/min；TPS = tokens/sec），直接影响服务容量与响应速度；
  - 长上下文模型（如支持 128K 输入）的阶梯计价，依据输入 Token 总量分档结算。

- **可观测性与监控**：
  - 应用监控（Application Monitoring）中每个 `LLM` 节点的「Token 总量」= 输入 Token 数 + 输出 Token 数，是链路成本与性能分析的关键指标；
  - 模型监控（Model Monitoring）在日志页明确展示单次调用的 Token 用量，并支持按 Token 统计调用量趋势、失败率与成本分布；
  - 向量与排序服务（如 `text-embedding-v4`）虽不直接返回 Token，但其输入文本长度仍参与 Token 计算，影响计费与限流。

- **模型能力边界**：
  - 上下文窗口（Context Length）以 Token 数表示（如 `qwen3.7-plus` 支持 200K context），决定单次请求可处理的最大输入规模；
  - 多模态模型（如 `qwen3-vl-embedding`）将图像/视频按像素或帧数折算为等效 Token，统一纳入 Token 配额与计费体系。

## 关键参数和配置

- **`budgetTokens`**：用于约束推理过程中中间步骤（如思考链、Plan 生成）的 Token 消耗上限，典型配置值为 `1024`，需在客户端配置文件（如 `opencode.json`）或交互式工具（如 `/config`）中显式设置。
  
- **`input_tokens` / `output_tokens`**：API 响应中标准字段（如 `usage` 对象），开发者应主动解析并记录，用于成本归因、配额预警与性能调优。

- **Token 折算规则（开发者须知）**：
  - 文本：1 个中文字符 ≈ 1–2 Token（取决于分词器），英文单词平均约 1.3 Token；标点、空格、特殊符号均计入；
  - 图像：`qwen3-vl` 等模型按分辨率折算（如 1024×1024 图像 ≈ 1200–2500 Token），具体由模型内部 tokenizer 动态计算，不可手动估算；
  - 向量服务：`text-embedding-v4` 输入 1000 字符 ≈ 1200–1500 Token；异步批处理按每行文本独立计 Token；
  - 缓存命中：部分模型（如 GLM-5.2）对缓存命中的输入 Token 按折扣系数（如 0.25）计费，实际消耗 Token 数 < 原始输入 Token 数。

- **地域与模型约束**：Token 监控数据（如单次用量详情）仅在开通推理日志的地域（北京/新加坡/弗吉尼亚）可用；预览版模型（如 `qwen3.6-max-preview`）拥有独立 Token 额度，不与正式版共享。

## 面向开发者，简洁实用

- ✅ **必做**：所有生产环境调用务必解析响应中的 `usage` 字段，提取 `input_tokens` 和 `output_tokens`，用于本地配额校验与成本追踪。
- ✅ **推荐**：对长文本输入，先调用 `text-embedding-v4` 或 `qwen3.7-text-embedding` 估算 Token 数（`input` 字段长度 × 1.2~1.5 系数），避免超限报错。
- ⚠️ **注意**：`Coding Plan` 套餐禁止 API 自动化调用，其 Token 消耗仅限交互式编程工具内使用；违规调用将导致 Key 封禁。
- ⚠️ **避坑**：快速模式（`glm-5.2-fast-preview`）必须使用专属域名（`maas.aliyuncs.com`），否则 Token 计费异常且无法监控；TPM 预留实例的 model ID 含 `-tpm-` 后缀，不可混用标准 model ID。
- 📊 **诊断建议**：若发现 Token 消耗远高于预期，优先检查是否启用了思考模式（`budgetTokens` 触发额外生成）、是否传入冗余系统提示词、或图像 URL 是否返回了非预期大图。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)


