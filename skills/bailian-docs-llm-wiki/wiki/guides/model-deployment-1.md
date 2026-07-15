# model deployment 1

`model deployment 1` 是百炼平台面向生产环境的模型服务化核心能力，提供三种主流部署模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费。其中 PTU 模式专为高并发、低延迟、流量可预估的场景设计，支持长输入与前缀缓存优化；MU 模式提供资源独占与性能自定义能力；[Token](../concepts/token.md) 用量模式适用于效果验证与轻量调用。所有模式均通过统一 API 接口调用，支持 OpenAI、Anthropic 和 DashScope 兼容协议。

## 支持的模型/功能

- **PTU 部署**：支持 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等主流预置模型，最高支持 **256K 输入 token**（如 `glm-5.2` 达 1M），并启用前缀缓存优惠 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **模型单元（MU）部署**：支持全部预置模型及 LoRA 微调模型（含千问、GLM、DeepSeek、Kimi、MiniMax 等），支持 PD 分离计算模式以降低首 [Token](../concepts/token.md) 延迟 [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。  
- **Token 用量部署**：仅支持经 LoRA 微调后的部分基础模型（如 `qwen3-32b`、`qwen3-14b` 等），不支持全参微调模型或视觉语言模型（VL）的 LoRA 导入 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **模型导入能力**：仅支持 LoRA 格式（`adapter_model.safetensors` + `adapter_config.json`），要求 rank ∈ {8,16,32,64}，且必须冻结 VIT（对 VL 模型）、禁用 vocab/chat_template 修改 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 2 中 `glm-5.1` 的输入上限标为 64K，但文档 1 明确其支持 200K；文档 2 表格中 `qwen3.7-plus-2026-05-26` 输入上限为 256K，与文档 1 一致。以文档 1 的实测能力为准，即 `glm-5.1` 实际支持 200K，控制台展示值可能滞后。

## 关键参数

| 参数 | PTU 模式 | MU 模式 | Token 用量模式 |
|------|----------|---------|----------------|
| **核心配置** | `input_tpm`, `output_tpm`（单位：token/分钟） | `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` | `plan: "lora"`，`capacity` 字段必须传但无效 |
| **缓存控制** | `provisioned_tokens`（含阶梯系数与缓存折扣）、`cached_tokens`（仅 OpenAI/DashScope 兼容格式返回） | 不支持前缀缓存 | 不支持前缀缓存 |
| **计费标识** | 响应头含 `x-dashscope-ptu-overflow:true`（溢出时），响应体含 `service_tier: "ptu-standard"` | 无专用额度字段，`service_tier` 不返回或为 `"default"` | 无专用额度字段，`service_tier` 不返回或为 `"default"` |

- **长输入阶梯系数**（仅 PTU）：`glm-5.1` 在 `[0,32K)` 区间系数为 1.0，`[32K,200K]` 区间输入系数升至 1.33、输出 1.17；`deepseek-v4-pro` 和 `qwen3.7-plus-2026-05-26` 无阶梯，全程系数为 1.0 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **缓存折扣率**（仅 PTU）：`glm-5.1` 和 `qwen3.7-plus-2026-05-26` 为 0.2（命中部分按 20% 折算），`deepseek-v4-pro` 为 0.08 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 使用方式

- **控制台部署**：登录 [百炼控制台 → 模型部署 → 创建部署](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，选择模型、计费方式及对应参数（如 PTU 容量计算器、MU 规格、限流阈值等）。
- **API 部署**（推荐自动化）：
  - PTU：`POST /api/v1/deployments`，`"plan": "ptu"`，携带 `ptu_capacity` 对象；
  - MU：`"plan": "mu"`，指定 `deploy_spec`、`capacity`、`enable_thinking` 等；
  - Token 用量：`"plan": "lora"`，`capacity` 必填但忽略 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **推理调用**：使用 `deployed_model`（即部署后生成的专属服务 ID）作为 `model` 参数，通过 `/api/v1/services/{deployed_model}/completions` 或 SDK（如 `dashscope.Generation.call(model='xxx')`）发起请求，**无需修改 endpoint 或鉴权逻辑**。

## 限制和注意事项

- **PTU 溢出行为**：超出购买 TPM 或输入超过模型上限（如千问系列 128K、DeepSeek 系列 64K）时，请求**自动降级为按量计费**，API 响应中 `service_tier` 缺失或为 `"default"`，响应头含 `x-dashscope-ptu-overflow:true`，业务无感知但费用结构变化 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **模型单元约束**：MU 部署不支持思考模式与非思考模式动态切换（需在部署时固定），且 `max_context_length` 设置受基础模型原生上限约束（如 `qwen3-8b` 最高支持 128K，不可设为 256K）。  
- **LoRA 导入硬性限制**：不支持全参微调模型；若 `adapter_model.safetensors` 中存在 `visual.` 开头的权重键，则导入失败；`chat_template` 必须与开源基础模型完全一致，否则部署后效果异常 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。  
- **地域与权限**：API 部署仅支持华北2（北京）地域；API Key 所属业务空间必须显式授权目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


