import ast
import time
import requests
from bs4 import BeautifulSoup, Tag
from typing import Optional

from repository import CarRepository, GroupRepository
from service import CarService

from tag_classes import BIDFAX_CONTAINER, BIDFAX_LINK, PHOTO_CLASS, PHOTOS_BLOCK, CAR_INFO_CONTAINER, CAR_ATTRIBUTES, \
    PRICE_CLASS, PRICE_ATTR, CITY_CLASS, MILEAGE_CLASS, AUTORIA_LINK_ATTR, CAR_CARD_CLASS, CAR_ID, \
    BIDFAX_PHOTO_CONTAINER, BIDFAX_PHOTO

SCRAP_DELAY = 600  # 10 minutes
BASE_LINK = 'https://auto.ria.com/uk'
ANNOUNCEMENT_PER_PAGE = 100
PHOTOS_COUNT = 5
SEARCH_LINK_PATTERN = '{base}/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page={page}&size={announcements}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
}

car_service = CarService()


def get_bidfax_link(page: BeautifulSoup) -> Optional[str]:
    history_container = page.find('div', id=BIDFAX_CONTAINER)

    if not history_container:
        return

    bidfax_link = history_container.find('a', class_=BIDFAX_LINK)

    if not bidfax_link:
        return

    return bidfax_link['href']


def get_car_images(page: BeautifulSoup) -> Optional[list]:
    image_tags = page.find('div', id=PHOTOS_BLOCK).find_all('div', class_=PHOTO_CLASS)
    images = []
    for index, image_tag in enumerate(image_tags):
        if index >= PHOTOS_COUNT:
            break

        image = image_tag.find_next('img')['src']

        if 'riastatic' in image:
            images.append(image)

    return images


# Not working
def get_bidfax_images(link: str) -> list:
    page = get_page(link)

    images = page.find('div', class_=BIDFAX_PHOTO_CONTAINER).find_all('img', class_=BIDFAX_PHOTO)

    return [image['src'] for image in images]


def parse_car_card(car_card: Tag) -> dict:
    car_info = car_card.find_next('div', class_=CAR_INFO_CONTAINER)

    car_id = car_info[CAR_ID]
    name = ' '.join([car_info[attr] for attr in CAR_ATTRIBUTES if car_info[attr]])
    price = float(car_card.find('div', class_=PRICE_CLASS)[PRICE_ATTR])
    city = car_card.find('li', class_=CITY_CLASS).text.split()[0]
    mileage = car_card.find('li', class_=MILEAGE_CLASS).text.strip()
    autoria_link = f'{BASE_LINK}{car_info[AUTORIA_LINK_ATTR]}'

    car_page = get_page(autoria_link)

    images = get_car_images(car_page)
    bidfax_link = get_bidfax_link(car_page)

    return {'autoria_id': car_id,
            'name': name,
            'price': price,
            'city': city,
            'mileage': mileage,
            'autoria_link': autoria_link,
            'images': images,
            'bidfax': {
                'link': bidfax_link,
                'images': None
            }}


def collect_cars_from_page(page: BeautifulSoup) -> Optional[list]:
    car_cards = page.find_all('section', class_=CAR_CARD_CLASS)
    if not car_cards:
        return

    cars = [parse_car_card(car_card) for car_card in car_cards]
    return cars


def get_page(link: str) -> Optional[BeautifulSoup]:
    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        return
    return BeautifulSoup(response.text, 'lxml')


def get_next_page(page_num: int) -> Optional[BeautifulSoup]:
    print(SEARCH_LINK_PATTERN.format(base=BASE_LINK, announcements=ANNOUNCEMENT_PER_PAGE, page=page_num))
    return get_page(SEARCH_LINK_PATTERN.format(base=BASE_LINK, announcements=ANNOUNCEMENT_PER_PAGE, page=page_num))


def collect_cars():
    cars = []
    page_num = 0
    while True:
        new_cars = collect_cars_from_page(get_next_page(page_num))

        if not new_cars:
            break

        cars.extend(new_cars)
        page_num += 1

    print('\n'.join([str(index + 1) + '. ' + str(car) for index, car in enumerate(cars)]))


def main():
    while True:
        start = time.perf_counter()
        try:
            collect_cars()
        except Exception as e:
            print(e.__traceback__)
        finally:
            end = time.perf_counter()
            print(start - end)
            work_time = end - start
            time.sleep(SCRAP_DELAY - (work_time if work_time >= 0 else 0))


# 50 per page - 125s
# 100 per page - 117s

if __name__ == '__main__':

    with open('test.txt', encoding='utf-8') as file:
        cars = [ast.literal_eval(car) for car in file.readlines()]
        print('\n'.join([str(index + 1) + '. ' + str(car) for index, car in enumerate(cars)]))
        print('=' * 50)
        car_service.process_cars(cars)

