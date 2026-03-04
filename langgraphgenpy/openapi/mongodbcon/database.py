from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings
import logging

# 配置日志
logger = logging.getLogger(__name__)

class Database:
    """数据库连接管理器"""
    
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    
    @classmethod
    async def connect(cls):
        """建立数据库连接"""
        try:
            # 创建异步MongoDB客户端
            cls.client = AsyncIOMotorClient(
                settings.MONGO_URI,
                maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
                minPoolSize=settings.MONGO_MIN_POOL_SIZE,
                serverSelectionTimeoutMS=settings.MONGO_SERVER_SELECTION_TIMEOUT_MS,
                connectTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS
            )
            
            # 获取数据库实例
            cls.db = cls.client[settings.MONGO_DB_NAME]
            
            # 验证连接
            await cls.client.server_info()
            logger.info("成功连接到MongoDB数据库")
            
        except Exception as e:
            logger.error(f"连接MongoDB数据库失败: {e}")
            raise
    
    @classmethod
    async def disconnect(cls):
        """关闭数据库连接"""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB数据库连接已关闭")
    
    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """获取数据库实例"""
        if cls.db is None:
            raise RuntimeError("数据库未连接，请先调用connect()方法")
        return cls.db

# 导出数据库实例获取函数
get_database = Database.get_db