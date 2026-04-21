class Client:
    def __init__(self, client_id, name, country):
        self.client_id = client_id
        self.name = name
        self.country = country

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "name":      self.name,
            "country":   self.country
        }