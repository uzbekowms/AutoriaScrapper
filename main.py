import time
import requests
from bs4 import BeautifulSoup
from typing import Optional

SCRAP_DELAY = 600  # 10 minutes

BASE_LINK = 'https://auto.ria.com/uk'

# ANNOUNCEMENT_PER_PAGE = 100
ANNOUNCEMENT_PER_PAGE = 10

SEARCH_LINK = f'{BASE_LINK}/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=1&size={ANNOUNCEMENT_PER_PAGE}'
# SEARCH_LINK = f'{BASE_LINK}/search/?lang_id=4&page=0&countpage=100&category_id=1&custom=1&abroad=2'


# total cars - span id="staticResultsCount"

# card - section data-mark-name=? data-model-name=? data-generation-name=? data-modification-name=? data-year=? data-link-to-view=? data-id=?
# couple images // get car link and get photos
# car name - 1. data-mark-name=? data-model-name=? data-generation-name=? data-modification-name=? data-year=?
# price - div class='price-ticket' data-main-price=?
# city - li class="item-char view-location js-location"
# mileage - li class="item-char js-race"
# link to autoria - 1. data-link-to-view=?
# other links - div class="vin-checked mb-15 _grey"

car_attributes = (
    'data-mark-name', 'data-model-name', 'data-generation-name',
    'data-modification-name', 'data-year'
)

PHOTOS_COUNT = 5


def get_bidfax_link(page: BeautifulSoup) -> Optional[str]:
    bidfax_container = page.find('div', class_='technical-info ticket-checked')
    if not bidfax_container:
        return

    bidfax_link = bidfax_container.find('a', class_='bidfaxLink')
    return bidfax_link


def get_car_images(page: BeautifulSoup) -> Optional[list]:
    image_tags = page.find('div', id='photosBlock').find_all('div', class_='photo-620x465')
    images = [image.find_next("img")['src'] for index, image in enumerate(image_tags) if index < PHOTOS_COUNT]
    return images


def parse_car_card(car_card):
    car_info = car_card.find_next('div', class_='hide')

    name = ' '.join([car_info[attr] for attr in car_attributes if car_info[attr]])
    price = float(car_card.find('div', class_='price-ticket')['data-main-price'])
    city = car_card.find('li', class_='item-char view-location js-location').text.split()[0]
    mileage = car_card.find('li', class_='item-char js-race').text.strip()
    autoria_link = f'{BASE_LINK}{car_info["data-link-to-view"]}'

    car_page = get_page(autoria_link)

    images = get_car_images(car_page)
    bidfax_link = get_bidfax_link(car_page)

    return name, price, city, mileage, autoria_link, images, bidfax_link


def collect_cars_from_page(page: BeautifulSoup):
    car_cards = page.find_all('section', class_='ticket-item')
    cars = [parse_car_card(car_card) for car_card in car_cards]
    return cars


def get_next_page_link(page: BeautifulSoup):
    print()
    print(page.find('span', class_='page-item next text-r'))
    return page.find('a', class_='page-link js-next')['href']


def get_page(link):
    response = requests.get(link)
    if response.status_code != 200:
        return

    with open('test.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    return BeautifulSoup(response.text, 'lxml')


def collect_cars():
    main_page = get_page(SEARCH_LINK)
    if not main_page:
        return

    next_page_link = get_next_page_link(main_page)
    cars = collect_cars_from_page(main_page)

    while next_page_link:
        next_page = get_page(next_page_link)
        cars.extend(collect_cars_from_page(next_page))
        next_page_link = get_next_page_link(next_page)

    print('\n'.join([str(car) for car in cars]))
    '''total = int(main_page.find('span', id='staticResultsCount').text)
    pages_count = math.ceil(total / ANNOUNCEMENT_PER_PAGE)
    cars = collect_cars_from_page(main_page)

    for i in range(2, pages_count + 1):
        cars.extend(collect_cars_from_page(page_number=i))


    print('\n'.join([str(car) for car in cars]))'''


def main():
    while True:
        time.sleep(SCRAP_DELAY)


if __name__ == '__main__':
    collect_cars()
