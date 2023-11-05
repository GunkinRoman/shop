from pydantic import BaseModel



class Cart(BaseModel):
    acc_id: int
    product_id: int
    quantity: int

class ProductInCart(BaseModel):
    order_id: int
    product: int
    quantity: int