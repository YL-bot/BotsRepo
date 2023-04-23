import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    if input('Есть двухкратная аунтификация (Y/N): ') == 'N':    
        login, password = input('LOGIN: '), input('PASSWORD: ')
        vk_session = vk_api.VkApi(login, password)
    else:       
        login, password = input('LOGIN: '), input('PASSWORD: ')
        vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
        
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    photo = vk_session.method('photos.get', {'album_id': int(input('Введите id альбома: ')), 'group_id': 'Введите id группы: '})
    
    for i in photo['items']:
        print(f"Высота: {i['sizes'][-1]['height']}\n"
              f"Ширина: {i['sizes'][-1]['width']}\n"
              f"URL: {i['sizes'][-1]['url']}")


if __name__ == '__main__':
    main()