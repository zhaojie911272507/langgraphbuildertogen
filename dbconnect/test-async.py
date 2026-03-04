import asyncio
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pprint import pprint

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mongodb_client")

load_dotenv()

class AsyncMongoDBClient:
    def __init__(self, uri=f"mongodb://:{os.getenv("MONGO_USER")}:27017", db_name="test_db",
                 max_pool_size=100, min_pool_size=10):
        self.uri = uri
        self.db_name = db_name
        self.max_pool_size = max_pool_size
        self.min_pool_size = min_pool_size
        self.client = None
        self.db = None

    async def connect(self):
        """建立数据库连接"""
        try:
            self.client = AsyncIOMotorClient(
                self.uri,
                maxPoolSize=self.max_pool_size,
                minPoolSize=self.min_pool_size,
                serverSelectionTimeoutMS=5000
            )
            await self.client.server_info()  # 验证连接
            self.db = self.client[self.db_name]
            logger.info(f"成功连接到 MongoDB: {self.uri}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            return False

    async def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            logger.info("数据库连接已关闭")

    async def insert_document(self, collection_name, document):
        """插入单个文档"""
        try:
            collection = self.db[collection_name]
            result = await collection.insert_one(document)
            logger.info(f"已插入文档 ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"插入失败: {str(e)}")
            return None

    async def find_documents(self, collection_name, query={}, limit=5):
        """查询多个文档"""
        try:
            collection = self.db[collection_name]
            cursor = collection.find(query).limit(limit)
            results = [doc async for doc in cursor]
            logger.info(f"查询到 {len(results)} 条结果")
            return results
        except Exception as e:
            logger.error(f"查询失败: {str(e)}")
            return []


async def main():
    # 初始化客户端（根据实际配置修改参数）
    db_client = AsyncMongoDBClient(
        uri=f"mongodb://admin:SecurePassword123!@{os.getenv("MONGO_HOST")}:27017/admin?authSource=admin",
        db_name="example_db"
    )

    # 建立连接
    if not await db_client.connect():
        return

    # 演示CRUD操作
    collection = "users"

    # 插入文档
    new_user = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 30,
        "tags": ["developer", "python"]
    }
    user_id = await db_client.insert_document(collection, new_user)
    print("插入结果:",type(user_id))
    # 查询文档
    if user_id:
        users = await db_client.find_documents(collection, {"_id": user_id})
        print("查询结果:")
        pprint(users)

    # 关闭连接
    await db_client.close()


if __name__ == "__main__":
    asyncio.run(main())
