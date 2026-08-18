# model deployment 1

`model deployment 1` 是百炼平台面向生产环境的模型服务化核心能力，提供三种部署模式：预置吞吐（PTU）、模型单元（MU）和按 Token 用量计费。其中 PTU 模式专为高并发、低延迟、流量可预估的场景设计，支持长输入、前缀缓存与阶梯额度消耗，是当前主流生产部署首选；MU 模式适用于需独占资源、自定义性能指标（如首 Token 延迟、TPM 上限）的私有模型推理；Token 用量模式则主要用于调优后模型的效果验证与轻量级调用。所有模式均通过统一 API 接口调用，兼容 OpenAI Chat、Anthropic 和 DashScope 协议。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持千问（Qwen）、GLM、DeepSeek 等主流预置模型，包括 `qwen3.8-Max`、`glm-5.2`、`deepseek-v4-pro` 等，详见[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **模型单元（MU）**：支持全部调优后 LoRA 模型及部分预置大模型（如 `qwen3.6-35b-a3b`、`glm-5.1`），支持 PD 分离计算模式以降低首 Token 延迟。  
- **Token 用量计费**：仅支持经 LoRA 高效微调后的自定义模型（`plan=lora`），不支持全参微调模型。  
- **核心功能**：PTU 模式独有长输入支持（最高 1M token）、前缀缓存（命中部分按折扣系数折算额度）、自动溢出策略（默认）与仅 PTU 容量策略（返回 429）。  

> **注意**：文档 2 中表格列出 `qwen3.7-flash-2026-07-15` 输入上限为 128K，但文档 1 明确其支持 1 Million token。以[预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)为准，该模型实际输入上限为 1M token。

## 关键参数

| 参数类型 | PTU 模式 | 模型单元（MU）模式 | Token 用量模式 |
|----------|-----------|----------------------|----------------|
| **核心配置** | `ptu_capacity: {input_tpm, output_tpm}` | `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` | `plan: "lora"`，`capacity` 字段必须填写但无效 |
| **长输入处理** | 阶梯容量系数（如 `glm-5.1`：`(32K,200K]` 输入系数 1.33）、缓存折扣率（如 `qwen3.7-plus-2026-05-26` 为 0.2） | 由 `max_context_length` 控制，超出模型原生上限将报错 | 不适用（仅支持 LoRA 模型，且无长输入优化机制） |
| **API 响应字段** | `service_tier="ptu-standard"`、`provisioned_tokens`（含阶梯/缓存折算）、`cached_tokens` | 无 PTU 特有字段，`service_tier` 不返回或为 `"default"` | 同 MU 模式，无 `cached_tokens` |

## 使用方式

- **控制台操作**：登录[百炼控制台 → 模型部署 → 创建部署](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，选择模型、计费模式及对应参数，PTU 模式推荐使用内置的**预置吞吐额度计算器**估算输入/输出 KTPM 需求 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。  
- **API 调用**：使用 `POST /api/v1/deployments` 接口，`plan` 字段指定模式（`"ptu"`/`"mu"`/`"lora"`），参数结构严格匹配对应模式要求。示例见[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。  
- **模型导入前提**：LoRA 模型需通过 OSS 导入，满足 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等约束，详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **计费锁定**：部署创建后计费方式不可更改，切换需先下线再重建。  
- **PTU 溢出行为**：默认「自动溢出」策略下，超额度请求转为按量计费（响应头含 `x-dashscope-ptu-overflow:true`）；「仅使用 PTU 容量」策略下直接返回 HTTP 429。  
- **长输入边界**：单次输入超过模型声明上限（如千问系列 128K、DeepSeek 系列 64K）时，无论 PTU 是否充足，均自动转为按量计费。  
- **缓存生效条件**：`cached_tokens > 0` 表示前缀缓存命中，但需确保请求间 system message 一致、间隔在缓存有效期、输入长度足够触发缓存；Anthropic 兼容格式不返回 `cached_tokens` 字段。  
- **模型单元限制**：仅支持部分高效微调（LoRA）后的模型；一个月内不使用将自动释放资源。  
- **地域限制**：API 示例仅适用于华北2（北京）地域，其他地域需调整 endpoint。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


