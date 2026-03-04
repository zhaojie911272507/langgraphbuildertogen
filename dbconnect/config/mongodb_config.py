import os
from dotenv import load_dotenv
from pathlib import Path
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient


class MongDBConfig:
    def __init__(self, bu_name) -> None:
        load_dotenv()
        self.bu_name = bu_name

    def initial_connect_config(self):
        username = os.getenv('MONGO_USER')
        password = os.getenv('MONGO_PASSWORD')
        DB_NAME = os.getenv('MONGO_DB_NAME')
        slice_A = os.getenv('MONGO_SLICE_A')
        # slice_B = os.getenv(f'{self.bu_name}_MONGO_SLICE_B')
        # slice_C = os.getenv(f'{self.bu_name}_MONGO_SLICE_C')
        # return username, password, DB_NAME, slice_A, slice_B, slice_C

        return username, password, DB_NAME, slice_A

print(MongDBConfig('ASD').initial_connect_config())

# AsyncIOMotorClient()
# 异步连接 MongoDB 并初始化客户端
async def init_mongodb():
    # 连接字符串格式：mongodb://用户名:密码@主机:端口/数据库名
    client = AsyncIOMotorClient(
        "mongodb://amdin:SecurePassword123!@121.4.79.138:27017?authMechanism=DEFAULT&tls=true&tlsAllowInvalidHostnames=true&serverSelectionTimeoutMS=100&connectTimeoutMS=1000",
        maxPoolSize=100,  # 连接池最大连接数（默认100）
        minPoolSize=10    # 连接池最小保持连接数
    )
    db = client["test_database"]  # 指定数据库
    collection = db["test_collection"]  # 指定集合
    return collection

# print(init_mongodb())