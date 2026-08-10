# Token

Token 是百炼平台中用于计量模型输入与输出文本单元的基本计费与资源消耗单位。它并非原始字符，而是由模型 tokenizer 对文本进行分词后生成的离散语义单元（如子词、标点或特殊符号），其数量直接决定调用成本、额度消耗及性能指标统计。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与额度管理**：所有按量付费的模型调用（除 Coding Plan 外）均以 `输入 Token 数 + 输出 Token 数` 为计费依据；新人免费额度（100 万 Token/模型）、节省计划、资源包均按 Token 消耗抵扣；Batch 调用享 50% Token 折扣。
- **高吞吐保障（TPM 预留）**：TPM（Tokens Per Minute）是容量预留的核心单位，按 kTPM（千 Token/分钟）预购专属输入/输出吞吐能力，确保高峰期稳定调用。
- **性能监控**：模型监控中 `model_usage` 指标即 Token 总消耗量；`model_tps_per_request`（Tokens Per Second）反映输出速度；应用监控中每个 LLM 节点明确展示 `input_tokens` 和 `output_tokens`，支持按 Token 量筛选异常请求。
- **推理加速（快速模式）**：虽不设 Token 配额，但计费仍基于实际输入/输出 Token 数，且返回结构中 `cached_tokens` 字段体现缓存优化带来的 Token 成本减免。
- **模型训练与部署**：视频训练按像素与轮数折算 Token 总量；PTU（预置吞吐单元）按 TPM 计费；自定义模型部署不享受免费额度，Token 消耗全额计费。

## 关键参数和配置

- **Token 计算方式**：由模型内置 tokenizer 精确计算，开发者无需手动分词；可通过 API 响应中的 `usage.input_tokens` / `usage.output_tokens` 字段获取（流式响应在末尾 `delta` 中返回）。
- **阶梯计费**：部分模型（如 `qwen3.6-max-preview`）对长输入（如 128K–256K 区间）应用系数加权（如 ×1.33），实际计费 Token = 基础 Token × 阶梯系数。
- **缓存优惠**：TPM 预留与快速模式均支持缓存，`cached_tokens` 字段显式返回命中缓存的 Token 数，对应部分按折扣单价计费（如 GLM-5.2 缓存折扣率 25%）。
- **地域约束**：免费额度仅限华北2（北京）地域生效；不同地域模型 Token 单价可能不同，需通过 Base URL 明确调用地域。

## 面向开发者，简洁实用

- ✅ 调用后务必检查响应 `usage` 字段，验证 Token 消耗是否符合预期（尤其长上下文场景）；
- ✅ 免费额度自动优先抵扣，无需配置；若需控制支出，可在账单设置中开启“免费额度用完即停”；
- ✅ 监控告警可配置“Token 消耗超阈值”规则，及时发现异常调用；
- ✅ 使用 TPM 预留时，替换 `model` 参数为专属 model code（如 `qwen3.8-max-tpm-abc123`），域名保持不变；
- ✅ 快速模式必须使用专属域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/...`），且仅支持 `glm-5.2-fast-preview`；
- ❌ Coding Plan 不计 Token，按请求次数计费，其 API Key 与 Token Plan 不互通，不可混用。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)


