# 模型压缩

通过量化等方式压缩模型，降低推理成本。

模型压缩 API 提供从查询模板、创建任务、轮询状态、获取日志到取消/删除任务的完整 RESTful 接口。本文档面向开发者通过 OpenAPI 或 SDK 集成压缩能力。控制台介绍见 [模型压缩](https://help.aliyun.com/zh/model-studio/model-compression-introduction)。

## 一、前提条件

在调用本文档接口前，请先完成：

1.  已开通阿里云百炼服务并完成实名认证。
    
2.  当前工作空间至少有一个基于 `qwen3.5-flash-2026-02-23` 的**自定义全参调优模型**（通过 [模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning/) 完成 ）。当前压缩功能仅支持该模型，LoRA 模型和已量化的模型不支持。
    
3.  已获取 API Key（参考 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
    

> 压缩产出的模型支持的部署单元规格由所选量化模板决定，部署数量在百炼控制台「模型部署」中配置。当前压缩功能限时免费。

> 当前模型压缩 API 仅在北京 Region 开放。如您使用其他 Region，请通过该 Region 的百炼控制台完成模型压缩操作。

## 二、接口列表

所有接口域名：`https://dashscope.aliyuncs.com`

#

方法

路径

说明

1

GET

`/api/v1/fine-tunes/compress/templates`

列举可量化模型及配置模板

2

POST

`/api/v1/fine-tunes/compress/jobs`

创建压缩任务

3

GET

`/api/v1/fine-tunes/compress/jobs`

列举压缩任务

4

GET

`/api/v1/fine-tunes/compress/jobs/{job_id}`

查询压缩任务详情

5

GET

`/api/v1/fine-tunes/compress/jobs/{job_id}/logs`

获取压缩任务日志

6

POST

`/api/v1/fine-tunes/compress/jobs/{job_id}/cancel`

取消压缩任务

7

DELETE

`/api/v1/fine-tunes/compress/jobs/{job_id}`

删除压缩任务

## 三、鉴权

所有接口通过 HTTP Header 携带 API Key：

```
Authorization: Bearer ${YOUR_API_KEY}
```

`Content-Type: application/json` 适用于 POST 请求体场景。

## 四、5 分钟上手

### HTTP

安装请求库：

```
pip install requests
```

创建任务 → 轮询 → 拿到产出模型的完整示例：

```
import requests, time

API_KEY = "YOUR_API_KEY"
BASE = "https://dashscope.aliyuncs.com/api/v1/fine-tunes/compress"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 1. 创建压缩任务
resp = requests.post(f"{BASE}/jobs", headers=HEADERS, json={
    "model": "qwen3.5-flash-2026-02-23-ft-***",  # 自定义调优模型 ID
    "template_id": "quant-flash-nvfp4-mlp-nomtp",          # 通过 GET /templates 获取
    "output_model_suffix": "test",                          # 最多 8 字符，仅小写字母和数字
}).json()
job_id = resp["output"]["job_id"]
print("Job:", job_id)

# 2. 轮询直到终态
status = resp["output"]["status"]
while status not in ("SUCCEEDED", "FAILED", "CANCELED"):
    time.sleep(30)
    resp = requests.get(f"{BASE}/jobs/{job_id}", headers=HEADERS).json()
    status = resp["output"]["status"]
    print("Status:", status)

# 3. 处理结果
if status == "SUCCEEDED":
    print("Quantized model:", resp["output"]["quantized_output"])
    # 用 quantized_output 调模型部署接口部署
elif status == "FAILED":
    print("Error:", resp["output"]["error"])
```

列举任务与获取日志：

```
# 列举所有压缩成功的任务
resp = requests.get(f"{BASE}/jobs", headers=HEADERS, params={"status": "SUCCEEDED", "page_size": 20}).json()
for j in resp["output"]["jobs"]:
    print(j["job_id"], j["template_name"], j["quantized_output"])

# 获取任务日志
resp = requests.get(f"{BASE}/jobs/{job_id}/logs", headers=HEADERS, params={"offset": 0, "line": 100}).json()
for line in resp["output"]["logs"]:
    print(line)
```

**产出模型的命名规则**：

```
quantized_output = {base_model}-{output_model_suffix}-{job_id}
```

例如 `base_model` 为 `qwen3.5-flash-2026-02-23`，`suffix` 为 `test`，`job_id` 为 `quant-202604111200-a1b2`，产出模型 ID 为：

```
qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2
```

各接口的 cURL 写法见各接口详情页。
