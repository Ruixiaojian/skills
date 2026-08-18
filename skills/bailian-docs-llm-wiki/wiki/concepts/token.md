# Token 计量与计费

Token 计量与计费是百炼平台统一、精准的资源消耗度量与成本核算机制：所有模型服务（文本、多模态、语音、向量等）均以 **Token** 为基本计量单位，按实际消耗的输入 Token 与输出 Token 总量计费；计费逻辑贯穿调用、训练、部署、缓存、监控等全生命周期，是开发者进行成本控制、预算规划与性能优化的核心依据。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时/批量推理调用**：  
  每次 `POST /v1/chat/completions` 等请求，系统自动解析请求内容（[prompt](../guides/prompt.md) + system message + tools + images 等）和响应内容（completion），分别统计输入 Token 数与输出 Token 数，二者之和即为本次调用的计费 Token 总量。Batch 调用单价为实时调用的 50%，但计量逻辑完全一致。

- **模型训练**：  
  按训练过程中实际消耗的 **训练 Token 总量**（即全部训练样本的输入 Token 数之和）计费，与 epoch 数、batch size 无关，仅取决于数据集规模与预处理后的 tokenized 长度。

- **模型部署（PTU/MU 模式）**：  
  PTU 模式下，部署实例持续占用预购的输入/输出 TPM（Tokens Per Minute）配额；超出部分自动按量计费（按 Token）。MU 模式虽以“模型单元”为计费单元，但底层资源调度仍基于 Token 吞吐能力建模，其规格（如 MU1 x 8）隐含对应的最大 TPM 上限。

- **上下文缓存（显式/隐式）**：  
  缓存命中时，系统对重复输入段落不重复计费，仅对新增输入 Token 和完整输出 Token 计费；缓存未命中或失效时，全程按标准 Token 计量。不同模型缓存折扣系数不同（如 Qwen3.8-max 为 0.125，GLM-5.2 为 0.25），直接影响有效 Token 成本。

- **应用与模型监控**：  
  所有可观测指标（如 `model_usage` Prometheus 指标、应用监控中的 `Token总量` 字段）均直接呈现原始 Token 消耗值，支持按分钟/小时粒度追踪、告警与归因分析，是成本治理的数据基石。

- **Token Plan 订阅**：  
  Credits 消耗非固定换算，而是动态映射为等效 Token 价值——例如图像生成按分辨率×长宽比折算为等效 Token，视频生成按秒数×码率加权，Harness 工具调用额外叠加思考 Token。最终仍归一为统一 Credits 消耗，本质是 Token 计量的抽象封装。

## 关键参数和配置

- **`model` 参数（必需）**：  
  必须精确指定完整模型 ID（如 `qwen3.7-max-2026-05-20`），带/不带日期后缀视为独立模型，拥有独立免费额度与计价规则；混用将导致额度无法抵扣或计费异常。

- **地域（Region）绑定**：  
  Token 计量与计费严格绑定服务地域。华北2（北京）是唯一支持新人免费额度的地域；Token Plan 仅支持 `cn-beijing`；TPM 预留、快速模式、高级监控等功能亦按地域隔离计费与用量统计。

- **API Key 类型决定计费路径**：  
  - `sk-` 开头通用 Key：可消耗免费额度 → 资源包/节省计划 → 按量付费；  
  - `sk-sp-` 开头 Token Plan Key：仅消耗订阅 Credits，不走账户余额；  
  - Coding Plan Key：独立额度体系，与 Token Plan 不互通。

- **Base URL（协议入口）**：  
  不同计费模式需匹配专属域名：  
  - 标准调用：`https://dashscope.aliyuncs.com/compatible-mode/v1`（华北2）；  
  - Token Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；  
  - 快速模式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。  
  域名错误将导致计费路径失效（如 Token Plan Key 走标准域名，Credits 不抵扣）。

- **TPM 配置（PTU 模式）**：  
  需显式声明 `input_tpm` 和 `output_tpm`（单位：kTPM），并设置溢出策略：`auto_overflow`（切按量）或 `only_use_ptu`（返回 429）。

## 面向开发者，简洁实用

- ✅ **始终检查 `model` + `region` + `API Key` + `Base URL` 四要素一致性**：任一错配都将导致免费额度失效、Credits 不抵扣或计费异常。  
- ✅ **Token 数可在控制台实时验证**：调用后 1–2 分钟内，进入「模型监控」→「调用统计」页查看本次请求的精确 Token 消耗；开通日志后可在「日志」页看到明细。  
- ✅ **批量调用更省**：Batch 单价为实时调用的 50%，适合离线处理、评测、数据合成等非交互场景。  
- ✅ **善用缓存降低成本**：对高频重复 [prompt](../guides/prompt.md)，启用上下文缓存可显著降低有效 Token 消耗（折扣系数见控制台模型详情页）。  
- ✅ **长期稳定调用优先选资源包或节省计划**：资源包按模型预购 Token 量（无有效期限制），节省计划承诺月消费额享最高 5.3 折，二者均可覆盖全部阿里直供模型。  
- ⚠️ **注意免费额度边界**：Batch、训练、部署、自定义模型、PAI-DSW、OSS 等均不享受免费额度；额度按模型快照版本独立计算，不可跨版本共享。  
- ⚠️ **Token Plan 严禁用于后端服务**：仅限交互式开发工具（如 Cursor、Claude Code）接入；自动化脚本或生产 API 服务请使用标准按量或资源包模式。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


