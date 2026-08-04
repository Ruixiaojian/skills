# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档整合了新人免费额度、模型调用价格、节省计划与资源包、账单查询及训练/部署计费五大维度，旨在为开发者提供清晰、可执行的成本控制指引。所有计费逻辑均以华北2（北京）地域为默认基准，跨地域调用需注意价格与额度差异。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型类型及其核心能力：
- **文本生成模型**：千问系列（Qwen3.x、Qwen2.5、Qwen-Max/Plus/Flash）、DeepSeek、GLM 等，支持实时推理、Batch 调用、Function Calling 和上下文缓存；
- **多模态模型**：千问VL、Qwen-Omni，支持图文理解与生成；
- **图像/视频生成模型**：万相（Wan2.x），支持文生图（t2i）、图生图（i2i）、图生视频（i2v）等训练与推理；
- **语音模型**：CosyVoice、Qwen-TTS/ASR，支持语音合成与识别；
- **向量与排序模型**：text-embedding-v4、qwen3-rerank 等，用于 RAG 场景。

> **注意**：文档 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 明确指出“仅华北2（北京）地域模型享有免费额度”，而 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 中新加坡、美国等地域的单价显著高于北京，且未提及对应地域的免费额度——这表明免费额度政策存在严格的地域绑定，开发者在跨地域部署时需主动规避额度误判风险。

## 关键参数

调用与计费行为由以下关键参数驱动：
- `model`：指定模型 ID（如 `qwen3.7-plus-2026-05-26`），不同快照版本视为独立模型，额度与计费单价均不互通；
- `input_tokens` / `output_tokens`：按实际消耗 [Token](../concepts/token.md) 数量计费，输入/输出单价分档（如 `qwen3.7-plus` 在北京地域 0–256K 输入档为 ¥2/百万[Token](../concepts/token.md)）；
- `max_steps`（训练）：万相图像/视频模型训练费用的核心变量，直接影响 [Token](../concepts/token.md) 总量计算；
- `max_pixels`（视频训练）：与 `n_epochs` 共同决定视频训练 Token 消耗；
- `enable_search`：启用联网搜索插件将产生独立后付费费用，不被节省计划抵扣；
- `free_quota_stop`：控制台配置的“免费额度用完即停”开关，影响服务连续性与计费路径。

## 使用方式

开发者可通过三种主要方式接入并管理 `test 1` 相关资源：
1. **API 调用**：使用通用 API Key（非 Token Plan/Coding Plan 专属 Key）发起 HTTP 请求，系统自动按优先级顺序抵扣：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费；
2. **控制台操作**：在[模型广场](https://bailian.console.aliyun.com/#/model-market)查看剩余额度、开启/关闭“免费额度用完即停”、购买节省计划或资源包；在[费用概览](https://bailian.console.aliyun.com/#/costing-balance)监控消费趋势；
3. **成本工具集成**：通过标签绑定业务空间实现分账；设置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)防止意外欠费；利用[账单详情](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)中的 `实例 ID（出账粒度）` 字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）精准溯源费用来源。

## 限制和注意事项

- **免费额度限制**：有效期严格为 90 天（以开通/模型发布/申请通过三者最晚时间起算），到期自动作废且不可续期；仅抵扣实时推理费用，明确排除 Batch 调用、模型调优、模型部署及自定义模型（见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)）；
- **地域与模型绑定**：免费额度、部分模型（如 CosyVoice 训练）仅限华北2（北京）；新加坡、美国等地域模型虽可调用，但无免费额度且单价更高（见 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)）；
- **抵扣顺序刚性**：若开启“免费额度用完即停”，服务将直接中断，AI 通用型节省计划无法生效——必须手动关闭该开关才能触发后续抵扣（见 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)）；
- **欠费全局影响**：账户欠费时，即使其他模型仍有免费额度或节省计划余额，所有按量付费服务（含推理、部署）均暂停，必须结清欠费方可恢复（见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)）；
- **训练与部署分离计费**：模型训练按 Token 总量计费（如 Qwen3.7-Plus 训练单价 ¥0.35/千Token），而模型部署按 PTU 或模型单元时长计费，二者费用互不抵扣（见 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)）。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


