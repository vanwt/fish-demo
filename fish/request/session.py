import uuid


class DictSession():

    def __init__(self):
        self.__map = dict()


    def get_session(self, session_id):
        return self.__map.get(session_id, None)

    def create_session(self, data=None):
        key = uuid.uuid1().hex
        self.__map[key] = data if data else {}
        return key

    def set_value(self, session_id, value):
        self.__map[session_id].update(value)

    def delete(self, key):
        try:
            self.__map.pop(key)
        except KeyError:
            pass

    def reload(self):
        self.__map.clear()
