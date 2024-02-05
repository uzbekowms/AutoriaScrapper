from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from car import Car, CarStatus
from car_service import CarService
from tag_classes import CAR_CARD_CLASS, CAR_INFO_CONTAINER, CAR_ID, PRICE_CLASS, PRICE_ATTR, CAR_ATTRIBUTES, CITY_CLASS, \
    MILEAGE_CLASS, AUTORIA_LINK_ATTR, BIDFAX_PHOTO_CONTAINER, BIDFAX_PHOTO, PHOTOS_BLOCK, PHOTO_CLASS, BIDFAX_CONTAINER, \
    BIDFAX_LINK


class AutoriaScrapper:
    __car_service = CarService()

    BASE_LINK = 'https://auto.ria.com/uk'
    ANNOUNCEMENT_PER_PAGE = 100
    PHOTOS_COUNT = 5
    SEARCH_LINK_PATTERN = '{base}/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page={page}&size={announcements}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }

    def collect_unique_cars(self) -> set[Car]:
        cars = set()
        page_num = 0
        while True:
            new_cars = self.__collect_cars_from_page(self.__get_next_page(page_num))

            if not new_cars:
                break

            cars.update(new_cars)
            page_num += 1

        return cars

    def __collect_cars_from_page(self, page: BeautifulSoup) -> Optional[set[Car]]:
        car_cards = page.find_all('section', class_=CAR_CARD_CLASS)
        if not car_cards:
            return

        cars = set()

        for car_card in car_cards:
            car = self.__process_car_card(car_card)
            if car:
                cars.add(car)

        return cars

    def __get_next_page(self, page_num: int) -> Optional[BeautifulSoup]:
        print(self.SEARCH_LINK_PATTERN.format(base=self.BASE_LINK, announcements=self.ANNOUNCEMENT_PER_PAGE,
                                              page=page_num))
        return self.__get_page(
            self.SEARCH_LINK_PATTERN.format(base=self.BASE_LINK, announcements=self.ANNOUNCEMENT_PER_PAGE,
                                            page=page_num))

    def __get_page(self, link: str) -> Optional[BeautifulSoup]:
        response = requests.get(link, headers=self.headers)

        if response.status_code != 200:
            return
        return BeautifulSoup(response.text, 'lxml')

    def __process_car_card(self, car_card: Tag) -> Car | None:
        car_info = car_card.find_next('div', class_=CAR_INFO_CONTAINER)
        car = Car()
        car.autoria_id = car_info[CAR_ID]
        car.new_price = float(car_card.find('div', class_=PRICE_CLASS)[PRICE_ATTR])

        if not self.__car_service.exists_by_autoria_id(car.autoria_id):
            self.__parse_car_info(car, car_info, car_card)
            car.status = CarStatus.new
            return car

        car.old_price = self.__car_service.get_price_difference(car.autoria_id, car.new_price)

        if car.old_price - car.new_price != 0:
            print(car.new_price)
            self.__parse_car_info(car, car_info, car_card)
            car.status = CarStatus.price_changed
            return car

    def __parse_car_info(self, car, car_info, car_card):
        car.name = ' '.join([car_info[attr] for attr in CAR_ATTRIBUTES if car_info[attr]])
        car.city = car_card.find('li', class_=CITY_CLASS).text.split()[0]
        car.mileage = car_card.find('li', class_=MILEAGE_CLASS).text.strip()
        car.autoria_link = f'{self.BASE_LINK}{car_info[AUTORIA_LINK_ATTR]}'

        car_page = self.__get_page(car.autoria_link)

        car.images = self.__get_car_images(car_page)
        car.bidfax_link = self.__get_bidfax_link(car_page)

    def __get_car_images(self, page: BeautifulSoup) -> Optional[list[str]]:
        image_tags = page.find('div', id=PHOTOS_BLOCK).find_all('div', class_=PHOTO_CLASS)
        images = []
        for index, image_tag in enumerate(image_tags):
            if index >= self.PHOTOS_COUNT:
                break

            image = image_tag.find_next('img')['src']

            if 'riastatic' in image:
                images.append(image)

        return images

    # Not working
    def __get_bidfax_images(self, link: str) -> list:
        page = self.__get_page(link)

        images = page.find('div', class_=BIDFAX_PHOTO_CONTAINER).find_all('img', class_=BIDFAX_PHOTO)

        return [image['src'] for image in images]

    def __get_bidfax_link(self, page: BeautifulSoup) -> Optional[str]:
        history_container = page.find('div', id=BIDFAX_CONTAINER)

        if not history_container:
            return

        bidfax_link = history_container.find('a', class_=BIDFAX_LINK)

        if not bidfax_link:
            return

        return bidfax_link['href']
