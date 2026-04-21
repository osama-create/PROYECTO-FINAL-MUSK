class Sale:
    def __init__(self, sale_id, client_id, product, category, amount):
        self.sale_id   = sale_id
        self.client_id = client_id
        self.product   = product
        self.category  = category
        self.amount    = amount

    def to_dict(self):
        return {
            "sale_id":   self.sale_id,
            "client_id": self.client_id,
            "product":   self.product,
            "category":  self.category,
            "amount":    self.amount
        }