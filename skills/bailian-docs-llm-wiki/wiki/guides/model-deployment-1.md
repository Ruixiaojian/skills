# model deployment 1

[模型部署](../concepts/model-deployment.md)是百炼平台提供的一种将预置模型或调优后模型转化为独立、资源专享推理服务的能力，适用于对高并发、低延迟、资源确定性有明确要求的生产场景。通过三种计费模式（预置吞吐/PTU、模型单元/MU、[Token](../concepts/token.md)用量），开发者可按业务负载特征选择最适配的部署方式，实现性能与成本的平衡。

## 支持的模型/功能

- **预置模型**：千问系列（Qwen3.7-Max/Plus、Qwen3-VL、Qwen-Flash等）、DeepSeek-v4/v3、GLM-5.x、Kimi-K2.5、CosyVoice 等主流模型均支持部署；具体支持列表及参数详见[模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **调优后模型**：所有通过百炼平台完成 LoRA 微调的模型均可部署；全参微调模型暂不支持 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **多模态支持**：千问VL系列（如 `qwen3-vl-plus-2025-09-23`）支持图像+文本联合推理，需使用对应 VL 模型单元规格部署。
- **高级能力**：
  - PTU 部署支持长输入（最高 256K token）与前缀缓存，可显著降低多轮对话/文档分析场景的额度消耗 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)；
  - 模型单元（MU）部署支持 PD 分离计算模式，有效降低首 [Token](../concepts/token.md) 延迟；
  - 推理模式可选：`Instruct`（非思考）或 `Thinking`（思考），部分模型在 MU 模式下可动态启用。

> **注意**：文档1中“支持模型”表格称“部分预置模型与所有调优后模型”支持模型单元计费，但文档4明确限定仅支持 LoRA 微调模型导入与部署，且文档1中“按模型 [Token](../concepts/token.md) 使用量”计费方式仅限“经过 LoRA 调优后的模型”。三者一致指向 LoRA 是当前唯一支持的调优类型，全参微调模型不在支持范围内。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置性 |
|----------|--------|------|-----------|
| **通用** | `name` | 部署服务唯一名称，用于 API 调用 | 必填 |
| **计费模式** | `plan` | 取值：`ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token用量） | 必填 |
| **PTU 模式** | `ptu_capacity.input_tpm` / `output_tpm` | 预置输入/输出吞吐量（单位：token per minute） | 必填（PTU 模式） |
| **MU 模式** | `deploy_spec` | 模型单元规格，如 `MU1`, `MU2 x 8`, `MU3 x 16`（PD分离） | 必填（MU 模式） |
| | `capacity` | 部署副本数（影响并发能力） | 可选，默认1 |
| | `enable_thinking` | 是否启用思考模式（布尔值） | 可选，默认false |
| | `max_context_length` | 最长上下文长度（token），部分模型支持自定义 | 可选 |
| | `rpm_limit` / `tpm_limit` | 服务级限流阈值（RPM/TPM） | 可选 |
| **Token用量模式** | `capacity` | 该参数在 `lora` 模式下**必须填写但实际无效**，扩缩容需走控制台人工流程 | 必填（占位） |

## 使用方式

### 控制台部署
1. 访问 [模型部署控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_deploy/create)；
2. 填写服务名称、选择模型、选择计费方式（PTU/MU/Lora）；
3. 根据所选模式配置对应参数（如 PTU 容量、MU 规格、推理模式等）；
4. 点击确认，状态变为 `RUNNING` 即部署成功。

### API 部署（推荐自动化）
使用 `curl` 或 SDK 调用 `/api/v1/deployments` 接口：

- **PTU 示例**（固定吞吐保障）：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --data '{
      "name": "my_qwen_flash",
      "model_name": "qwen-flash-2025-07-28",
      "plan": "ptu",
      "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
    }'
  ```

- **MU 示例**（资源独占、性能可调）：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --data '{
      "name": "my_qwen_plus",
      "model_name": "qwen-plus-2025-12-01",
      "plan": "mu",
      "deploy_spec": "MU1",
      "enable_thinking": true,
      "capacity": 4
    }'
  ```

- **Token用量示例**（按量付费、高性价比）：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --data '{
      "model_name": "qwen3-8b-ft-202511132025-0260",
      "plan": "lora",
      "capacity": 1,
      "name": "qwen3-8b-ft"
    }'
  ```

> 部署成功后立即开始计费，无论是否发起推理请求。详情见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 限制和注意事项

- **地域限制**：API 部署目前**仅支持华北2（北京）地域**，其他地域需使用控制台或等待后续开放 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **权限要求**：API 调用需确保 API Key 所属业务空间已授权目标模型的部署权限，否则返回 `Workspace xxx does not have deployment privilege for model xxxx` 错误。
- **OSS 导入约束**：LoRA 模型导入必须满足严格格式要求——必需文件为 `adapter_model.safetensors` 和 `adapter_config.json`；`rank` 值仅限 8/16/32/64；禁止修改 vocab 或 chat_template；VL 模型必须冻结 VIT [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **溢出策略影响**：PTU 模式下，若选择「自动溢出」，超额度请求将无缝转为按量计费，并在响应头中携带 `x-dashscope-ptu-overflow:true`；若选择「仅使用 PTU 容量」，则直接返回 HTTP 429 错误 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **计费不可变**：服务创建后计费方式无法更改，如需切换，必须先下线再重新部署。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


