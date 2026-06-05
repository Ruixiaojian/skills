# [model compression](../guides/model-compression.md) api

模型压缩 API 通过量化等方式压缩自定义调优模型，降低推理成本。本文档介绍 RESTful 接口的前提条件、接口清单、鉴权方式以及完整的端到端调用流程，面向通过 OpenAPI 或 SDK 集成压缩能力的开发者。控制台操作请参考 [模型压缩](../../raw/model-api-reference/model-compression-api.md) 的概述章节。

## 支持的模型与功能范围

当前压缩功能**仅支持**基于 `qwen3.5-flash-2026-02-23` 完成的**自定义全参调优模型**，LoRA 模型和已经量化过的模型均不支持。调优过程依赖于百炼的模型调优流水线。

> **注意**：当前模型压缩 API 仅在**北京 Region**开放。若使用其他 Region，需通过对应 Region 的控制台进行压缩操作。压缩功能当前**限时免费**。

详细的前置条件（开通百炼服务、实名认证、获取 API Key、准备自定义全参调优模型）见 [模型压缩](../../raw/model-api-reference/model-compression-api.md) 的「前提条件」章节。

## 接口列表

所有接口域名：`https://dashscope.aliyuncs.com`，按生命周期可分为三类：

**模板与任务管理**

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/fine-tunes/compress/templates` | 列举可量化模型及配置模板 |
| POST | `/api/v1/fine-tunes/compress/jobs` | 创建压缩任务 |
| GET | `/api/v1/fine-tunes/compress/jobs` | 列举压缩任务 |

**任务查询与诊断**

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/fine-tunes/compress/jobs/{job_id}` | 查询压缩任务详情 |
| GET | `/api/v1/fine-tunes/compress/jobs/{job_id}/logs` | 获取压缩任务日志 |

**任务控制**

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/fine-tunes/compress/jobs/{job_id}/cancel` | 取消压缩任务 |
| DELETE | `/api/v1/fine-tunes/compress/jobs/{job_id}` | 删除压缩任务 |

完整的接口清单和各接口 cURL 写法见 [模型压缩](../../raw/model-api-reference/model-compression-api.md) 的「接口列表」章节。

## 鉴权

所有接口通过 HTTP Header 携带 API Key：

```
Authorization: Bearer ${YOUR_API_KEY}
```

POST 请求体场景需额外设置 `Content-Type: application/json`。

## 关键参数

创建压缩任务（POST `/jobs`）的核心参数：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 自定义全参调优模型 ID，例如 `qwen3.5-flash-2026-02-23-ft-***` |
| `template_id` | string | 量化模板 ID，通过 `GET /templates` 获取，例如 `quant-flash-nvfp4-mlp-nomtp` |
| `output_model_suffix` | string | 产出模型后缀，**最多 8 个字符，仅允许小写字母和数字** |

任务终态包含 `SUCCEEDED` / `FAILED` / `CANCELED` 三种，需通过轮询任务详情接口判断。

## 使用方式

### 1. 创建任务并轮询

```python
import requests, time

API_KEY = "YOUR_API_KEY"
BASE = "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 创建压缩任务
resp = requests.post(f"{BASE}/jobs", headers=HEADERS, json={
    "model": "qwen3.5-flash-2026-02-23-ft-***",
    "template_id": "quant-flash-nvfp4-mlp-nomtp",
    "output_model_suffix": "test",
}).json()
job_id = resp["output"]["job_id"]

# 轮询直到终态
status = resp["output"]["status"]
while status not in ("SUCCEEDED", "FAILED", "CANCELED"):
    time.sleep(30)
    resp = requests.get(f"{BASE}/jobs/{job_id}", headers=HEADERS).json()
    status = resp["output"]["status"]

if status == "SUCCEEDED":
    quantized_model_id = resp["output"]["quantized_output"]
```

建议轮询间隔不低于 30 秒，避免过于频繁的请求。

### 2. 列举任务与获取日志

```python
# 列举所有压缩成功的任务
resp = requests.get(f"{BASE}/jobs", headers=HEADERS,
                    params={"status": "SUCCEEDED", "page_size": 20}).json()

# 获取任务日志（offset + line 分页）
resp = requests.get(f"{BASE}/jobs/{job_id}/logs", headers=HEADERS,
                    params={"offset": 0, "line": 100}).json()
```

### 3. 产出模型命名规则

任务成功后，量化产出模型的 ID 遵循固定拼接规则：

```
quantized_output = {base_model}-{output_model_suffix}-{job_id}
```

例如：`base_model = qwen3.5-flash-2026-02-23`，`suffix = test`，`job_id = quant-202604111200-a1b2`，则产出模型 ID 为 `qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2`。

完整的 5 分钟上手示例（含错误处理与日志拉取）见 [模型压缩](../../raw/model-api-reference/model-compression-api.md) 的「5 分钟上手」章节。

## 限制和注意事项

- **模型范围**：只接受基于 `qwen3.5-flash-2026-02-23` 的全参调优模型；LoRA 和已量化模型直接拒绝。
- **Region 限制**：API 当前仅在**北京 Region**开放；其他 Region 用户需切换控制台操作。
- **产出后缀规则**：`output_model_suffix` 最长 8 字符且仅允许小写字母和数字，超出或包含非法字符会被拒绝。
- **部署规格**：压缩产出模型支持的部署单元规格由所选量化模板决定，部署数量在百炼控制台「模型部署」中配置，不在本 API 范围内。
- **计费**：当前压缩功能限时免费，正式计费策略以官方通知为准。
- **任务状态机**：任务终态为 `SUCCEEDED` / `FAILED` / `CANCELED`，需主动轮询；`FAILED` 时通过 `output.error` 字段定位错误，配合日志接口排查。

## 来源文档

- [模型压缩](../../raw/model-api-reference/model-compression-api.md)


