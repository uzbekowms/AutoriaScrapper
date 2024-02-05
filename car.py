from enum import Enum


class CarStatus(Enum):
    new = 1
    price_changed = 2


class Car:
    def __init__(self,
                 autoria_id: int = None,
                 name: str = None,
                 new_price: float = None,
                 city: str = None,
                 mileage: str = None,
                 autoria_link: str = None,
                 images: list[str] = None,
                 bidfax_link: str = None,
                 old_price: float = None,
                 status: CarStatus = None):
        self.status = status
        self.old_price = old_price
        self.bidfax_link = bidfax_link
        self.images = images
        self.autoria_link = autoria_link
        self.mileage = mileage
        self.city = city
        self.new_price = new_price
        self.name = name
        self.autoria_id = autoria_id

    def __str__(self):
        return f"Car(autoria_id={self.autoria_id}, name='{self.name}', price={self.new_price}, " \
               f"city='{self.city}', mileage='{self.mileage}', autoria_link='{self.autoria_link}', " \
               f"images={self.images}, bidfax={self.bidfax_link})"
