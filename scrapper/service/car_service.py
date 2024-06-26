import time

from telebot.apihelper import ApiTelegramException

from scrapper.service.group_service import GroupService
from scrapper.repo.repository import CarRepository
from scrapper.entity.singleton import Singleton
from scrapper.utils.message_utils import car_to_message
from scrapper.bot.autoria_scrapper_bot import send_car


class CarService(metaclass=Singleton):
    _car_repository = CarRepository()
    _group_service = GroupService()

    def exists_by_autoria_id(self, autoria_id: str):
        return self._car_repository.exists_by_id(autoria_id)

    def get_price_by_id(self, autoria_id):
        return self._car_repository.get_price_by_id(autoria_id)

    def save_all(self, cars):
        self._car_repository.save_all(cars)

    def send_car_with_retry(self, chat_id, media, max_retries=5, delay_between_retries=30):
        retries = 0
        while retries < max_retries:
            try:
                send_car(chat_id, media)
                return
            except ApiTelegramException as e:
                if e.error_code == 429:
                    print(f"Rate limit exceeded. Retrying after {delay_between_retries} seconds.")
                    time.sleep(delay_between_retries)
                    retries += 1
                elif e.error_code == 403:
                    self._group_service.unsubscribe(chat_id)
                    return
                else:
                    raise

        print("Max retries reached. Consider adjusting your rate limit handling.")

    def send_out_cars(self, cars):
        cars_messages = [car_to_message(car) for car in cars]
        for car_message in cars_messages:
            for chat_id in self._group_service.get_all_group_ids():
                self.send_car_with_retry(chat_id, car_message)
                time.sleep(1)
