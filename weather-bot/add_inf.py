  # may be useless


import json


class AddInfo:
    def __init__(self, user_path):
        self.user_path = user_path
        with open(user_path, 'w+') as path:
            self.user = {"num":0, "0":{}}
            json.dump(self.user, path, indent=2)
            self._user = json.load(user_path)
        

    def set_weather(self, basic_weather):
        self._user[0]['0'] = basic_weather
        self._save()

    def _save(self):
        with open(self.user_path, 'w') as path:
            json.dump(self.user_path, path, indent=2)