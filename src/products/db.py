import asyncio
from conn.conn import connect_to_db
from products.models import Product, Filters


class Product_new:
    async def save_new_product(self, product: Product):
        conn = await connect_to_db()
        await conn.execute(
            """
        INSERT INTO product (
            article, name, cost, description, photo, discount, quantity, category
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """,
            product.article,
            product.name,
            product.cost,
            product.description,
            product.photo,
            product.discount,
            product.quantity,
            product.category,
        )

        await conn.close()

    async def get_product_list(
        self,
    ) -> list[Product]:
        conn = await connect_to_db()
        list_of_products = []
        try:
            res = await conn.fetch("SELECT * FROM product")
            for i in res:
                list_of_products.append(
                    Product(
                        article=i["article"],
                        name=i["name"],
                        cost=i["cost"],
                        description=i["description"],
                        photo=i["photo"],
                        discount=i["discount"],
                        quantity=i["quantity"],
                        category=i["category"],
                    )
                )
        except Exception as err:
            print(repr(err))
        finally:
            await conn.close()
            return list_of_products

    # async def get_product_filter_category(
    #     self,
    #     dict_of_filters: dict,
    # ):
    #     conn = await connect_to_db()

    #     dopustimii_filtri = [
    #         "category",
    #         "voda",
    #         "eda"
    #     ]

    #     where = ""
    #     list_of_filter = []
    #     for key, value in dict_of_filters.items():
    #         if key in dopustimii_filtri and value:
    #             list_of_filter.append(f"{key}={value}")
    #         else:
    #             print(f"ключа нет в списке{key}")
    #     if list_of_filter:
    #         where = "WHERE " + ",".join(list_of_filter)

    #     await conn.execute(
    #         """
    #         SELECT * FROM product
    #         """
    #         + where
    #     )

    #     await conn.close()
    async def get_product_filter_category(
        self,
        filter: Filters,
    ):
        conn = await connect_to_db()

        await conn.fetch(
            """
            SELECT * FROM product WHERE category = $1
        """, filter
        )
        await conn.close()

    # # уточнить
    #     async def get_product_filter_cost() -> list:
    #         conn = await connect_to_db()
    #         query = "SELECT * FROM product ORDER BY cost DESC NULLS LAST, cost ASC"
    #         results = await conn.fetch(query)
    #         await conn.close()
    #         return results

    # loop = asyncio.get_event_loop()
    # sorted_products = loop.run_until_complete(get_product_filter_cost())
    # print(sorted_products)

    async def get_product_filter_name(self, name: str):
        conn = await connect_to_db()

        list_of_filter_name = []
        try:
            res = await conn.fetch(
                f"""
                SELECT * FROM product
                WHERE LOWER(name) LIKE '%{name.lower()}%'
                """,
            )
            for i in res:
                list_of_filter_name.append(
                    Product(
                        article=i["article"],
                        name=i["name"],
                        cost=i["cost"],
                        description=i["description"],
                        photo=i["photo"],
                        discount=i["discount"],
                        quantity=i["quantity"],
                        category=i["category"],
                    )
                )
        except Exception as err:
            print(repr(err))
        finally:
            await conn.close()
            return list_of_filter_name


db = Product_new()
