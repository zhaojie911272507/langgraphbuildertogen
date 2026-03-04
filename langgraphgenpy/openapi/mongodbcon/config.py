import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class MongoDBSettings:
    """MongoDB配置设置"""
    
    # MongoDB数据库连接信息
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER: str = os.getenv("MONGO_USER", "admin")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD", "password")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "test_db")
    MONGO_AUTH_SOURCE: str = os.getenv("MONGO_AUTH_SOURCE", "admin")
    
    # 连接池配置
    MONGO_MAX_POOL_SIZE: int = int(os.getenv("MONGO_MAX_POOL_SIZE", 100))
    MONGO_MIN_POOL_SIZE: int = int(os.getenv("MONGO_MIN_POOL_SIZE", 10))
    
    # 连接超时配置
    MONGO_SERVER_SELECTION_TIMEOUT_MS: int = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", 5000))
    MONGO_CONNECT_TIMEOUT_MS: int = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", 5000))
    
    # URI构建
    @property
    def MONGO_URI(self) -> str:
        """构建MongoDB连接URI"""
        if self.MONGO_USER and self.MONGO_PASSWORD:
            return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}?authSource={self.MONGO_AUTH_SOURCE}"
        else:
            return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}"

# 实例化配置
settings = MongoDBSettings()