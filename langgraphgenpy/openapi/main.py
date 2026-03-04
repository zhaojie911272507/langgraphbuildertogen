import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraphgenpy.langgraph_gen.generate import generate_from_spec
# from langgraphgenpy.langgraph_gen.generatenoconditional import generate_from_spec

from langgraphgenpy.openapi.schemas import  CodeGenerationRequest, CodeGenerationResponse


# 初始化FastAPI应用
app = FastAPI(title="LangGraph Generator Service")

# 配置CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 匹配langgraph-builder默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/generate", response_model=CodeGenerationResponse)
async def generate_code_handler(request: CodeGenerationRequest):
    """处理代码生成请求"""
    try:
        stub, impl = generate_from_spec(
            request.spec,
            "yaml",
            language=request.language,
            templates=["stub", "implementation"]
        )


        return CodeGenerationResponse(
            stub=stub,
            implementation=impl
        )

    except Exception as e:
        return CodeGenerationResponse(
            success=False,
            stub="",
            implementation="",
            error=str(e)
        )


# 健康检查接口
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "langgraph-gen-api"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # 开发模式自动重载
        log_level="info"
    )

# 终端运行：uvicorn main:app --reload