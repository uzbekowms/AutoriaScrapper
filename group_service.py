from repository import GroupRepository
from singleton import Singleton


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
        chat_ids = list(map(lambda chat: chat[0], self._group_repository.get_all_ids()))
        return chat_ids
