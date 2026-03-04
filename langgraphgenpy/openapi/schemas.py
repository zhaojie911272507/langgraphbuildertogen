from pydantic import BaseModel
from typing import Literal

class CodeGenerationRequest(BaseModel):
    """代码生成请求参数模型"""
    spec: str  # 工作流YAML规范内容
    language: Literal["python", "typescript"]  # 支持的目标语言
    format: str # yaml

class CodeGenerationResponse(BaseModel):
    """代码生成响应模型"""
    success: bool = True
    stub: str  # 生成的框架代码
    implementation: str  # 生成的实现代码
    error: str | None = None  # 错误信息（失败时返回）