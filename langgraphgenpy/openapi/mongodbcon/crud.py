from typing import Type, TypeVar, List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime, timezone


# 泛型类型变量
T = TypeVar('T', bound=BaseModel)

class CRUDBase:
    """CRUD操作基础类"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(self, obj_in: BaseModel) -> str:
        """创建文档"""
        # 转换为字典并添加创建时间
        obj_dict = obj_in.model_dump(by_alias=True, exclude_unset=True)
        obj_dict["created_at"] = datetime.now(timezone.utc)
        obj_dict["updated_at"] = datetime.now(timezone.utc)
        
        # 插入文档
        result = await self.collection.insert_one(obj_dict)
        return str(result.inserted_id)
    
    async def get(self, id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取文档"""
        try:
            obj = await self.collection.find_one({"_id": ObjectId(id)})
            if obj:
                obj["id"] = str(obj["_id"])
                del obj["_id"]
            return obj
        except Exception:
            return None
    
    async def get_multi(self, skip: int = 0, limit: int = 100, 
                       filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """获取多个文档"""
        if filters is None:
            filters = {}
            
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        results = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            del document["_id"]
            results.append(document)
        return results
    
    async def update(self, id: str, obj_in: BaseModel) -> bool:
        """更新文档"""
        # 检查文档是否存在
        existing = await self.get(id)
        if not existing:
            return False
        
        # 准备更新数据
        update_data = obj_in.model_dump(by_alias=True, exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        return False
    
    async def delete(self, id: str) -> bool:
        """删除文档"""
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计文档数量"""
        if filters is None:
            filters = {}
        return await self.collection.count_documents(filters)

# 用户CRUD操作
class CRUDUser(CRUDBase):
    """用户CRUD操作"""
    pass

# 产品CRUD操作
class CRUDProduct(CRUDBase):
    """产品CRUD操作"""
    pass

# Graph操作
class CRUDGraph(CRUDBase):
    """Graph CRUD操作"""
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
        self.graph_collection = collection.database["graphs"]

    async def set_graph(self, user_id: str, graph_id: str, graph_data: Dict[str, Any]):
        """设置用户的Graph数据"""
        await self.graph_collection.update_one(
            {"user_id": user_id, "graph_id": graph_id},
            {"$set": {"graph_data": graph_data}},
            upsert=True
        )
    
    async def get_graph(self, user_id: str, graph_id: str) -> Optional[Dict[str, Any]]:
        """获取用户的Graph数据"""
        graph = await self.graph_collection.find_one({"user_id": user_id, "graph_id": graph_id})
        if graph:
            graph["id"] = str(graph["_id"])
            del graph["_id"]
        return graph


