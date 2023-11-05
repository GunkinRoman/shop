class ProductInCart:
    def __init__(self, id: int, acc_id: int, product_id: int, quantity: int):
        self.id = id
        self.acc_id = acc_id
        self.product_id = product_id
        self.quantity = quantity

class ProductOrder:
    def __init__(self, order_id: int, product_id: int, quantity: int):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity