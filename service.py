from line_profiler import LineProfiler

from car import Car
from repository import GroupRepository, CarRepository
from singleton import Singleton


class CarService(metaclass=Singleton):
    _car_repository = CarRepository()

    def process_cars(self, cars: set[Car]):
        cars = set(cars)
        # Find unique cars
        new_cars = self._get_new_cars(cars)

        cars = cars.difference(new_cars)
        # Find cars that price has been changed
        price_changed_cars = self._get_price_changed_cars(cars)

    def _get_new_cars(self, cars: set) -> set:
        car_ids = self._car_repository.get_all_car_ids()
        new_cars = {car for car in cars if car.autoria_id not in car_ids}
        print(type(new_cars))
        return new_cars

    def _get_price_changed_cars(self, cars: set) -> set:
        price_changed_cars = set()

    def exists_by_autoria_id(self, autoria_id):
        return self._car_repository.exists_by_id(autoria_id)

    def has_been_price_changed(self, autoria_id, price):
        return self._car_repository.has_been_price_changed(autoria_id, price)


class GroupService(metaclass=Singleton):
    _group_repository = GroupRepository()

    def subscribe(self, chat_id) -> str:
        if self._group_repository.is_already_subscribed(chat_id):
            return 'You already subscribed!'

        try:
            self._group_repository.register_group_id(chat_id)
            return 'You have subscribed for updates'
        except:
            return 'Something went wrong. Try later'

    def unsubscribe(self, chat_id) -> str:
        if not self._group_repository.is_already_subscribed(chat_id):
            return 'You are not subscribed to updates'

        try:
            self._group_repository.delete_group(chat_id)
            return 'You have unsubscribed for updates'
        except:
            return 'Something went wrong. Try later'

    def get_all_group_ids(self):
        chat_ids = list(map(lambda chat: chat[1], self._group_repository.get_all_chats()))
        return chat_ids

# Надіслати якщо
# Авто нове
# Змінилась ціна
