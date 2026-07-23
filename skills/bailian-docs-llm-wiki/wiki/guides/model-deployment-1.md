# model deployment 1

`model deployment 1` 是百炼平台面向生产环境的核心推理服务部署能力，提供三种正交计费与资源模型：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量（LoRA）。开发者可根据业务对吞吐稳定性、延迟确定性、成本敏感度及模型定制深度的需求，选择最适配的部署方式。所有部署均通过统一 API 接口管理，支持自动化扩缩容与细粒度监控。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、可预测流量场景，支持长输入（最高 256K token）与前缀缓存，当前覆盖 `qwen3.7-plus-2026-05-26`、`deepseek-v4-pro`、`glm-5.1` 等主流模型，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **模型单元（MU）**：适用于需独占算力、自定义性能指标（如首 [Token](../concepts/token.md) 延迟、TPM 上限）的场景，支持 PD 分离计算模式、思考/非思考推理模式切换及最长上下文配置，覆盖全部千问系列、GLM、DeepSeek 及千问 VL 模型，详见[模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **按 [Token](../concepts/token.md) 用量（LoRA）**：仅支持经百炼平台完成 LoRA 微调后的自定义模型，按实际输入/输出 token 计费，不支持全参微调模型；该模式下模型必须满足严格格式约束（如 `adapter_model.safetensors` + `adapter_config.json`、rank ∈ {8,16,32,64}、未修改 vocab/chat_template 等），详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 3 中表格显示 `glm-5.1` 输入上限为 64K，但文档 1 明确其支持 200K token 长输入且阶梯系数生效。以[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)为准，该模型实际支持 200K。

## 关键参数

| 参数名 | 适用部署类型 | 说明 | 示例值 |
|--------|--------------|------|--------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置输入/输出吞吐量（单位：token/min），决定额度购买量 | `"input_tpm": 10000` |
| `deploy_spec` / `capacity` | MU | 模型单元规格（如 `MU1`, `MU3`）与副本数，直接影响算力与并发 | `"deploy_spec": "MU1", "capacity": 4` |
| `enable_thinking` | MU | 是否启用思考模式（影响推理逻辑与计费单价） | `true` |
| `max_context_length` | MU | 最长上下文长度（部分模型支持，单位：token） | `10000` |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值（RPM/TPM），用于保障服务质量 | `"rpm_limit": 500` |
| `plan: "lora"` | LoRA | 必须显式指定，`capacity` 字段在该模式下无效但需填写 | `"plan": "lora", "capacity": 1` |

## 使用方式

- **控制台操作**：前往[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)，选择模型、计费方式及对应参数后提交。
- **API 调用**：使用 DashScope REST API 创建部署任务：
  - PTU：`POST /api/v1/deployments`，`"plan": "ptu"` + `ptu_capacity` 对象；
  - MU：`"plan": "mu"` + `deploy_spec`, `capacity`, `enable_thinking` 等字段；
  - LoRA：`"plan": "lora"` + `model_name`（必须为已导入的 LoRA 模型 ID）。
  全流程示例见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **状态管理**：通过 `GET /api/v1/deployments/{deployed_model}` 查询状态（`PENDING` → `RUNNING` 表示就绪），`DELETE /api/v1/deployments/{deployed_model}` 下线服务。

## 限制和注意事项

- **PTU 溢出策略**：创建时必须选择「自动溢出」（默认）或「仅使用 PTU 容量」。前者超限转按量计费（响应头含 `x-dashscope-ptu-overflow:true`），后者直接返回 HTTP 429；两种策略下超出模型原生 token 上限（如 Qwen 128K）均自动转按量计费。
- **LoRA 导入硬约束**：仅支持 LoRA 微调模型，不支持全参微调；要求 `adapter_config.json` 中 `rank` 值为 8/16/32/64，且所有层一致；禁止修改基础模型 vocab 或 `chat_template`；VL 模型必须冻结 VIT（即 `adapter_model.safetensors` 中不得含 `visual.*` 权重）。
- **地域与权限**：API 部署仅支持华北2（北京）地域；调用方 API Key 所属业务空间必须已获目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`。
- **计费生效时机**：部署成功（状态变为 `RUNNING`）即开始计费，与是否发起推理请求无关。PTU 和 MU 为预付费/后付费按使用时长计费，LoRA 为随用随付按 token 计费。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


