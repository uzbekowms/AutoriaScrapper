from scrapper.service.car_service import CarService
from scrapper.parser.parser import AutoriaScrapper
from apscheduler.schedulers.background import BackgroundScheduler

SCRAP_DELAY = 10

autoria_parser = AutoriaScrapper()
cars = autoria_parser.collect_unique_cars()
car_service = CarService()

car_service.send_out_cars(cars)

autoria_parser = AutoriaScrapper()
car_service = CarService()

scheduler = BackgroundScheduler()

i = 0


def main():
    global i
    print(f'{i:=^100}')
    try:
        cars = autoria_parser.collect_unique_cars()
        print('Parsed')
        car_service.save_all(cars)

        car_service.send_out_cars(cars)
        print('Sended')
    except Exception as e:
        print(e)

    i += 1


if __name__ == '__main__':
    scheduler.add_job(main, minutes=SCRAP_DELAY)
    scheduler.start()
