# LangGraph Designer Server

LangGraph 工具套件是一个完整的 LangGraph 应用开发解决方案，包含两个核心组件：用于可视化设计的 **LangGraph Builder** 和用于代码生成的 **langgraph-gen**。

## 目录

- [快速开始](#快速开始)
- [Docker 部署](#docker-部署)
- [项目结构](#项目结构)
- [LangGraph Builder](#langgraph-builder)
- [LangGraph-gen](#langgraph-gen)

---

## 快速开始

完整使用流程需要同时启动 Builder 和 gen 服务：

```bash
# 1. 克隆/进入项目根目录
cd langgraph0723  # 或你的项目根目录

# 2. 启动 langgraph-gen 后端（Terminal 1）
conda create -n freestyle-designer python=3.12 -y
conda activate freestyle-designer
pip install -r requirements.txt --no-cache-dir
python langgraphgenpy/openapi/main.py

# 3. 启动 LangGraph Builder 前端（Terminal 2）
cd langgraphbuilder
yarn install
yarn dev

# 4. 浏览器访问
# Builder: http://localhost:3000
# Gen API:  http://localhost:8001
```

---

## Docker 部署

使用 Docker Compose 一键启动所有服务：

```bash
docker-compose up -d --build
```

启动后访问：
- **LangGraph Builder**：http://localhost:3000
- **Gen API**：http://localhost:8001
- **健康检查**：http://localhost:8001/health

如需同时启动 MongoDB（供 mongodbcon 服务使用）：

```bash
docker-compose --profile with-mongodb up -d --build
```

---

## 项目结构

```
langgraph0723/
├── langgraphbuilder/                    # 可视化设计工具
│   └── src/
│       └── pages/
│           └── api/
│               └── generate-code.ts     # LANGGRAPH_API_URL 控制调用 gen 服务的 URL
│
├── langgraphgenpy/                      # 代码生成库
│   ├── openapi/
│   │   ├── main.py                      # langgraph-gen 后端服务启动入口 (端口 8001)
│   │   └── mongodbcon/
│   │       └── main.py                  # MongoDB 后端服务启动入口
│   ├── tests/
│   │   └── test-yml-generation.py       # 测试从 YAML 生成 py 文件
│   └── langgraph_gen/
│       ├── assets/                      # 代码生成模板
│       └── generate.py                  # 代码生成引擎
│
├── requirements.txt                     # Python 依赖
└── .env.template                        # 环境变量模板（含 MongoDB 配置）
```

---

## LangGraph Builder

### 简介

LangGraph Builder 提供可视化画布，用于设计 LangGraph 应用的认知架构。设计完成后，可生成 Python 和 TypeScript 的应用样板代码。

### 主要功能

- 拖放式界面设计 LangGraph 架构
- 支持多种节点类型和连接方式
- 代码生成支持 Python 和 TypeScript
- 提供模板快速开始常见模式

### 启动步骤

```bash
cd langgraphbuilder
yarn install
yarn dev
```

在浏览器中打开：**http://localhost:3000**

### 配置

如需修改 Builder 调用的 gen 服务地址，编辑 `langgraphbuilder/src/pages/api/generate-code.ts` 中的 `LANGGRAPH_API_URL`（默认：`http://localhost:8001/api/generate`）。

---

## LangGraph-gen

### 简介

langgraph-gen 是为 Builder 提供代码生成的后端服务，支持从规范文件（如 YAML）自动生成 LangGraph 存根代码。

### 环境要求

- Python 3.12
- Conda（推荐）或 venv

### 启动步骤

```bash
# 1. 创建并激活环境
conda create -n freestyle-designer python=3.12 -y
conda activate freestyle-designer  # 或使用你自定义的环境名

# 2. 进入项目根目录
cd langgraph0723  # 确保与 requirements.txt 同目录

# 3. 安装依赖
pip install -r requirements.txt --no-cache-dir

# 4. 启动服务
python langgraphgenpy/openapi/main.py
```

服务启动后：
- **API 地址**：http://localhost:8001
- **健康检查**：http://localhost:8001/health
- **代码生成**：POST `/api/generate`

---

## 环境变量

项目根目录下可参考 `.env.template` 配置环境变量，主要用于 MongoDB 等服务的连接信息。
