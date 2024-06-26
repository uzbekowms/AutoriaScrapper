import time

from scrapper.service.car_service import CarService
from scrapper.parser.parser import AutoriaScrapper

SCRAP_DELAY = 600

autoria_parser = AutoriaScrapper()
car_service = CarService()


def main():
    while True:
        start = time.perf_counter()
        try:
            cars = autoria_parser.collect_unique_cars()
            car_service.save_all(cars)
            car_service.send_out_cars(cars)
        except Exception as e:
            print(e)
        finally:
            end = time.perf_counter()
            time_difference = end - start
            delay = (SCRAP_DELAY - time_difference) if time_difference < SCRAP_DELAY else 0
            time.sleep(delay)


if __name__ == '__main__':
    main()
