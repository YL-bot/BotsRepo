import vk_api
import json
from datetime import datetime


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = False

    return key, remember_device


def photo(vk: vk_api.vk_api.VkApiMethod):
    up = vk_api.VkUpload(vk)
    up.photo(photos=[f'static/img/{i}.jpeg' for i in range(1, 4)], album_id=int(input('ВВЕДИТЕ ID АЛЬБОМА: ')), group_id=int(input('ВВЕДИТЕ ID ГРУППЫ: ')))


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
    
    vk = vk_session.get_api()
    photo(vk)


if __name__ == '__main__':
    main()