# SmartRobert

SmartRobert 是一个基于 FastAPI 的飞书任务机器人后端。项目包含飞书消息接入、自然语言任务解析、任务与项目管理、定时调度和消息推送等模块。

本项目仅供学习与参考。使用前需自行在飞书开放平台创建应用，并在本地 `.env` 中填写对应配置。

## 技术栈

- Python 3.12
- FastAPI / Uvicorn
- SQLAlchemy / MySQL
- 飞书开放平台 SDK
- LangChain / OpenAI 兼容接口
- APScheduler
- uv

## 项目结构

```text
app/                  应用代码
  llm/                大语言模型调用
  mapper/             数据映射
  models/             数据库模型
  repositories/       数据访问层
  schemas/            请求与响应模型
  services/           业务服务
  utils/              公共工具
docker/               容器相关配置
scripts/              飞书机器人和数据库脚本
docs/                 项目文档
```

## 本地开发

### 1. 安装环境

请先安装 Python 3.12 和 [uv](https://docs.astral.sh/uv/)，然后同步依赖：

```bash
uv sync
```

### 2. 配置环境变量

复制示例配置并填写本地凭据：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

主要配置项：

| 变量 | 说明 |
| --- | --- |
| `DATABASE_URL` | MySQL 异步连接地址 |
| `FEISHU_APP_ID` | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret |
| `FEISHU_VERIFICATION_TOKEN` | 飞书事件校验 Token |
| `FEISHU_ENCRYPT_KEY` | 飞书事件加密 Key |
| `OPENAI_API_KEY` | OpenAI 或兼容服务 API Key |
| `OPENAI_BASE_URL` | OpenAI 兼容接口地址 |

`.env`、日志、IDE 配置、本地数据库、私钥和证书均已被 Git 与 Docker 构建上下文忽略。请勿把真实凭据写入 `.env.example` 或源码。

### 3. 初始化数据库

根据本地 MySQL 配置执行：

```bash
mysql -u root -p < scripts/init_db.sql
```

如需演示数据：

```bash
mysql -u root -p feishu_task_bot < scripts/seed_demo_data.sql
```

### 4. 启动服务

```bash
uv run uvicorn app.main:app --reload
```

服务默认监听 `http://127.0.0.1:8000`，OpenAPI 文档位于 `http://127.0.0.1:8000/docs`。

## 飞书长连接机器人

在飞书开放平台的“事件与回调”中选择“使用长连接接收事件”，并订阅：

```text
im.message.receive_v1
```

启动监听：

```bash
uv run python scripts/feishu_ws_bot.py
```

## Docker Compose

准备好 `.env` 后启动应用和 MySQL：

```bash
docker compose up --build
```

## 测试

```bash
uv run pytest
```

## 更多文档

- [产品需求](docs/PRD.md)
- [详细设计](docs/DESIGN.md)
- [代码说明](docs/CODE_GUIDE.md)
- [部署手册](docs/DEPLOY.md)
