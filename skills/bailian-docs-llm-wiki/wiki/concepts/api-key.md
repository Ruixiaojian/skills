# API Key 管理

API Key 是调用阿里云百炼平台大模型和应用的鉴权凭证，是所有 API 请求的身份标识。开发者在调用任何百炼服务前，必须先创建 API Key 并妥善管理其权限、归属和生命周期。

## 基本概念与特性

| 特性 | 说明 |
|------|------|
| **格式** | 通用 API Key 以 `sk-` 开头（如 `sk-xxxxx`）；Coding Plan 专属 Key 以 `sk-sp-` 开头 |
| **有效期** | 永久有效，无过期时间，手动删除后即失效且不可恢复 |
| **归属关系** | 单个 API Key 只能归属**一个地域**内的**一个业务空间**和**一个用户**，不可转移 |
| **权限模型** | 权限由归属业务空间决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建 |
| **数量限制** | 华北2（北京）、新加坡、德国（法兰克福）每个主账号每个地域最多 50 个；美国（弗吉尼亚）每个归属账号最多 20 个 |

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## 创建与权限要求

### 操作入口

前往百炼控制台的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建密钥。

### 角色权限

创建和管理 API Key 需要以下角色之一：

| 角色 | API Key 管理权限 |
|------|-----------------|
| 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户） | ✅ |
| 业务空间管理员（拥有"权限管理"页面访问权的 RAM 用户） | ✅ |
| 普通用户 | ❌ |

### 权限配置选项

创建 API Key 时可选择两种权限模式：

- **全部**：授予调用所有模型与应用的权限。
- **自定义**：可配置 IP 访问白名单（最多 20 个 IPv4/IPv6 地址或网段）。

> **注意**：目前仅华北2（北京）地域支持为 API Key 配置 IP 白名单等精细权限控制，其他地域暂不支持。

## 各地域 Base URL

每个地域有独立的 API Key 和 Base URL，**不可跨地域混用**。

| 地域 | Base URL（OpenAI 兼容） |
|------|------------------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

## 环境变量配置

为避免在代码中硬编码 API Key 导致泄漏风险，建议将其配置为环境变量，统一使用 `DASHSCOPE_API_KEY` 作为变量名。

```bash
# Linux / macOS（永久生效）
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

```cmd
# Windows CMD（永久生效，需新开窗口）
setx DASHSCOPE_API_KEY "sk-xxx"
```

### 环境变量不生效的常见原因

- 仅设置了临时环境变量，对已启动的 IDE 或应用不生效
- 设置永久环境变量后未重启 IDE、命令行或应用服务
- 使用 `sudo` 执行脚本时未继承环境变量（可用 `sudo -E` 解决）
- 应用通过 systemd 等服务管理器启动，需在其配置文件中添加环境变量

## 临时 API Key

在浏览器、移动 App 等不可信环境中调用模型时，应避免暴露永久 API Key。百炼支持通过后端服务生成临时 API Key。

### 请求方式

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期（TTL），范围 [1, 1800] 秒，默认 60 秒 |

### 响应示例

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

| 字段 | 说明 |
|------|------|
| `token` | 临时 API Key，以 `st-` 开头 |
| `expires_at` | 过期时间，UNIX 时间戳（秒） |

### 注意事项

- 临时 API Key **继承**生成它的永久 API Key 的全部权限（含模型和知识库访问限制）
- 到期后自动失效，**不支持手动删除**
- 各地域 Endpoint 不同，需使用对应地域的地址

## API Key 生命周期管理

### 状态变更规则

| 操作 | 主账号 API Key | RAM 账号 API Key |
|------|--------------|-----------------|
| 主动删除 | 失效，不可恢复 | 失效，不可恢复 |
| 账号移出业务空间 | — | 失效（重新加入后恢复） |
| RAM 控制台删除账号 | — | 失效，不可恢复 |

### 停止服务

如需停止百炼服务调用（百炼开通后暂不支持关闭），可在控制台删除已创建的 API Key 来阻止所有 API 请求。

## 子业务空间中的 API Key

如需限制特定用户可调用的模型范围，或对模型调用费用进行分账，可使用

## 关联主题页

- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [application permission management](../guides/application-permission-management.md)
- [get started with models](../guides/get-started-with-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [support](../guides/support.md)

