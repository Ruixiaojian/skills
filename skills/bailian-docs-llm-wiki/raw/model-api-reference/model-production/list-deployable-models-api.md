# 列举可部署模型

列举当前支持部署的模型列表。

## 前提条件

-   您已经阅读了[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)和[使用 API 进行模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)的相关内容，掌握了模型部署的使用方法，并熟悉了在阿里云百炼平台上进行模型部署的基本步骤。
    
-   已配置百炼的 API-KEY， 请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

## 获取可以部署的模型列表

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

### **请求示例**

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

查询用户调优模型：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为50，最大值为100，最小值为1。

model\_source

String

query

否

模型来源。`base`表示系统模型（默认），`custom`表示用户调优模型。

version

String

query

否

API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。

### **响应示例**

命令执行完成后，获得以下结果：

```
{
    "request_id": "f7da015c-ea90-4d96-af89-2f8d7604026a",
    "output": {
        "page_no": 1,
        "page_size": 100,
        "total": 5,
        "models": [
            {
                "model_name": "qwen3-8b",
                "plans": [
                    {
                        "plan": "mu",
                        "templates": [
                            {
                                "template_id": "MU1",
                                "template_name": "单机部署-标准推理型",
                                "template_type": "COUPLED",
                                "template_version": "v1",
                                "template_desc": "适用于标准推理场景",
                                "roles": {
                                    "unified": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            },
                            {
                                "template_id": "MU1-PD",
                                "template_name": "PD分离部署-标准推理型",
                                "template_type": "SEPERATED",
                                "template_version": "v1",
                                "template_desc": "适用于PD分离推理场景",
                                "roles": {
                                    "prefill": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    },
                                    "decode": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "plan": "lora"
                    }
                ]
            }
        ]
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

models

Array

可部署模型列表。

models\[\].model\_name

String

模型名称。

models\[\].plans

Array

该模型支持的部署方案列表。使用`version=v1.0`时返回。

models\[\].plans\[\].plan

String

部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`ptu`（预置吞吐量）、`lora`（LoRA共享部署）。

models\[\].plans\[\].templates

Array

部署模板列表（`plan=mu`时返回）。

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有模型个数。

### **模板字段说明（templates）**

**参数**

**类型**

**说明**

template\_id

String

模板 ID，在[创建模型部署任务](https://help.aliyun.com/zh/model-studio/model-deployment-api#13f7a7d05829h)时作为`deploy_spec`参数传入。

template\_name

String

模板显示名称。

template\_type

String

模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。

template\_version

String

模板版本。

template\_desc

String

模板描述。

roles

Object

节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。

### **roles 节点字段说明**

**参数**

**类型**

**说明**

model\_unit\_spec

String

模型单元规格。

capacity\_unit\_per\_instance

Number

单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。

## 异常响应

### **响应示例**

```
{
    "request_id": "ca218d57-b91b-46b2-bd35-c41c6287bcf4",
    "message": "Model: qwen-plus-20230703-cx7f not found!",
    "code": "NotFound"
}
```

### **响应参数**

**字段**

**类型**

**描述**

request\_id

String

本次请求的系统唯一码。

code

String

错误码。

message

String

错误信息。

当请求出错时，可能返回以下错误：

**错误码**

**错误信息**

**错误原因**

**NotFound**

Model: xxx not found!

-   创建部署任务时指定了不存在的模型。
    
-   查询/更新/删除部署任务时指定了不存在的模型。
    

**Conflict**

Deployed model xxx already exists, please specify a suffix.

创建部署任务时使用了已使用过的suffix。

**InvalidParameter**

Invalid capacity (xx), capacity must be larger than or equal to 0 and multiples of 1 and less than 1000!

创建/更新部署任务时指定了无效的算力单元数量。
