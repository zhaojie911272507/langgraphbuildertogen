from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from models import Graph, User, Product
from schemas import (
    UserCreate, UserUpdate, UserResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    BaseResponse, PaginatedResponse, PaginationParams,
    GraphCreate, GraphUpdate, GraphResponse
)
from crud import CRUDUser, CRUDProduct, CRUDGraph

# 创建路由实例
router = APIRouter(prefix="/api/generator", tags=["mongodb"])

# 依赖项：获取数据库
async def get_db() -> AsyncIOMotorDatabase:
    return get_database()

# 用户路由
@router.post("/users", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """创建用户"""
    try:
        # 检查用户是否已存在
        existing_user = await db[User.Config.collection].find_one({"username": user_in.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 创建用户
        user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name
        )
        
        crud_user = CRUDUser(db[User.Config.collection])
        user_id = await crud_user.create(user)
        
        return BaseResponse(
            status="success",
            message="用户创建成功",
            data={"id": user_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=BaseResponse)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """获取用户信息"""
    try:
        crud_user = CRUDUser(db[User.Config.collection])
        user = await crud_user.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return BaseResponse(
            status="success",
            message="获取用户信息成功",
            data=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )

@router.get("/users", response_model=BaseResponse)
async def get_users(
    pagination: PaginationParams = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """获取用户列表"""
    try:
        crud_user = CRUDUser(db[User.Config.collection])
        users = await crud_user.get_multi(
            skip=(pagination.page - 1) * pagination.size,
            limit=pagination.size
        )
        
        total = await crud_user.count()
        pages = (total + pagination.size - 1) // pagination.size
        
        return BaseResponse(
            status="success",
            message="获取用户列表成功",
            data={
                "items": users,
                "total": total,
                "page": pagination.page,
                "size": pagination.size,
                "pages": pages
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户列表失败: {str(e)}"
        )

@router.put("/users/{user_id}", response_model=BaseResponse)
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """更新用户信息"""
    try:
        crud_user = CRUDUser(db[User.Config.collection])
        user_data = user_in.dict(exclude_unset=True)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        user = User(**user_data)
        updated = await crud_user.update(user_id, user)
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return BaseResponse(
            status="success",
            message="用户信息更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败: {str(e)}"
        )

@router.delete("/users/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """删除用户"""
    try:
        crud_user = CRUDUser(db[User.Config.collection])
        deleted = await crud_user.delete(user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return BaseResponse(
            status="success",
            message="用户删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除用户失败: {str(e)}"
        )

# 产品路由
@router.post("/products", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """创建产品"""
    try:
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            category=product_in.category,
            tags=product_in.tags
        )
        
        crud_product = CRUDProduct(db[Product.Config.collection])
        product_id = await crud_product.create(product)
        
        return BaseResponse(
            status="success",
            message="产品创建成功",
            data={"id": product_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建产品失败: {str(e)}"
        )

@router.get("/products/{product_id}", response_model=BaseResponse)
async def get_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """获取产品信息"""
    try:
        crud_product = CRUDProduct(db[Product.Config.collection])
        product = await crud_product.get(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="产品不存在"
            )
        
        return BaseResponse(
            status="success",
            message="获取产品信息成功",
            data=product
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取产品信息失败: {str(e)}"
        )

@router.get("/products", response_model=BaseResponse)
async def get_products(
    pagination: PaginationParams = Depends(),
    category: Optional[str] = Query(None, description="产品分类筛选"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """获取产品列表"""
    try:
        # 构建筛选条件
        filters = {}
        if category:
            filters["category"] = category
            
        crud_product = CRUDProduct(db[Product.Config.collection])
        products = await crud_product.get_multi(
            skip=(pagination.page - 1) * pagination.size,
            limit=pagination.size,
            filters=filters
        )
        
        total = await crud_product.count(filters)
        pages = (total + pagination.size - 1) // pagination.size
        
        return BaseResponse(
            status="success",
            message="获取产品列表成功",
            data={
                "items": products,
                "total": total,
                "page": pagination.page,
                "size": pagination.size,
                "pages": pages
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取产品列表失败: {str(e)}"
        )

@router.put("/products/{product_id}", response_model=BaseResponse)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """更新产品信息"""
    try:
        crud_product = CRUDProduct(db[Product.Config.collection])
        product_data = product_in.dict(exclude_unset=True)
        
        if not product_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        product = Product(**product_data)
        updated = await crud_product.update(product_id, product)
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="产品不存在"
            )
        
        return BaseResponse(
            status="success",
            message="产品信息更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新产品信息失败: {str(e)}"
        )

@router.delete("/products/{product_id}", response_model=BaseResponse)
async def delete_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """删除产品"""
    try:
        crud_product = CRUDProduct(db[Product.Config.collection])
        deleted = await crud_product.delete(product_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="产品不存在"
            )
        
        return BaseResponse(
            status="success",
            message="产品删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除产品失败: {str(e)}"
        )


# graph 路由
@router.post("/graphs", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_graph(graph_in: GraphCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """创建graph"""
    try:
        graph = Graph(
            user_id = graph_in.user_id,
            graph_id = graph_in.graph_id,
            graph_name = graph_in.graph_name,
            graph_description = graph_in.graph_description,
            graph_category= graph_in.graph_category,
            graph_tags = graph_in.graph_tags,
            graph_data = graph_in.graph_data
        )
        
         # 使用正确的 CRUD 类
        crud_graph = CRUDGraph(db[Graph.Config.collection])
        graph_id = await crud_graph.create(graph)

        return BaseResponse(
            status="success",
            message="graph创建成功",
            data={"id": graph_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建graph失败: {str(e)}"
        )

