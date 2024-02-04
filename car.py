class Car:

    def __init__(self,
                 autoria_id: int = None,
                 name: str = None,
                 price: float= None,
                 city: str= None,
                 mileage: str= None,
                 autoria_link: str= None,
                 images: list[str]= None,
                 bidfax: dict= None):
        self.bidfax_link = bidfax
        self.images = images
        self.autoria_link = autoria_link
        self.mileage = mileage
        self.city = city
        self.price = price
        self.name = name
        self.autoria_id = autoria_id

    def __str__(self):
        return f"Car(autoria_id={self.autoria_id}, name='{self.name}', price={self.price}, " \
               f"city='{self.city}', mileage='{self.mileage}', autoria_link='{self.autoria_link}', " \
               f"images={self.images}, bidfax={self.bidfax_link})"