# Token

Token 是百炼平台中用于计量模型调用资源消耗的核心计费与调度单元，代表模型处理输入/输出内容的最小语义单位（如中文字符、子词或标点）。在百炼生态中，Token 不是固定长度的字节单位，而是由模型 tokenizer 动态生成的离散标识符，其数量直接影响额度消耗、性能调度与计费结果。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 订阅服务**：以 Credits 为统一计量单位，实际消耗按模型类型、Token 数量、思考模式（如工具调用、多步推理）动态折算。例如，视频生成按分辨率与时长线性增加 Token 消耗；Harness 工具调用（如 `code_interpreter`）会额外计入工具执行过程中的中间 Token。**不支持**将 Token 数简单乘以单价估算费用。

- **高吞吐推理（TPM 预留）**：Token 是容量保障的基本粒度。TPM（Token Per Minute）指每分钟可稳定处理的输入+输出 Token 总量（单位：kTPM），用于锁定专属推理资源。溢出策略（如自动降级至按量）和缓存折扣（如输入缓存命中按 25% 折算）均基于 Token 数计算。

- **快速模式（Fast mode）**：虽不显式暴露 Token 参数，但 TPS（Tokens Per Second）是核心性能指标——`glm-5.2-fast-preview` 通过优化调度路径，将输出速度提升至标准 API 的 1.5~2 倍（80~100 TPS），直接反映 Token 级别的实时吞吐能力。

- **模型评测与数据管理**：Token 用于评估数据规模与质量。例如，CPT 训练建议数据量 ≥5000 万 Token；日志回流生成训练集时，系统按 Token 数统计有效样本容量；评测集虽不直接计费，但大模型评估器（如裁判模型）的调用本身也按 Token 消耗 Credits。

> ⚠️ 注意：Token 的具体数值取决于所用模型的 tokenizer（如 Qwen 使用 tiktoken 兼容分词器，GLM 使用自研分词器），同一文本在不同模型下 Token 数可能差异显著。开发者应通过 `/v1/tokenize` 接口（若开放）或 SDK 的 `count_tokens()` 方法实测，不可跨模型套用经验值。

## 关键参数和配置

| 场景 | 关键参数 | 说明 | 开发者须知 |
|------|----------|------|------------|
| **Token Plan** | `sk-sp-xxx` API Key | 必须使用 `sk-sp-` 开头的专属密钥，与通用 `sk-` 密钥隔离 | 错误密钥会导致 `401 Unauthorized`，且无法抵扣 Token Plan 额度 |
| | Base URL | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 仅限华北2（北京）地域，其他地域请求返回 `403 Forbidden` |
| | Credits 消耗 | 动态计算，非 `Token × 单价`；含模型系数、工具调用加成、缓存折扣等 | 查看消耗请登录控制台「额度中心」，或解析响应头 `X-Credits-Used` 字段 |
| **TPM 预留** | `model` 字段 | 使用专属 model code（如 `qwen3-max-dedicated-xxxxx`） | 替换标准模型 ID 后即生效，无需改 Base URL（仍用 DashScope 域名） |
| | kTPM 配置值 | 创建时设定，如 `100 kTPM` = 每分钟 10 万 Token 容量 | 溢出策略需显式选择：`自动溢出至按量`（默认）或 `仅预留容量（429）` |
| **快速模式** | `model` 字段 | 固定为 `glm-5.2-fast-preview` | 必须使用专属域名 `https://{workspace_id}.{region}.maas.aliyuncs.com/...`，否则降级为标准模式 |
| | 输入缓存单价 | `glm-5.2-fast-preview` 输入缓存为 4 元/百万 Token | 缓存命中时，仅按折扣后 Token 数计费，响应头 `X-Cache-Hit: true` 可验证 |

## 面向开发者，简洁实用

- ✅ **必做**：  
  - 所有 Token Plan 调用必须使用 `sk-sp-` 密钥 + 北京地域 Base URL；  
  - TPM 预留需替换 `model` 字段，快速模式需替换 `model` + Base URL；  
  - 多模态模型（图像/视频/语音）**不可**通过 Chat Completions 接口调用，必须走独立 API 或 Harness 工具扩展机制。

- ❌ **禁止**：  
  - 将 Token Plan 用于自动化脚本、批量任务或应用后端服务（仅限交互式开发工具）；  
  - 在非北京地域尝试 Token Plan 或基线评测（控制台对应入口将隐藏）；  
  - 混用 TPM 预留 model code 与快速模式域名（返回 `404 Not Found` 或降级）。

- 🔍 **调试技巧**：  
  - 用 `curl -H "Authorization: Bearer sk-sp-xxx" "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/models"` 查看当前可用模型列表；  
  - 响应头中关注 `X-Credits-Used`（消耗 Credits）、`X-TPM-Remaining`（TPM 预留剩余）、`X-Cache-Hit`（缓存状态）；  
  - 对长文本，先调用 `/v1/tokenize`（如有）预估 Token 数，避免因超限触发 429。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model data overview](../guides/model-data-overview.md)


