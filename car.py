class Car:

    def __init__(self, name: str, images: list, price: float, city: str, mileage: str, link: str):
        super().__init__()
        self.link = link
        self.mileage = mileage
        self.city = city
        self.price = price
        self.images = images
        self.name = name
