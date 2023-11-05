from fastapi import routing
from products.db import db
from products.models import Filters, Product

router = routing.APIRouter()


@router.post("/product_add")
async def product_add(product: Product):
    await db.save_new_product(product)


@router.get("/product_list")
async def product_all() -> list[Product]:
    return await db.get_product_list()


# проработать фильтры
@router.get("/product_filter_category")
async def product_filter_category(category_filter: Filters):
    await db.get_product_filter_category(category_filter)


# @router.get("/product_filter_cost")
# async def product_filter_cost(cost_min_filter: Optional[float],
#                               cost_max_filter: Optional[float]):
#     await db.get_product_filter_cost()


@router.get("/product_filter_name")
async def product_filter_name(name: str):
    return await db.get_product_filter_name(name)
