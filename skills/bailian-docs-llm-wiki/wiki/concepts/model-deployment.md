# 模型部署

模型部署是百炼平台将训练完成或预置的模型转化为稳定、可扩展、生产就绪的在线推理服务的核心能力。它通过资源隔离、性能保障与标准化接口，使模型可被业务系统以低延迟、高可靠方式调用。

## 在百炼平台的不同场景中，这个概念如何使用

- **预置模型即开即用**：无需训练，直接在控制台或 API 中选择千问（Qwen3/Qwen2.5）、DeepSeek、GLM、Kimi-K2.5、CosyVoice 等官方预置模型，按需部署为专属服务。
- **微调模型服务化**：对通过 `supervised_fine_tuning`（SFT）等范式完成训练的自定义模型（如 `qwen3-8b-ft-20251113`），一键部署为独立 endpoint，支持灰度发布、版本回滚与弹性扩缩容。
- **LoRA 模型轻量部署**：仅支持从 OSS 导入的 LoRA 微调模型（rank ∈ {8,16,32,64}，chat_template 和 tokenizer 未修改），适用于低成本验证与快速上线；全参微调模型暂不支持导入部署。
- **压缩后模型部署**：经量化压缩（如 INT8）的微调模型，可部署为更低规格（如 MU8）实例，在成本降低 50%+ 的同时保持可用推理质量。
- **[多模态](multi-modal.md)与语音模型服务化**：支持 Qwen-VL、Wan 图像/视频生成模型、CosyVoice 语音合成模型等统一通过 `/v1/chat/completions` 或专用接口调用，部署逻辑一致。

> ⚠️ 所有部署均**仅支持华北2（北京）地域**；跨地域调用需通过 API Gateway 或应用层代理实现。

## 关键参数和配置

| 部署模式 | 必填参数 | 说明 | 典型值示例 |
|----------|-----------|------|-------------|
| **通用** | `name` | 服务唯一标识，≤50 字符，建议含模型名与用途 | `"qwen3-8b-chat-prod"` |
| | `model_name` | 模型 ID（预置模型）或 `model_id`（微调/压缩产出模型） | `"qwen3-8b"` / `"qwen3-8b-ft-20251113"` |
| **PTU（预置吞吐）** | `plan: "ptu"`<br>`ptu_capacity.input_tpm`<br>`ptu_capacity.output_tpm` | 按分钟 [Token](token.md) 吞吐量预购资源，保障长上下文（最高 256K）与缓存命中率 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| **MU（模型单元）** | `plan: "mu"`<br>`deploy_spec`<br>`capacity` | 按计算单元规格（如 MU1/MU8）和副本数分配资源，支持 PD 分离、思考模式、RPM/TPM 限流 | `"MU1"`, `4`（4 个副本） |
| **[Token](token.md) 计费（LoRA 专属）** | `plan: "lora"` | 仅适用于 SFT 训练的 LoRA 模型；`capacity` 参数必须传但无效，扩缩容需走控制台申请 | `"lora"` |
| **生产级运维（API 方式）** | `instance_type`<br>`replicas` | 底层 GPU 实例规格与副本数（用于 `model production` 流程） | `"gpu.g1.2xlarge"`, `2` |

- 所有部署均返回 `deployment_id`，用于后续调用（如 `Generation.call(model='dp-xxx')`）与监控；
- `max_context_length`、`enable_thinking` 等高级能力需在 MU 模式下显式配置，且受基础模型能力限制；
- 部署成功后，自动接入百炼统一监控体系，支持用量、延迟、错误率、缓存命中率等指标实时观测。

## 面向开发者，简洁实用

- ✅ **首选控制台**：新手或快速验证 → 进入 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，可视化配置，5 分钟完成；
- ✅ **自动化集成**：CI/CD 或批量部署 → 使用 DashScope SDK 或 curl 调用 `/v1/deployments` API，参数 JSON 化，支持幂等创建；
- ✅ **调用即标准**：无论何种部署模式，均兼容 OpenAI/DashScope 标准接口：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"dp-xxxxxx","input":{"messages":[{"role":"user","content":"你好"}]}}'
  ```
- ✅ **监控必开**：部署后立即前往 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 页面，开通「推理日志」与「性能指标」，分钟级定位超时、OOM 或 token 截断问题；
- ❌ **避坑提示**：  
  - 不要尝试部署全参微调模型（仅 LoRA 支持）；  
  - 不要跨地域部署（北京以外地域会报错）；  
  - [Token](token.md) 计费模式不支持扩缩容 API，需提工单或控制台操作；  
  - 压缩模型部署后不可再微调，务必保留原始微调模型作为备份。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [model monitoring](../guides/model-monitoring.md)


