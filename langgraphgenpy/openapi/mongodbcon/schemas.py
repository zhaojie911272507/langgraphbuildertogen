from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# 响应状态枚举
class ResponseStatus(str, Enum):
    success = "success"
    error = "error"

# 通用响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    status: ResponseStatus = ResponseStatus.success
    message: Optional[str] = None
    data: Optional[Any] = None
    error_code: Optional[str] = None

# 分页参数
class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页大小")

# 分页响应
class PaginatedResponse(BaseResponse):
    """分页响应模型"""
    total: int = 0
    page: int = 1
    size: int = 10
    pages: int = 0

# 用户相关模式
class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None

class UserResponse(BaseModel):
    """用户响应"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    roles: List[str]
    created_at: datetime
    updated_at: datetime

# 产品相关模式
class ProductCreate(BaseModel):
    """创建产品请求"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(...)
    tags: List[str] = Field(default=[])

class ProductUpdate(BaseModel):
    """更新产品请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None

class ProductResponse(BaseModel):
    """产品响应"""
    id: str
    name: str
    description: Optional[str]
    price: float
    category: str
    tags: List[str]
    in_stock: bool
    created_at: datetime
    updated_at: datetime

# graph相关
class GraphCreate(BaseModel):
    """创建Graph请求"""
    user_id: str = Field(..., description="用户ID")
    graph_id: str = Field(..., description="Graph ID")
    graph_name: str = Field(..., min_length=1, max_length=50, description="Graph名称")
    graph_description: Optional[str] = Field(None, max_length=100, description="Graph描述")
    graph_category: str = Field(..., min_length=8, description="Graph类别")
    graph_tags: List[str] = Field(default=[],description="Graph标签")
    graph_data: Dict[str, Any] = Field(..., description="Graph数据")

class GraphUpdate(BaseModel):
    """创建Graph请求"""
    user_id: str = Field(..., description="用户ID")
    graph_id: str = Field(..., description="Graph ID")  # 添加 ... 表示必填
    graph_name: str = Field(..., min_length=1, max_length=50, description="Graph名称")
    graph_description: Optional[str] = Field(None, max_length=100, description="Graph描述")
    graph_category: str = Field(..., min_length=8, description="Graph类别")
    graph_tags: List[str] = Field(default=[],description="Graph标签")
    graph_data: Dict[str, Any] = Field(..., description="Graph数据")

class GraphResponse(BaseModel):
    """Graph响应"""
    id: str
    user_id: str = Field(..., description="用户ID")
    graph_id: str = Field(description="Graph ID")
    graph_name: str = Field(..., min_length=1, max_length=50, description="Graph名称")
    graph_description: Optional[str] = Field(None, max_length=100, description="Graph描述")
    graph_category: str = Field(..., min_length=8, description="Graph类别")
    graph_tags: List[str] = Field(default=[],description="Graph标签")
    graph_data: Dict[str, Any] = Field(..., description="Graph数据")
    created_at: datetime
    updated_at: datetime

class GraphDelete(BaseModel):
    """创建Graph请求"""
    user_id: str = Field(..., description="用户ID")
    graph_id: str = Field(..., description="Graph ID")  # 添加 ... 表示必填
    graph_name: str = Field(..., min_length=1, max_length=50, description="Graph名称")
    graph_description: Optional[str] = Field(None, max_length=100, description="Graph描述")
    graph_category: str = Field(..., min_length=8, description="Graph类别")
    graph_tags: List[str] = Field(default=[],description="Graph标签")
    graph_data: Dict[str, Any] = Field(..., description="Graph数据")

