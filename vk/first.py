#1 вк
import vk_api
from datetime import datetime


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = False

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
    
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=5, offset=1)
    if response['items']:
        for i in response['items']:
            text = i['copy_history'][-1]['text']
            date = i['copy_history'][-1]['date']
            
            print(text)
            print('date: ', datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d'), '; time: ', datetime.fromtimestamp(int(date)).strftime('%H:%M:%S'))
            
            


if __name__ == '__main__':
    main()