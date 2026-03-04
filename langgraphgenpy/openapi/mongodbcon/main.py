from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import Database
from routes import router
from contextlib import asynccontextmanager

# 定义应用的生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时连接数据库
    await Database.connect()
    yield
    # 应用关闭时断开数据库连接
    await Database.disconnect()

# 创建FastAPI应用，使用lifespan参数
app = FastAPI(
    title="MongoDB FastAPI Service",
    description="基于FastAPI和MongoDB的异步后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)

# 健康检查端点
@app.get("/health", tags=["health"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "MongoDB FastAPI Service"
    }

# 根路径
@app.get("/", tags=["root"])
async def root():
    """根路径"""
    return {
        "message": "欢迎使用MongoDB FastAPI服务!",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)