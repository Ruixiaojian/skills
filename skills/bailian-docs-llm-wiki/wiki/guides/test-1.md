# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与使用规范主题，涵盖模型调用、训练、部署及成本管理的全链路规则。其核心逻辑围绕“免费额度优先抵扣 → 资源包/节省计划次级抵扣 → 按量付费兜底”的三级费用结算体系展开，所有模型服务均默认按 Token 或时长计量，地域（如华北2北京）和模型版本（如带日期后缀的快照）直接影响额度归属与计价标准。开发者需特别注意免费额度的独立性、地域限制及自动失效机制，避免因配置疏漏导致意外计费。

## 支持的模型/功能

- **支持模型类型**：覆盖文本生成（千问系列、DeepSeek、GLM）、多模态（千问VL、万相图像/视频）、语音（CosyVoice、Qwen-TTS/ASR）及向量/排序模型。其中，仅华北2（北京）地域的模型享有新人免费额度，其他地域（如新加坡、美国弗吉尼亚）无此权益 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **关键功能覆盖**：
  - 实时推理（支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）
  - Batch 批量调用（输入/输出 Token 单价为实时推理的 50%）
  - 模型训练（按训练 Token 总量计费）
  - 模型部署（支持预置吞吐 PTU 和模型单元 MU 两种计费模式）
  - 上下文缓存（显式/隐式缓存有独立计价规则，未包含在基础单价中）[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、自定义模型（调优后或已部署模型）、PAI-DSW、OSS 存储及请求费用 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 5 中 `qwen3.7-max` 在华北2（北京）标注为“当前能力等同于 `qwen3.7-max-2026-05-20`”，但文档 2 的部署价格表中 `qwen3.7-max-2026-05-20` 与 `qwen3.7-max` 分列为两个独立模型代码，且单价一致。这表明二者在部署计费上视为同一模型，但免费额度规则要求“带日期后缀的快照版本与不带日期的最新版本视为两个独立模型，各自拥有独立额度” [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。因此，开发者需严格按 `model` 参数指定完整模型 ID，不可混用。

## 关键参数

- **Token 计量**：输入/输出 Token 统一计入免费额度总额度，不单独区分；调用时系统自动按 `输入 Token + 输出 Token` 扣减 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域参数**：Base URL 必须匹配服务地域（如华北2北京为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），否则无法使用免费额度或触发对应地域的计价 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **API Key 类型**：通用 API Key 可消耗免费额度；Token Plan/Coding Plan 专属 API Key 不消耗免费额度，直接按量付费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署参数**：
  - PTU 模式：需指定 `输入 TPM` 和 `输出 TPM`，溢出策略可选「自动溢出」（切至按量付费）或「仅使用 PTU 容量」（返回 429）。
  - 模型单元（MU）模式：需选择 `模型单元规格`（如 MU1 x 8）及计费周期（小时/月）。

## 使用方式

- **开通与额度获取**：首次开通百炼即自动发放免费额度（无需实名认证），仅限华北2（北京）地域模型，有效期 90 天（以开通/模型发布/申请通过三者最晚时间起算） [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **调用流程**：
  1. 在控制台 [模型广场](https://bailian.console.aliyun.com/#/model-market) 确认目标模型支持免费额度（蓝色额度条标识）；
  2. 使用通用 API Key，通过标准 REST API 调用（如 `POST /v1/chat/completions`）；
  3. 系统自动优先抵扣免费额度，余额不足时按配置顺序启用资源包、节省计划或按量付费。
- **成本优化路径**：
  - 长期稳定使用：优先购买 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖全部阿里直供模型；
  - 单模型集中调用：购买对应模型的 [资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，一次性预购 Token 量；
  - 团队协作：选用 Token Plan 团队版，按席位共享 credits 额度。

## 限制和注意事项

- **免费额度限制**：
  - 主账号与 RAM 子账号共享额度，但不同模型（含不同快照版本）额度完全独立，不可互通；
  - 额度到期自动作废，不支持补发、延期或重置；重新注册账号无法再次领取 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **计费生效延迟**：模型推理账单为分钟级出账（通常 2~10 分钟），训练/部署账单为小时级；控制台显示的剩余额度为分钟级更新，需手动刷新页面以获取最新状态 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响**：账户可用额度 < 0 时，即使免费额度或节省计划仍有剩余，所有按量付费服务（包括模型调用）将暂停；Coding Plan/Token Plan 套餐额度独立于账户余额，欠费期间仍可使用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **部署服务持续计费**：模型部署状态为「运行中」即开始计费，与是否发生 API 调用无关；需主动下线部署实例才能停止计费 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


