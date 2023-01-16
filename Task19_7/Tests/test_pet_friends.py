from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """проверка получения авторизационного ключа с валидными email и пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_list_of_pets_whit_valid_key(filter=''):
    """Проверка получения списка питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pet_whit_valid_key_and_data(name="Васька", animal_type="Кот", age="2", pet_photo='images\cat1.jpg'):
    """проверка добавления питомца с фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name="Сеня", animal_type="Котэ", age="5"):
    """Проверка измения данных о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pet_id=my_pets['pets'][0]['id'],
                                            name=name, animal_type=animal_type, age=age)

        assert status == 200
        assert result['name'] == name

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_post_new_pet_whit_valid_key_and_data_without_photo(name="Васька", animal_type="Кот", age="2"):
    """Проверка добавления нового питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet(pet_photo='images\cat2.jpg'):
    """проверкаа добавления фото к уже существующему питомцу"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, pet_id=my_pets['pets'][0]['id'], pet_photo=pet_photo)

        assert status == 200

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_invalid_email_valid_password(email=invalid_email, password=valid_password):
    """проверяем получение авторизационного ключа с неверным логином и верным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_valid_email_invalid_password(email=valid_email, password=invalid_password):
    """проверяем получение авторизационного ключа с верным логином и неверным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_invalid_email_invalid_password(email=invalid_email, password=invalid_password):
    """проверяем получение авторизационного ключа с неверным логином и неверным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_successful_update_self_pet_info_empty_name(name="", animal_type="Котэ", age="2"):
    """Проверяем можно ли изменить значение поля "имя" на пустое"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pet_id=my_pets['pets'][0]['id'],
                                            name=name, animal_type=animal_type, age=age)

        assert status == 200
        assert result['name'] != ""

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_empty_animal_type(name="Василий", animal_type="", age="2"):
    """Проверяем можно ли изменить значение поля "тип животного" на пустое"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pet_id=my_pets['pets'][0]['id'],
                                            name=name, animal_type=animal_type, age=age)

        assert status == 200
        assert result['animal_type'] != ""

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_empty_age(name="Василий", animal_type="Кот", age=""):
    """Проверяем можно ли изменить значение поля "возраст" на пустое"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pet_id=my_pets['pets'][0]['id'],
                                            name=name, animal_type=animal_type, age=age)

        assert status == 200
        assert result['age'] != ""

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_list_of_pets_whit_invalid_key(filter=''):
    """проврка получения списка питомцев для неавторизованного пользователя"""
    auth_key = {'key': ''}  # задаем неверное значение авторизационного ключа
    status, result = pf.get_list_of_pets(auth_key, filter)  # запрашиваем список питомвцев
    assert status == 403  # проверяем статус код страницы на отсутствие доступа


def test_post_new_pet_whit_invalid_key_and_data(name="Васька", animal_type="Кот", age="2", pet_photo='images\cat1.jpg'):
    """Проверка добавления новго питомца без авторизации"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {'key': ''}  # задаем неверное значение авторизационного ключа
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)  # добавляем питомца
    assert status == 403  # проверяем статус код страницы на отсутствие доступа


def test_successful_delete_self_pet_invalid_key():
    """проверка на удаление питомца с неверным авторизационным ключем"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    auth_key = {'key': ''}  # задаем неверное значение авторизационного ключа
    pet_id = my_pets['pets'][0]['id']  # выбираем id существующего питомца
    status, _ = pf.delete_pet(auth_key, pet_id)  # удаляем существующего питомца без авторизации

    assert status == 403  # Проверяем что статус ответа равен 403


def test_successful_update_self_pet_info_invalid_key(name="Сеня", animal_type="Котэ", age="5"):
    """Проверка изменения данных питомца без авторизации"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        auth_key = {'key': ''}  # задаем неверное значение авторизационного ключа
        status, result = pf.update_pet_info(auth_key, pet_id=my_pets['pets'][0]['id'],
                                            name=name, animal_type=animal_type, age=age)

        assert status == 403

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
