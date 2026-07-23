# 模型部署

模型部署是将训练或微调完成的模型（包括基础模型、LoRA 微调模型、量化模型等）发布为高可用、可计量、可管理的生产级推理服务的过程。在百炼平台中，模型部署是连接模型开发与业务调用的关键环节，提供统一 API 接口、多维度资源模型和细粒度控制能力，确保模型在真实场景中稳定、高效、合规地对外提供服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **面向基础模型直接推理**：无需微调，可直接选择 `qwen3.7-plus-2026-05-26`、`glm-5.1`、`deepseek-v4-pro` 等官方模型，按 PTU、MU 或 LoRA（仅限已导入 LoRA）方式部署，快速获得生产就绪 endpoint。
- **面向微调模型上线**：通过 `model production` 流程完成微调后，使用生成的 `fine_tuned_model_id` 创建部署实例，支持绑定 `version_id` 实现版本可追溯，并自动分配专属 `endpoint_url`。
- **面向高性能推理需求**：结合 `model high speed inference` 能力，在 MU 部署中启用 `enable_thinking`，或为 PTU 实例配置长输入与前缀缓存；也可单独选用 TPM 预留或快速模式（如 `glm-5.2-fast-preview`），实现吞吐保障或低延迟响应。
- **面向成本与资源优化**：对已完成微调的模型，先执行 `model compression` 生成量化版本（如 `my-qwen-ft-awq`），再以该压缩模型 ID 进行 MU 部署，显著降低所需算力规格（如从 MU3→MU1），从而节省部署成本。
- **面向[多模态](multi-modal.md)与定制化场景**：图像/视频/语音类微调模型（如 `wan2.7-image-pro`、`cosyvoice-v3-flash`）同样支持部署，但需注意其仅支持 LoRA 微调路径，且部署时必须使用对应模型 ID 及兼容的 `instance_type`（如 GPU 类型）。

> ⚠️ 注意：所有部署均强制要求地域为 **华北2（北京）**；API Key 所属业务空间须具备目标模型的部署权限；部署成功（状态变为 `RUNNING`）即开始计费，与是否发起请求无关。

## 关键参数和配置

| 参数名 | 适用部署类型 | 说明 | 示例值 |
|--------|--------------|------|--------|
| `plan` | 全部 | 必填，指定部署策略：`"ptu"` / `"mu"` / `"lora"` | `"plan": "mu"` |
| `model_id` | 全部 | 必填，模型唯一标识（基础模型 ID、微调产出 ID 或 LoRA 导入 ID） | `"model_id": "qwen3.7-plus-2026-05-26"` |
| `endpoint_name` | 全部 | 必填，全局唯一服务标识（3–63 字符，小写字母/数字/连字符） | `"endpoint_name": "qa-bot-prod"` |
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置吞吐量（token/min），决定容量购买与计费基线 | `"input_tpm": 5000, "output_tpm": 2000` |
| `deploy_spec` / `capacity` | MU | 算力规格（`MU1`/`MU3`/`MU8`）与副本数，直接影响并发与首 [Token](token.md) 延迟 | `"deploy_spec": "MU3", "capacity": 2` |
| `enable_thinking` | MU | 是否启用思考模式（影响推理逻辑、计费单价及输出结构） | `"enable_thinking": true` |
| `max_context_length` | MU（部分模型） | 显式设置最大上下文长度（单位：token），覆盖模型默认值 | `"max_context_length": 128000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值，用于保护服务质量 | `"rpm_limit": 300, "tpm_limit": 10000` |
| `instance_type` | [model production](../api/model-production.md)（通用部署） | 可选，指定底层计算资源（默认 `gpu-a10`；测试可用 `cpu-small`） | `"instance_type": "gpu-v100"` |

> ✅ 提示：  
> - LoRA 部署时，`capacity` 字段必须填写（如 `1`），但实际无效；`model_id` 必须为已成功导入的 LoRA 模型 ID（含 `adapter_config.json` 和 `adapter_model.safetensors`）。  
> - TPM 预留（TPM Reservation）属于 PTU 的增强形态，使用时需替换 API 请求中的 `model` 字段为专属 `dedicated model code`，而非通用模型 ID。  
> - 快速模式（Fast Mode）为独立部署形态，需使用专属域名和固定模型 ID（如 `glm-5.2-fast-preview`），不参与 MU/PTU/LoRA 的统一部署流程。

## 面向开发者，简洁实用

- **一句话启动**：用 DashScope SDK 一行代码部署（以 MU 为例）：
  ```python
  from dashscope import Deployments
  res = Deployments.create(
      model_id="qwen3.7-plus-2026-05-26",
      endpoint_name="my-llm-api",
      plan="mu",
      deploy_spec="MU1",
      capacity=2,
      enable_thinking=False
  )
  print(res.output.endpoint_url)  # 获取调用地址
  ```
- **状态检查**：部署后立即轮询 `GET /api/v1/deployments/{endpoint_name}`，直到 `status == "RUNNING"` 再发起推理请求。
- **错误速查**：
  - `Workspace xxx does not have deployment privilege for model xxxx` → 检查业务空间模型授权；
  - HTTP 429 + `x-dashscope-ptu-overflow:true` → PTU 已溢出，转为按量计费；
  - `health_check` 返回 503 → 实例仍在初始化（通常 2–5 分钟），请实现指数退避重试。
- **最佳实践**：
  - 高并发可预测业务 → 优先选 PTU，配前缀缓存 + 自动溢出；
  - 需独占资源/低首 [Token](token.md) 延迟 → 选 MU，调优 `deploy_spec` + `enable_thinking`；
  - LoRA 微调后轻量上线 → 选 LoRA 模式，严格校验 adapter 格式；
  - 成本敏感且精度可接受 → 先压缩再部署，对比多个量化模板效果。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)


