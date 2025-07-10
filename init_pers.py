

# useless

import json
import os


k = 0


class JSONDatabase:
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.db = json.load(file)
        else:
            self.db = {"users": [{f"user_{k}": {}}]}

    def get(self, key):
        return self.db.get(key, None)

    def set(self, key, value):
        global k
        k = len(self.db['users'])-1
        self.db['users'][k][f'user_{k}'][key] = value   # бд[ключ 'users'][индекс объекта][ключ объекта][ключ, под которым сохраняется значение]
        if key == 'age':
            k += 1
            self.db['users'].append({f"user_{k}": {}})
        self._save()

    def delete(self, key):  # требует модернизации
        if key in self.db:
            del self.db[key]
            self._save()

    def clear(self):  # очистка бд
        global k
        k = 0
        self.db = self.db = {"users": [{f"user_{k}": {}}]}
        self._save()

    def _save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.db, fp=file, indent=2, ensure_ascii=False)

    def check(self, chat_id):  # проверка на наличие user_id в бд
        id_list = []
        for i in range(len(self.db['users'])):
            try:
                id_list.append(self.db['users'][i][f'user_{i}']['user_id'])
            except KeyError:
                break
        print(id_list, len(id_list))
        if chat_id in id_list:
            return False
        else:
            return True


db = JSONDatabase('json_files/private_jsons/database.json')


# class JSONDatabase:                       базовый вид бд
#     def __init__(self, file_path):
#         self.file_path = file_path
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as file:
#                 self.db = json.load(file)
#         else:
#             self.db = {}
#
#     def get(self, key):
#         return self.db.get(key, None)
#
#     def set(self, key, value):
#         self.db[key] = value
#         self._save()
#
#     def delete(self, key):
#         if key in self.db:
#             del self.db[key]
#             self._save()
#
#     def _save(self):
#         with open(self.file_path, 'w') as file:
#             json.dump(self.db, file, indent=1)


# {                                         как примерно должна выглядеть база данных
#   "users": [
#     {"user_0": {
#       "user_id": 5927881424,
#       "name": "max",
#       "surname": "dax",
#       "number": "89999999999",
#       "age": "89"
#     }},
#     {"user_1": {
#       "user_id": 5927881424,
#       "name": "max",
#       "surname": "dax",
#       "number": "89999999999",
#       "age": "89"
#     }}, ...
#   }
# }
