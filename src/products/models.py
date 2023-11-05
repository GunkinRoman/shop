from enum import Enum
from pydantic import BaseModel


class Product(BaseModel):
    article: int
    name: str
    cost: float
    description: str
    photo: str
    discount: float
    quantity: int
    category: str


class Filters(str, Enum):
    filter1 = "FILTR1"
    filtr2 = "123"
    filter3 = "eda"

# res = [
#     {"article": 123, "name": "voda"},
#     {"article": 1234, "name": "pivo"},
# ]

# list_of_products: list[Product] = []

# for elemen in res:
#     list_of_products.append(
#         Product(
#             article=elemen["article"],
#             name=elemen["name"]
#         )
#     )


# print(list_of_products)