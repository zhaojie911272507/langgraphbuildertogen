import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

try:
    load_dotenv()
    # 连接到容器中的 MongoDB
    client = MongoClient(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        authSource=os.getenv("DB_AUTHSOURCE")
    )

    # 验证连接
    client.admin.command('ismaster')
    print("成功连接到 MongoDB!")

    # 创建/访问数据库
    db = client["mydatabase"]

    # 创建/访问集合
    collection = db["customers"]

    # 插入文档
    doc = {"name": "Docker User", "value": 99, "value2": 100}
    insert_result = collection.insert_one(doc)
    print(f"插入文档 ID: {insert_result.inserted_id}")

    # 查询文档
    print("\n所有文档:")
    for record in collection.find():
        print(record)

except ConnectionFailure as e:
    print(f"连接失败: {e}")
finally:
    if 'client' in locals():
        client.close()
        