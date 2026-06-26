# 微调参数参考

> 本文件补充 [`SKILL.md`](../SKILL.md) 第 2 步「创建微调任务」的 `--training-type` 取值与超参细节。流程编排与避坑见 SKILL.md。

## training-type 取值与映射

CLI 用 `<method>` / `<method>-lora` 约定，提交时在 CLI 边界映射到服务端字段（你永远传 CLI 值，不要传服务端字符串）：

| CLI 值 | 服务端 | 适用 |
|---|---|---|
| `sft-lora` | efficient_sft | **默认**，LoRA，便宜快，大多数场景 |
| `sft` | 全参 SFT | 效果上限高，成本显著增加 |
| `dpo-lora` / `dpo` | dpo | 偏好对齐，需 preference 数据 |
| `cpt` | 继续预训练 | 注入领域知识，需非对话格式数据 |

> `cpt` 服务端没有 `-lora` 变体，只有全参；其余方法（sft / dpo）均有 `<method>` 与 `<method>-lora` 两个变体。

## 超参建议

- `n-epochs` 默认 3。小数据集（几百条）3 够用；过拟合降到 1-2。
- `batch-size` 按数据量自适应（<100KB 自动设 8），一般不手动设。
- `learning-rate` 以**字符串**传入避免 JSON 精度丢失，如 `"1e-4"`。LoRA 默认 `3e-4`（平台对小数据集的设定），过拟合可调小。
- `--validations <path>` 可选，传验证集观察指标。

## 必填 flag

- `--model`：基座模型名（如 `qwen3-8b`）。
- `--datasets`：file-id 或本地 `.jsonl` 路径（逗号分隔多个）；本地路径会先校验上传再取 file-id。

## 提交前校验

`bl finetune create` 提交前会用 listFoundationModels 校验模型是否支持所选 training-type，不支持会快速失败（不耗配额）。若训练集样本数 ≤ batch_size，会在上传/耗配额前被拒。可用 `bl finetune capability --model <base>` 提前确认。
