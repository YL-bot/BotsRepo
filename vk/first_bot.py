import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

do = True


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def name_town(id):
    global do
    if do:
        if input('Есть двухкратная аунтификация (Y/N): ') == 'N' :    
            login, password = '+79259151082', 'Lmao_@Dude1234'
            vk_session = vk_api.VkApi(login, password)
        else:       
            login, password = '+79259151082', 'Lmao_@Dude1234'
            vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)   
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
    else:
        login, password = '+79259151082', 'Lmao_@Dude1234'
        vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)   
        
    
    vk = vk_session.get_api()
    user_get=vk.users.get(user_ids = (id), fields='city')
    user_get=user_get[0]
    first_name=user_get['first_name']  
    try:
        town=user_get['city']['title']
    except Exception:
        town = ''
    
    
    return first_name, town
    

def main():
    vk_session = vk_api.VkApi(token='vk1.a.lhwzGcDCDlTAR8PIAQdwYb7eqP0KVs3T6LcqnlOJ0a58cq27HoVqGt4FKluOuIgu8Z9Mokx5A_Z8XZcV5ys3-o0OMmh-tOIRPz2Lge87yacgYtvx5sqVN7irfpLipyJh1XcLi6kSE3y5DpR0Z03Hx65qv3UypQcV0QKMNKegqu8fZv2UwQ2FWzYo3ak_I5alpBEpxAYYdmDpzMAXk1ViMA')

    longpoll = VkBotLongPoll(vk_session, 220073744)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:   
            #print('Текст:', event.obj.message['text'])
            
            vk = vk_session.get_api()
            id = event.obj.message['from_id']
            
            name, town = name_town(id)
            
            
            if not town:
                vk.messages.send(user_id=id, message=f"Привет, {name}!", random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=id, message=f"Привет, {name}! Как поживает {town}?", random_id=random.randint(0, 2 ** 64))                       


if __name__ == '__main__':
    main()