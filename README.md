# 实验室预约管理系统

一个前后端分离的实验室预约管理系统，包含用户认证、实验室与设备浏览、预约管理、审核流程以及 AI 知识库问答等功能。

## 项目结构

```text
lab-agent/
├── frontend/     # Vue 3 + Vite 前端
└── backend/      # FastAPI 后端
```

## 环境要求

- Node.js 18 或更高版本
- Python 3.10 或更高版本
- 按后端配置提供数据库和 AI 服务环境变量

## 启动前端

```bash
cd frontend
npm install
npm run dev
```

接口地址请根据本地环境配置 `frontend/.env.development`。

## 启动后端

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
# Windows CMD
.\\.venv\\Scripts\\activate.bat

pip install -r requirements.txt

# 启动后端服务
uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
uvicorn app.main:app --reload
```

后端默认监听 `http://127.0.0.1:8000`，API 文档可在 `/docs` 查看。

## 配置说明

本地密钥、数据库连接、AI 服务密钥等配置写入环境变量或 `.env` 文件，不要提交到 Git。仓库的 `.gitignore` 已默认忽略这些文件。

## 开发约定

- 不提交 `frontend/node_modules/`。
- 不提交后端上传文件、向量数据库和运行时缓存。
- 提交前确认没有包含密码、Token、私钥或其他敏感信息。

## License

当前项目尚未指定开源许可证。如需公开发布，请补充 License 文件。
