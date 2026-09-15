class Client:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.membership = None

    def has_active_membership(self, on_date=None):
        return self.membership is not None and self.membership.is_active(on_date)

    def __str__(self):
        return f"Клиент: {self.name}"