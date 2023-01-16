import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


class PetFriends:  # объявляем новый класс
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"  # задаем переменную с адресом сервера

    def get_api_key(self, email: str, password: str) -> json:  # Обьявляем метод
        """Метод делает запрос к API ссервера и возвращает статус запроса и результат в формате JSON с уникальным ключем
        пользователя, найденного по указанным email и паролем.
        (get: /api/key)
        """
        headers = {  # создаем переменную в котой храниться email и пароль
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+'/api/key', headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result  # возвращаем статус код и ключ авторизации

    def get_list_of_pets(self, aust_key, filter):
        """Метод делает запрос к API ссервера и возвращает статус запроса и результат в формате JSON с данными о питомцах
        пользователя, найденых по указанному ключу пользователя
        (get: /api/pets)
        """
        headers = {'auth_key': aust_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет данные на сервер о новом (добавляемом) питомце и возвращает статус запроса и результат добавления
        в формате json с данными добавленного питомца
        (post: /api/pets)
        """
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """отправляем PUT запрос на сервер для измениея атребутов питомца
        (put: /api/pets)
        """

        headers = {'auth_key': auth_key['key']}
        data = {
                'name': name,
                'age': age,
                'animal_type': animal_type
            }

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200
        (delete: /api/pets)
        """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int,) -> json:
        """Метод отправляет данные на сервер о новом (добавляемом) питомце и возвращает статус запроса и результат добавления
        в формате json с данными добавленного питомца, без фото
        (post: /api/create_pet_simple)
        """

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
            }

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод добавляет фото питомца по указанному ID питомца
        (post: /api/pets/set_photo)
        """

        data = MultipartEncoder(fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
