class Client:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.membership = None  # абонемент оформляется отдельным сценарием

    def __str__(self):
        return f"Клиент: {self.name}"