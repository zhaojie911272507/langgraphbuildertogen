from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

# 基础模型
class BaseMongoModel(BaseModel):
    """MongoDB基础模型"""
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# 示例用户模型
class User(BaseMongoModel):
    """用户模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = Field(default=True)
    roles: List[str] = Field(default=["user"])
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        collection = "users"

# 示例产品模型
class Product(BaseMongoModel):
    """产品模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(...)
    tags: List[str] = Field(default=[])
    in_stock: bool = Field(default=True)
    
    class Config:
        collection = "products"


# Graph信息存储
class Graph(BaseMongoModel):
    """Graph"""

    user_id: str = Field(..., description="用户ID")
    graph_id: str = Field(description="Graph ID")
    graph_name: str = Field(..., min_length=1, max_length=50, description="Graph名称")
    graph_description: Optional[str] = Field(None, max_length=100, description="Graph描述")
    graph_category: str = Field(..., min_length=8, description="Graph类别")
    graph_tags: List[str] = Field(default=[])
    graph_data: Dict[str, Any] = Field(..., description="Graph数据")

    class Config:
        collection = "graphs"

